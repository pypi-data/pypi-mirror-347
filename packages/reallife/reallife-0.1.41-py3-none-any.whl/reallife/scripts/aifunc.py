""" ai 脚本"""

from datetime import datetime
from promptlibz import Templates,TemplateType
from llmada import BianXieAdapter
from llmada import GoogleAdapter

import re


def extract_type_code(text: str)->str:
    """从文本中提取python代码

    Args:
        text (str): 输入的文本。

    Returns:
        str: 提取出的python文本
    """
    pattern = r'```type([\s\S]*?)```'
    matches = re.findall(pattern, text)
    return matches[0].replace('\n','')


def give_a_task_time(task:str)->str:
    llm = GoogleAdapter()
    template = Templates(TemplateType.ESTIMATE_DURATION)
    prompt = template.format(task=task)

    completion = llm.product(prompt)
    if completion and len(completion)<5:
        return completion + " "+ task
    else:
        return "2P" + " "+ task

def generate_schedule(text: str,habit: str="") -> str:
    """
    使用 GPT 模型生成日程安排
    :param text: 输入文本
    :return: 生成的日程安排结果
    """
    llm = BianXieAdapter()
    llm.set_model("o3-mini")
    template = Templates(TemplateType.GENERATE_SCHEDULE)
    current_utc_time = str(datetime.today())[:-7]
    prompt = template.format(text=text,habit=habit,current_utc_time = current_utc_time)
    completion = llm.product(prompt)
    return completion

def judge_type(task:str):
    """判断任务类型

    Args:
        task (str): 任务
    """

    llm = BianXieAdapter()
    llm.set_model('gpt-4.1-mini')
    prompt = Templates(TemplateType.JUDGETYPE)
    completion = llm.product(prompt.format(task=task))
    return extract_type_code(completion)

