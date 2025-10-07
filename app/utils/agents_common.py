import numpy as np
import logging


class AgentsCommon:
    @staticmethod
    def get_confidence_score_from_llm_response(response) -> float | None:
        """
        Extracts a confidence score from an LLM response object.

        Args:
            response: The LLM response containing choices and logprobs.

        Returns:
            Average confidence score as a float or None if not available.
        """
        try:
            if not response.choices:
                return None
            choice = response.choices[0]
            if not choice.logprobs or not choice.logprobs.content:
                return None
            token_logprobs = choice.logprobs.content
            logprob_values = [t.logprob for t in token_logprobs]
            if not logprob_values:
                return None
            confidences = np.exp(logprob_values)
            return float(np.mean(confidences))
        except Exception as e:
            logging.error(f"Error extracting confidence score: {e}")
            return None
