# llm_for_machine_translation

A sentimantal side project where I benchmark LLMs on their ability to understand and translate Punjabi Song Lyrics to English. 

## Powerful Open-Source Tools 

ollama: for locally hosting open-source models like LLama3 and DeepseekLLM on my Macbook Pro

litellm: for making it easy to switch out the underlying model used without requiring major code changes

Opik: for providing a framework to systemicatically and quantatively test and evaluate your LLM Apps 

## Getting Started 

### Upload our labeled dataset to Opik 

I created json file of 21 punjabi song lyrics and their english translations to use as my "golden" dataset. I first upload this to Opik and we'll use
this dataset for benchmarking.

```sh
python upload_dataset_to_opik.py
```

### Serve an open-source model locally 

```sh
ollama run deepseek-llm
```

### Run the Evaluation Script 
When building with LLMs, we want to find the ideal recipe that will give us the best results and we can deploy it to production. This recipie is some ideal combination of the model, the prompt, hyper-parameters, and if your building a more advanced solution: your RAG pipeline or agenetic workflow. LiteLLM and Opik make a deadly combo for developers to set up the experimentation to find this recepie. 

To make a data driven decision on what recipie we need some metrics to benchmark performance. For machine-translation, I decided to use two metrics: BLEU and GEMBA. BLEU is an out-of-the-box heuristic metric found in Opik thats been historically used to evaluate machine translation systems. GEMBA is a new llm-as-a-judge metric which I implemented as a custom metric in the 'gemba_metric.py' file. 

```sh
python mt_eval_app.py
```
Runs an eval on our lyric dataset and returns our metrics. 

As we iterate on the prompt, maybe change the model to llama3/gpt-4/claude3.5, agentify the app, or add a RAG workflow, we use to the Opik UI to see how the experiment performed, debug at the sample-level, and even compare eval runs side-by-side. 











