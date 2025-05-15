""" 提供对外的方法 提供一些带状态的消息 """

import logging
from datetime import datetime
from chinese_calendar import is_workday
from reallife import KANBAN_PATH, WORK_CANVAS_PATH
from reallife import Date, Setting

from .actions.status import status
from .actions.action import KanBanManager, APPIO
from .utils import check_action_, push_task
from .scripts.aifunc import judge_type
from .scripts.applescript import ShortCut, Display

from .tasks import clean_and_update, edit_coder, test_and_study
from .tasks import design, meeting_and_talk
from .tasks import task_failed, task_complete

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    kbmanager = KanBanManager(kanban_path=KANBAN_PATH, pathlib=WORK_CANVAS_PATH)
    appio = APPIO()
except Exception as e:
    logging.error(f"Failed to initialize managers: {e}")
    # Depending on the severity, you might want to exit or handle this differently
    kbmanager = None
    appio = None


def create_func(task: str, date: str) -> object:
    """创建特定对象

    Args:
        task (str): 任务
        date (str): 日期.

    Returns:
        object: 状态函数
    """
    @status(task=task, date=date)
    def func_():
        return task
    return func_


def check_(func):
    """检查信息的封装

    Args:
        func (object): 信息方法

    Raises:
        TaskInfo: 遇到信息抛出消息等待被捕捉
    """
    try:
        result = func()
        if result:
            raise TaskInfo(result)
    except Exception as e:
        logging.error(f"Error during check_ execution: {e}")
        raise  # Re-raise the exception after logging


