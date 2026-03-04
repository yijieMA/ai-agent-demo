from langchain.tools import BaseTool
from datetime import datetime

class CalculatorTool(BaseTool):
    """一个简单的计算器工具"""
    name: str = "Calculator"          # 添加了类型注解 :str
    description: str = "用于进行数学运算，输入应为数学表达式，如 '2+2'。"  # 添加了类型注解

    def _run(self, query: str) -> str:
        try:
            # 使用 eval 计算表达式，注意限制了命名空间，相对安全
            result = eval(query, {"__builtins__": {}}, {})
            return f"计算结果：{result}"
        except Exception as e:
            return f"计算失败：{str(e)}"

    async def _arun(self, query: str) -> str:
        # 异步方法，这里简单同步调用
        return self._run(query)

class TimeTool(BaseTool):
    """返回当前时间的工具"""
    name: str = "Time"
    description: str = "返回当前日期和时间，输入任意内容即可。"

    def _run(self, query: str) -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"当前时间：{now}"

    async def _arun(self, query: str) -> str:
        return self._run(query)