from pydantic import BaseModel, Field
from typing import Dict, Any

# Prompt documentation constants (optional and reusable across models/modules)
NOTES_DESCRIPTION = (
    "Full, unstructured PA notes for a single patient (e.g., copied from an EHR)."
)
QSET_DESCRIPTION = "Questionnaire (Qset) structure with dynamic branching logic, provided as a parsed JSON object."

EXAMPLE_NOTES = "Assessment: Patient has Type 2 Diabetes. No A1C recorded. History of elevated glucose."
EXAMPLE_QSET = {
    "6328799": {
        "question": "Does the patient have a diagnosis of type 2 diabetes mellitus?",
        "next_true": "6328801",
        "next_false": None,
    }
}


class SummarizeRequest(BaseModel):
    text: str


class QsetExtractionRequest(BaseModel):
    """
    Request model for initiating LLM-based Qset extraction from unstructured clinical notes.
    This is typically POSTed to the /api/qset/bulk-extract endpoint.
    """

    notes: str = Field(..., description=NOTES_DESCRIPTION, examples=[EXAMPLE_NOTES])
    qset: Dict[str, Any] = Field(
        ..., description=QSET_DESCRIPTION, examples=[EXAMPLE_QSET]
    )
