"""
أدوات معالجة النصوص لمشروع AutoEdu

يوفر وظائف مساعدة للعمل مع النصوص والسلاسل النصية.
"""

import re
from typing import List
import hashlib
import secrets
import string


def clean_text(
    text: str,
    remove_extra_spaces: bool = True,
    remove_special_chars: bool = False,
    keep_arabic: bool = True
) -> str:
    """
    تنظيف النص من الأحرف غير المرغوب فيها.

    Args:
        text: النص المطلوب تنظيفه
        remove_extra_spaces: إزالة المسافات الإضافية
        remove_special_chars: إزالة الأحرف الخاصة
        keep_arabic: الاحتفاظ بالأحرف العربية

    Returns:
        النص المُنظف
    """
    if not text:
        return ""

    # إزالة المسافات الزائدة
    if remove_extra_spaces:
        text = re.sub(r'\s+', ' ', text).strip()

    # إزالة الأحرف الخاصة
    if remove_special_chars:
        if keep_arabic:
            # الاحتفاظ بالأحرف العربية والإنجليزية والأرقام فقط
            text = re.sub(r'[^\w\s\u0600-\u06FF]', '', text)
        else:
            # الاحتفاظ بالأحرف الإنجليزية والأرقام فقط
            text = re.sub(r'[^\w\s]', '', text)

    return text.strip()


def extract_emails(text: str) -> List[str]:
    """
    استخراج عناوين البريد الإلكتروني من النص.

    Args:
        text: النص المطلوب البحث فيه

    Returns:
        قائمة بعناوين البريد الإلكتروني
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)


def generate_password(
    length: int = 12,
    include_uppercase: bool = True,
    include_lowercase: bool = True,
    include_numbers: bool = True,
    include_symbols: bool = True
) -> str:
    """
    توليد كلمة مرور قوية.

    Args:
        length: طول كلمة المرور
        include_uppercase: تضمين أحرف كبيرة
        include_lowercase: تضمين أحرف صغيرة
        include_numbers: تضمين أرقام
        include_symbols: تضمين رموز

    Returns:
        كلمة مرور قوية
    """
    characters = ""

    if include_lowercase:
        characters += string.ascii_lowercase
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if not characters:
        raise ValueError("يجب تحديد نوع واحد على الأقل من الأحرف")

    return ''.join(secrets.choice(characters) for _ in range(length))


def validate_email(email: str) -> bool:
    """
    التحقق من صحة عنوان البريد الإلكتروني.

    Args:
        email: عنوان البريد الإلكتروني

    Returns:
        True إذا كان صحيحاً
    """
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    return bool(re.match(pattern, email))
