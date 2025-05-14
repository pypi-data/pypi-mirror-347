"""命令行主模块"""

import os
import sys
import logging
import typer

from dotenv import load_dotenv
from app import __version__
from app.config import LOG_LEVEL
from rich.console import Console
from app.utils.helpers import setup_logger
from app.core.logger import configure_remote_logging, feedback_handler
from app.core.runner import Runner
from app.core.tasks import init_celery_app, celery_app
from app.tasks import video_processing  # 导入视频处理任务


# 加载环境变量
if "RUNNER_TEMP" in os.environ:
    load_dotenv()
else:
    load_dotenv(dotenv_path=".env")

app = typer.Typer(
    name = "octopus_queue",
    help = "Octopus Queue CLI",
    rich_markup_mode = "rich",
    add_completion = False
)

console = Console()
logger = setup_logger(__name__, level=LOG_LEVEL)

def shutdown_celery():
    """
    关闭Celery
    """
    logger.info("Shutting down Celery")
    # 这里不需要真正关闭Celery Worker，因为它会随着主进程退出而终止

def main():
    """主函数"""
    # 打印版本信息
    console.print("Octopus Queue CLI v{__version__}", style="bold blue")

    # 配置远程日志
    configure_remote_logging()

    # 初始化Celery应用
    init_celery_app()
    logger.info("Celery app initialized")

    # 导入所有任务模块，确保任务被注册到Celery
    logger.info(f"Available video tasks: {', '.join(dir(video_processing))}")

    # 创建运行管理器
    runner = Runner()
    
    # 注册关闭回调
    runner.register_shutdown_callback(shutdown_celery)
    
    # 启动运行管理器
    return runner.start()


@app.command("run")
def run():
    """运行命令行"""
    exit_code = main()
    sys.exit(exit_code)

@app.command("info")
def info():
    """命令信息"""
    print(f"Hahaha!!!")

if __name__ == "__main__":
    app()
