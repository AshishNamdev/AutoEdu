from common import login_user
from common.logger import logger
from portals.udise import StudentImport

if __name__ == "__main__":
    logger.info("=================== Starting AutoEdu ===================")

    try:
        login_user()
        importer = StudentImport()
        importer.init_student_import()
        # If the second call is intentional, consider adding a comment or loop
        # importer.init_student_import()
    except Exception as e:
        logger.exception("AutoEdu encountered an error: %s", str(e))
    finally:
        logger.info("=================== End AutoEdu ===================")
