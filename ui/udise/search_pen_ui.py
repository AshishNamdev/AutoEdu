from common.ui_handler import UIHandler as UI
from ui.locators.udise import SearchPENLocators


class SearchPENUI:
    """
    UI handler for searching and validating student PENs in the UDISE portal.

    This class encapsulates methods to interact with the search PEN interface,
    including inputting search criteria, submitting the form, and validating
    the results against expected student data.

    Attributes:
    -----------
    driver : WebDriver
        The Selenium WebDriver instance used for browser interactions.

    Methods:
    --------
    enter_search_criteria(pen, dob):
        Inputs the provided PEN and DOB into the search fields.
    submit_search():
        Clicks the search button to submit the form.
    validate_search_results(expected_student):
        Validates the search results against the expected student data.
    """

    def __init__(self):
        """
        Initializes the SearchPENUI object with a WebDriver instance.

        The WebDriver is managed by the WebDriverManager singleton to ensure
        consistent browser sessions across the application.
        """

    def _go_to_get_pen_ui(self):
        """"""
        UI.wait_and_click(SearchPENLocators.GET_PEN_AND_DOB_BUTTON)

    def _submit_search(self):
        """
        Clicks the search button to submit the PEN and DOB search form.

        Raises:
            TimeoutException: If the search button is not clickable within
                              the expected time.
        """
        UI.wait_and_click(SearchPENLocators.SEARCH_BUTTON)

    def get_pen_and_dob(self, aadhaar_no, birth_year):
        """
        Navigates to the Get PEN and DOB interface and inputs the provided
        Aadhaar number and birth year.

        Args:
            aadhaar_no (str): The student's Aadhaar number.
            birth_year (str): The student's birth year.
        """
        self._go_to_get_pen_ui()
        field_data = [
            (aadhaar_no, SearchPENLocators.AADHAAR_NO),
            (birth_year, SearchPENLocators.YEAR_OF_BIRTH),
        ]
        UI.fill_fields(field_data)
        self._submit_search()
