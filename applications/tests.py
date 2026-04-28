from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from requests import RequestException

from .verification import auto_verify


class AutoVerifyTests(SimpleTestCase):
	@staticmethod
	def _mock_response(payload):
		response = Mock()
		response.raise_for_status.return_value = None
		response.json.return_value = payload
		return response

	@patch("applications.verification.requests.get")
	def test_auto_verify_handles_service_outage(self, mock_get):
		mock_get.side_effect = RequestException("service down")

		verified, payload = auto_verify(application=None, aadhaar="123456789012")

		self.assertFalse(verified)
		self.assertIn("service unavailable", payload.lower())

	@patch("applications.verification.requests.get")
	def test_auto_verify_rejects_invalid_domicile(self, mock_get):
		mock_get.side_effect = [
			self._mock_response({"income": "ok", "caste": "ok", "domicile": "ok"}),
			self._mock_response({"fraud": False, "domicile": "Punjab"}),
		]

		verified, payload = auto_verify(application=None, aadhaar="123456789012")

		self.assertFalse(verified)
		self.assertEqual(payload, "Invalid domicile")

	@patch("applications.verification.requests.get")
	def test_auto_verify_passes_valid_records(self, mock_get):
		digi_payload = {"income": "ok", "caste": "ok", "domicile": "ok"}
		mock_get.side_effect = [
			self._mock_response(digi_payload),
			self._mock_response({"fraud": False, "domicile": "Jammu & Kashmir"}),
		]

		verified, payload = auto_verify(application=None, aadhaar="123456789012")

		self.assertTrue(verified)
		self.assertEqual(payload, digi_payload)
