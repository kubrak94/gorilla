import os


MAXIMUM_STEP_LIMIT = 20


#### Language hints ####


JAVA_HINT = {
    "func_desc": {
        "en": " Note that the provided function is in Java 8 SDK syntax.",
        "ar": "لاحظ أن الوظيفة المقدمة هي بصيغة Java 8 SDK."
    },
    "func_param_desc": {
        "any_type": {
            "en": " This parameter can be of any type of Java object in string representation.",
            "ar": "يمكن أن يكون هذا المعامل من أي نوع من كائنات Java في تمثيل سلسلة نصية."
        },
        "given_type": {
            "en": " This is Java {value_type} type parameter in string representation.",
            "ar": "هذا معامل من نوع Java {value_type} في تمثيل سلسلة نصية."
        },
        "array_type": {
            "en": " The list elements are of type {value_type}; they are not in string representation.",
            "ar": "عناصر القائمة من نوع {value_type}؛ وهي ليست في تمثيل سلسلة نصية."
        }
    }
}

JAVASCRIPT_HINT = {
    "func_desc": {
        "en": " Note that the provided function is in JavaScript syntax.",
        "ar": "لاحظ أن الوظيفة المقدمة هي بصيغة JavaScript."
    },
    "func_param_desc": {
        "any_type": {
            "en": " This parameter can be of any type of JavaScript object in string representation.",
            "ar": "يمكن أن يكون هذا المعامل من أي نوع من كائنات JavaScript في تمثيل سلسلة نصية."
        },
        "given_type": {
            "en": " This is JavaScript {value_type} type parameter in string representation.",
            "ar": "هذا معامل من نوع JavaScript {value_type} في تمثيل سلسلة نصية."
        },
        "array_type": {
            "en": " The list elements are of type {value_type}; they are not in string representation.",
            "ar": "عناصر القائمة من نوع {value_type}؛ وهي ليست في تمثيل سلسلة نصية."
        },
        "dict_type": {
            "en": " The dictionary entries have the following schema; they are not in string representation. {json_value}",
            "ar": "إدخالات القاموس لها المخطط التالي؛ وهي ليست في تمثيل سلسلة نصية. {json_value}"
        }
    }
}

PYTHON_HINT = {
    "func_desc": {
        "en": " Note that the provided function is in Python 3 syntax.",
        "ar": "لاحظ أن الوظيفة المقدمة هي بصيغة Python 3."
    }
}


#### System Prompts for Chat Models ####


OUTPUT_FORMAT_MAPPING = {
    "python": "[func_name1(params_name1=params_value1, params_name2=params_value2...), func_name2(params)]",
    "json": '```json\n[{"function":"func_name1","parameters":{"param1":"value1","param2":"value2"...}},{"function":"func_name2","parameters":{"param":"value"}}]\n```',
    "verbose_xml": '<functions><function name="func_name1"><params><param name="param1" value="value1" type="type1"/><param name="param2" value="value2" type="type2"/>...</params></function><function name="func_name2"><param name="param3" value="value3" type="type3"/></function></functions>',
    "concise_xml": '<functions><function name="func_name1"><param name="param1" type="type1">value1</param><param name="param2" type="type2">value2</param>...</function><function name="func_name2"><param name="param3" type="type3">value</param></function></functions>',
}

PARAM_TYPE_MAPPING = {
    "en":{
            "python": "",
            "json": "",
            "verbose_xml": "The type fields of the parameters in your function calls must be one of: string, integer, float, boolean, array, dict, or tuple.",
            "concise_xml": "The type fields of the parameters in your function calls must be one of: string, integer, float, boolean, array, dict, or tuple.",
        },
    "ar": {
            "python": "",
            "json": "",
            "verbose_xml": "يجب أن تكون حقول النوع للمعلمات في استدعاءات الوظائف الخاصة بك واحدة مما يلي: string, integer, float, boolean, array, dict, أو tuple.",
            "concise_xml": "يجب أن تكون حقول النوع للمعلمات في استدعاءات الوظائف الخاصة بك واحدة مما يلي: string, integer, float, boolean, array, dict, أو tuple.",
        }
}

