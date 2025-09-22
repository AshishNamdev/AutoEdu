"""
أدوات التوقيت والتاريخ لمشروع AutoEdu

يوفر وظائف مساعدة للعمل مع التواريخ والأوقات.
"""

from datetime import datetime, timedelta
from typing import Optional, Union


def get_current_timestamp(
    timezone_name: str = "UTC",
    format_string: Optional[str] = None
) -> Union[datetime, str]:
    """
    الحصول على الطابع الزمني الحالي.

    Args:
        timezone_name: اسم المنطقة الزمنية (افتراضي UTC)
        format_string: تنسيق التاريخ (اختياري)

    Returns:
        كائن datetime أو نص مُنسق
    """
    now = datetime.now()

    if format_string:
        return now.strftime(format_string)

    return now


def format_datetime(
    dt: datetime,
    format_string: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """
    تنسيق كائن datetime.

    Args:
        dt: كائن datetime
        format_string: تنسيق التاريخ

    Returns:
        التاريخ المُنسق كنص
    """
    return dt.strftime(format_string)


def get_academic_year(date: datetime) -> str:
    """
    الحصول على السنة الأكاديمية للتاريخ المعطى.

    Args:
        date: التاريخ

    Returns:
        السنة الأكاديمية (مثل: "2024-2025")
    """
    if date.month >= 9:  # سبتمبر فما بعد
        return f"{date.year}-{date.year + 1}"
    else:
        return f"{date.year - 1}-{date.year}"


def get_semester(date: datetime) -> str:
    """
    تحديد الفصل الدراسي للتاريخ المعطى.

    Args:
        date: التاريخ

    Returns:
        الفصل الدراسي ("first", "second", "summer")
    """
    month = date.month

    if 9 <= month <= 12 or month == 1:
        return "first"
    elif 2 <= month <= 5:
        return "second"
    else:  # 6, 7, 8
        return "summer"
