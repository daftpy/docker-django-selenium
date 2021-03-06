import time
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import resolve
from main.views import index
from upload.models import FileSubmission, LinkSubmission

# Create your tests here.
class HomePageTest(TestCase):
    def setUp(self):
        video = SimpleUploadedFile(
            "file.mp4", b"file_content", content_type="video/mp4"
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")
        self.instance1 = FileSubmission(
            file=video,
            title="Test Submission 1",
            description="A test description",
            author=self.user,
        )
        self.instance1.save()
        self.instance2 = LinkSubmission(
            title="Test Submission 2",
            description="A test description",
            author=self.user,
            link="https://google.com",
        )
        self.instance2.save()

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, index)

    def test_home_page_displays_list_of_submissions(self):
        response = self.client.get("/")
        self.assertIn('<li class="submission">', response.content.decode())

    def test_home_page_displays_submissions_in_order(self):
        response = self.client.get("/")
        latestSubmision = response.content.decode().find(self.instance2.title)
        olderSubmission = response.content.decode().find(self.instance1.title)
        self.assertGreater(olderSubmission, latestSubmision)

    def test_home_page_annotates_queryset_with_correct_submission_type(self):
        response = self.client.get("/")
        # Keep in mind the submission_list is sorted by -created_at
        test_submissions = response.context["submission_list"]
        self.assertEqual(test_submissions[0].submission_type, "link")
        self.assertEqual(test_submissions[1].submission_type, "file")
