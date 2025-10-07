import logging
import json
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from app.config import settings
from app.utils.agents_common import AgentsCommon
from openai import AzureOpenAI


class SummaryAgent:
    SYSTEM_MESSAGE = "You are a clinical summarization assistant. Given structured patient data extracted from FHIR resources, generate a concise and clinically relevant summary. Include the patient's demographics, conditions, encounters, medications, observations (e.g., labs and vitals), and any adverse events. Focus on active problems and recent clinical activity. Use clear and concise language suitable for a clinician."
    PROMPT_TEMPLATE = (
        '''
      Patient: John Doe, 67M
Conditions:
- Type 2 Diabetes Mellitus (SNOMED 44054006), diagnosed 2015
- Hypertension (SNOMED 38341003)

resourceType: MedicationRequest
id: 123456
status: active
intent: order
medicationCodeableConcept.coding[0].system: http://www.nlm.nih.gov/research/umls/rxnorm
medicationCodeableConcept.coding[0].code: 860975
medicationCodeableConcept.coding[0].display: Metformin 500 MG Oral Tablet
subject.reference: Patient/789
authoredOn: 2023-05-01
dosageInstruction[0].text: Take one tablet twice daily


Allergies:
- Penicillin (rash)

Recent Encounter:
- Date: 2024-11-21
- Chief complaint: Increased thirst and urination

'''
    )

    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.llm_service = AzureOpenAI(
            api_key=settings.azure_openai_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_openai_api_version,
        )
        self.deployment_name = settings.azure_openai_model

    @kernel_function(description="Summarize clinical text in 2-3 clear sentences.")
    async def summarize(self, text: str) -> str:
        prompt = self.PROMPT_TEMPLATE.format(text=text)

        try:
            response = self.llm_service.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": self.SYSTEM_MESSAGE},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.0,
                max_tokens=500,
                top_p=0.8,
                logprobs=True,
            )

            summary = ""
            if (
                response.choices
                and response.choices[0].message
                and response.choices[0].message.content
            ):
                summary = response.choices[0].message.content.strip()

            avg_confidence = AgentsCommon.get_confidence_score_from_llm_response(
                response
            )

            summary_json = {"summary": summary, "confidence_score": avg_confidence}
            return json.dumps(summary_json)

        except Exception as e:
            logging.error(f"LLM error in summarization: {e}")
            error_response = {"error": "Summary unavailable due to an internal error."}
            return json.dumps(error_response)


    async def flatten_fhir_json(data, parent_key='', sep='.'):
        """
        Recursively flattens FHIR JSON into a flat dict with dot-separated keys.
        """
        items = []
        
        if isinstance(data, dict):
            for k, v in data.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                items.extend(flatten_fhir_json(v, new_key, sep=sep).items())
        elif isinstance(data, list):
            for i, v in enumerate(data):
                new_key = f"{parent_key}[{i}]"
                items.extend(flatten_fhir_json(v, new_key, sep=sep).items())
        else:
            items.append((parent_key, data))
        
        return dict(items)
