import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class InstituteViewGuardTests(TestCase):
	def setUp(self):
		self.user_model = get_user_model()

	def test_student_cannot_open_institute_applications(self):
		student = self.user_model.objects.create_user(
			aadhaar="123456789012",
			password="Secret123!",
			role="STUDENT",
		)
		self.client.force_login(student)

		response = self.client.get(reverse("institute_applications"))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse("home"))

	def test_institute_without_profile_redirects_from_dashboard(self):
		institute_user = self.user_model.objects.create_user(
			aadhaar="999999999999",
			password="Secret123!",
			role="INSTITUTE",
		)
		self.client.force_login(institute_user)

		response = self.client.get(reverse("institute_dashboard"))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse("home"))

	def test_student_cannot_open_institute_verification_view(self):
		student = self.user_model.objects.create_user(
			aadhaar="111111111111",
			password="Secret123!",
			role="STUDENT",
		)
		self.client.force_login(student)

		response = self.client.get(
			reverse("institute_verify_application", kwargs={"application_id": uuid.uuid4()})
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse("home"))
