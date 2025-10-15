"""
Module: search_pen_ui.py

Provides UI automation for retrieving and validating student PEN and DOB
information from the UDISE portal using Aadhaar and birth year as search
criteria.

Intended for use in automated workflows that require PEN resolution
or validation against student records.

Author: Ashish Namdev (ashish28 [dot] sirt [at] gmail [dot] com)

Date Created: 2025-10-03
Last Modified: 2025-10-15

Version: 1.0.0
"""

from common.logger import logger
from ui.locators.udise import SearchPENLocators
from ui.ui_actions import UIActions as UI


class SearchPENUI:
    """
    UI automation handler for retrieving student PEN and DOB from the
    UDISE portal.

    This class encapsulates the UI flow for:
    - Opening the PEN search interface
    - Filling Aadhaar and birth year fields
    - Submitting the search
    - Extracting PEN and DOB from the UI
    - Closing the interface

    Attributes:
    -----------
    aadhaar_no : [str]
        Aadhaar number used for search.
    birth_year : [str]
        Year of birth used for search.
    pen_no : [str]
        Retrieved PEN number from the UI.
    dob : [str]
        Retrieved date of birth from the UI.
    """

    def __init__(self, aadhaar_no, birth_year=None):
        """
        Initializes the SearchPENUI instance with Aadhaar number
        and birth year.

        Parameters:
        -----------
        aadhaar_no : str
            The Aadhaar number used to search for the student's PEN and DOB.
        birth_year : str
            The year of birth used as part of the search criteria.
        """
        self.aadhaar_no = aadhaar_no
        self.birth_year = birth_year
        self.pen_no = None
        self.dob = None
        self.error_message = None
        self.search_status = None

    def set_birth_year(self, birth_year):
        """
        Updates the birth year used for the search.

        Parameters:
        -----------
        birth_year : str
            The new year of birth to be used in the search.
        """
        self.birth_year = birth_year

    def _open_search_ui(self):
        """
        Opens the Get PEN & DOB search interface in the UDISE portal.
        """
        UI.wait_and_click(SearchPENLocators.GET_PEN_AND_DOB_BUTTON)
        logger.debug("Opened Get PEN & DOB search interface.")

    def _fill_search_fields(self):
        """
        Fills the Aadhaar number and Year of Birth fields in the
        Get PEN & DOB search interface form.
        """
        field_data = [
            (self.aadhaar_no, SearchPENLocators.AADHAAR_NO),
            (self.birth_year, SearchPENLocators.YEAR_OF_BIRTH),
        ]
        UI.fill_fields(field_data)
        logger.debug("Filled search fields with Aadhaar and Year of Birth.")

    def _submit_search_data(self):
        """
        Submits the search form by clicking the search button.
        """
        UI.wait_and_click(SearchPENLocators.SEARCH_BUTTON)
        logger.debug("Submitted search form for Get PEN & DOB.")

    def _get_search_status(self):
        """
        Determines the outcome of the search.

        Returns:
            str: "ok" if student data is found, "error" otherwise.
        """
        return UI.wait_for_first_match(
            locators={
                "error": SearchPENLocators.ERROR_MESSAGE,
                "ok": SearchPENLocators.STUDENT_PEN_VALUE,
            },
            timeout=15,
        )

    def _get_ui_pen_value(self):
        """
        Extracts the PEN value from the UI.

        Returns:
            str: Student PEN number.
        """
        return UI.wait_and_find_element(
            SearchPENLocators.STUDENT_PEN_VALUE
        ).get_attribute("innerHTML")

    def _get_ui_dob_value(self):
        """
        Extracts the DOB value from the UI.

        Returns:
            str: Student date of birth.
        """
        return UI.wait_and_find_element(
            SearchPENLocators.STUDENT_DOB_VALUE
        ).get_attribute("innerHTML")

    def _get_ui_pen_and_dob_values(self):
        """
        Retrieves both PEN and DOB values from the UI.

        Returns:
            tuple[str, str]: (PEN, DOB) values.
        """
        return (self._get_ui_pen_value(),
                self._get_ui_dob_value()
                )

    def _get_ui_error_message(self):
        """
        Extracts the error message from the UI if the search fails.

        Returns:
            str: Error message text.
        """
        return UI.wait_and_find_element(
            SearchPENLocators.ERROR_MESSAGE
        ).get_attribute("innerHTML")

    def _close_search_pen_ui(self):
        """
        Closes the Get PEN & DOB search interface form.
        """
        UI.wait_and_click(SearchPENLocators.CLOSE_BUTTON)

    def _close_error_message_ui(self):
        """
        Closes the error message dialog in the UDISE portal
        Get PEN & DOB search interface UI.

        This method clicks the 'OK' button on the error popup to dismiss it,
        allowing the workflow to continue or retry.
        """
        UI.wait_and_click(SearchPENLocators.ERROR_OK_BUTTON)

    def search_ui_pen_and_dob(self):
        """
        Executes the full PEN search flow:
        - Opens Get PEN & DOB search interface UI
        - Fills search fields
        - Submits form
        - Extracts PEN and DOB if found
        - Extracts error message if not found
        - Closes error message UI if present
        - Closes Get PEN & DOB search interface UI

        Sets:
            self.pen_no, self.dob : Retrieved values or None if not found.
        """
        logger.info(
            "Starting PEN and DOB search for Aadhaar No: %s, "
            "Year of Birth: %s",
            self.aadhaar_no,
            self.birth_year
        )
        self._open_search_ui()
        self._fill_search_fields()
        self._submit_search_data()

        search_status = self._get_search_status()
        logger.info("Search Status: %s", search_status)

        if search_status == "ok":
            self.pen_no, self.dob = self._get_ui_pen_and_dob_values()
            logger.info("Retrieved PEN: %s, DOB: %s", self.pen_no, self.dob)
        else:
            self.error_message = self._get_ui_error_message()
            logger.error("Search failed with error: %s", self.error_message)
            self._close_error_message_ui()

        self.search_status = search_status
        # Close the search UI
        self._close_search_pen_ui()

    def get_pen_no(self):
        """
        Returns the retrieved PEN Number value.

        Returns:
            str or None: The student's PEN number if found, else None.
        """
        return self.pen_no.strip() if self.pen_no else None

    def get_dob(self):
        """
        Returns the retrieved DOB value.

        Returns:
            str or None: The student's DOB if found, else None.
        """
        return self.dob.strip() if self.dob else None

    def get_error_message(self):
        """
        Returns the retrieved error message if the search failed.

        Returns:
            str or None: The error message if search failed, else None.
        """
        return self.error_message.strip() if self.error_message else None

    def get_search_status(self):
        """
        Returns the status of the last search operation.

        Returns:
            str or None: "ok" if search was successful, "error" if failed,
                         else None if no search performed.
        """
        return self.search_status.strip() if self.search_status else None
