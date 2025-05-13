import { useRef, useState } from 'react';
import { NotebookPanel } from '@jupyterlab/notebook';
import { IModelConfig, IMessage } from '../types/api';
import { CellOperation, StreamChunk } from '../types/stream';
import { extractNotebookState } from '../utils/notebook-state-extractor';
import {
  streamAgenticAssistant,
  IAgenticAssistantPayload
} from '../services/api-service';
import { removeCellOperationTags } from '../utils/chatUtils';

// Assuming NotebookState is implicitly defined by extractNotebookState's return type
// If a specific type exists, it should be imported, e.g.:
// import { NotebookState } from '../types/notebook';
type NotebookState = ReturnType<typeof extractNotebookState>;

interface IUseAgenticLoopManagerArgs {
  plan: string | null;
  setPlan: (plan: string | null) => void;
  planStage: string | null;
  setPlanStage: (stage: string | null) => void;
  cellOutput: string | null;
  setCellOutput: (output: string | null) => void;
  notebookPanel: NotebookPanel | undefined;
  sessionId: string;
  setMessages: React.Dispatch<React.SetStateAction<IMessage[]>>;
  onStreamingStateChange?: (isStreaming: boolean) => void;
  executeCellOperation: (op: CellOperation) => Promise<string | undefined>;
  extractTextOutputFromCell: (cell: any) => string;
}

/**
 * React hook to manage the agentic loop for the Jupyt AI assistant.
 * Handles multi-step plans, cell execution, and streaming chat updates.
 * Ensures all streamed content for a single step is appended to a single chat bubble.
 */
