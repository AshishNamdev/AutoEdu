from common.config import MODULE, TASK

if MODULE == "student" and TASK == "import":
    from .student_module.import_module.student import Student
    from .student_module.import_module.student_import import StudentImport
    from .student_module.release_request import ReleaseRequest

    __all__ = ["StudentImport", "Student", "ReleaseRequest"]
