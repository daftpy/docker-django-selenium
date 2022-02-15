import time
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import resolve
from main.views import index
from upload.models import FileSubmission, LinkSubmission

# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_home_page_displays_list_of_submissions(self):
        video = SimpleUploadedFile(
            "file.mp4", b"file_content", content_type="video/mp4"
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.client.login(
            username='testuser',
            password='testpassword'
        )
        instance1 = FileSubmission(
            file=video,
            title='Test Submission 1',
            description="A test description",
            author=self.user
        )
        instance1.save()
        instance2 = FileSubmission(
            file=video,
            title='Test Submission 2',
            description="Another test description",
            author=self.user
        )
        instance2.save()
        response = self.client.get('/')
        self.assertIn('<li class="submission">', response.content.decode())

    def test_home_page_displays_submissions_in_order(self):
        video = SimpleUploadedFile(
            "file.mp4", b"file_content", content_type="video/mp4"
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.client.login(
            username='testuser',
            password='testpassword'
        )
        instance1 = FileSubmission(
            file=video,
            title='Test Submission 1',
            description="A test description",
            author=self.user
        )
        instance1.save()
        instance2 = FileSubmission(
            file=video,
            title='Test Submission 2', 
            description="Another test description",
            author=self.user
        )
        instance2.save()
        response = self.client.get('/')
        latestSubmision = response.content.decode().find(instance2.title)
        olderSubmission = response.content.decode().find(instance1.title)
        self.assertGreater(olderSubmission, latestSubmision)
        
    def test_home_page_annotates_queryset_with_correct_submission_type(self):
        video = SimpleUploadedFile(
            "file.mp4", b"file_content", content_type="video/mp4"
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.client.login(
            username='testuser',
            password='testpassword'
        )
        instance1 = FileSubmission(
            file=video,
            title='Test Submission 1',
            description="A test description",
            author=self.user
        )
        instance2 = LinkSubmission(
            title='Test Submission 2',
            description='A test description',
            author=self.user,
            link='https://google.com'
        )
        instance1.save()
        instance2.save()
        response = self.client.get('/')
        # Keep in mind the submission_list is sorted by -created_at
        test_submissions = response.context['submission_list']
        self.assertEqual(test_submissions[0].submission_type, 'link')
        self.assertEqual(test_submissions[1].submission_type, 'file')
