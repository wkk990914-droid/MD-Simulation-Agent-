#!/usr/bin/env python3
"""
主函数：启动交互式聊天对话框，调用Supervisor Agent处理用户输入
输入 'exit' 退出，输入 'help' 查看示例指令
"""
import sys
import os

# 获取项目根目录并添加到sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from agentframework.multi_agent.supervisor import supervisor_query

def run_chat_dialog():
    """启动交互式聊天对话框"""
    print("="*50)
    print("分子模拟Agent聊天助手")
    print("提示：输入 'exit' 退出 | 输入 'help' 查看示例指令")
    print("="*50)

    while True:
        # 获取用户输入
        user_input = input("\n请输入您的指令：").strip()
        
        # 退出逻辑
        if user_input.lower() == "exit":
            print("感谢使用，再见！")
            break
        
        # 帮助逻辑
        if user_input.lower() == "help":
            print("\n【示例指令】")
            print("1. 分子数量计算：How many methane molecules are needed in a cubic box of size 30 Angstroms for a density of 0.423 g/cm3. The molar mass is 16.04 g/mol.")
            print("2. 生成LAMMPS数据文件：Generate LAMMPS data file for Methane (SMILES: C, Box size: 3.0 nm, Number of molecules: 100)")
            print("3. 生成LAMMPS输入文件：Create a LAMMPS input file for Methane.data (Temp: 150K, Pres: 1atm, input file name: Methane_npt)")
            print("4. 分析模拟收敛性：Analyze the convergence of the Density in '../log.lammps' (tolerance: 0.1, window: 50)")
            continue
        
        # 空输入处理
        if not user_input:
            print("错误：指令不能为空，请重新输入！")
            continue
        
        # 调用Supervisor Agent处理指令
        try:
            print("\n正在处理您的指令...\n")
            result = supervisor_query(user_input)
            if result:
                print(f"\n【最终回复】\n{result}")
            else:
                print("\n【最终回复】\n未获取到有效响应，请检查指令是否合法。")
        except Exception as e:
            print(f"\n错误：处理指令失败 - {str(e)}")

if __name__ == "__main__":
    # 启动聊天对话框
    run_chat_dialog()