from common.config import MODULE, TASK

if MODULE == "student" and TASK = "import":
    from .student_module.import_module.student_import import StudentImport
    __all__ = ["StudentImport"]
