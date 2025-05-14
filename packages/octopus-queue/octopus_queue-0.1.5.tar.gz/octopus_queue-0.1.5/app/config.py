"""配置信息模块"""

import os
from dotenv import load_dotenv

# 加载环境变量
if "RUNNER_TEMP" in os.environ:
    load_dotenv(override=True)
else:
    load_dotenv(dotenv_path=".env", override=True)

# Redis 配置
REDIS_URL = os.getenv("QUEUE_URL", "redis://localhost:6379/0")

# Celery 配置
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# 下载文件临时存储目录
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "/tmp")

# API 反馈配置
API_FEEDBACK_URL = os.getenv("API_FEEDBACK_URL", "http://localhost:6000/gateway")
API_KEY = os.getenv("API_KEY", "")

# 运行时配置
MAX_RUNTIME_SECONDS = int(os.getenv("MAX_RUNTIME_SECONDS", 60))
SHUTDOWN_GRACE_PERIOD_SECONDS = int(os.getenv("SHUTDOWN_GRACE_PERIOD_SECONDS", 5))
RETRY_DELAY_SECONDS = int(os.getenv("RETRY_DELAY_SECONDS", 10))

# 任务配置
TASK_RETRY_COUNT = int(os.getenv("TASK_RETRY_COUNT"))  # 任务失败后重试次数

# 云存储保存路径
TEMP_DIR = os.getenv("TEMP_DIR", "/tmp")

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S" # 日志日期格式
