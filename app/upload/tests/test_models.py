from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from upload.models import Submission


class UploadModelTests(TestCase):

    def test_saving_and_retrieving_submissions(self):
        video = SimpleUploadedFile(
            "file.mp4",
            b"file_content",
            content_type="video/mp4"
        )
        user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        first_submission = Submission(
            title='Test Submission 1',
            description='This is test submission 1.',
            author=user,
            file=video
        )
        second_submission = Submission(
            title='Test Submission 2',
            description='This is test submission 2.',
            author=user,
            file=video
        )
        first_submission.save()
        second_submission.save()

        saved_submissions = Submission.objects.all()
        self.assertEqual(saved_submissions.count(), 2)

        first_saved_submission = saved_submissions[0]
        second_saved_submission = saved_submissions[1]
        self.assertEqual(
            first_saved_submission.description,
            'This is test submission 1.'
        )
        self.assertEqual(
            second_saved_submission.description,
            'This is test submission 2.'
        )

    def test_submission_requires_title(self):
        video = SimpleUploadedFile(
            "file.mp4",
            b"file_content",
            content_type="video/mp4"
        )
        user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        test_submission = Submission(
            title='',
            description='Test description',
            author=user,
            file=video
        )
        with self.assertRaises(ValidationError):
            test_submission.save()
            test_submission.full_clean()

    def test_submission_requires_description(self):
        video = SimpleUploadedFile(
            "file.mp4",
            b"file_content",
            content_type="video/mp4"
        )
        user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        test_submission = Submission(
            title='Test Submission 1',
            description='',
            author=user,
            file=video
        )
        with self.assertRaises(ValidationError):
            test_submission.save()
            test_submission.full_clean()

    def test_submission_requires_file(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        test_submission = Submission(
            title='Test Submission 1',
            description='This is a test submission.',
            author=user   
        )
        with self.assertRaises(ValidationError):
            test_submission.save()
            test_submission.full_clean()

    def test_submission_requires_author(self):
        video = SimpleUploadedFile(
            "file.mp4",
            b"file_content",
            content_type="video/mp4"
        )
        test_submission = Submission(
            title='Test Submission 1',
            description='This is a test submission.',
            file=video
        )
        with self.assertRaises(IntegrityError):
            test_submission.save()
            test_submission.full_clean()