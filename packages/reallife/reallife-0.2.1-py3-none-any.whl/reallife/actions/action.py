""" 动作函数 """

import requests
from datetime import datetime
from grapherz.canvas.core import Canvas,Color
from kanban.core import Pool,Kanban
from contextlib import contextmanager
from ..scripts.aifunc import give_a_task_time,generate_schedule
from reallife import KANBAN_PATH,WORK_CANVAS_PATH,Date
from .status import status
from ..scripts.applescript import Calulate,Notes,Reminder
from .utils import parse_execution_jiangyou_pool,parse_execution_pool, read_file
from .utils import git_pull, git_push
import asyncio

date_c = Date()
date = date_c.date

@contextmanager
def controlKanban(kanban:Kanban):
    kanban.pull()
    yield kanban
    kanban.push()

@contextmanager
def sync_obsidian_github(commit:str):
    git_pull("obsidian")
    yield
    git_push('obsidian',commit=commit)


class KanBanManager():
    def __init__(self,kanban_path,pathlib):
        self.kanban_path = kanban_path
        self.pathlib = pathlib
        self.kanban = Kanban(self.kanban_path)
        self.main_path = "/Users/zhaoxuefeng/GitHub/obsidian/工作"

    @status(task="同步预备池",date=date,run_only=True)
    def sync_ready(self):
        def encode(i,project_name):
            return project_name+'-'+i
        
        def save_in_pauses(i,pauses):
            for pause in pauses:
                if i.get('text') in pause:
                    return True
            return False
        with sync_obsidian_github("同步预备池"):
            for path in self.pathlib:
                canvas_path=self.main_path+path
                try:
                    canvas = Canvas(file_path=canvas_path)
                except FileNotFoundError as e:
                    print(e)
                    continue
                with controlKanban(self.kanban) as kb:
                    project_name = canvas_path.rsplit('/',2)[-2] 
                    pauses = kb.get_tasks_in(pool=Pool.阻塞池)
                    readys = kb.get_tasks_in(pool=Pool.预备池)

                    nodes = [i.get('text') or '' for i in canvas.select_by_color(Color.yellow,type='node') if not save_in_pauses(i,pauses=pauses)]
                    for i in nodes:
                        if i not in readys:
                            kb.insert(text=encode(i,project_name),pool=Pool.预备池)
        return 'success'

    @status(task="同步就绪池",date=date,run_only=True)
    def sync_order(self):
        with sync_obsidian_github("调整优先级"):
            with controlKanban(self.kanban) as kb:
                tasks = kb.get_tasks_in(Pool.预备池)
                order_tasks = kb.get_tasks_in(Pool.就绪池)
                orders = ' '.join(order_tasks)
                for task in tasks:
                    kb.pop(text = task,pool = Pool.预备池)
                    if task not in orders:
                        task_ = give_a_task_time(task)
                        kb.insert(text=task_,pool=Pool.就绪池)
        return 'success'

    @status(task="同步执行池",date=date,run_only=True)
    def sync_run(self)->str:
        with sync_obsidian_github("同步到执行池"):
            with controlKanban(self.kanban) as kb:
                tasks = kb.get_tasks_in(Pool.就绪池)
                all_task_time = 0
                for task in tasks:
                    if task.split(' ')[0][-1].lower() != 'p':
                        continue
                    task_time = int(task.split(' ')[0][:-1])

                    if all_task_time + task_time <=14:
                        all_task_time += task_time
                        kb.pop(text=task,pool=Pool.就绪池)
                        kb.insert(text=task,pool=Pool.执行池)

                    elif all_task_time < 8:
                        pass
        return 'success'
    
    @status(task="回收未完成的任务",date=date,run_only=True)
    def sync_run2order(self):
        with controlKanban(self.kanban) as kb:
            tasks = kb.get_tasks_in(Pool.执行池)
            if tasks:
                for task in tasks:
                    kb.pop(text=task,pool=Pool.执行池)
                    kb.insert(text=task,pool=Pool.就绪池)
            
        return 'success'

    @status(task="任务完成的任务",date=date,run_only=True)
    def sync_run2over(self,task:str,
                      canvas_path:str):

        """从执行池添加到完成池
        # multi_line_input = "备案-新域名做域名备案$/工程系统级设计/项目级别/数字人生/模拟资质认证/模拟资质认证.canvas\n"

        1 将task从执行池添加到完成池
        2 将canvas 中的颜色变绿
        Args:
            kanban_path (str): 看板路径

        Returns:
            None: None
        """
        
        canvas_path = canvas_path.replace('\n','')
        canvas_path =self.main_path+canvas_path


        with controlKanban(self.kanban) as kb:
            task = task.split('-',1)[-1]
            if len(kb.get_task_by_word(task,pool=Pool.执行池)) == 0:
                kb.insert(text=task,pool=Pool.完成池)
                kb.push()
                return 'failed'

            task_ = kb.get_task_by_word(task,pool=Pool.执行池)[0]
            kb.pop(text=task_,pool=Pool.执行池)
            kb.insert(text=task_,pool=Pool.完成池)

            # and
            canvas = Canvas(file_path=canvas_path)
            tasks = canvas.select_nodes_by_text(task)
            try:
                tasks[0].color = Color.green.value
            except IndexError as e:
                return f'error: {e}'
            canvas.to_file(canvas_path)

        return 'success'

    @status(task="同步记录",date=date,run_only=False)
    def add_tips(self,task:str):
        """从执行池添加到完成池
        1 将task从执行池添加到完成池
        2 将canvas 中的颜色变绿
        Args:
            kanban_path (str): 看板路径

        Returns:
            None: None
        """
        with controlKanban(self.kanban) as kb:
            kb.insert(text=task,pool=Pool.预备池)
        return 'success'

    @status(task="同步体重",date=date,run_only=True)
    def sync_weight(self)->str:
        """
        同步体重
        """

        url = f"http://101.201.244.227:8000/weight/{date}"
        response = requests.get(url)
        result = response.json().get('weight')
        x = f"""---
番茄: 14
体重: {result}
---
"""

        with open(self.main_path + f'/日记/{date}.md','a') as f:
            f.write(x)
        return 'success'


