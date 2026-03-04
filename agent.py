import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_community.llms.fake import FakeListLLM
from tools import CalculatorTool, TimeTool

# 加载 .env 文件（如果有），但我们不需要真实的 API 密钥
load_dotenv()

def main():
    # 预设的回复列表，每个元素是一个完整的 ReAct 格式的字符串
    # 这样 FakeListLLM 会按照这些字符串输出，Agent 会解析出 Action 并真正调用工具
    responses = [
        """Thought: I need to calculate 123+456.
Action: Calculator
Action Input: 123+456
Observation: 579
Thought: I now know the final answer.
Final Answer: 579""",
        """Thought: I need to get the current time.
Action: Time
Action Input: 
Observation: 2026-03-04 15:30:00
Thought: I now know the final answer.
Final Answer: 当前时间是 2026-03-04 15:30:00"""
    ]
    
    # 使用模拟 LLM
    llm = FakeListLLM(responses=responses)

    # 定义工具列表
    tools = [CalculatorTool(), TimeTool()]

    # 初始化 Agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,          # 打印思考过程
        handle_parsing_errors=True
    )

    print("AI Agent 已启动（模拟 LLM + 真实工具），输入 'exit' 退出。")
    while True:
        user_input = input("\n你的问题：")
        if user_input.lower() == 'exit':
            break
        try:
            # 运行 Agent，传入用户输入
            response = agent.run(user_input)
            print(f"AI回复：{response}")
        except Exception as e:
            print(f"处理出错：{e}")

if __name__ == "__main__":
    main()