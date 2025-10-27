# Multilingual Berkley Function Calling Leaderboard

This update enhances the [**BFCL (Berkeley Function Calling Leaderboard)**](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard) codebase by introducing full support for multilingual configurations. It enables robust testing and validation of language-aware behavior across critical components of the system, ensuring consistent performance and contextual accuracy in diverse linguistic environments.

The system now allows dynamic language configuration for:
- System prompt  
- User query  
- Function description  
- Function parameter descriptions  

This capability ensures that model responses and output formatting remain contextually appropriate, culturally sensitive, and linguistically accurate — regardless of the input language.

*Current Language Support*:
- **English** (default/original)
- **Arabic** (fully supported with bidirectional text handling)


## Installation & Setup

```bash
# Create a new Conda environment with Python 3.10
conda create -n BFCL python=3.10
conda activate BFCL

# Clone the Gorilla repository
git clone https://gitlab.gcp.gosi.cloud/gosi-ai-sandbox/gosi-ai/rnd.git

# Change directory to the `tool_calling_benchmark`
cd rnd/tool_calling_benchmark

# Install the package in editable mode
pip install -e .
```

## Running Evaluation

```bash
export SYSTEM_PROMPT_LANG=en; python -m gosi_benchmark -m "+model=Qwen/Qwen3-30B-A3B-Instruct-2507" "+openai_base_url=https://your.base.url/v1" "+openai_api_key=YOUR_API_KEY" "+vllm_model_name=YOUR_MODEL_NAME" "+user_prompt_lang=en" "+func_desc_lang=en" "+func_param_desc_lang=en" "+num_threads=100" "+is_multi_turn=True"
```
- `SYSTEM_PROMPT_LANG`: setting language of a system prompt, available options ar, en;
- `model`: name of the model being tested, please refer to **Model ID on BFCL** column of [SUPPORTED_MODELS.md](./SUPPORTED_MODELS.md), choose *Self-hosted* provider
- `openai_base_url`: URL of endpoint for testing model
- `openai_api_key`: API key of endpoint for testing `model`
- `user_prompt_lang`: setting language of a user prompt, available options `ar`, `en`;
- `func_desc_lang`: setting language of a  function description, available options `ar`, `en`;
- `func_param_desc_lang`: setting language of a function parameters description, available options `ar`, `en`;
- `num_threads`: # of concurrent requests to be sent to the endpoint;
- `is_multi_turn`: whether run time-comsuming set of multi-turn experiments (True) or just single-turn one (False).

## (Optional) Configuring Project Root Directory
By default, Project Root Directory is `berkeley-function-call-leaderboard` directory.

If you wish to change, set `BFCL_PROJECT_ROOT` as an environment variable in your shell environment:

```bash
# In your shell environment
export BFCL_PROJECT_ROOT=/path/to/your/desired/project/directory
```