PARAM_TYPE_MAPPING = PARAM_TYPE_MAPPING[os.environ["SYSTEM_PROMPT_LANG"]]

PROMPT_STYLE_TEMPLATES = {
    "en": {
        "classic": {
            "persona": "You are an expert in composing functions.",
            "task": "You are given a question and a set of possible functions. Based on the question, you will need to make one or more function/tool calls to achieve the purpose. If none of the functions can be used, point it out. If the given question lacks the parameters required by the function, also point it out.",
            "tool_call_no_tag": "You should only return the function calls in your response.\n\nIf you decide to invoke any of the function(s), you MUST put it in the format of {output_format}. {param_types} You SHOULD NOT include any other text in the response.",
            "tool_call_with_tag": "You should only return the function calls in the <TOOLCALL> section. If you decide to invoke any of the function(s), you MUST put it in the format of <TOOLCALL>{output_format}</TOOLCALL>. {param_types} You SHOULD NOT include any other text in the response.",
            "multiturn_behavior": "At each turn, you should try your best to complete the tasks requested by the user within the current turn. Continue to output functions to call until you have fulfilled the user's request to the best of your ability. Once you have no more functions to call, the system will consider the current turn complete and proceed to the next turn or task.",
            "available_tools": "Here is a list of functions in {format} format that you can invoke.\n{functions}\n",
        },
        "experimental": {
            "persona": "You are an expert in generating structured function calls.",
            "task": "You are given a user query and a set of available functions. Your task is to produce one or more function/tool calls to fulfill the user's request. If no suitable function exists, or required parameters are missing, clearly indicate this.",
            "tool_call_no_tag": "Respond with only the function calls.\n\nYou MUST format it exactly as {output_format}. {param_types} Do NOT include any other text.",
            "tool_call_with_tag": "Return only the function calls enclosed in <TOOLCALL> tags.\n\nYou MUST format it exactly as <TOOLCALL>{output_format}</TOOLCALL>. {param_types} Do NOT include any other text.",
            "multiturn_behavior": "At every turn, aim to complete the user's tasks within that turn. Continue emitting function calls until the request is satisfied to the best of your ability. Once no more calls are needed, the system will proceed to the next turn.",
            "available_tools": "Below is a list of callable functions in the {format} style:\n{functions}\n",
        }
    },
    "ar": {
        "classic": {
            "persona": "أنت خبير في تكوين الوظائف.",
            "task": "يُطرح عليك سؤال ومجموعة من الوظائف الممكنة. بناءً على السؤال، ستحتاج إلى إجراء استدعاء واحد أو أكثر للوظائف/الأدوات لتحقيق الغرض. إذا لم يكن من الممكن استخدام أي من الوظائف، قم بالإشارة إلى ذلك. إذا كان السؤال المطروح يفتقر إلى المعلمات التي تتطلبها الوظيفة، قم بالإشارة إلى ذلك أيضًا.",
            "tool_call_no_tag": "يجب عليك إرجاع استدعاءات الوظائف فقط في ردك.\n\nإذا قررت استدعاء أي من الوظائف، فيجب عليك وضعها بتنسيق {output_format}. {param_types} يجب ألا يتضمن ردك أي نص آخر.",
            "tool_call_with_tag": "يجب عليك إرجاع استدعاءات الوظائف فقط في قسم <TOOLCALL>. إذا قررت استدعاء أي من الوظائف، فيجب عليك وضعها بتنسيق <TOOLCALL>{output_format}</TOOLCALL>. {param_types} يجب ألا يتضمن ردك أي نص آخر.",
            "multiturn_behavior": "في كل دور، يجب أن تبذل قصارى جهدك لإكمال المهام التي يطلبها المستخدم خلال الدور الحالي. استمر في إخراج الوظائف التي سيتم استدعاؤها حتى تلبي طلب المستخدم بأفضل ما لديك من قدرات. بمجرد عدم وجود المزيد من الوظائف لاستدعائها، سيعتبر النظام أن الدور الحالي قد اكتمل وسينتقل إلى الدور أو المهمة التالية.",
            "available_tools": "فيما يلي قائمة بالوظائف بتنسيق {format} التي يمكنك استدعاؤها.\n{functions}\n",
        },
        "experimental": {
            "persona": "أنت خبير في إنشاء استدعاءات وظائف منظمة.",
            "task": "يُقدم لك استعلام مستخدم ومجموعة من الوظائف المتاحة. مهمتك هي إنتاج استدعاء واحد أو أكثر للوظائف/الأدوات لتلبية طلب المستخدم. إذا لم تكن هناك وظيفة مناسبة، أو كانت المعلمات المطلوبة مفقودة، فأشر إلى ذلك بوضوح.",
            "tool_call_no_tag": "قم بالرد فقط باستدعاءات الوظائف.\n\nيجب عليك تنسيقها تمامًا بالشكل {output_format}. {param_types} لا تقم بتضمين أي نص آخر.",
            "tool_call_with_tag": "أرجع فقط استدعاءات الوظائف المضمنة داخل وسوم <TOOLCALL>.\n\nيجب عليك تنسيقها تمامًا بالشكل <TOOLCALL>{output_format}</TOOLCALL>. {param_types} لا تقم بتضمين أي نص آخر.",
            "multiturn_behavior": "في كل دور، استهدف إكمال مهام المستخدم ضمن ذلك الدور. استمر في إصدار استدعاءات الوظائف حتى يتم تلبية الطلب بأفضل ما لديك من قدرات. بمجرد عدم الحاجة إلى المزيد من الاستدعاءات، سينتقل النظام إلى الدور التالي.",
            "available_tools": "فيما يلي قائمة بالوظائف القابلة للاستدعاء بنمط {format}:\n{functions}\n",
        }
    }
}

