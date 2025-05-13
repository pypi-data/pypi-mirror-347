import argparse
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import os
import json5
import pyautogui
import pyperclip
import platform
import time
from typing import Literal, Optional
import pydash
from flowjson.utils.index import execRun, findOnScreen, imagesDirPath, printDebug


async def bootstrap():
    # confidence 取值 预期是 选中能识别 未选中 不能识别
    # confidence = 0.99
    # [res1, res2, res3] = await asyncio.gather(
    #     *[
    #         # n 选中
    #         findOnScreen(
    #             os.path.join(imagesDirPath, "dmr/ck/job2/7-1-n-selected-include.png"),
    #             confidence=confidence,
    #         ),
    #         # n 未选中
    #         findOnScreen(
    #             os.path.join(imagesDirPath, "dmr/ck/job2/3-1-n-unselected-click.png"),
    #             confidence=confidence,
    #         ),
    #         # 模糊 能匹配
    #         findOnScreen(
    #             os.path.join(
    #                 imagesDirPath, "dmr/ck/job2/6-1-breakdown-prompt-click.png"
    #             ),
    #             confidence=0.8,
    #         ),
    #     ]
    # )
    # printDebug(res1, res2, res3)
    # pyautogui.press("e")
    # pyautogui.press("space")

    # pyautogui.typewrite('Manet演示测试队列', interval=0.25)  # 不支持中文直接输入 每个字符之间的间隔为0.25秒
    # 直接使用失效 仅会输出v 参考 https://github.com/asweigart/pyautogui/issues/796 https://github.com/asweigart/pyautogui/issues/687
    # pyperclip.copy("你好，世界！")
    # pyautogui.hotkey('ctrl', 'v') # Windows/Linux
    # 方法1
    # pyautogui.keyUp('fn') 
    # pyautogui.hotkey('command', 'v') # macOS
    # 方法2
    # with pyautogui.hold(['command']):
    #     pyautogui.press('v')
    # 方法3
    # pyautogui.hotkey("command")
    # pyautogui.hotkey("command", "v") 

    return


def main():
    startTime = int(time.time() * 1000)
    # 运行异步函数 它自己本身是同步的
    asyncio.run(bootstrap())
    printDebug(f"整体任务耗时：{int(time.time() * 1000) - startTime} ms")


main()
