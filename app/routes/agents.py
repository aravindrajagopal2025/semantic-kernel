from app.models.models import SummarizeRequest
from semantic_kernel.functions.kernel_arguments import KernelArguments
from app.kernel.kernel import get_kernel
from fastapi import APIRouter, HTTPException, Body
import json
from fastapi import status

router = APIRouter()


@router.post("/summarize/", response_model=dict)
async def summarize(request: SummarizeRequest) -> dict:
    """
    Summarize the given clinical text using the SummaryAgent.

    Args:
        request (SummarizeRequest): The clinical text to summarize.

    Returns:
        dict: { "summary": "<Summary text>" }

    Raises:
        HTTPException: 500 for internal errors.
    """
    kernel = get_kernel()
    try:
        out = await kernel.invoke(
            plugin_name="summary_agent",
            function_name="summarize",
            arguments=KernelArguments(text=request.text),
        )
        return {"summary": out.value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
