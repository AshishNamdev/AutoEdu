from common import login_user
from portals.udise import StudentImport

login_user()
StudentImport().init_student_import()
