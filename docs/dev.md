# Agent sdk knowledge base

# 1. Condensation & Persistence Technical Guide

This guide provides an in-depth look at how the OpenHands SDK manages long-running conversations through context condensation and robust state persistence.

---

## 1. Conversation Condensation

Condensation is the process of reducing the conversation history to fit within an LLM's context window while preserving essential information.

### Core Concepts
*   **View**: A linear, filtered list of events derived from the full history. It represents exactly what the LLM sees.
*   **Condenser**: An implementation (e.g., `LLMSummarizingCondenser`) that decides which events to "forget" and how to summarize them.
*   **Events**: Condensation is driven by two specific event types:
    *   `CondensationRequest`: A signal that condensation is needed.
    *   `Condensation`: The event that records the result of a condensation (what was forgotten and the summary).

### Triggering Mechanisms
1.  **Automatic (Resource-based)**: Triggered when `max_size` (event count) or `max_tokens` thresholds are reached.
2.  **Reactive (Error-based)**: Triggered automatically if the LLM returns a `ContextWindowExceed` or `MalformedHistory` error.
3.  **Manual (Explicit)**: Triggered by code or user request using a `CondensationRequest`.

### Manual Invocation through Code
To force condensation from within your agent logic (e.g., responding to a `/condense` command):

```python
from openhands.sdk.event.condenser import CondensationRequest

# Inside Agent.step()
if is_special_command:
    on_event(CondensationRequest())
    return 
```

From outside the agent, you can use the high-level API:
```python
conversation.condense()
```

---

## 2. Conversation Persistence

The SDK implements an incremental, always-on persistence model designed for reliability and performance.

### Serialization Architecture
*   **`base_state.json`**: Stores metadata including agent configuration, token usage statistics, user-defined tags, and the current execution status. This file is automatically updated on every public field change.
*   **`events/` Directory**: Each event is stored as a standalone JSON file. This "Event Log" approach allows for high-performance incremental writes—only new events are written to disk.

### Key Persistence Features
*   **`agent_state`**: A dedicated `dict[str, Any]` on the conversation state. This allows agents to store their own runtime "memories" (e.g., search results, task progress) that persist across sessions but don't appear in the LLM chat history.
*   **`stats`**: Accumulates cost and token metrics across the entire lifetime of the conversation, even across server restarts.
*   **`secret_registry`**: When used with a `Cipher`, sensitive data like API keys are encrypted on disk and decrypted only in memory upon loading.

### Loading & Resumption
To resume a conversation, simply point a new `Conversation` object to the existing directory:
```python
conversation = Conversation(
    agent=my_agent,
    persistence_dir="./persistence",
    conversation_id=existing_uuid
)
```

---

## 3. Conversation Forking

Forking creates a "deep copy" of a conversation, enabling parallel experimentation and branching logic.

### Isolation and Remediation
*   **Full Isolation**: Every fork receives a new, unique UUID. It is stored in a sibling directory (e.g., `./persistence/fork-uuid/`). There are no shared files between the original and the fork.
*   **Eliminating a Fork**: To delete a fork entirely with no remnants, simply delete its specific subdirectory (`shutil.rmtree(fork_conv.state.persistence_dir)`).
*   **Retaining a Fork**: Forks are persistent by default. To move a fork to a different base directory, close the conversation and move the entire subdirectory on the filesystem.

### Advanced Forking Scenarios
1.  **A/B Testing**: Branch a conversation to test different instructions or LLM models from the same starting state.
2.  **Checkpointing**: Create a "template" conversation with a complex environment setup and fork it for every new task to save setup time/cost.
3.  **Error Recovery**: Fork a conversation at the iteration just before a failure to debug or try a different approach without losing the original trace.

---

## 4. Best Practices
*   **Configure Condensers Early**: Manual condensation requires an `LLMSummarizingCondenser` to be registered with the agent.
*   **Use `agent_state` for Metadata**: Avoid polluting the conversation transcript with internal agent tracking; use `state.agent_state` instead.
*   **Close Conversations**: Always call `conversation.close()` to ensure tool executors (like terminal sessions or browser instances) are properly cleaned up.
