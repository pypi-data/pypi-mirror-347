import os
import yaml
import openai
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.syntax import Syntax
import sys
import psutil
import json


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
    # 显示命令预览
    #console.print("\n[bold cyan]生成的命令:[/]")
    console.print(f"\n[bold magenta]命令预览:[/]")

    console.print(Panel(
        Syntax(cmd, "bash", theme="monokai"),
        border_style="cyan"
    ))

    # 用户确认
    if Confirm.ask("\n[yellow]是否执行这个命令?[/]"):
        with console.status("[bold green]执行中...[/]\n") as status:
            result = os.system(cmd)
            if result == 0:
                console.print("\n[bold green]✓[/] 命令执行成功!")
            else:
                console.print("\n[bold red]✗[/] 命令执行失败!")
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
        clean_content = response_content.replace('```json', '').replace('```', '').strip()
        response_json = json.loads(clean_content)
        response_json = json.loads(clean_content)
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



