"""
Conditional initializer for UDISE student import workflow.

This module dynamically exposes core components of the student import pipeline
based on the configured MODULE and TASK values. When MODULE is set to "student"
and TASK to "import", it imports and exposes:

    - StudentImport: Handles UI-driven student import operations
    - Student: Manages student data and school context
    - ReleaseRequest: Prepares and submits release requests for student
      transfers

These components are made available via `__all__` for streamlined access in
workflow orchestration, automation scripts, or UI integration layers.

Author: Ashish Namdev (ashish28 [at] sirt [dot] gmail [dot] com)

Date Created: 2025-08-19
Last Modified: 2025-10-14

Version: 1.0.0
"""


from common.config import MODULE, TASK

if MODULE == "student" and TASK == "import":
    from .student_module.import_module.release_request import ReleaseRequest
    from .student_module.import_module.search_pen import SearchPEN
    from .student_module.import_module.student import Student
    from .student_module.import_module.student_import import StudentImport

    __all__ = ["StudentImport", "Student", "ReleaseRequest", "SearchPEN"]
