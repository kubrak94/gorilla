import json
from pathlib import Path

from tqdm.auto import tqdm


###################
#                 #
#   single-turn   #
#                 #
###################


arabic_root = "data_translated"
english_root = "data"

the_root = Path("/home/kkubrak/rnd/tool_calling_benchmark/bfcl_eval/data_translated")

simple_files = [file_path 
for file_path in the_root.glob("*.json") 
if "multi_turn" not in str(file_path) and "memory" not in str(file_path) and "web_search" not in str(file_path)]

pbar = tqdm(simple_files)

save_folder_mask = "tool_calling_benchmark/bfcl_eval/data/user_prompt_{user_prompt}/func_desc_{func_desc}/func_param_desc_{func_param_desc}"

languages = ("ar", "en")

for user_prompt in languages:
    for func_desc in languages:
        for func_param_desc in languages:

            if user_prompt == func_desc and func_desc == func_param_desc:
                continue

            save_folder_path = Path(save_folder_mask.format(user_prompt=user_prompt, 
                                                            func_desc=func_desc, 
                                                            func_param_desc=func_param_desc))

            for file_path in pbar:
                pbar.set_description_str(f"{user_prompt} {func_desc} {func_param_desc} {file_path.name}")

                result = list()
            
                with open(file_path, "r") as file:
                    arabic_content = file.readlines()

                with open(str(file_path).replace(arabic_root, english_root), "r") as file:
                    english_content = file.readlines()

                for arab, eng in zip(arabic_content, english_content):
                    res = json.loads(eng)

                    ar_json = json.loads(arab)

                    # replace user prompt with Arabic
                    if user_prompt == "ar":
                        for i, question in enumerate(ar_json["question"]):
                            for j, _q in enumerate(question):

                                res["question"][i][j]["content"] = _q["content"]

                    # replace function description with Arabic
                    if func_desc == "ar":
                        for i, function in enumerate(ar_json["function"]):

                            res["function"][i]["description"] = function["description"]

                    # replace function parameters description with Arabic
                    if func_param_desc == "ar":
                        for i, function in enumerate(ar_json["function"]):
                            for param, param_info in function["parameters"]["properties"].items():

                                if (res["id"] == "parallel_9" and param == "time") \
                                or (res["id"] == "irrelevance_57" and param == "constraints") \
                                or (res["id"] == "irrelevance_128" and param == "user_responses") \
                                or (res["id"] == "irrelevance_149" and param == "available_colors"):
                                    res["function"][i]["parameters"]["properties"][param]["items"]["description"] = param_info["items"]["description"]
                                elif (res["id"] == "irrelevance_129" and param == "traits") \
                                or (res["id"] == "irrelevance_219" and param == "ingredients"):
                                    for _param, _param_info in param_info["items"]["properties"].items():
                                        res["function"][i]["parameters"]["properties"][param]["items"]["properties"][_param]["description"] = _param_info["description"]
                                elif (res["id"] == "irrelevance_238" and param == "pointA") \
                                or (res["id"] == "irrelevance_238" and param == "pointB"):
                                    for _param, _param_info in param_info["properties"].items():
                                        res["function"][i]["parameters"]["properties"][param]["properties"][_param]["description"] = _param_info["description"]
                                else:
                                    res["function"][i]["parameters"]["properties"][param]["description"] = param_info["description"]

                    result.append(res)

                with open(save_folder_path / file_path.name, "w") as file:
                    file.write("\n".join([json.dumps(res, ensure_ascii=False) for res in result]))


##########################
#                        #
#   multi-turn func doc  #
#                        #
##########################


arabic_root = "data_translated"
english_root = "data"

the_root = Path("/home/kkubrak/rnd/tool_calling_benchmark/bfcl_eval/data_translated/multi_turn_func_doc")

simple_files = [file_path 
for file_path in the_root.glob("*.json") 
]

pbar = tqdm(simple_files)

save_folder_mask = "tool_calling_benchmark/bfcl_eval/data/user_prompt_{user_prompt}/func_desc_{func_desc}/func_param_desc_{func_param_desc}/multi_turn_func_doc"

languages = ("ar", "en")

for user_prompt in languages:
    for func_desc in languages:
        for func_param_desc in languages:

            if user_prompt == func_desc and func_desc == func_param_desc:
                continue

            save_folder_path = Path(save_folder_mask.format(user_prompt=user_prompt, 
                                                            func_desc=func_desc, 
                                                            func_param_desc=func_param_desc))

            for file_path in pbar:
                pbar.set_description_str(f"{user_prompt} {func_desc} {func_param_desc} {file_path.name}")

                result = list()
            
                with open(file_path, "r") as file:
                    arabic_content = file.readlines()

                with open(str(file_path).replace(arabic_root, english_root), "r") as file:
                    english_content = file.readlines()

                for arab, eng in zip(arabic_content, english_content):
                    res = json.loads(eng)

                    ar_json = json.loads(arab)

                    # no need to replace user prompt with Arabic, since only the functions

                    # replace function description with Arabic
                    if func_desc == "ar":

                        res["description"] = ar_json["description"]

                    # replace function parameters description with Arabic
                    if func_param_desc == "ar":
                        for param, param_info in ar_json["parameters"]["properties"].items():
                            res["parameters"]["properties"][param]["description"] = param_info["description"]

                    result.append(res)

                with open(save_folder_path / file_path.name, "w") as file:
                    file.write("\n".join([json.dumps(res, ensure_ascii=False) for res in result]))


##################
#                #
#   multi-turn   #
#                #
##################

arabic_root = "data_translated"
english_root = "data"

the_root = Path("/home/kkubrak/rnd/tool_calling_benchmark/bfcl_eval/data_translated")

simple_files = [file_path 
for file_path in the_root.glob("*.json") 
if "multi_turn" in str(file_path)
]

pbar = tqdm(simple_files)

save_folder_mask = "tool_calling_benchmark/bfcl_eval/data/user_prompt_{user_prompt}/func_desc_{func_desc}/func_param_desc_{func_param_desc}"

languages = ("ar", "en")

for user_prompt in languages:
    for func_desc in languages:
        for func_param_desc in languages:

            if user_prompt == func_desc and func_desc == func_param_desc:
                continue

            save_folder_path = Path(save_folder_mask.format(user_prompt=user_prompt, 
                                                            func_desc=func_desc, 
                                                            func_param_desc=func_param_desc))

            for file_path in pbar:
                pbar.set_description_str(f"{user_prompt} {func_desc} {func_param_desc} {file_path.name}")

                result = list()
            
                with open(file_path, "r") as file:
                    arabic_content = file.readlines()

                with open(str(file_path).replace(arabic_root, english_root), "r") as file:
                    english_content = file.readlines()

                for arab, eng in zip(arabic_content, english_content):
                    res = json.loads(eng)

                    ar_json = json.loads(arab)

                    # replace user prompt with Arabic
                    if user_prompt == "ar":
                        for i, question in enumerate(ar_json["question"]):
                            for j, _q in enumerate(question):
                                # if "content" not in _q:
                                #     print("question", _q)
                                #     print(ar_json)
                                #     continue

                                res["question"][i][j]["content"] = _q["content"]
                        res["initial_config"] = ar_json["initial_config"]

                    # no need to replace  function description with Arabic, since only the user input

                    # no need to replace function parameters description with Arabic, since only the user input
                    result.append(res)

                with open(save_folder_path / file_path.name, "w") as file:
                    file.write("\n".join([json.dumps(res, ensure_ascii=False) for res in result]))
