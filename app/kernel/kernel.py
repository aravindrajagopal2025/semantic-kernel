from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from app.config import settings
from app.agents.summary_agent import SummaryAgent


def get_kernel() -> Kernel:
    """
    Sets up the Semantic Kernel with Azure OpenAI and all plugin agents.

    :return: Initialized Kernel object with agents registered.
    """
    kernel = Kernel()
    azure_chat_completion = AzureChatCompletion(
        service_id="azure_openai",
        deployment_name=settings.azure_openai_model,
        endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_key,
        api_version=settings.azure_openai_api_version,
    )
    kernel.add_service(azure_chat_completion)
    kernel.add_plugin(SummaryAgent(kernel), plugin_name="summary_agent")
    return kernel
