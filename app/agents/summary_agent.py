import logging
import json
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from app.config import settings
from app.utils.agents_common import AgentsCommon
from openai import AzureOpenAI


class SummaryAgent:
    SYSTEM_MESSAGE = "You are a clinical summarization assistant. Given a text, generate a concise and clinically relevant summary."
    PROMPT_TEMPLATE = (
        '''
         type-2 diabetes
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
