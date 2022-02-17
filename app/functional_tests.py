# import os
# import time
# import unittest
# from django.core.files.uploadedfile import SimpleUploadedFile
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_django.settings')
# import django
# django.setup()
# from upload.models import Submission


# class NewVisitorTest(unittest.TestCase):

#     def setUp(self):
#         caps = {'browserName': os.getenv('BROWSER', 'chrome')}
#         self.browser = webdriver.Remote(
#             command_executor='http://selenium-hub:4444/wd/hub',
#             desired_capabilities=caps
#         )
#         video = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")
#         instance1 = Submission(file=video)
#         instance1.save()
#         instance2 = Submission(file=video)
#         instance2.save()

#     def test_user_visits_site_for_first_time(self):
#         browser = self.browser
#         browser.get('http://web:8000/')
#         time.sleep(3)  # simulate long running test
#         # The user notices the website title.
#         self.assertIn('CritBoard', browser.title)
#         # The user notices a list of user submitted art awaiting
#         # feedback.
#         submission_list = self.browser.find_elements(By.CLASS_NAME, 'submissionLink')
#         self.assertEqual(len(submission_list), 2)


#     def test_user_can_upload_art_for_critique(self):
#         # The user visits the site and notices you can upload
#         # art and recieve feedback.
#         self.browser.get('http://web:8000/')
#         uploadButton = self.browser.find_element(By.ID, 'uploadPage')

#         # The user clicks the button and is taken to the
#         # upload page.
#         uploadButton.click()
#         self.assertIn('/upload/', self.browser.current_url)
#         pageHeader = self.browser.find_element(By.CLASS_NAME, 'pageHeader').text
#         self.assertEqual(pageHeader, 'Upload')

#         # The user wants critique and types the path of a file to
#         # upload for review.
#         fileField = self.browser.find_element(By.XPATH, "//input[@type='file']")
#         fileField.send_keys(os.getcwd() + '/upload_test_pic.png')

#         # The user clicks the upload button.
#         uploadButton = self.browser.find_element(By.CSS_SELECTOR, "input[type='submit']")
#         uploadButton.click()

#         # The user sees they are taken to a unique page for their
#         # file with a section for comments.
#         commentHeader = self.browser.find_elements(By.ID, 'commentHeader')
#         self.assertEqual(len(commentHeader), 1)


#     def tearDown(self):
#         self.browser.quit()  # quit vs close?


# if __name__ == '__main__':
#     unittest.main()
