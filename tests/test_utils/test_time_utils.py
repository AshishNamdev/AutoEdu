"""
اختبارات وحدة time_utils

اختبارات شاملة لوظائف التوقيت والتاريخ.
"""

import pytest
from datetime import datetime
from autoedu.utils.time_utils import (
    get_current_timestamp,
    format_datetime,
    get_academic_year,
    get_semester
)


class TestTimeUtils:
    """فئة اختبارات وظائف التوقيت."""

    def test_get_current_timestamp(self):
        """اختبار الحصول على الطابع الزمني الحالي."""
        # اختبار بدون تنسيق
        timestamp = get_current_timestamp()
        assert isinstance(timestamp, datetime)

        # اختبار مع تنسيق
        formatted = get_current_timestamp(format_string="%Y-%m-%d")
        assert isinstance(formatted, str)
        assert len(formatted) == 10  # YYYY-MM-DD

    def test_format_datetime(self):
        """اختبار تنسيق التاريخ."""
        dt = datetime(2024, 1, 15, 14, 30, 0)
        formatted = format_datetime(dt, "%Y-%m-%d %H:%M")
        assert formatted == "2024-01-15 14:30"

    def test_get_academic_year(self):
        """اختبار الحصول على السنة الأكاديمية."""
        # سبتمبر 2024
        sept_2024 = datetime(2024, 9, 1)
        assert get_academic_year(sept_2024) == "2024-2025"

        # يناير 2024
        jan_2024 = datetime(2024, 1, 1)
        assert get_academic_year(jan_2024) == "2023-2024"

    def test_get_semester(self):
        """اختبار تحديد الفصل الدراسي."""
        # الفصل الأول (سبتمبر)
        sept = datetime(2024, 9, 1)
        assert get_semester(sept) == "first"

        # الفصل الثاني (فبراير)
        feb = datetime(2024, 2, 1)
        assert get_semester(feb) == "second"

        # الفصل الصيفي (يونيو)
        june = datetime(2024, 6, 1)
        assert get_semester(june) == "summer"
