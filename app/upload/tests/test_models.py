from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from upload.models import FileSubmission, LinkSubmission


class UploadModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.video = SimpleUploadedFile(
            "file.mp4", b"file_content", content_type="video/mp4"
        )

    def test_saving_and_retrieving_submissions(self):
        first_submission = FileSubmission(
            title="Test Submission 1",
            description="This is test submission 1.",
            author=self.user,
            file=self.video,
        )
        second_submission = FileSubmission(
            title="Test Submission 2",
            description="This is test submission 2.",
            author=self.user,
            file=self.video,
        )
        first_submission.save()
        second_submission.save()

        saved_submissions = FileSubmission.objects.all()
        self.assertEqual(saved_submissions.count(), 2)

        first_saved_submission = saved_submissions[0]
        second_saved_submission = saved_submissions[1]
        self.assertEqual(
            first_saved_submission.description, "This is test submission 1."
        )
        self.assertEqual(
            second_saved_submission.description, "This is test submission 2."
        )

    def test_submission_requires_title(self):
        test_submission = FileSubmission(
            title="", description="Test description", author=self.user, file=self.video
        )
        with self.assertRaises(ValidationError):
            test_submission.save()
            test_submission.full_clean()

    def test_submission_requires_description(self):
        test_submission = FileSubmission(
            title="Test Submission 1", description="", author=self.user, file=self.video
        )
        with self.assertRaises(ValidationError):
            test_submission.save()
            test_submission.full_clean()

    def test_submission_requires_file(self):
        test_submission = FileSubmission(
            title="Test Submission 1",
            description="This is a test submission.",
            author=self.user,
        )
        with self.assertRaises(ValidationError):
            test_submission.save()
            test_submission.full_clean()

    def test_submission_requires_author(self):
        test_submission = FileSubmission(
            title="Test Submission 1",
            description="This is a test submission.",
            file=self.video,
        )
        with self.assertRaises(IntegrityError):
            test_submission.save()
            test_submission.full_clean()


class LinkModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

    def test_saving_and_retrieving_link_submission(self):
        test_submission = LinkSubmission(
            title="Test Submission 1",
            description="This is a test link submission",
            link="https://soundcloud.com",
            author=self.user,
        )
        test_submission2 = LinkSubmission(
            title="Test Submission 2",
            description="This is another test link submission",
            link="https://google.com",
            author=self.user,
        )
        test_submission.save()
        test_submission2.save()
        saved_submissions = LinkSubmission.objects.all()
        self.assertEqual(saved_submissions.count(), 2)

    def test_link_submissions_validates_link(self):
        test_submission = LinkSubmission(
            title="Test Submission 1",
            description="This is another test link submission",
            link="not a link",
            author=self.user,
        )
        with self.assertRaises(ValidationError):
            test_submission.full_clean()
