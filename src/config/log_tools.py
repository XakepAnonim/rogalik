"""
Модуль log_tools.py, отвечает за инициализацию и настройку логгера.
"""

from loguru import logger as l_logger

logger = l_logger

exception_catch = logger.catch
