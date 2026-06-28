#!/usr/bin/env python3
import subprocess
import re
import sys
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import box

console = Console()

def get_all_packages():
    """通过 pkgutil --pkgs 获取所有包标识符，并查询详情"""
    try:
        result = subprocess.run(['pkgutil', '--pkgs'], capture_output=True, text=True, check=True)
        pkgs = result.stdout.strip().split('\n')
    except subprocess.CalledProcessError:
        return []

    package_data = []
    for pkg in pkgs:
        if not pkg:
            continue
        try:
            info = subprocess.run(['pkgutil', '--pkg-info', pkg], capture_output=True, text=True, check=True)
            # 解析 install-time
            match = re.search(r'install-time:\s*(\d+)', info.stdout)
            if match:
                timestamp = int(match.group(1))
                install_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            else:
                timestamp = 0
                install_date = 'Unknown'
            # 解析版本
            ver_match = re.search(r'version:\s*(\S+)', info.stdout)
            version = ver_match.group(1) if ver_match else 'N/A'
            package_data.append({
                'id': pkg,
                'version': version,
                'install_date': install_date,
                'timestamp': timestamp
            })
        except subprocess.CalledProcessError:
            continue
    return package_data

def display_table(packages, sort_by='timestamp'):
    """显示表格，默认按时间升序"""
    sorted_pkgs = sorted(packages, key=lambda x: x.get(sort_by, 0), reverse=False)
    table = Table(title='📦 Installed Packages', box=box.ROUNDED)
    table.add_column('Package ID', style='cyan', no_wrap=True)
    table.add_column('Version', style='green')
    table.add_column('Install Date', style='magenta')
    for pkg in sorted_pkgs:
        table.add_row(pkg['id'], pkg['version'], pkg['install_date'])
    console.print(table)

def get_package_files(pkg_id):
    """获取指定包安装的所有文件列表"""
    try:
        result = subprocess.run(['pkgutil', '--files', pkg_id], capture_output=True, text=True, check=True)
        files = result.stdout.strip().split('\n')
        # 过滤空行
        return [f for f in files if f]
    except subprocess.CalledProcessError:
        return None

def display_package_details(pkg, show_files=True):
    """显示单个包的详细信息 + 文件列表"""
    # 基本信息面板
    info_panel = Panel(
        f"[bold]Package ID:[/] {pkg['id']}\n"
        f"[bold]Version:[/] {pkg['version']}\n"
        f"[bold]Install Date:[/] {pkg['install_date']}\n"
        f"[bold]Timestamp:[/] {pkg['timestamp']}",
        title='📋 Package Details',
        border_style='yellow'
    )
    console.print(info_panel)

    if not show_files:
        return

    # 获取文件列表
    files = get_package_files(pkg['id'])
    if files is None:
        console.print('[yellow]⚠️  Could not retrieve file list (package may not have a receipt).[/yellow]')
        return

    total = len(files)
    console.print(f'[bold cyan]📂 Total files: {total}[/bold cyan]')

    if total == 0:
        console.print('[dim]This package installed no files (or only directories).[/dim]')
        return

    # 智能展示
    if total <= 50:
        # 少文件，直接全部显示
        console.print(Panel('\n'.join(files), title=f'File List ({total})', border_style='green'))
    else:
        # 多文件，询问用户
        choice = Prompt.ask(
            f'[bold]File list has {total} entries. How to view?[/]\n'
            '[1] Preview first 30 lines\n'
            '[2] Open in [cyan]less[/] pager (press [b]q[/] to exit)\n'
            '[3] Skip',
            choices=['1', '2', '3'],
            default='1'
        )
        if choice == '1':
            preview = '\n'.join(files[:30])
            remaining = total - 30
            if remaining > 0:
                preview += f'\n\n[dim]... and {remaining} more files (use option 2 to see all)[/dim]'
            console.print(Panel(preview, title=f'File List Preview (showing 30/{total})', border_style='green'))
        elif choice == '2':
            # 用 less 分页查看（支持鼠标滚动和搜索）
            try:
                subprocess.run(['less', '-R'], input='\n'.join(files), text=True, check=False)
            except FileNotFoundError:
                console.print('[red]Error: less command not found. Falling back to full print.[/red]')
                console.print(Panel('\n'.join(files), title=f'File List ({total})', border_style='green'))
        else:
            console.print('[dim]Skipped file list display.[/dim]')

def main():
    console.print(Panel.fit('📦 PKG Install History Viewer', style='bold blue'))
    
    with console.status('Scanning packages, please wait...') as status:
        packages = get_all_packages()
    
    if not packages:
        console.print('[red]No packages found or error occurred.')
        return

    display_table(packages)

    # 交互循环
    while True:
        console.print('\n[bold]--- Actions ---[/]')
        choice = Prompt.ask(
            'Enter [cyan]package ID[/] (supports partial match) to view details, [b]r[/] to refresh, or [b]q[/] to quit',
            default='q'
        )
        
        if choice.lower() == 'q':
            break
        if choice.lower() == 'r':
            with console.status('Refreshing...'):
                packages = get_all_packages()
            if packages:
                display_table(packages)
            else:
                console.print('[red]Failed to refresh.')
            continue

        # 查找匹配的包（支持部分匹配）
        found = [p for p in packages if choice in p['id']]
        if not found:
            console.print(f'[red]No package matches "{choice}". Try a different keyword.[/red]')
            continue

        # 如果匹配多个，让用户选择
        if len(found) > 1:
            console.print(f'[yellow]Found {len(found)} matches:[/yellow]')
            for i, p in enumerate(found, 1):
                console.print(f'  {i}. {p["id"]} ({p["version"]})')
            idx = Prompt.ask('Enter number to select', choices=[str(i) for i in range(1, len(found)+1)])
            selected = found[int(idx)-1]
        else:
            selected = found[0]

        # 显示详情（包含文件列表）
        display_package_details(selected, show_files=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print('\n[dim]Exited by user.[/dim]')
        sys.exit(0)