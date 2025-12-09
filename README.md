# 🎄 The 12 Days of Christmas - Durable AI Agent

A festive demo showcasing **Temporal's durability** with **OpenAI Agents SDK**! This AI agent teaches and performs "The 12 Days of Christmas" song, and if it crashes mid-performance, Temporal ensures it resumes exactly where it left off.

## 🎯 Why This Demo?

**The Perfect Analogy**: Everyone forgets their place in "The 12 Days of Christmas" song. Temporal solves that exact problem by checkpointing progress after each verse!

**Key Insight**: By wrapping the OpenAI agent loop in a Temporal activity, the entire AI interaction becomes durable and resumable. No more lost progress, no duplicate work.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│  User Request: "Sing the whole song!"               │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  Temporal Workflow (TwelveDaysWorkflow)             │
│  ┌───────────────────────────────────────────────┐  │
│  │  OpenAI Agent Activity (Durable!)            │  │
│  │  ┌─────────────────────────────────────────┐ │  │
│  │  │  GPT-4 Agent decides tool calls         │ │  │
│  │  │  → sing_verse(1)                        │ │  │
│  │  │  → sing_verse(2)                        │ │  │
│  │  │  ... [Crash here? No problem!] ...      │ │  │
│  │  │  → sing_verse(6) [Resumes here!]        │ │  │
│  │  │  ...                                     │ │  │
│  │  └─────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- `uv` package manager
- Temporal CLI (for running local Temporal server)
- OpenAI API key

### Installation

```bash
# 1. Install uv (if not already installed)
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install dependencies using uv
uv sync

# 3. Install Temporal CLI (if not already installed)
# macOS/Linux:
curl -sSf https://temporal.download/cli.sh | sh

# 4. Create .env file with your OpenAI API key
cat > .env << EOF
OPENAI_API_KEY=sk-your-openai-key-here
TEMPORAL_ADDRESS=localhost:7233
EOF
```

### Running the Demo

**Terminal 1: Start Temporal Server**
```bash
temporal server start-dev
```

**Terminal 2: Start the Worker**
```bash
uv run python worker.py
```

You should see:
```
🔑 OpenAI API key found
🔌 Connecting to Temporal at localhost:7233...
✅ Connected to Temporal!

============================================================
🎄 12 Days of Christmas Worker Started!
============================================================
📋 Task queue: twelve-days-queue
🔄 Workflows: TwelveDaysWorkflow
🛠️  Activities: OpenAI Agent Activity

✨ Waiting for workflows... (Press Ctrl+C to stop)
============================================================
```

**Terminal 3: Run the Agent (CLI)**
```bash
uv run python starter.py
```

**OR Terminal 3: Run the Streamlit UI** 🎨
```bash
uv run streamlit run streamlit_app.py
```

The Streamlit UI provides the same functionality with a holiday-themed web interface!
It will open automatically in your browser at `http://localhost:8501`

Watch the magic happen! 🎵

## 🎭 Demo: Showing Durability

This is the **killer feature** of combining Temporal with AI agents:

### Step 1: Start the Song
```bash
uv run python starter.py
```

The agent will start singing...
```
🎵 On the first day of Christmas,
   my true love gave to me:
   🐦 A partridge in a pear tree
✓ Completed verse 1 of 12

🎵 On the second day of Christmas,
   my true love gave to me:
   🕊️ Two turtle doves
   🐦 And a partridge in a pear tree
✓ Completed verse 2 of 12
...
```

### Step 2: Crash the Worker! 💥
Around day 5 or 6, press **Ctrl+C** in the worker terminal to simulate a crash.

### Step 3: Restart the Worker
```bash
uv run python worker.py
```

### Step 4: Resume (Same Workflow ID!)
```bash
uv run python starter.py
```

**🎉 BOOM!** The agent resumes from where it left off! No duplicate verses, perfect continuation.

### What Just Happened?

1. **Temporal checkpointed** the workflow state after each activity execution
2. When the worker crashed, Temporal remembered exactly where we were
3. On restart, Temporal **replayed** the workflow
4. The OpenAI agent activity **resumed** from its last checkpoint
5. The song continued seamlessly! 🎶

