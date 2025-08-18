from common.config import MODULE, PORTAL, TASK

if PORTAL == "udsie" and MODULE == "student":
    from ui.udise.login import AcademicChoice, SchoolInformation, StudentLogin
    __all__ = ["StudentLogin", "AcademicChoice", "SchoolInformation"]
    if TASK == "import":
        from ui.udise.student_import import StudentImportUI
        __all__.append("StudentImportUI")
