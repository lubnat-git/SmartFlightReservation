from fastapi import APIRouter, HTTPException

from app.schemas import AgentAsk, AgentResponse
from ai_agent.agent import run_flight_agent

router = APIRouter(prefix="/agent", tags=["AI Flight Agent"])


@router.post("/ask", response_model=AgentResponse)
def ask_flight_agent(request: AgentAsk):
    try:
        result = run_flight_agent(request.question)

        return AgentResponse(
            answer=result["answer"],
            flights=result["flights"],
            tools_used=result["tools_used"]
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="The AI flight agent encountered an unexpected error."
        )