# from unittest.mock import patch
#
# from rest_framework import status
#
#
# @patch("rollbar.report_message")
# def test_cors_failure_is_reported(mock_report, client):
#     response = client.get("/", HTTP_ORIGIN="http://example.com")
#     assert response.status_code == status.HTTP_200_OK
#     mock_report.assert_called_once()
#
#
# @patch("rollbar.report_message")
# def test_cors_success_is_not_reported(mock_report, settings, client):
#     settings.CORS_ALLOWED_ORIGINS = ["http://example.com"]
#     response = client.get("/", HTTP_ORIGIN="http://example.com")
#     assert response.status_code == status.HTTP_200_OK
#     mock_report.assert_not_called()
