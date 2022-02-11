from .base import FunctionalTest
from selenium.webdriver.common.by import By


class SubmissionOrderTest(FunctionalTest):

    def test_submissions_display_in_order_created(self):
        # The user visits the site and sees the newest submissions are at
        # the top of the submissions list.
        self.browser.get(self.live_server_url)
        submissionList = self.browser.find_elements(
            By.CLASS_NAME, 'submission'
        )
        self.assertIn('Test submission 2', submissionList[0].text)
        self.assertIn('Test submission 1', submissionList[1].text)
