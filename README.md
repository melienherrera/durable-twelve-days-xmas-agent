# 🎄 The 12 Days of Christmas - Durable AI Agent

A festive demo showcasing **Temporal's durability** with **OpenAI Agents SDK**! This AI agent teaches and performs "The 12 Days of Christmas" song. If it crashes mid-performance, Temporal ensures it resumes exactly where it left off.

**The Perfect Analogy**: Everyone forgets their place in "The 12 Days of Christmas" song or in order to remember a specific day they have to re-sing all the verses. Temporal solves that exact problem by checkpointing progress after each verse!

## 🛠️ How It Works
Each tool call the AI agent makes is ran as a **Temporal Activity**, giving us fine-grained durability and safe retries:

```python
# The agent's tools are Temporal activities
@workflow.defn
class TwelveDaysWorkflow:
    @workflow.run
    async def run(self, prompt: str) -> str:
        agent = Agent(
            name="twelve-days-teacher",
            instructions="You are a 12 days of Christmas Agent. Sing all 12 days in order...",
            tools=[
                openai_agents.workflow.activity_as_tool(sing_verse),
                openai_agents.workflow.activity_as_tool(get_gift_info)
            ]
        )
...

# When the agent runs:
# 1. GPT-4 calls sing_verse(1) → Temporal Activity is logged as checkpoint ✓
# 2. GPT-4 calls sing_verse(2) → Temporal Activity is logged as checkpoint ✓
# 3. [Worker crashes] 💥
# 4. [Worker restarts]
# 5. Temporal replays Workflow from most recent checkpoint
# 6. GPT-4 continues with sing_verse(3) → No duplicates!
```

**Key Components:**

- **`activities.py`**: Tool implementations (`sing_verse`, `get_gift_info`) as Temporal activities
- **`workflow.py`**: OpenAI Agent wrapped in a Temporal workflow for durability
- **`worker.py`**: Temporal worker that executes workflows and activities
- **`starter.py`**: CLI to start the agent
- **`streamlit_app.py`**: Optional web UI for the agent

## 📚 References

- [Temporal + OpenAI Agents Cookbook](https://docs.temporal.io/ai-cookbook/openai-agents-sdk-python)
- [Temporal Python SDK](https://github.com/temporalio/sdk-python)
- [OpenAI Agents SDK](https://platform.openai.com/docs/agents)
- [Temporal OpenAI Integration](https://github.com/temporalio/sdk-python/tree/main/temporalio/contrib/openai_agents)

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- `uv` package manager ([install here](https://github.com/astral-sh/uv))
- Temporal CLI ([install here](https://docs.temporal.io/cli))
- OpenAI API key

### Setup

```bash
# Install dependencies
uv sync

# Create .env file with your OpenAI API key
export OPENAI_API_KEY=sk-your-openai-key-here
```

### Run the Demo

Open three terminals:

**Terminal 1: Start Temporal Server**
```bash
temporal server start-dev
```

**Terminal 2: Start the Worker**
```bash
uv run python worker.py
```

**Terminal 3: Run the Agent Workflow**

CLI version:
```bash
uv run python -m durable_temporal.worker
```

OR Streamlit UI:
```bash
uv run streamlit run streamlit_app.py
```

The Streamlit UI will open at `http://localhost:8501` 🎨

The UI includes two tabs to compare:
- **Temporal version** (durable, resumable) - requires worker running
- **Pure OpenAI Agents SDK** (non-durable, loses context on crash)

### Test Durability 🧪

1. Start the agent in the CLI with `uv run python starter.py`
2. Notice the verses printing in the Worker terminal. View the Workflow progress in the Temporal UI at `http://localhost:8233`
3. Around day 5, press **Ctrl+C** in the worker terminal to crash it. 
4. Restart the worker: `uv run python worker.py`
5. **🎉 The agent resumes from where it left off!** No duplicate verses.

## 🎄 Happy Holidays!
This demo shows that building reliable AI agents doesn't have to be hard. With Temporal, your agents are:
- ✅ Durable across crashes
- ✅ Resumable from any point
- ✅ Observable and debuggable
- ✅ Production-ready out of the box

Now go build something amazing! 🚀 Happy Holidays!

---

**Made with ❤️ using Temporal + OpenAI**

*"On the 12th day of Christmas, Temporal gave to me... a durable AI agent that never loses its place!"* 🎵