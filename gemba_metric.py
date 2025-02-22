from opik.evaluation.metrics import base_metric, score_result
from opik.evaluation import models
from pydantic import BaseModel
import json
from typing import Any

class LLMJudgeResult(BaseModel):
    score: int
    reason: str

class GEMBAMetric(base_metric.BaseMetric):
    def __init__(self, target_lang, source_lang, model_name: str = "gpt-4o"):
        self.name = "GEMBA"
        self.llm_client = models.LiteLLMChatModel(model_name=model_name)
        self.source_lang = source_lang
        self.target_lang = target_lang
        
        self.prompt_template = """
        Score the following translation from {source_lang} to {target_lang} with respect
        to the human reference on a continuous scale from 0 to 100, where score of zero means
        "no meaning preserved" and score of one hundred means "perfect meaning and grammar".
        {source_lang} source: "{source_seg}"
        {target_lang} human reference: {reference_seg}
        {target_lang} translation: "{target_seg}"
        
        The format of the your response should be a JSON object with no additional text or backticks that follows the format:
        {{
            "score": <score between 0 and 100>,
            "reason": "<reason for the score>"
        }}
        """
      
    def score(self, input: str, reference: str, output:str, **ignored_kwargs: Any):
        """
        Score the output of an LLM.
        Args:
            output: The output of an LLM to score.
            **ignored_kwargs: Any additional keyword arguments. This is important so that the metric can be used in the `evaluate` function.
        """
        # Construct the prompt based on the output of the LLM
        prompt = self.prompt_template.format(source_seg=input, reference_seg=reference, target_seg=output, source_lang=self.source_lang, target_lang=self.target_lang)
        # Generate and parse the response from the LLM
        response = self.llm_client.generate_string(input=prompt)
        response_dict = json.loads(response)
        
        return score_result.ScoreResult(
            name=self.name,
            value=response_dict["score"],
            reason=response_dict["reason"]
        )
    