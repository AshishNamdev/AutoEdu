from common.logger import logger
from portals.udise.student_module.import_module import student
from ui.udise.search_pen_ui import SearchPENUI
from utils.date_time_utils import get_year_from_date


class SearchPEN:
    def __init__(self, student, student_data):
        self.student = student
        self.student_data = student_data

    def search_pen(self):
        """
        Searches for the student's PEN and DOB in the UDISE system.

        Steps:
        - Navigates to the search PEN UI.
        - Inputs the student's PEN and DOB.
        - Validates the search results.
        - Updates the student data with retrieved information or error status.

        Raises:
            TimeoutException: If UI elements are not interactable.
        """
        birth_year = get_year_from_date(student.get_dob())
        if birth_year is None:
            logger.warning("Invalid DOB format for student PEN: %s, "
                           "Skipping PEN search", student.get_student_pen())
            self.student_data["import_status"] = "No"
            self.student_data["remarks"] = "Invalid DOB format"
            return
        ui = SearchPENUI()
        ui.navigate_to_search_pen()
        pen_no = self.student.get_student_pen()
        dob = self.student.get_pen_dob()
        ui.input_pen_and_dob(pen_no, dob)
        status = ui.get_search_status()

        if "ok" == status:
            retrieved_pen, retrieved_dob = ui.get_ui_pen_and_dob_values()
            self.student.set_pen_dob(retrieved_dob)
            self.student_data["import_status"] = "Yes"
            self.student_data["remarks"] = "PEN found"
            logger.info("PEN found: %s, DOB: %s", retrieved_pen,
                        retrieved_dob)
        else:
            error_message = ui.get_ui_error_message()
            self.student_data["import_status"] = "No"
            self.student_data["remarks"] = error_message
            logger.warning("PEN search failed for PEN: %s, Error: %s",
                           pen_no, error_message)
