from .base import FunctionalTest
from selenium.webdriver.common.by import By


class AuthenticateSubmissionTest(FunctionalTest):

    def test_must_be_authenticated_to_view_submission_page(self):
        browser = self.browser
        browser.get(self.live_server_url + '/upload/')
        self.browser.find_element(By.XPATH, '//h2[text()="Registration Form"]')
