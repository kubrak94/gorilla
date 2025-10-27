from typing import Optional
import os, json
from pathlib import Path

import mlflow, hydra
from omegaconf import OmegaConf
import pandas as pd
from pydantic import BaseModel

from bfcl_eval.utils import create_files_subpath


class Config(BaseModel):
    model: str
    openai_base_url: str
    openai_api_key: str
    vllm_model_name: str
    user_prompt_lang: str
    func_desc_lang: str
    func_param_desc_lang: str
    num_threads: int = 5
    is_multi_turn: bool = False


@hydra.main(config_path="gosi-config", config_name="config", version_base="1.2")
def main(cfg):
    config = Config(**OmegaConf.to_container(cfg, resolve=True))
    system_prompt_lang = os.environ["SYSTEM_PROMPT_LANG"]

    if config.is_multi_turn:
        test_category = "multi_turn_base,multi_turn_miss_func,multi_turn_miss_param,multi_turn_long_context"
    else:
        test_category = "simple_python,simple_java,simple_javascript,parallel,multiple,parallel_multiple,irrelevance,live_simple,live_multiple,live_parallel,live_parallel_multiple,live_irrelevance,live_relevance"

    exit_code = os.system(f'bfcl generate --model "{config.model}" --test-category {test_category} --skip-server-setup --openai-base-url "{config.openai_base_url}" --openai-api-key "{config.openai_api_key}" --vllm-model-name "{config.vllm_model_name}" --user-prompt-lang "{config.user_prompt_lang}" --func-desc-lang "{config.func_desc_lang}" --func-param-desc-lang "{config.func_param_desc_lang}" --num-threads {config.num_threads}')

    if exit_code != 0:
        raise Exception("Did not run, see error")

    exit_code = os.system(f'export OPENAI_API_KEY={config.openai_api_key}; export OPENAI_BASE_URL={config.openai_base_url}; export VLLM_MODEL_NAME={config.vllm_model_name}; bfcl evaluate --model "{config.model}" --test-category {test_category} --user-prompt-lang "{config.user_prompt_lang}" --func-desc-lang "{config.func_desc_lang}" --func-param-desc-lang "{config.func_param_desc_lang}"')

    if exit_code != 0:
        raise Exception("Did not evaluate, see error")
    
    # make model name in accordance with the public leaderboard
    file_model_name = config.model[config.model.find("/") + 1:]
    file_model_name = file_model_name.replace("-FC", " (FC)") if file_model_name.endswith("-FC") else f"{file_model_name} (Prompt)"

    params_to_log = config.model_dump()
    params_to_log["system_prompt_lang"] = system_prompt_lang  # add system prompt language to logs

    # remove unnecessary params
    del params_to_log["openai_api_key"]
    del params_to_log["openai_base_url"]
    del params_to_log["vllm_model_name"]
    del params_to_log["num_threads"]

    mlflow.set_tracking_uri("")
    mlflow.set_experiment("gosi-fc-benchmark")
    mlflow.start_run(run_name=file_model_name)

    mlflow.log_params(params_to_log)
    
    subpath = create_files_subpath(config.user_prompt_lang, 
                                   config.func_desc_lang, 
                                   config.func_param_desc_lang,
                                   system_prompt_lang)
    
    file_path = Path("./score") / subpath / "data_overall.csv"  # path to .csv with all metrics stored

    df = pd.read_csv(file_path)

    entry = df[df["Model"] == file_model_name]

    metrics_to_log = ["Non-Live AST Acc", "Non-Live Simple AST", "Non-Live Multiple AST", "Non-Live Parallel AST",
                        "Non-Live Parallel Multiple AST", "Live Acc", "Live Simple AST", "Live Multiple AST",
                        "Live Parallel AST", "Live Parallel Multiple AST", "Multi Turn Acc", "Multi Turn Base", "Multi Turn Miss Func",
                        "Multi Turn Miss Param", "Multi Turn Long Context", "Relevance Detection", "Irrelevance Detection"]
    
    results = dict(entry[metrics_to_log].iloc[0])
    results = {k: float(results[k].replace("%", "")) if isinstance(results[k], str) else results[k] for k in results}

    mlflow.log_metrics(results)
    mlflow.end_run()


if __name__ == "__main__":
    main()