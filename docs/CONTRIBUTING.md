# دليل المساهمة في مشروع AutoEdu

نرحب بجميع المساهمات في مشروع AutoEdu! 🎉

## كيفية المساهمة

### 1. إعداد بيئة التطوير

```bash
# استنساخ المستودع
git clone https://github.com/yourusername/autoedu-refactor-solution.git
cd autoedu-refactor-solution

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # على Linux/Mac

# تثبيت متطلبات التطوير
pip install -r requirements-dev.txt

# تثبيت المشروع في وضع التطوير
pip install -e .
```

### 2. معايير الكود

#### تنسيق الكود
- نستخدم **Black** لتنسيق الكود
- نستخدم **isort** لترتيب الواردات
- نتبع معايير **PEP 8**

```bash
# تنسيق الكود قبل الcommit
black .
isort .
flake8 .
```

### 3. الاختبارات

```bash
# تشغيل جميع الاختبارات
pytest

# تشغيل اختبارات مع تقرير التغطية
pytest --cov=autoedu --cov-report=html
```

### 4. عملية المساهمة

1. **Fork المستودع** على GitHub
2. **إنشاء فرع جديد** للميزة أو الإصلاح
3. **كتابة الكود** مع اتباع المعايير المذكورة أعلاه
4. **إضافة اختبارات** للكود الجديد
5. **تشغيل جميع الاختبارات** والتأكد من نجاحها
6. **Commit التغييرات** برسالة واضحة
7. **Push الفرع** إلى مستودعك
8. **فتح Pull Request** مع وصف واضح للتغييرات

---

شكراً لك على اهتمامك بالمساهمة في مشروع AutoEdu! 🚀
