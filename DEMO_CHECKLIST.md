# 🎄 12 Days of Christmas - Demo Checklist

A streamlined demo flow to showcase Temporal's durability vs non-durable agents.

---

## 🎯 Core Demo Flow (10 minutes)

### Demo 1: Worker Crash & Recovery
**Shows: Durability + Observability + Event Sourcing**

- [ ] **Setup** (30 seconds)
  - Open Temporal UI: `http://localhost:8233`
  - Open Streamlit with both tabs visible
  - Show Worker terminal running

- [ ] **Execute & Crash** (3 minutes)
  - Temporal tab: "Sing the entire 12 Days of Christmas song"
  - Watch verses in Worker terminal (point out full cumulative verses)
  - Switch to Temporal UI: Show workflow running, activities completing
  - Around verse 5-6: **Ctrl+C in Worker terminal** 💥
  - Point out: Worker died, but Temporal UI shows workflow still running!

- [ ] **Recovery** (2 minutes)
  - Restart worker: `uv run python worker.py`
  - Submit request again in Streamlit
  - **Watch it resume from verse 7** - no duplicates!
  - In Temporal UI: Show event history - all previous verses recorded
  - Explain: Event sourcing preserved state, deterministic replay reconstructed it

**Key Points to Cover:**
- ✅ Worker (execution) ≠ Workflow state (preserved in server)
- ✅ Event history in Temporal UI = full audit trail
- ✅ Zero wasted compute - completed work never redone

---

### Demo 2: The Contrast - Non-Durable Agent Failure
**Shows: Why durability matters**

- [ ] **Non-Temporal Comparison** (2 minutes)
  - Non-Temporal tab: "Sing the entire song"
  - Around verse 3-4: **Ctrl+C in Streamlit terminal** 💥
  - Restart Streamlit
  - Show: Everything lost, no memory, must start over
  - Explain: Single process = single point of failure

**Key Point:**
- ❌ No separation of concerns = lose everything on crash

---

### Demo 3: State Persistence Across UI Changes
**Shows: Workflow independence from client**

- [ ] **UI Independence** (2 minutes)
  - Temporal tab: Start "Sing the entire song"
  - While running: **Refresh browser page**
  - Show: Temporal UI still shows workflow running
  - Or: **Kill Streamlit entirely** (Ctrl+C)
  - Show: Temporal UI - workflow happily continues!
  - Restart Streamlit, submit again
  - Show: Reconnects to existing workflow, resumes

**Key Point:**
- ✅ Workflow lives in server, not in your UI process

---

## 🚀 Advanced Demos (Optional, if time)

### Demo 4: Multiple Crashes (Extreme Durability)
- [ ] Start full song → crash at verse 3 → restart → crash at verse 8 → restart
- [ ] Result: Still completes perfectly, survives multiple failures

### Demo 5: Time-Based Persistence
- [ ] Start full song → crash at verse 5 → wait 2-3 minutes → restart
- [ ] Result: Instantly resumes - state persisted the whole time

---

## 💡 Key Talking Points

**While demoing, weave these in:**

### The Problem (Non-Temporal)
- [ ] Long-running AI tasks crash = start over
- [ ] No visibility into what happened
- [ ] Wasted compute, wasted API calls, wasted money

### The Solution (Temporal)
- [ ] **Durability**: Event sourcing + deterministic replay
- [ ] **Observability**: Full history in Temporal UI
- [ ] **Separation**: Stateless workers + stateful server
- [ ] **Scalability**: Crash one worker, others pick up the work

### Production Use Cases
- [ ] Multi-step AI agents (research, data pipelines)
- [ ] Customer service workflows (survives deploy/restart)
- [ ] Long-running processes (hours/days)
- [ ] Error handling (smart retries, not start-over)

---

## 🎬 Quick Demo Script (5 minutes)

**For rushed demos:**

1. [ ] Temporal tab → "Sing entire song"
2. [ ] Kill worker at verse 5 → show Temporal UI still running
3. [ ] Restart worker → resumes perfectly
4. [ ] Non-Temporal tab → same test → everything lost
5. [ ] One-liner: "This is why production AI agents need durability"

---

## 🛠️ Setup Checklist

**Before demo:**
- [ ] Terminal 1: Temporal server running (`temporal server start-dev`)
- [ ] Terminal 2: Worker running (`uv run python worker.py`)
- [ ] Terminal 3: Streamlit running (`uv run streamlit run streamlit_app.py`)
- [ ] Browser: Temporal UI open (`http://localhost:8233`)
- [ ] Browser: Streamlit open (`http://localhost:8501`)

---

**Pro Tips:**
- Crash around verse 5-7 for dramatic effect (not too early/late)
- Keep Temporal UI visible to show real-time workflow state
- Point to Worker terminal to show activity execution
- Use "entire song" request for maximum impact (12 activities)
- Emphasize: This is production-ready, not a demo trick

**Happy Holidays! 🎄** Show why durable AI agents matter! 🚀

