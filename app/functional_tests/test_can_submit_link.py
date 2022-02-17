from django.contrib.auth.models import User
from .base import FunctionalTest
from selenium.webdriver.common.by import By


class NewVisitorSubmitLinkTest(FunctionalTest):
    def test_visitor_visits_site_and_submits_link(self):
        user = User.objects.create_user(username="Testuser", password="testuser")
        # Login the client for the test
        self.client.login(username="Testuser", password="testuser")
        cookie = self.client.cookies["sessionid"]
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(
            {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
        )
        self.browser.refresh()

        # The user visits the site and notices you can submit art
        # and recieve feedback.
        submitButton = self.browser.find_element(By.ID, "submitPage")
        # The user clicks the button and is taken to the
        # submission page.
        submitButton.click()
        self.assertIn("/submission/", self.browser.current_url)
        # The user sees they can choose between submitting a link or
        # or uploading a file. Since the user already uploaded their
        # file to soundcloud, they will just submit the link.
        self.browser.find_element(By.ID, "linkPage").click()

        # The user is taken to the link submission page.
        self.assertIn("/submission/link/", self.browser.current_url)

        pageHeader = self.browser.find_element(By.CLASS_NAME, "pageHeader").text
        self.assertEqual(pageHeader, "Link Submission")

        # The user see's a form and begins to fill it out in order
        # to submit their link.
        titleField = self.browser.find_element(By.NAME, "title")
        titleField.send_keys("The Best Art")
