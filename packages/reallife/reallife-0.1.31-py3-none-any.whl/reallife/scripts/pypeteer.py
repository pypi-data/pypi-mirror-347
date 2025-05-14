""" pyppeteer 脚本"""

import asyncio
import pyppeteer

async def get_page_html(url: str) -> str | None:
    """
    使用 pypeteer 访问指定 URL，等待页面完全加载后获取 HTML 内容。

    Args:
        url: 要访问的网页 URL。

    Returns:
        页面的 HTML 内容字符串，如果发生错误则返回 None。
    """
    browser = None # 初始化 browser 变量，以便在 finally 块中检查
    try:
        # 启动浏览器
        # headless=True 表示无头模式运行（不显示浏览器窗口）
        # 可以设置为 headless=False 进行调试，会弹出一个浏览器窗口
        print("正在启动浏览器...")
        browser = await pyppeteer.launch(headless=True, 
                                         userDataDir='/Users/zhaoxuefeng/GitHub/test1/userdata3', 
                                         args=['--no-sandbox']) # 添加 --no-sandbox 参数，某些环境下可能需要

        page = await browser.newPage()

        print(f"正在访问网页: {url}")
        # 导航到指定 URL 并等待页面完全加载
        # waitUntil='networkidle0' 会等待直到网络连接数降至 0 且持续 500ms
        # 这通常意味着页面上的主要资源（包括通过 JS 加载的）都已经加载完成
        # 其他选项包括 'load', 'domcontentloaded', 'networkidle2'
        await page.goto(url, waitUntil='networkidle0')
        print("页面加载完毕，正在获取 HTML 内容...")

        # 获取页面的完整 HTML 内容
        html_content = await page.content()
        print("HTML 内容获取成功。")

        return html_content

    except pyppeteer.errors.TimeoutError:
        print(f"访问 {url} 超时。")
        return None
    except Exception as e:
        print(f"访问 {url} 时发生错误: {e}")
        return None
    finally:
        # 关闭浏览器实例
        if browser:
            print("正在关闭浏览器...")
            await browser.close()
            print("浏览器已关闭。")

