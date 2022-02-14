from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import resolve, reverse
from upload.models import FileSubmission
from upload.views import image_upload, submission, submit_view, submit_link


class UploadPageTest(TestCase):

    def test_upload_url_resolves_to_upload_page_view(self):
        found = resolve('/submission/file/')
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
            reverse('upload:submit_file'),
            {
                'file': video,
                'title': 'Test Submission',
                'description': 'Yooo',
                'permission': 'on'
            }
        )
        # Get the ID of the object we just created so we can test the correct url
        newObjectID = FileSubmission.objects.first().id
        self.assertRedirects(
            response, 
            f'/submission/file/{newObjectID}/', 
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
            reverse('upload:submit_file'),
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
            reverse('upload:submit_file'),
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


class SubmissionSelectPageTest(TestCase):

    def test_must_be_logged_in_to_view_submit_select_page(self):
        response = self.client.post(reverse('upload:submit_select'))
        self.assertEqual(response.status_code, 302)

    def test_submission_url_resolves_to_submit_select_page_view(self):
        found = resolve('/submission/')
        self.assertEqual(found.func, submit_view)


class SubmissionPageTest(TestCase):

    def test_submission_url_resolves_to_submission_page_view(self):
        found = resolve('/submission/file/1/')
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
        instance1 = FileSubmission(
            title='Test Submission 1',
            description='This is test submission 1',
            file=video,
            author=self.user
        )
        instance1.save()
        response = self.client.post(reverse('upload:submission', kwargs={
            'submission_type': 'file',
            'submission_id': instance1.id
        }),
            data={'comment': 'This is bad'},
            follow=True
        )
        self.assertIn('This is bad', response.content.decode())


class SubmitLinkViewTest(TestCase):

    def test_submit_link_url_resolves_to_submit_link_view(self):
        found = resolve('/submission/link/')
        self.assertEqual(found.func, submit_link)

    def test_submit_link_view_can_save_POST_request(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(
            username='testuser',
            password='testpassword'
        )
        response = self.client.post(
            reverse('upload:submit_link'),
            {
                'title': 'Test Link Submission',
                'description': 'This is a test link submission',
                'link': 'https://soundcloud.com',
                'permission': 'on'
            },
            follow=True
        )
        response = self.client.post(reverse('main:index'))
        self.assertIn('Test Link Submission', response.content.decode())
