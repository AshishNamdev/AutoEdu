from udise import login_user, select_academic_year
from udise.student_module.import_module.student_import import StudentImport

login_user()
select_academic_year()

StudentImport().init_student_import()
