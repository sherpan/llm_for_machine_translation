from litellm import completion
from opik import Opik
from opik import track
import opik
from opik.evaluation import evaluate
from opik.evaluation.metrics import LevenshteinRatio
from pydantic import BaseModel 
from gemba_metric import GEMBAMetric
import json

client = Opik()
dataset = client.get_dataset(name="punjabi_song_lyrics")

PROMPT_TEXT = """
Translate the following punjabi lyrics to english. Only return the translated lyrics in your response. 
Don't repeat the punjabi lyrics input as the answer

punjabi lyrics: {{lyrics}}

The format of the your response should be a JSON object with no additional text or backticks that follows the format:
        {{
            "english_lyrics": "<reason for the score>"
        }}
"""
# Create a prompt
prompt = opik.Prompt(
    name="prompt-mt",
    prompt=PROMPT_TEXT,
)


model = "ollama/deepseek-llm"
judge_model = "ollama/deepseek-llm"

@track(project_name="mt_lyrics_translations")
def mt_app(song_lyrics):
   response = completion(
        model=model, 
        messages=[{ "content": prompt.format(lyrics=song_lyrics),"role": "user"}], 
        api_base="http://localhost:11434"
    )
   output = response['choices'][0]['message']['content']
   json_output = json.loads(output)
   return json_output['english_lyrics']
          

def evaluation_task(x):
    return {
        "input": x['input'],
        "output": mt_app(x['input']),
        "reference": x['expected_output']
    }

leven_ratio = LevenshteinRatio()
gemba = GEMBAMetric(target_lang='english', source_lang='punjabi',model_name=judge_model)


evaluation = evaluate(
    project_name="mt_lyrics",
    dataset=dataset,
    task=evaluation_task, 
    scoring_metrics=[leven_ratio, gemba], 
    experiment_config={"model": model}, 
    prompt=prompt)
