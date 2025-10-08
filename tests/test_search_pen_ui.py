from common import launch_browser
from common.config import PASSWORD, URL, USERNAME
from portals.udise import StudentImport
from ui.udise.login import StudentLogin
from ui.udise.search_pen_ui import SearchPENUI


def test_search_pen():
    launch_browser(URL)
    login = StudentLogin()
    login.student_login(USERNAME, PASSWORD, max_attempts=3)
    logged_in_school = login.get_logged_in_school()
    stu_import = StudentImport(logged_in_school)
    stu_import.import_ui.select_import_options()

    aadhaar_nos = ["686127303251", "686127303251"]
    birth_years = ["2010", "2014"]
    for aadhaar_no, birth_year in zip(aadhaar_nos, birth_years):
        search_pen_ui = SearchPENUI(aadhaar_no=aadhaar_no, birth_year=birth_year)
        search_pen_ui.search_pen_dob()
        print("PEN:", search_pen_ui.get_pen())
        print("DOB:", search_pen_ui.get_dob())
        print("Error Message:", search_pen_ui.get_error_message())
