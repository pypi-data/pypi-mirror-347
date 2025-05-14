import json
import os
import subprocess
import sys

import openai
import psutil
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.syntax import Syntax

console = Console()


def load_config():
    config_path = os.path.expanduser("~/.nl2shell.yaml")
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    else:
        return {}

config = load_config()
api_key = config.get("api_key", "")
base_url = config.get("base_url", "https://aigc.sankuai.com/v1/openai/native")
model = config.get("model", "gpt-4o-2024-11-20")

def get_current_shell():
    try:
        # 获取当前进程
        current_process = psutil.Process()
        # 获取父进程
        parent = current_process.parent()
        while parent:
            if parent.name().lower() in ['bash', 'zsh', 'fish', 'sh', 'csh', 'tcsh']:
                return parent.name()
            parent = parent.parent()
        # 如果没找到，返回环境变量中的 SHELL
        return os.path.basename(os.environ.get("SHELL", "unknown"))
    except:
        return os.path.basename(os.environ.get("SHELL", "unknown"))

system_info = {
    "os": os.name,
    "platform": sys.platform,
    "version": sys.version,
    "architecture": os.uname().machine,
    "shell": get_current_shell()
}


prompt_template = config.get(
    "prompt_template",
    """根据以下系统信息和需求生成一个shell命令，输出格式为JSON，格式为：{{"command": "生成的shell命令"}}。
系统信息：{system_info}
需求：{query}"""
)
#print(prompt_template)


def execute_command(cmd):
    console.print(f"\n[bold magenta]命令预览:[/]")
    console.print(Panel(
        Syntax(cmd, "bash", theme="monokai"),
        border_style="cyan"
    ))

    if Confirm.ask("\n[yellow]是否执行这个命令?[/]"):
        with console.status("[bold green]执行中...[/]\n") as status:
            try:
                # 使用 subprocess.run 替代 os.system
                result = subprocess.run(
                    cmd,
                    shell=True,
                    text=True,
                    capture_output=True
                )

                # 显示输出
                if result.stdout:
                    console.print("\n[bold cyan]命令输出:[/]")
                    console.print(Panel(result.stdout.strip(), border_style="green"))

                # 显示错误
                if result.stderr:
                    console.print("\n[bold red]错误输出:[/]")
                    console.print(Panel(result.stderr.strip(), border_style="red"))

                if result.returncode == 0:
                    console.print("\n[bold green]✓[/] 命令执行成功!")
                else:
                    console.print("\n[bold red]✗[/] 命令执行失败!")
            except Exception as e:
                console.print(f"\n[bold red]✗[/] 执行出错: {str(e)}")
    else:
        console.print("\n[yellow]命令已取消[/]")

def nl2shell(user_input):
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    with console.status("[bold blue]正在生成命令...[/]"):
        prompt = prompt_template.format(system_info=system_info, query=user_input)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

    response_content = response.choices[0].message.content.strip()
    try:
        # 移除可能存在的 ```json 和 ``` 标记
        # 移除前后的说明文字，只保留 JSON 部分
        if "```json" in response_content:
            # 提取 ``[json 和 ](file://nl2shell/main.py#97#21)`` 之间的内容
            json_content = response_content.split("```json")[1].split("```")[0].strip()
        else:
            json_content = response_content
        response_json = json.loads(json_content)
        return response_json.get("command", "")
    except json.JSONDecodeError:
        console.print("\n[bold red]✗[/] 无法解析生成的JSON!")
        console.print("\n[bold cyan]生成的结果:[/]")
        console.print(Panel(response_content, border_style="green"))

        sys.exit(1)

def main():
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        console.print("\n[bold red]✗[/] 未提供输入参数，已退出!")
        sys.exit(1)

    cmd = nl2shell(user_input)
    if cmd != None:
        execute_command(cmd)

if __name__ == "__main__":
    main()



