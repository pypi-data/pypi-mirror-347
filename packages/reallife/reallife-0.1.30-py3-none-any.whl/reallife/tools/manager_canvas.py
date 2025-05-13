from grapherz.core import CanvasMermaidConverter
import os
import json

def manager_canvs(prompt:str, canvas_path = "/Users/zhaoxuefeng/GitHub/obsidian/工作/事件看板/TODO/未命名.canvas")
    converter = CanvasMermaidConverter()
    with open(canvas_path,'r') as f:
        canvas_data = json.loads(f.read())
        mermaid_text = converter.load_canvas(canvas_data).canvas_to_mermaid()
    #TODO 与llm交流
    mermaid_text2 = mermaid_text

    with open(canvas_path,'w') as f:
        canvas_data_2 = converter.load_mermaid(mermaid_text2).mermaid_to_canvas()
        f.write(json.dumps(canvas_data_2, indent=2))