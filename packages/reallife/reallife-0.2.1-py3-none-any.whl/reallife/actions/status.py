import functools
import requests

def status(task:str,date:str,run_only = False):
    """执行任务并记录执行状态, 如果已经执行了则不再执行(每日)

    Args:
        task (str): 任务名称
        date (str): 2019-12-12

    Returns:
        str: '是否成功'
    """
    def outer_packing(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            response = requests.get(
                f"http://101.201.244.227:8000/action/{task}/{date}/status",timeout=20)
            print(response.json(),'vvv')
            if response.json().get('status') == '未执行':
                result = func(*args, **kwargs)
            else:
                result = None
            if run_only:
                response = requests.post(
                f"http://101.201.244.227:8000/action/{task}/{date}/execute",timeout=20)
            return result
        return wrapper
    return outer_packing
