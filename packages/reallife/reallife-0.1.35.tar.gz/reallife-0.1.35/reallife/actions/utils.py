from typing import Optional
import re
import os

# 正则解析相关
def parse_execution_pool(text: str) -> Optional[str]:
    """
    使用正则表达式解析 "执行池" 内容
    :param text: 输入文本
    :return: 解析后的执行池内容
    """
    pattern = r'## 执行池\n(.+?)\n##'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        content = match.group(1).strip()
        formatted_content = '\n'.join([line.strip()
                                       for line in content.split('\n') if line.strip()])
        return formatted_content
    else:
        return None


# 正则解析相关
def parse_execution_jiangyou_pool(text: str) -> Optional[str]:
    """
    使用正则表达式解析 "执行池" 内容
    :param text: 输入文本
    :return: 解析后的执行池内容
    """
    pattern = r'## 酱油池\n(.+?)\n##'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        content = match.group(1).strip()
        formatted_content = '\n'.join([line.strip()
                                       for line in content.split('\n') if line.strip()])
        return formatted_content
    else:
        return None
    


# 数据读取相关
def read_file(file_path: str) -> str:
    """
    读取文件内容
    :param file_path: 文件路径
    :return: 文件内容字符串
    """
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
        return ""

def git_pull(repo: str):
    """拉取 git 仓库最新更改
    Args:
        repo (str): 仓库名称 (例如 'my-awesome-project')
    """
    repo_path = os.path.join("/Users/zhaoxuefeng/GitHub", repo)
    # 切换目录并执行 git pull
    # git pull 默认会尝试拉取当前分支对应的远程分支
    command = f"cd {repo_path} && git pull"
    print(f"Executing command: {command}") # 打印执行的命令，方便调试
    os.system(command)
    print(f"Pull command finished for repo: {repo}")


def git_push(repo: str,commit:str='test'):
    """推送 git 仓库更改到远程
    Args:
        repo (str): 仓库名称 (例如 'my-awesome-project')
    """
    repo_path = os.path.join("/Users/zhaoxuefeng/GitHub", repo)
    # 切换目录并执行 git push
    # git push 默认会尝试推送当前分支到其对应的远程分支
    command = f"cd {repo_path} && git commit -a -m {commit} && git push"
    print(f"Executing command: {command}") # 打印执行的命令，方便调试
    os.system(command)
    print(f"Push command finished for repo: {repo}")
