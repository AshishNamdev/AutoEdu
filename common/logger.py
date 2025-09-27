"""
نظام السجلات المحسن لمشروع AutoEdu

يوفر إعداداً شاملاً لتسجيل الأحداث والأخطاء.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from loguru import logger as loguru_logger


def setup_logger(
    name: str = "autoedu",
    level: str = "INFO",
    log_file: Optional[str] = None,
    enable_console: bool = True,
    enable_file: bool = True,
) -> logging.Logger:
    """
    إعداد نظام السجلات للمشروع.

    Args:
        name: اسم السجل
        level: مستوى السجل (DEBUG, INFO, WARNING, ERROR)
        log_file: مسار ملف السجل (اختياري)
        enable_console: تفعيل السجل في وحدة التحكم
        enable_file: تفعيل السجل في ملف

    Returns:
        كائن السجل المُعد
    """
    # إنشاء مجلد السجلات
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # إعداد ملف السجل الافتراضي
    if log_file is None:
        log_file = log_dir / "autoedu.log"

    # مسح الإعدادات الحالية
    loguru_logger.remove()

    # إضافة handler للوحة التحكم
    if enable_console:
        loguru_logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                   "<level>{message}</level>",
            level=level,
            colorize=True,
        )

    # إضافة handler للملف
    if enable_file:
        loguru_logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
                   "{name}:{function}:{line} - {message}",
            level=level,
            rotation="10 MB",
            retention="30 days",
            compression="zip",
        )

    return logging.getLogger(name)


def get_logger(name: str = "autoedu") -> logging.Logger:
    """الحصول على كائن السجل الموجود."""
    return logging.getLogger(name)
