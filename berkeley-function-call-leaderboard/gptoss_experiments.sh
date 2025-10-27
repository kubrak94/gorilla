#!/bin/bash

# ==============================================================================
# Bash Script for Running Generation and Evaluation Commands
#
# This script automates the process of running bfcl commands with all possible
# language combinations as per the specified requirements.
#
# It iterates through 8 unique combinations for:
#   - SYSTEM_PROMPT_LANG (en, ar)
#   - user-prompt-lang (en, ar)
#   - func-desc-lang / func-param-desc-lang (en, ar)
#
# For each combination, it first runs the 'generate' command, and upon
# successful completion, it runs the corresponding 'evaluate' command.
# ==============================================================================

# --- Configuration ---
# You can modify these variables if your base command changes in the future.
MODEL_PREFIX="openai/"
MODEL="gpt-oss-20b"
TEST_CATEGORY="simple_python,simple_java,simple_javascript,parallel,multiple,parallel_multiple,irrelevance,live_simple,live_multiple,live_parallel,live_parallel_multiple,live_irrelevance,live_relevance"
TEST_CATEGORY="multi_turn_base,multi_turn_miss_func,multi_turn_miss_param,multi_turn_long_context"
NUM_THREADS=15
VLLM_MODEL_NAME="gpt-oss-20b"
OPENAI_API_KEY=""
OPENAI_BASE_URL=""
MLFLOW_URL=""
MLFLOW_EXP="gosi-fc-benchmark"
# --- End of Configuration ---


# --- Main Execution Loop ---
# Nested loops to iterate through all possible language combinations.
for sys_lang in "en" "ar"; do
  for user_lang in "en" "ar"; do
    for func_lang in "en" "ar"; do
      
      # --- Print Current Combination ---
      echo "======================================================================"
      echo "RUNNING COMBINATION:"
      echo "  - SYSTEM_PROMPT_LANG:   $sys_lang"
      echo "  - user-prompt-lang:     $user_lang"
      echo "  - func-desc-lang:       $func_lang"
      echo "  - func-param-desc-lang: $func_lang"
      echo "----------------------------------------------------------------------"

      # --- 1. Generation Step ---
      echo "--> Starting Generation..."
      export SYSTEM_PROMPT_LANG=$sys_lang
      
      bfcl generate \
        --model "$MODEL" \
        --test-category "$TEST_CATEGORY" \
        --num-threads "$NUM_THREADS" \
        --user-prompt-lang "$user_lang" \
        --func-desc-lang "$func_lang" \
        --func-param-desc-lang "$func_lang" \
        --vllm-model-name "$VLLM_MODEL_NAME" \
        --openai-api-key "$OPENAI_API_KEY" \
        --openai-base-url "$OPENAI_BASE_URL"

      # Check the exit code of the generate command.
      if [ $? -ne 0 ]; then
        echo "[ERROR] Generation failed for the combination above. Skipping evaluation and moving to the next set."
        echo "======================================================================"
        echo ""
        continue # Skip to the next combination
      fi
      echo "--> Generation finished successfully."
      echo ""


      # --- 2. Evaluation Step ---
      echo "--> Starting Evaluation..."
      export OPENAI_API_KEY=$OPENAI_API_KEY; export OPENAI_BASE_URL=$OPENAI_BASE_URL; \
      bfcl evaluate \
        --model "$MODEL" \
        --test-category "$TEST_CATEGORY" \
        --user-prompt-lang "$user_lang" \
        --func-desc-lang "$func_lang" \
        --func-param-desc-lang "$func_lang"

      python -c """from pathlib import Path

import mlflow
import pandas as pd

from bfcl_eval.utils import create_files_subpath


file_model_name = '$MODEL_PREFIX$MODEL (FC)'

params_to_log = dict()
params_to_log['system_prompt_lang'] = '$sys_lang'  # add system prompt language to logs
params_to_log['user_prompt_lang'] = '$user_lang'
params_to_log['func_desc_lang'] = '$func_lang'
params_to_log['func_param_desc_lang'] = '$func_lang'
params_to_log['model'] = '$MODEL'

mlflow.set_tracking_uri('$MLFLOW_URL')
mlflow.set_experiment('$MLFLOW_EXP')
mlflow.start_run(run_name=file_model_name)

mlflow.log_params(params_to_log)

subpath = create_files_subpath('$user_lang', 
                               '$func_lang', 
                               '$func_lang',
                               '$sys_lang')

file_path = Path('./score') / subpath / 'data_overall.csv'  # path to .csv with all metrics stored

df = pd.read_csv(file_path)

entry = df[df['Model'] == file_model_name]

metrics_to_log = ['Non-Live AST Acc', 'Non-Live Simple AST', 'Non-Live Multiple AST', 'Non-Live Parallel AST',
'Non-Live Parallel Multiple AST', 'Live Acc', 'Live Simple AST', 'Live Multiple AST',
'Live Parallel AST', 'Live Parallel Multiple AST', 'Multi Turn Acc', 'Multi Turn Base', 'Multi Turn Miss Func',
'Multi Turn Miss Param', 'Multi Turn Long Context', 'Relevance Detection', 'Irrelevance Detection']

results = dict(entry[metrics_to_log].iloc[0])
results = {k: float(results[k].replace('%', '')) if isinstance(results[k], str) else results[k] for k in results}

mlflow.log_metrics(results)
mlflow.end_run()
"""

      # Check the exit code of the evaluate command.
      if [ $? -ne 0 ]; then
        echo "[ERROR] Evaluation failed for the combination above."
      else
        echo "--> Evaluation finished successfully."
      fi
      
      echo "======================================================================"
      echo ""
      echo ""

    done
  done
done

echo "All 8 combinations have been processed. Script finished."
