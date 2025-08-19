from common import launch_browser
from common.logger import logger
from portals.udise import StudentImport
from common.config import URL, log_config

if __name__ == "__main__":
    logger.info("=================== Starting AutoEdu ===================")
    log_config()

    try:
        launch_browser(URL)
        student_import = StudentImport()
        student_import.init_student_import()
        # If the second call is intentional, consider adding a comment or loop
        # importer.init_student_import()
    except Exception as e:
        logger.exception("AutoEdu encountered an error: %s", str(e))
    finally:
        logger.info("=================== End AutoEdu ===================")
