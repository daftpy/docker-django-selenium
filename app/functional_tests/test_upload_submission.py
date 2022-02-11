import os
from django.contrib.auth.models import User
from .base import FunctionalTest
from selenium.webdriver.common.by import By


class NewVisitorTest(FunctionalTest):

    def test_user_can_upload_art_for_critique(self):
        user = User.objects.create_user(
            username='Testuser',
            password='testuser'
        )
        # Login the client for the test
        self.client.login(
            username='Testuser',
            password='testuser'
        )
        cookie = self.client.cookies['sessionid']
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh()

        # The user visits the site and notices you can upload
        # art and recieve feedback.
        # self.browser.get(self.live_server_url)
        uploadButton = self.browser.find_element(By.ID, 'uploadPage')
        
        # The user clicks the button and is taken to the
        # upload page.
        uploadButton.click()
        self.assertIn('/upload/', self.browser.current_url)
        pageHeader = self.browser.find_element(By.CLASS_NAME, 'pageHeader').text
        self.assertEqual(pageHeader, 'Upload')

        # The user wants critique and types the path of a file to
        # upload for review.
        fileField = self.browser.find_element(By.XPATH, "//input[@type='file']")
        fileField.send_keys(os.getcwd() + '/upload_test_pic.png')

        titleField = self.browser.find_element(By.NAME, 'title')
        titleField.send_keys('The Best Art')

        # The user gives the submission a brief description.
        descriptionField = self.browser.find_element(By.NAME, 'description')
        descriptionField.send_keys('This is a test description.')

        # The user checks the box to aknlowedge they have permission to
        # upload the file.
        self.browser.find_element(By.NAME, 'permission').click()

        # The user clicks the upload button.
        uploadButton = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
        uploadButton.click()

        # The user sees they are taken to a unique page for their
        # file with a section for comments.
        commentHeader = self.browser.find_elements(By.ID, 'commentHeader')
        self.assertEqual(len(commentHeader), 1)

        # The user see's their title and description were saved accurately.
        content = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('The Best Art', content)
        self.assertIn('This is a test description.', content)