class APPIO():
    def __init__(self):
        self.year = '2025年'
        self.kanban_path ="/Users/zhaoxuefeng/GitHub/obsidian/工作/事件看板/事件看板.md"
        self.habit ="7点-9点起床洗漱, 12点到14点吃饭+午休,19点以后就是自由时间"
    @status(task="同步日历",date=date,run_only=True)
    def sync_calulate(self):

        # 读取文件
        text = read_file(self.kanban_path)
        if not text:
            print("文件内容为空，无法解析执行池")
            return "文件内容为空，无法解析执行池"

        # 解析执行池
        execution_pool = parse_execution_pool(text)
        if execution_pool:
            # 生成日程安排
            schedule_result = generate_schedule(execution_pool,habit =self.habit)
            print(schedule_result,'schedule_result')
            xx = [i for i in schedule_result.split('\n') if i!='']
            for xp in xx:
                v = [("2025年"+k if i<2 and k[4]!="年" else k) for i,k in enumerate(xp.split('$'))]
                Calulate.update(*v)
        else:
            print("未能解析到执行池内容")

    @status(task="同步备忘录",date=date,run_only=False) # 晚上也需要同步
    def sync_notes(self):
        # 读取文件
        date_c = Date()
        text = read_file(self.kanban_path)
        # 解析执行池
        execution_pool = parse_execution_jiangyou_pool(text)

        # 生成日程安排
        current_utc_time = datetime.utcnow()
        schedule_result = str(current_utc_time)[:10] + '\n' + execution_pool

        Notes.write_notes(schedule_result)

        for content in schedule_result.split("\n")[1:]:
            Reminder.write_reminder(content, 
                list_name="工作",
                due_date=f"{date_c.date} {date_c.time}",
                priority=2,
                notes="")
    # @status(task="收集资讯",date=date,run_only=True)
    # def sync_news(self,date:str):
    #     """同步资讯

    #     Args:
    #         date (str): 日期,字符串格式
    #     """
    #     def _get_articlie_link():
    #         # 目标网页的 URL
    #         url = "https://www.jiqizhixin.com"
    #         file_links = ["https://www.jiqizhixin.com/articles/2025-05-07-9",
    #                       "https://www.jiqizhixin.com/articles/2025-05-07-8",
    #                       "https://www.jiqizhixin.com/articles/2025-05-07-7",
    #                       "https://www.jiqizhixin.com/articles/2025-05-07-6",
    #                       ]
    #         return file_links
        
    #     def _get_articlie_link_2():
    #         # 目标网页的 URL
    #         url = "https://www.jiqizhixin.com"

    #         headers = {
    #             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    #                 AppleWebKit/537.36 (KHTML, like Gecko) \
    #                     Chrome/91.0.4472.124 Safari/537.36"
    #         }
    #         # 发送 HTTP 请求获取网页内容
    #         # response = requests.get(url)
    #         response = requests.get(url, headers=headers)

    #         # 检查请求是否成功
    #         if response.status_code == 200:
    #             # 解析 HTML 内容
    #             soup = BeautifulSoup(response.content, 'html.parser')

    #             # 提取所有文件链接
    #             file_links = []
    #             for link in soup.find_all('a', href=True,attrs={
    #                 'class': 'article-item__title t-strong js-open-modal',
    #             }):
    #                 href = link['href']
    #                 file_links.append(url + href)
    #         else:
    #             print("请求失败，状态码：", response.status_code)
    #         return file_links
        
    #     async def _get_context_from_jq_url(url):
    #         # 目标网页的 URL
             
    #         target_url = url
    #         html = await get_page_html(target_url)


    #         soup = BeautifulSoup(html, 'html.parser')

    #         # 提取网页中的文字内容
    #         text = soup.get_text()
    #         return text
            
    #     @lru_cache(maxsize=100)
    #     def _extra_text(text):
    #         template = """
    #         我希望你可以对一个内容进行汇总和总结, 我会给你一段网页的内容，你来用一些简短的文字告诉我这篇内容的主要信息, 以及列出其中相关的重点和链接

    #         网页内容:
    #         ---
    #         {text}
    #         ---

    #         输出信息:
    #         """

    #         llm = BianXieAdapter()
    #         llm.set_model("gpt-4o")
    #         prompt = template.format(text = text)
    #         completion = llm.product(prompt)
    #         return completion
        
    #     file_links = _get_articlie_link()
    #     print(file_links,'file_links')
    #     article = []
    #     for file_link in file_links:
    #         print(file_link)
    #         result = asyncio.run(_get_context_from_jq_url(file_link))
    #         xx = _extra_text(result)
    #         article.append(xx)

    #     file_path = f"/Users/zhaoxuefeng/GitHub/obsidian/工作/日记/{date}.md"
    #     with open(file_path,'a') as f:
    #         f.write("\n\n# 今日资讯\n---\n## 消息\n" +'\n\n---\n## 消息\n'.join(article))