export function useAgenticLoopManager(args: IUseAgenticLoopManagerArgs) {
  const isLoopingRef = useRef(false);
  const [isLooping, setIsLooping] = useState(false);
  const initialNotebookStateRef = useRef<NotebookState | null>(null);

  // Helper function to clean message content within the agentic loop
  const cleanAgenticContent = (content: string): string => {
    // Replace [COMPLETION_STATUS:...] with a newline
    const cleanedOfStatus = content
      .replace(/\[COMPLETION_STATUS:[^\]]*\]/gi, '\n')
      .trim();
    // Remove <cell_operation> tags
    return removeCellOperationTags(cleanedOfStatus);
  };

  // Helper to wait for cell output with timeout
  async function waitForCellOutput(
    notebookPanel: NotebookPanel | undefined,
    cell_index: number,
    extractTextOutputFromCell: (cell: any) => string,
    timeoutMs: number
  ) {
    return new Promise<string>(resolve => {
      const cell = notebookPanel?.content?.widgets?.[cell_index];
      if (!cell) {
        return resolve('');
      }
      let resolved = false;

      const hasOutputs = (model: any): boolean => {
        return (
          model &&
          typeof model === 'object' &&
          'outputs' in model &&
          model.outputs
        );
      };

      const checkOutput = () => {
        if (hasOutputs(cell.model)) {
          const output = extractTextOutputFromCell(cell.model as any);
          if (output && output.length > 0) {
            resolved = true;
            resolve(output);
          }
        }
      };

      // Listen for output changes
      const outputChanged = () => {
        if (!resolved) {
          checkOutput();
        }
      };
      if (hasOutputs(cell.model)) {
        (cell.model as any).outputs.changed.connect(outputChanged);
      }

      // Initial check
      checkOutput();

      // Timeout fallback
      setTimeout(() => {
        if (!resolved) {
          resolved = true;
          if (hasOutputs(cell.model)) {
            (cell.model as any).outputs.changed.disconnect(outputChanged);
            resolve(extractTextOutputFromCell(cell.model as any));
          } else {
            resolve('');
          }
        }
      }, timeoutMs);
    });
  }

  const startAgenticLoop = async ({
    query,
    llmConfig,
    initialState
  }: {
    query: string;
    llmConfig: IModelConfig;
    initialState?: NotebookState;
  }) => {
    const {
      plan,
      setPlan,
      planStage,
      setPlanStage,
      cellOutput,
      setCellOutput,
      notebookPanel,
      sessionId,
      setMessages,
      onStreamingStateChange,
      executeCellOperation,
      extractTextOutputFromCell
    } = args;

    // Use provided initial state or capture current state
    if (initialState) {
      initialNotebookStateRef.current = initialState;
    } else if (notebookPanel) {
      try {
        initialNotebookStateRef.current = extractNotebookState(notebookPanel);
      } catch (e) {
        console.error(
          '[AgenticLoop] Failed to extract initial notebook state:',
          e
        );
        initialNotebookStateRef.current = null;
      }
    } else {
      initialNotebookStateRef.current = null;
    }

    isLoopingRef.current = true;
    setIsLooping(true);
    let currentPlan = plan;
    let currentPlanStage = planStage;
    let currentCellOutput = cellOutput;
    let completionStatus: string | undefined = undefined;
    let first = true;
    while (isLoopingRef.current && (first || completionStatus === 'continue')) {
      first = false;
      const notebookState = extractNotebookState(notebookPanel);
      const payload: IAgenticAssistantPayload = {
        query,
        session_id: sessionId,
        notebook_state: notebookState,
        llm_config: llmConfig,
        plan: currentPlan || undefined,
        plan_stage: currentPlanStage || undefined,
        cell_output: currentCellOutput || undefined
      };
      if (onStreamingStateChange) {
        onStreamingStateChange(true);
      }
      // Add a new assistant message and update its content as we stream
      let assistantMsgIndex = -1;
      setMessages(prev => {
        assistantMsgIndex = prev.length;
        return [
          ...prev,
          {
            role: 'assistant',
            content: '',
            timestamp: Date.now()
          }
        ];
      });
      let lastChunk: StreamChunk | undefined = undefined;
      let fullContent = '';
      try {
        for await (const chunk of streamAgenticAssistant(payload)) {
          lastChunk = chunk;
          if (chunk.chunk_type !== 'end' && chunk.content) {
            fullContent += chunk.content;
            setMessages(prev => {
              const updated = [...prev];
              if (updated.length > 0 && updated[assistantMsgIndex]) {
                updated[assistantMsgIndex] = {
                  ...updated[assistantMsgIndex],
                  // Clean the content as it streams within the agentic loop
                  content: cleanAgenticContent(fullContent)
                };
              }
              return updated;
            });
          }
        }
      } catch (err) {
        setMessages(prev => [
          ...prev,
          {
            role: 'assistant',
            content: `Error: ${err instanceof Error ? err.message : 'Unknown error'}`,
            timestamp: Date.now()
          }
        ]);
        break;
      } finally {
        if (onStreamingStateChange) {
          onStreamingStateChange(false);
        }
      }
      if (!lastChunk) {
        break;
      }
      // Print the end chunk for debugging
      console.log('[AgenticLoop] Received end chunk:', lastChunk);

      // Function to normalize operation types (internal helper)
      const normalizeOperation = (op: any) => {
        if (op.operation === 'update') {
          return { ...op, type: 'update_cell' };
        }
        if (op.operation === 'create') {
          return { ...op, type: 'create_cell' };
        }
        if (op.operation === 'delete') {
          return { ...op, type: 'delete_cell' };
        }
        return op;
      };
      // Extract operations *before* potential execution
      const operations = lastChunk.next_action
        ? lastChunk.next_action.map(normalizeOperation)
        : [];

      // Update the final message content *and* add operations
      setMessages(prev => {
        const updated = [...prev];
        if (updated.length > 0 && updated[assistantMsgIndex]) {
          updated[assistantMsgIndex] = {
            ...updated[assistantMsgIndex],
            content: cleanAgenticContent(fullContent), // Ensure final content is clean
            operations: operations.length > 0 ? operations : undefined // Add operations
          };
        }
        return updated;
      });

      // Extract plan, plan_stage, completion_status
      if (lastChunk.plan) {
        setPlan(lastChunk.plan);
      }
      if (lastChunk.plan_stage) {
        setPlanStage(lastChunk.plan_stage);
      }
      currentPlan = lastChunk.plan || currentPlan;
      currentPlanStage = lastChunk.plan_stage || currentPlanStage;
      completionStatus = lastChunk.completion_status || undefined;

      // Debug: Print next_action array
      if (lastChunk.next_action) {
        console.log('[AgenticLoop] next_action array:', lastChunk.next_action);
      }

      // If cell operations are required, execute them and get the output of the last one needing execution
      let output = '';
      let lastExecutedOperationIndex = -1; // Index of the last operation that required running
      if (operations && operations.length > 0) {
        // Use the extracted operations variable
        for (let i = 0; i < operations.length; i++) {
          const op = operations[i]; // Use the extracted operations variable
          await executeCellOperation(op);
          if (op.run_needed && typeof op.cell_index === 'number') {
            lastExecutedOperationIndex = i; // Track the last operation that needs output check
          }
        }

        // Wait for the output of the *last* operation that needed to be run
        if (lastExecutedOperationIndex !== -1) {
          const lastOpToRun = operations[lastExecutedOperationIndex];
          // Ensure cell_index is valid before waiting
          if (typeof lastOpToRun.cell_index === 'number') {
            output = await waitForCellOutput(
              notebookPanel,
              lastOpToRun.cell_index,
              extractTextOutputFromCell,
              10000
            );
          }
        }
      }

      // If error output was explicitly provided in the chunk, use it (overwrites executed output)
      if (lastChunk.cell_output) {
        output = lastChunk.cell_output;
      }

      setCellOutput(output);
      currentCellOutput = output;

      setMessages(prev => {
        const updated = [...prev];
        if (updated.length > 0 && updated[assistantMsgIndex]) {
          updated[assistantMsgIndex] = {
            ...updated[assistantMsgIndex],
            content: cleanAgenticContent(fullContent)
          };
        }
        return updated;
      });
    }
    isLoopingRef.current = false;
    setIsLooping(false);
  };

  const cancelAgenticLoop = () => {
    isLoopingRef.current = false;
    setIsLooping(false);
  };

  const revertAllChanges = async () => {
    // stop the loop if it's running
    if (isLoopingRef.current) {
      cancelAgenticLoop();
    }

    if (!initialNotebookStateRef.current || !args.notebookPanel) {
      console.warn(
        '[AgenticLoop] Cannot revert: initial state or notebook panel not available.'
      );
      args.setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content:
            'Cannot revert: initial notebook state was not saved or panel is not available.',
          timestamp: Date.now()
        }
      ]);
      return;
    }

    if (isLoopingRef.current) {
      cancelAgenticLoop(); // Stop any ongoing loop first
    }

    const { cells: initialCells } = initialNotebookStateRef.current;
    const currentNotebookPanel = args.notebookPanel;

    args.setMessages(prev => [
      ...prev,
      {
        role: 'assistant',
        content: 'Attempting to revert changes...',
        timestamp: Date.now()
      }
    ]);

    try {
      const model = currentNotebookPanel.content.model;
      if (!model) {
        console.error('[AgenticLoop] Revert failed: Notebook model not found.');
        args.setMessages(prev => {
          const updated = [...prev];
          if (
            updated.length > 0 &&
            updated[updated.length - 1].content.startsWith(
              'Attempting to revert'
            )
          ) {
            updated[updated.length - 1].content =
              'Revert failed: Notebook model not found.';
          }
          return updated;
        });
        return;
      }

      const currentCells = currentNotebookPanel.content.widgets;

      // Track cells that need to be reverted
      const cellsToRevert: { index: number; operation: 'delete' | 'update' }[] =
        [];

      // Compare current cells with initial cells
      for (let i = 0; i < currentCells.length; i++) {
        const currentCell = currentCells[i];
        const initialCell = initialCells[i];

        // If cell exists in initial state but content is different, mark for update
        if (
          initialCell &&
          currentCell.model.toJSON().source !== initialCell.source
        ) {
          cellsToRevert.push({ index: i, operation: 'update' });
        }
        // If cell doesn't exist in initial state, mark for deletion
        else if (!initialCell) {
          cellsToRevert.push({ index: i, operation: 'delete' });
        }
      }

      // Process deletions first (from bottom to top to maintain indices)
      for (const cell of cellsToRevert
        .filter(cell => cell.operation === 'delete')
        .sort((a, b) => b.index - a.index)) {
        await args.executeCellOperation({
          type: 'delete_cell',
          cell_index: cell.index
        });
      }

      // Then process updates
      for (const cell of cellsToRevert
        .filter(cell => cell.operation === 'update')
        .sort((a, b) => b.index - a.index)) {
        const initialCell = initialCells[cell.index];
        if (initialCell) {
          await args.executeCellOperation({
            type: 'update_cell',
            cell_index: cell.index,
            code: initialCell.source
          });
        }
      }

      // Run all cells to clear outputs
      for (let i = 0; i < currentCells.length; i++) {
        const cellSource = currentCells[i].model.toJSON().source;
        await args.executeCellOperation({
          type: 'update_cell',
          cell_index: i,
          code: Array.isArray(cellSource) ? cellSource.join('\n') : cellSource,
          run_needed: true
        });
      }

      args.setPlan(null);
      args.setPlanStage(null);
      args.setCellOutput(null);
      console.log('[AgenticLoop] Changes reverted successfully.');
      args.setMessages(prev => {
        const updated = [...prev];
        if (
          updated.length > 0 &&
          updated[updated.length - 1].content.startsWith('Attempting to revert')
        ) {
          updated[updated.length - 1].content =
            'Changes reverted successfully.';
        } else {
          return [
            ...prev,
            {
              role: 'assistant',
              content: 'Changes reverted successfully.',
              timestamp: Date.now()
            }
          ];
        }
        return updated;
      });
    } catch (error) {
      console.error('[AgenticLoop] Error during revert:', error);
      args.setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: `Failed to revert changes: ${error instanceof Error ? error.message : String(error)}`,
          timestamp: Date.now()
        }
      ]);
    } finally {
      initialNotebookStateRef.current = null; // Clear the stored state after attempt
    }
  };

  return { startAgenticLoop, cancelAgenticLoop, isLooping, revertAllChanges };
}