class TaskInfo(Exception):
    """任务的抛出机制

    Args:
        Exception (_type_): 抛出
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        logging.info(f"TaskInfo raised: {message}")


def morning(date: str) -> dict:
    """清晨动作

    Returns:
        dict: 系统消息
    """
    try:
        check_(create_func(task='记录灵感', date=date))
        check_(create_func(task='记录体重', date=date))
        check_(create_func(task='跑步', date=date))
        check_(create_func(task='记录吃了什么', date=date))
        check_(create_func(task='洗漱护肤', date=date))
        check_(create_func(task='收拾家与锻炼', date=date))
    except TaskInfo as e:
        return {"message": str(e)}
    except Exception as e:
        logging.error(f"Error in morning tasks: {e}")
        return {"message": f"Error during morning tasks: {e}"}

    return {"message": "任务没了"}


def start_work(date: str, debug: bool = True) -> dict:
    """开工

    Args:
        debug (bool, optional): 是否调试模式. Defaults to True.

    Returns:
        dict: 系统消息
    """
    if kbmanager is None or appio is None:
        return {"message": "Managers not initialized properly."}

    try:
        check_(create_func(task='上班打卡', date=date))
        check_action_(kbmanager.sync_ready, debug)
        check_action_(kbmanager.sync_order, debug)
        check_action_(kbmanager.sync_weight, debug)
        check_(create_func(task='调整优先级', date=date))
        check_action_(kbmanager.sync_run, debug)
        # check_action_(sync_news) # 对方改版了,等着用pypeteer去做吧
        check_action_(appio.sync_calulate, debug)
        check_action_(appio.sync_notes, debug)
        check_(create_func(task='倒水茶水', date=date))
        # bulid知识库
    except TaskInfo as e:
        return {"message": str(e)}
    except Exception as e:
        logging.error(f"Error in start_work tasks: {e}")
        return {"message": f"Error during start_work tasks: {e}"}

    return {"message": "任务没了"}


def tasks(date: str) -> dict:
    """任务列表

    Returns:
        dict: 系统消息
    """
    try:
        logging.info('Starting tasks function')
        check_(create_func(task='写下灵感', date=date))
        check_(create_func(task='跟进阻塞池', date=date))

        task = ShortCut.run_shortcut("获取任务")
        logging.info(f"Task obtained from shortcut: {task}")

        if not task:
            return {"message": "无任务"}

        task_type = judge_type(task)
        logging.info(f"Task type: {task_type}")

        try:
            if task_type == "代码与练习":
                edit_coder(task)
            elif task_type == "实验与学习":
                test_and_study(task)
            elif task_type == "整理与优化":
                clean_and_update(task)
            elif task_type == "设计":
                design(task)
            elif task_type == "开会与对齐":
                meeting_and_talk(task)
            else:
                logging.warning(f'New task category: {task_type}. Defaulting to meeting_and_talk.')
                meeting_and_talk(task)
        except Exception as e:
            logging.error(f"Error executing task {task} of type {task_type}: {e}")
            # Decide how to handle task execution errors - maybe mark as failed?
            task_failed(task=task)
            return {"message": f"Error executing task: {e}"}


        task_result = Display.display_dialog("判断", f"任务是否完成: ", buttons='"complete","blockage"', button_cancel=True)
        logging.info(f"Task completion dialog result: {task_result}")

        if task_result == 'complete':
            task_complete(task=task)
            logging.info(f"Task marked as complete: {task}")
        elif task_result == 'blockage':
            # TODO: Implement blockage handling
            logging.info(f"Task marked as blockage: {task}")
            pass
        else:
            task_failed(task=task)
            logging.info(f"Task marked as failed: {task}")

        # Attempt to remove the task regardless of completion status
        try:
            ShortCut.run_shortcut("移除完成的任务", task)
            logging.info(f"Attempted to remove task via shortcut: {task}")
        except Exception as e:
            logging.error(f"Error removing task via shortcut: {e}")
            # This error might not be critical, so we log and continue

    except TaskInfo as e:
        return {"message": str(e)}
    except Exception as e:
        logging.error(f"An unexpected error occurred in tasks function: {e}")
        return {"message": f"An unexpected error occurred: {e}"}

    return {"message": "任务结束"}


def finish_work(date: str, debug: bool = True) -> dict:
    """收工动作

    Returns:
        dict: 系统信息
    """
    if kbmanager is None or appio is None:
        return {"message": "Managers not initialized properly."}

    try:
        # TODO 知识库整理
        check_action_(kbmanager.sync_weight, debug)
        check_action_(appio.sync_notes, debug)
        check_(create_func(task='检查和收集咨询', date=date))
        check_(create_func(task='检查是否仍在禅模式', date=date))
        check_(create_func(task='检测git提交', date=date))
        check_(create_func(task='下班打卡', date=date))
        check_(create_func(task='倒水茶水晚上', date=date))
    except TaskInfo as e:
        return {"message": str(e)}
    except Exception as e:
        logging.error(f"Error in finish_work tasks: {e}")
        return {"message": f"Error during finish_work tasks: {e}"}

    return {"message": "任务没了"}


def evening(date: str) -> dict:
    """晚间休息的任务

    Returns:
        dict: 系统消息
    """
    try:
        check_(create_func(task='整理家里和猫猫', date=date))
        check_(create_func(task='晚上洗漱,刷牙,护肤', date=date))
        check_(create_func(task='锻炼', date=date))
        check_(create_func(task='睡觉', date=date))
    except TaskInfo as e:
        return {"message": str(e)}
    except Exception as e:
        logging.error(f"Error in evening tasks: {e}")
        return {"message": f"Error during evening tasks: {e}"}

    return {"message": "任务没了"}


def rest(date: str) -> dict:
    """休息日的任务"""
    try:
        # TODO 强化型健身  1周一次 在突破技能   5000米 + 负重 + 拳击
        check_(create_func(task='吃早饭', date=date))
        check_(create_func(task='洗漱', date=date))
        check_(create_func(task='锻炼', date=date))
        check_(create_func(task='睡觉', date=date))
    except TaskInfo as e:
        return {"message": str(e)}
    except Exception as e:
        logging.error(f"Error in rest day tasks: {e}")
        return {"message": f"Error during rest day tasks: {e}"}

    return {"message": "任务没了"}


def receive(server: bool = True) -> dict:
    """领取一个任务(普通模式)

    Args:
        server (bool, optional): 是否在服务器模式下运行. Defaults to True.

    Returns:
        dict: 任务信息或系统消息
    """
    try:
        current_date_obj = Date()
        current_time_str = current_date_obj.time
        current_date_str = current_date_obj.date
        debug_mode = Setting().debug

        logging.info(f"Receive called. Date: {current_date_str}, Time: {current_time_str}, Server mode: {server}")

        date_obj = datetime.strptime(current_date_str, '%Y-%m-%d').date()

        if is_workday(date_obj):
            current_datetime = datetime.strptime(f"{current_date_str} {current_time_str}", "%Y-%m-%d %H:%M:%S")

            # Define time boundaries
            time_boundaries = {
                "morning_end": datetime.strptime(current_date_str + " 08:50:00", "%Y-%m-%d %H:%M:%S"),
                "start_work_end": datetime.strptime(current_date_str + " 10:00:00", "%Y-%m-%d %H:%M:%S"),
                "tasks_end": datetime.strptime(current_date_str + " 18:00:00", "%Y-%m-%d %H:%M:%S"),
                "finish_work_end": datetime.strptime(current_date_str + " 19:00:00", "%Y-%m-%d %H:%M:%S"),
                "evening_end": datetime.strptime(current_date_str + " 23:00:00", "%Y-%m-%d %H:%M:%S"),
            }

            if current_datetime < time_boundaries["morning_end"]:
                logging.info("Executing morning tasks.")
                return morning(date=current_date_str)

            elif time_boundaries["morning_end"] <= current_datetime < time_boundaries["start_work_end"]:
                logging.info("Executing start_work tasks.")
                return start_work(date=current_date_str, debug=debug_mode)

            elif time_boundaries["start_work_end"] <= current_datetime < time_boundaries["tasks_end"]:
                if not server:
                    logging.info("Executing tasks (non-server mode).")
                    return tasks(date=current_date_str)
                else:
                    logging.info("In work hours, but in server mode. No task assigned automatically.")
                    return {"message": "In work hours, waiting for specific task request."}

            elif time_boundaries["tasks_end"] <= current_datetime < time_boundaries["finish_work_end"]:
                logging.info("Executing finish_work tasks.")
                return finish_work(date=current_date_str)

            elif time_boundaries["finish_work_end"] <= current_datetime < time_boundaries["evening_end"]:
                logging.info("Executing evening tasks.")
                return evening(date=current_date_str)
            else:
                logging.info("Outside defined work/evening hours on a workday.")
                return {"message": "Outside defined task hours."}
        else:
            logging.info("Executing rest day tasks.")
            return rest(date=current_date_str)

    except Exception as e:
        logging.error(f"An unexpected error occurred in receive function: {e}")
        return {"message": f"An unexpected error occurred: {e}"}


def complete() -> dict:
    """完成当前任务
    """
    try:
        date = Date().date
        # Calling receive here might not be the intended behavior for 'complete'.
        # 'complete' should likely act on a *currently active* task, not fetch a new one.
        # Re-evaluate the logic here based on how tasks are managed.
        # For now, keeping the original logic but adding a warning.
        logging.warning("complete() is calling receive(). This might not be the correct logic for completing a specific task.")
        task_info = receive(server=False) # Assuming complete is called in a context where tasks are being processed

        # Check if receive returned a task message or a system message
        if isinstance(task_info, dict) and "message" in task_info:
             # If receive returned a system message, there might not be a task to complete
             logging.info(f"receive() returned a message: {task_info['message']}. No specific task to complete.")
             return {"message": f"No active task to complete based on current time: {task_info['message']}"}

        # Assuming task_info is the task string if receive successfully returned one
        task_to_complete = task_info # This is likely incorrect based on receive's return type

        # A more robust approach would be to pass the task to complete as an argument
        # or retrieve the currently active task from a state management system.
        # For now, let's assume 'receive' somehow returned the task string to complete.
        # This part needs clarification based on the overall task management flow.

        # Placeholder logic assuming task_to_complete is the task string
        # This part is highly dependent on how tasks are tracked and completed.
        # The original code just called push_task with the result of receive(), which seems wrong.
        # Let's simulate completing the task that 'receive' *would* have returned if it was a task.
        # This is a guess based on the original code's structure.

        # *** This logic is likely flawed and needs correction based on actual task state management ***
        # A better approach: complete(task_id: str) or complete_current_task()
        # For now, let's return a message indicating this needs review.
        logging.error("The logic in complete() is ambiguous. It calls receive() which returns a message, not a specific task to complete.")
        return {"message": "Complete function logic needs review. Cannot determine which task to complete."}

        # Original logic (commented out as it seems incorrect):
        # result = push_task(task=task, date=date)
        # return {"message": result}

    except Exception as e:
        logging.error(f"An unexpected error occurred in complete function: {e}")
        return {"message": f"An unexpected error occurred during completion: {e}"}


def add_tip(task: str) -> dict:
    """添加一个提示/灵感"""
    if kbmanager is None:
        return {"message": "KanBanManager not initialized."}
    try:
        kbmanager.add_tips(task)
        logging.info(f"Added tip: {task}")
        return {"message": f"Tip added: {task}"}
    except Exception as e:
        logging.error(f"Error adding tip: {e}")
        return {"message": f"Error adding tip: {e}"}
