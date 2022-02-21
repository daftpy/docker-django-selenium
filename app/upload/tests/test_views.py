from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.test import TestCase
from django.urls import resolve, reverse
from upload.models import FileSubmission
from upload.views import (
    submit_view,
    FileSubmissionView,
    LinkSubmissionView,
    SubmissionView,
)
from pathlib import Path


class BaseTest(TestCase):
    def setUp(self):
        # Get the posix path for two directories up
        self.path = str(Path(__file__).resolve().parents[2])
        file_path = self.path + "/upload_test_vid.mp4"
        # We read in real video content so it passes python-magic validation
        # in the view
        self.video = SimpleUploadedFile(
            name="test_vid.mp4",
            content=open(file_path, "rb").read(),
            content_type="video/mp4",
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )


class UploadPageTest(BaseTest):
    def test_upload_url_resolves_to_upload_page_view(self):
        found = resolve("/submission/file/")
        self.assertEqual(found.func.__name__, FileSubmissionView.as_view().__name__)

    def test_upload_view_redirects_after_upload(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("upload:submit_file"),
            {
                "file": self.video,  # make the posix path a string
                "title": "Test Submission",
                "description": "Yooo",
                "permission": "on",
            },
        )
        # Get the ID of the object we just created so we can test the correct url
        newObjectID = FileSubmission.objects.first().id
        self.assertRedirects(
            response,
            f"/submission/file/{newObjectID}/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_upload_view_can_save_a_POST_request(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("upload:submit_file"),
            {
                "file": self.video,
                "description": "Yooo",
                "title": "Test Title",
                "permission": "on",
            },
            follow=True,  # Required to follow through the redirect
        )
        self.assertIn("Yooo", response.content.decode())

    def test_can_upload_a_private_submission(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("upload:submit_file"),
            {
                "file": self.video,
                "description": "Yooo",
                "title": "Test Title",
                "private": "on",
                "permission": "on",
            },
            follow=True,  # Required to follow through the redirect
        )
        response = self.client.post(reverse("main:index"))
        self.assertNotIn("Yooo", response.content.decode())

    def test_upload_view_validates_file_type(self):
        self.client.login(username="testuser", password="testpassword")
        bad_file = SimpleUploadedFile(
            name="test_text.txt",
            content=open(self.path + "/requirements.txt", "rb").read(),
            content_type="text/plain",
        )
        response = self.client.post(
            reverse("upload:submit_file"),
            {
                "file": bad_file,
                "description": "Yooo",
                "title": "Test Title",
                "permission": "on",
            },
            follow=True,
        )
        self.assertIn(
            "Not the correct file type. Try .jpg, .png, .mp3, .mp4, or .flac",
            response.content.decode(),
        )


class SubmissionSelectPageTest(TestCase):
    def test_must_be_logged_in_to_view_submit_select_page(self):
        response = self.client.post(reverse("upload:submit_select"))
        self.assertEqual(response.status_code, 302)

    def test_submission_url_resolves_to_submit_select_page_view(self):
        found = resolve("/submission/")
        self.assertEqual(found.func, submit_view)


class SubmissionPageTest(BaseTest):
    def test_submission_url_resolves_to_submission_page_view(self):
        found = resolve("/submission/file/1/")
        self.assertEqual(found.func.__name__, SubmissionView.as_view().__name__)

    def test_submission_view_can_save_a_POST_request(self):
        self.client.login(username="testuser", password="testpassword")
        instance1 = FileSubmission(
            title="Test Submission 1",
            description="This is test submission 1",
            file=self.video,
            author=self.user,
        )
        instance1.save()
        response = self.client.post(
            reverse(
                "upload:submission",
                kwargs={"submission_type": "file", "submission_id": instance1.id},
            ),
            data={"comment": "This is bad"},
            follow=True,
        )
        self.assertIn("This is bad", response.content.decode())

    def test_must_be_authenticated_to_post_to_submission_view(self):
        instance1 = FileSubmission(
            title="Test Submission 1",
            description="This is test submission 1",
            file=self.video,
            author=self.user,
        )
        instance1.save()
        response = self.client.post(
            reverse(
                "upload:submission",
                kwargs={"submission_type": "file", "submission_id": instance1.id},
            ),
            data={"comment": "This is bad"},
            follow=True,
        )
        # Make sure client is sent to the login page.
        self.assertIn("<h2>Login</h2>", response.content.decode())


class SubmitLinkViewTest(BaseTest):
    def test_submit_link_url_resolves_to_submit_link_view(self):
        found = resolve("/submission/link/")
        self.assertEqual(found.func.__name__, LinkSubmissionView.as_view().__name__)

    def test_submit_link_view_can_save_POST_request(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("upload:submit_link"),
            {
                "title": "Test Link Submission",
                "description": "This is a test link submission",
                "link": "https://soundcloud.com",
                "permission": "on",
            },
            follow=True,
        )
        response = self.client.post(reverse("main:index"))
        self.assertIn("Test Link Submission", response.content.decode())