## 📁 Project Structure

```
twelve-days-agent/
├── activities.py          # Tool implementations (sing_verse, get_gift_info)
├── workflow.py            # Agent workflow using OpenAI Agents SDK
├── worker.py             # Temporal worker
├── starter.py            # CLI to start the agent
├── pyproject.toml        # Project config & dependencies
├── uv.lock               # Locked dependencies (managed by uv)
├── .python-version       # Python version specification
├── .env                  # Environment variables (you create this)
└── README.md            # You are here!
```

## 📦 Why `uv`?

This project uses [`uv`](https://github.com/astral-sh/uv) for blazingly fast package management:
- ⚡ **10-100x faster** than pip
- 🔒 **Automatic lock file** management
- 🎯 **Built-in virtual environment** handling
- 🔄 **Drop-in replacement** for pip workflows

Run any Python file with: `uv run python your_file.py`

## 🛠️ How It Works

### The Tools (activities.py)

The AI agent has access to these **Temporal activities**:

- **`sing_verse(day: int)`**: Sings one verse with all previous gifts
- **`get_gift_info(day: int)`**: Returns info about a specific day's gift

These are **Temporal activities** decorated with `@activity.defn`. They're automatically wrapped as agent tools using `activity_as_tool()`.

### The Agent (workflow.py)

The OpenAI agent is configured with:
- **Model**: GPT-4 (via the Agent SDK)
- **Instructions**: "Be a cheerful teacher, sing all 12 days in order"
- **Tools**: Activities wrapped with `activity_as_tool()`

Each tool call runs as a **separate Temporal activity**, which gives us fine-grained durability and observability.

### The Workflow Sandbox (worker.py)

Temporal workflows run in a **sandbox** to ensure determinism. However, the OpenAI Agents SDK needs to make HTTP calls (to OpenAI's API), which normally aren't allowed in workflows.

We solve this by configuring **passthrough modules** - telling Temporal that certain modules (like `openai`, `httpx`, `agents`) are safe to use:

```python
sandbox_restrictions = SandboxRestrictions.default.with_passthrough_modules(
    "openai",
    "openai_agents", 
    "agents",
    "httpx",
    "httpcore",
    "anyio",
    "sniffio",
    # ... other HTTP-related modules
)
```

This allows the agent to communicate with OpenAI while still maintaining Temporal's durability guarantees.

### The Durability Pattern

```python
# Create agent with activities as tools
agent = Agent(
    name="twelve-days-teacher",
    instructions="...",
    tools=[
        openai_agents.workflow.activity_as_tool(
            sing_verse,
            start_to_close_timeout=timedelta(seconds=10)
        ),
        openai_agents.workflow.activity_as_tool(
            get_gift_info,
            start_to_close_timeout=timedelta(seconds=5)
        )
    ]
)

# Run the agent
result = await Runner.run(agent, prompt)
```

When the agent runs:
1. GPT-4 decides to call `sing_verse(1)`
2. Temporal executes it as an activity → checkpoints
3. GPT-4 decides to call `sing_verse(2)`
4. Temporal executes it as an activity → checkpoints
5. **[Worker crashes]**
6. **[Worker restarts]**
7. Temporal replays the workflow
8. Already completed verses (1-2) are not re-executed
9. GPT-4 continues with `sing_verse(3)`!

## 🎮 Different Scenarios to Try

Edit `starter.py` to change the `user_request`:

### Full Song
```python
user_request = "Please sing the entire 12 Days of Christmas song for me!"
```

### Specific Question
```python
user_request = "What gift comes on day 8?"
```

### Partial Song
```python
user_request = "Sing days 5 through 9"
```

### Test Agent's Understanding
```python
user_request = "What's special about day 5?"
```

## 🐛 Troubleshooting

### "uv: command not found"
Install uv first:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "OPENAI_API_KEY not found"
Create a `.env` file in the project root:
```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### "Failed to connect to Temporal"
Make sure Temporal server is running:
```bash
temporal server start-dev
```

### Agent Doesn't Sing All Verses
The GPT-4 agent should sing all 12 days. If it stops early:
- Check the instructions in `workflow.py`
- Try being more explicit in your request
- Ensure you're using GPT-4, not a weaker model

### "Cannot access threading.local" or sandbox errors
This happens when Temporal's workflow sandbox blocks non-deterministic code. The `worker.py` is already configured with passthrough modules for OpenAI. If you see this error:
- Make sure you're using the updated `worker.py` with `SandboxRestrictions`
- Restart the worker after making changes

### "Activity timeout"
If singing all 12 verses takes too long, increase the timeout in `workflow.py`:
```python
start_to_close_timeout=timedelta(seconds=30),  # Increase this
```

### Python version issues
This project requires Python 3.10+. Check your version:
```bash
python --version
```
`uv` will automatically use the correct Python version specified in `.python-version`.

## 📊 Monitoring

### Temporal Web UI
Visit http://localhost:8233 to see:
- Workflow execution history
- Activity task details
- Event timeline (see exactly when verses were sung!)
- Retry attempts

### Workflow ID
The workflow ID is `"twelve-days-demo"`. This is important for resumability!
- Same ID = Temporal can resume after crash
- Different ID = New workflow from scratch

## 🎓 Key Learnings

### 1. Activity-as-Tool Pattern
Each tool call = one Temporal activity. This gives fine-grained durability and observability. The `activity_as_tool()` helper:
- Automatically generates OpenAI-compatible tool schemas
- Wraps activity execution so Temporal can track it
- Handles serialization and errors

### 2. Tools Are Temporal Activities
The tools (`sing_verse`, `get_gift_info`) are proper Temporal activities decorated with `@activity.defn`. Benefits:
- Each tool call is a separate activity in Temporal UI
- Individual timeouts per tool
- Better error handling and retries
- Full observability

### 3. Agent SDK Integration
The OpenAI Agents SDK (`Agent` and `Runner`) integrates seamlessly with Temporal:
- `Agent` defines the agent's behavior and tools
- `Runner.run()` executes the agent loop
- All tool calls are automatically durable

### 4. No Duplicate Work
Temporal's event sourcing ensures that completed tool calls aren't repeated on replay. If you crash at verse 6, verses 1-5 won't re-execute.

### 5. Production-Ready AI
This pattern makes AI agents production-ready:
- Durable across crashes (workflow-level)
- Observable via Temporal UI (activity-level)
- Retryable with backoff (per-activity)
- Versioned workflows
- Individual activity timeouts

## 🚀 Production Considerations

To make this production-ready:

1. **Error Handling**: Add retry policies for transient failures
2. **Rate Limiting**: Handle OpenAI rate limits gracefully
3. **Streaming**: Use OpenAI streaming for real-time responses
4. **Monitoring**: Add custom metrics for agent performance
5. **Testing**: Mock OpenAI responses for unit tests
6. **Versioning**: Use workflow versioning for updates
7. **Scaling**: Run multiple workers for high throughput

## 📚 References

- [Temporal + OpenAI Agents Cookbook](https://docs.temporal.io/ai-cookbook/openai-agents-sdk-python)
- [Temporal Python SDK](https://github.com/temporalio/sdk-python)
- [OpenAI Agents SDK](https://platform.openai.com/docs/agents)
- [Temporal OpenAI Integration](https://github.com/temporalio/sdk-python/tree/main/temporalio/contrib/openai_agents)
- [uv Package Manager](https://github.com/astral-sh/uv)

## 🎄 Happy Holidays!

This demo shows that building reliable AI agents doesn't have to be hard. With Temporal, your agents are:
- ✅ Durable across crashes
- ✅ Resumable from any point
- ✅ Observable and debuggable
- ✅ Production-ready out of the box

Now go build something amazing! 🚀

---

**Made with ❤️ using Temporal + OpenAI**

*"On the 12th day of Christmas, Temporal gave to me... a durable AI agent that never loses its place!"* 🎵

