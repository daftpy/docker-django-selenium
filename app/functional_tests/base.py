import os
import time
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from selenium import webdriver
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_django.settings')
import django
django.setup() # Needs to be done before import models
from upload.models import FileSubmission

class FunctionalTest(LiveServerTestCase):
    # Needed to make django.test LiveServerTestCase work
    # https://stackoverflow.com/questions/32408429/running-django-tests-with-selenium-in-docker
    host = 'web' 
    def setUp(self):
        caps = {'browserName': os.getenv('BROWSER', 'chrome')}
        self.browser = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=caps
        )
        video = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.client.login(
            username='testuser',
            password='testpassword'
        )
        instance1 = FileSubmission(
            title='Test submission 1',
            description='This is test submission 1',
            file=video,
            author=self.user
        )
        instance1.save()
        time.sleep(1)
        instance2 = FileSubmission(
            title='Test submission 2',
            description='This is test submission 2',
            file=video,
            author=self.user
        )
        instance2.save()

    def tearDown(self):
        self.browser.quit()  # quit vs close?
