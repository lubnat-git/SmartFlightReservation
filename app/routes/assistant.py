
from fastapi import APIRouter, HTTPException

from app.schemas import AssistantAsk, AssistantResponse
from rag_pipeline import ask_travel_assistant


router = APIRouter(
    prefix="/assistant",
    tags=["AI Travel Assistant"]
)


@router.post("/ask", response_model=AssistantResponse)
def ask_assistant(request: AssistantAsk):

    try:
        result = ask_travel_assistant(request.question)

        return AssistantResponse(
            answer=result["answer"],
            sources=result["sources"]
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="The AI travel assistant encountered an unexpected error."
        )
