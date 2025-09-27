"""
اختبارات وحدة string_utils

اختبارات شاملة لوظائف معالجة النصوص.
"""

import pytest
from autoedu.utils.string_utils import (
    clean_text,
    extract_emails,
    generate_password,
    validate_email
)


class TestStringUtils:
    """فئة اختبارات وظائف النصوص."""

    def test_clean_text(self):
        """اختبار تنظيف النص."""
        # إزالة المسافات الزائدة
        text = "  مرحبا    بك    "
        cleaned = clean_text(text)
        assert cleaned == "مرحبا بك"

    def test_extract_emails(self):
        """اختبار استخراج البريد الإلكتروني."""
        text = "تواصل معنا على admin@university.edu أو support@autoedu.com"
        emails = extract_emails(text)
        assert len(emails) >= 1

    def test_generate_password(self):
        """اختبار توليد كلمة المرور."""
        password = generate_password(12)
        assert len(password) == 12

        # كلمة مرور بأرقام فقط
        password_numbers = generate_password(
            8, 
            include_uppercase=False,
            include_lowercase=False,
            include_symbols=False
        )
        assert len(password_numbers) == 8
        assert password_numbers.isdigit()

    def test_validate_email(self):
        """اختبار التحقق من صحة البريد الإلكتروني."""
        # بريد صحيح
        assert validate_email("user@example.com") == True
        assert validate_email("student.123@university.edu.sa") == True

        # بريد غير صحيح
        assert validate_email("invalid-email") == False
        assert validate_email("user@") == False
        assert validate_email("@example.com") == False