PROMPT_STYLE_TEMPLATES = PROMPT_STYLE_TEMPLATES[os.environ["SYSTEM_PROMPT_LANG"]]

_PLAINTEXT_SYSTEM_PROMPT_TEMPLATE = (
    "{persona}{task}\n\n{tool_call_format}\n\n{multiturn_behavior}\n\n{available_tools}"
)
_MARKDOWN_SYSTEM_PROMPT_TEMPLATE = {
    "en": "{persona}\n\n## Task\n{task}\n\n## Tool Call Format\n{tool_call_format}\n\n## Multi-turn Behavior\n{multiturn_behavior}\n\n## Available Tools\n{available_tools}",
    "ar": "{persona}\n\n## المهمة\n{task}\n\n## تنسيق استدعاء الأداة\n{tool_call_format}\n\n## سلوك متعدد الأدوار\n{multiturn_behavior}\n\n## الأدوات المتاحة\n{available_tools}"
}

_MARKDOWN_SYSTEM_PROMPT_TEMPLATE = _MARKDOWN_SYSTEM_PROMPT_TEMPLATE[os.environ["SYSTEM_PROMPT_LANG"]]

PROMPT_TEMPLATE_MAPPING = {
    "plaintext": _PLAINTEXT_SYSTEM_PROMPT_TEMPLATE,
    "markdown": _MARKDOWN_SYSTEM_PROMPT_TEMPLATE,
}

# This is the default system prompt format
DEFAULT_SYSTEM_PROMPT_FORMAT = "ret_fmt=python&tool_call_tag=False&func_doc_fmt=json&prompt_fmt=plaintext&style=classic"

