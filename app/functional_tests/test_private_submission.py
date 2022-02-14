import os
from django.contrib.auth.models import User
from .base import FunctionalTest
from selenium.webdriver.common.by import By

class PrivateSubmissionTest(FunctionalTest):

    def test_user_can_upload_private_art(self):
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
        self.browser.add_cookie({
            'name': 'sessionid',
            'value': cookie.value,
            'secure': False,
            'path': '/'
        })
        self.browser.refresh()
        # The user is feeling a little self concious about their art
        # submission. They want to make sure it won't appear on the wall.
        # They go to the upload page.
        self.browser.find_element(By.ID, 'submitPage').click()

        # They want to upload the file since it has never been uploaded
        # anywhere else.
        self.browser.find_element(By.ID, 'uploadPage').click()
        
        # The user wants critique and types the path of a file to
        # upload for review.
        fileField = self.browser.find_element(
            By.XPATH, "//input[@type='file']"
        )
        fileField.send_keys(os.getcwd() + '/upload_test_pic.png')

        titleField = self.browser.find_element(By.NAME, 'title')
        titleField.send_keys('The Best Art')

        # The user gives the submission a brief description.
        descriptionField = self.browser.find_element(By.NAME, 'description')
        descriptionField.send_keys('This is a test description.')

        # The user checks the private box to make sure the submission will
        # not appear on the front page.
        self.browser.find_element(By.NAME, 'private').click()
