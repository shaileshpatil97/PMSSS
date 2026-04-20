from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class InstituteLoginLegacyPasswordTests(TestCase):
	def test_institute_login_upgrades_plaintext_password(self):
		User = get_user_model()

		user = User.objects.create(
			aadhaar="999999999999",
			role="INSTITUTE",
			is_active=True,
		)
		user.password = "Secret123!"
		user.save(update_fields=["password"])

		response = self.client.post(
			reverse("institute_login"),
			{"aadhaar": user.aadhaar, "password": "Secret123!"},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response["Location"], reverse("institute_dashboard"))

		user.refresh_from_db()
		self.assertNotEqual(user.password, "Secret123!")
		self.assertIn("$", user.password)
