import time
from django.contrib.auth.models import User
from .base import FunctionalTest
from selenium.webdriver.common.by import By


class NewCommentTest(FunctionalTest):

    def test_user_visits_site_for_first_time_and_leaves_feedback(self):
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

        self.browser.get(self.live_server_url)
        time.sleep(2)  # simulate long running test
        
        # The user notices the website title.
        self.assertIn('CritBoard', self.browser.title)

        # The user notices a list of user submitted art awaiting
        # feedback.
        submission_list = self.browser.find_elements(By.CLASS_NAME, 'submissionLink')
        self.assertEqual(len(submission_list), 2)

        # The user clicks on top submission and reads the description.
        self.browser.find_element(By.CLASS_NAME, 'submissionLink').click()
        self.browser.find_element(By.ID, 'submissionDescription')

        # The user leaves a comment, 'Good work!'
        commentInput = self.browser.find_element(By.NAME, 'comment')
        commentInput.send_keys('Great work!')
        self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        # The page refreshes and the user see's the comment.
        commentList = self.browser.find_elements(By.CLASS_NAME, 'commentWrapper')
        self.assertEqual(len(commentList), 1)
