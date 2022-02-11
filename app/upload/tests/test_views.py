from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import resolve, reverse
from upload.models import Submission
from upload.views import image_upload, submission


class UploadPageTest(TestCase):

    def test_upload_url_resolves_to_upload_page_view(self):
        found = resolve('/upload/')
        self.assertEqual(found.func, image_upload)

    def test_upload_view_redirects_after_upload(self):
        video = SimpleUploadedFile(
            "file.mp4",
            b"file_content",
            content_type="video/mp4"
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.client.login(
            username='testuser',
            password='testpassword'
        )
        response = self.client.post(
            reverse('upload:index'),
            {
                'file': video,
                'title': 'Test Submission',
                'description': 'Yooo',
                'permission': 'on'
            }
        )
        # Get the ID of the object we just created so we can test the correct url
        newObjectID = Submission.objects.first().id
        self.assertRedirects(
            response, 
            f'/upload/submission/{newObjectID}/', 
            status_code=302, 
            target_status_code=200, 
            fetch_redirect_response=True
        )

    def test_upload_view_can_save_a_POST_request(self):
        video = SimpleUploadedFile(
            "file.mp4",
            b"file_content",
            content_type="video/mp4"
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.client.login(
            username='testuser',
            password='testpassword'
        )
        response = self.client.post(
            reverse('upload:index'),
            {
                'file': video,
                'description': 'Yooo',
                'title': 'Test Title',
                'permission': 'on'
            },
            follow=True  # Required to follow through the redirect
        )
        self.assertIn('Yooo', response.content.decode())

    def test_can_upload_a_private_submission(self):
        video = SimpleUploadedFile(
            "file.mp4",
            b"file_content",
            content_type="video/mp4"
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.client.login(
            username='testuser',
            password='testpassword'
        )
        response = self.client.post(
            reverse('upload:index'),
            {
                'file': video,
                'description': 'Yooo',
                'title': 'Test Title',
                'private': 'on',
                'permission': 'on'
            },
            follow=True  # Required to follow through the redirect
        )
        response = self.client.post(reverse('main:index'))
        self.assertNotIn('Yooo', response.content.decode())

    def test_must_be_logged_in_to_view_upload_page(self):
        response = self.client.post(reverse('upload:index'))
        self.assertEqual(response.status_code, 302)


class SubmissionPageTest(TestCase):

    def test_submission_url_resolves_to_submission_page_view(self):
        found = resolve('/upload/submission/1/')
        self.assertEqual(found.func, submission)

    def test_submission_view_can_save_a_POST_request(self):
        video = SimpleUploadedFile(
            "file.mp4",
            b"file_content",
            content_type="video/mp4"
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.client.login(
            username='testuser',
            password='testpassword'
        )
        instance1 = Submission(
            title='Test Submission 1',
            description='This is test submission 1',
            file=video,
            author=self.user
        )
        instance1.save()
        response = self.client.post(
            reverse('upload:submission', kwargs={'submission_id': instance1.id}),
            {'comment': 'This is bad'},
            follow=True
        )
        self.assertIn('This is bad', response.content.decode())