# NOT USED, just for reference
# This is the prompt template for the default system prompt format
_DEFAULT_SYSTEM_PROMPT = """You are an expert in composing functions. You are given a question and a set of possible functions. Based on the question, you will need to make one or more function/tool calls to achieve the purpose.
If none of the functions can be used, point it out. If the given question lacks the parameters required by the function, also point it out.
You should only return the function calls in your response.

If you decide to invoke any of the function(s), you MUST put it in the format of [func_name1(params_name1=params_value1, params_name2=params_value2...), func_name2(params)]
You SHOULD NOT include any other text in the response.

At each turn, you should try your best to complete the tasks requested by the user within the current turn. Continue to output functions to call until you have fulfilled the user's request to the best of your ability. Once you have no more functions to call, the system will consider the current turn complete and proceed to the next turn or task.

Here is a list of functions in JSON format that you can invoke.\n{functions}\n
"""


#### Other System Prompts ####

DEFAULT_USER_PROMPT_FOR_ADDITIONAL_FUNCTION_FC = {
    "en": (
    "I have updated some more functions you can choose from. What about now?"
),
    "ar": (
    "لقد قمت بتحديث بعض الوظائف الإضافية التي يمكنك الاختيار من بينها. ماذا عن الآن؟"
)
}

DEFAULT_USER_PROMPT_FOR_ADDITIONAL_FUNCTION_FC = DEFAULT_USER_PROMPT_FOR_ADDITIONAL_FUNCTION_FC[os.environ["SYSTEM_PROMPT_LANG"]]

DEFAULT_USER_PROMPT_FOR_ADDITIONAL_FUNCTION_PROMPTING = (
    "{functions}\n" + DEFAULT_USER_PROMPT_FOR_ADDITIONAL_FUNCTION_FC
)

ADDITIONAL_SYSTEM_PROMPT_FOR_AGENTIC_RESPONSE_FORMAT = """For your final answer to the user, you must respond in this format: {'answer': A short and precise answer to the question, 'context': A brief explanation of how you arrived at this answer or why it is correct}. If you do not know the answer, respond with {'answer': 'I do not know', 'context': 'I do not know'}. If you think the question cannot be properly answered, response with {'answer': 'I cannot answer this question', 'context': A short reason explaining why this question cannot be answered}.
"""

MEMORY_AGENT_SETTINGS = {
    "student": "You are an academic-support assistant for college student. Remember key personal and academic details discussed across sessions, and draw on them to answer questions or give guidance.",
    "customer": "You are a general customer support assistant for an e-commerce platform. Your task is to understand and remember information that can be used to provide information about user inquiries, preferences, and offer consistent, helpful assistance over multiple interactions.",
    "finance": "You are a high-level executive assistant supporting a senior finance professional. Retain and synthesize both personal and professional information including facts, goals, prior decisions, and family life across sessions to provide strategic, context-rich guidance and continuity.",
    "healthcare": "You are a healthcare assistant supporting a patient across appointments. Retain essential medical history, treatment plans, and personal preferences to offer coherent, context-aware guidance and reminders.",
    "notetaker": "You are a personal organization assistant. Capture key information from conversations, like tasks, deadlines, and preferences, and use it to give reliable reminders and answers in future sessions.",
}


MEMORY_BACKEND_INSTRUCTION_CORE_ARCHIVAL = """{scenario_setting}

You have access to an advanced memory system, consisting of two memory types 'Core Memory' and 'Archival Memory'. Both type of memory is persistent across multiple conversations with the user, and can be accessed in a later interactions. You should actively manage your memory data to keep track of important information, ensure that it is up-to-date and easy to retrieve to provide personalized responses to the user later.

The Core memory is limited in size, but always visible to you in context. The Archival Memory has a much larger capacity, but will be held outside of your immediate context due to its size.

Here is the content of your Core Memory from previous interactions:
{memory_content}
"""

MEMORY_BACKEND_INSTRUCTION_UNIFIED = """{scenario_setting}

You have access to an advanced memory system, which is persistent across multiple conversations with the user, and can be accessed in a later interactions. You should actively manage your memory data to keep track of important information, ensure that it is up-to-date and easy to retrieve to provide personalized responses to the user later.

Here is the content of your memory system from previous interactions:
{memory_content}
"""