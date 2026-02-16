# Assignment 5: Financial Approval System with Human-in-the-Loop

## Tech Stack
- **Backend**: Python 3.11+, FastAPI, LangGraph, LangChain
- **Frontend**: Next.js 15, React 19, CopilotKit, Tailwind CSS
- **LLM**: OpenAI GPT-4o-mini (default) or Google Gemini 2.0 Flash
- **Persistence**: SQLite (checkpoints), SqliteSaver
- **Evaluation**: LangSmith
- **Testing**: pytest

## Project Structure
```
assignment-5/
├── backend/
│   ├── server.py              # FastAPI + CopilotKit endpoint
│   ├── config.py              # Env loading, LLM factory, budget limits
│   ├── models.py              # Pydantic schemas
│   ├── seed_data.py           # Sample financial requests
│   ├── agent/
│   │   ├── state.py           # ApprovalState TypedDict
│   │   ├── graph.py           # ★ LangGraph StateGraph (STUDENT)
│   │   ├── nodes.py           # ★ 8 nodes + 6 routers (STUDENT)
│   │   └── checkpointer.py   # SQLite checkpointer factory
│   ├── guardrails/
│   │   ├── input_validator.py # ★ Input validation (STUDENT)
│   │   └── output_filter.py  # ★ Output/PII filtering (STUDENT)
│   └── evaluation/
│       ├── dataset.py         # 10 eval test cases
│       ├── evaluators.py      # ★ LangSmith evaluators (STUDENT)
│       └── run_eval.py        # Evaluation runner
├── frontend/
│   └── src/
│       ├── app/
│       │   ├── layout.tsx     # CopilotKit provider
│       │   ├── page.tsx       # Main page with CopilotChat
│       │   └── api/copilotkit/route.ts
│       └── components/
│           ├── ApprovalPanel.tsx # Interrupt UI (useLangGraphInterrupt)
│           ├── RequestForm.tsx
│           ├── WorkflowStatus.tsx
│           └── RequestHistory.tsx
└── tests/                     # Test harnesses (all GIVEN)
```

## Student Tasks (5 files, 75 points + 25 bonus)

### Part 1: LangGraph Workflow (35 pts)
- `backend/agent/nodes.py`: 8 node functions + 6 routing functions
- `backend/agent/graph.py`: StateGraph assembly with conditional edges

### Part 2: Safety Guardrails (20 pts)
- `backend/guardrails/input_validator.py`: validate_request, validate_amount, sanitize_text
- `backend/guardrails/output_filter.py`: sanitize_output, mask_financial_details

### Part 3: CopilotKit Frontend (GIVEN)
- Frontend is fully implemented — study the code to learn the patterns

### Part 4: LangSmith Evaluation (20 pts)
- `backend/evaluation/evaluators.py`: risk accuracy + approval consistency evaluators

## Key Commands

```bash
# Setup
conda create -n hitl-agent python=3.11 -y && conda activate hitl-agent
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..

# Run
python -m backend.server                    # Backend on :8000
cd frontend && npm run dev                  # Frontend on :3000

# Test
python -m pytest tests/ -v                  # All tests
python -m backend.evaluation.run_eval       # Evaluation pipeline
```

## Key Patterns
- **interrupt()**: Pauses graph execution, sends data to frontend
- **Command(resume=value)**: Resumes graph with human decision
- **SqliteSaver**: Checkpoints graph state for interrupt/resume
- **useLangGraphInterrupt**: React hook that fires on graph interrupts
- **resolve()**: Sends decision from frontend back to graph
