from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import Contact, Profile, Project, Visit


class PortfolioTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/csrf/")
        self.token = self.client.cookies["csrftoken"].value

    def test_cms_content_and_admin_access(self):
        Profile.objects.create(headline="From the CMS")
        Project.objects.create(title="Draft")
        Project.objects.create(title="Published", published=True)
        data = self.client.get("/api/content/").json()
        self.assertEqual(data["profile"]["headline"], "From the CMS")
        self.assertEqual([project["title"] for project in data["projects"]], ["Published"])
        url = reverse("admin:portfolio_profile_changelist")
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(get_user_model().objects.create_superuser("editor"))
        self.assertContains(self.client.get(url), "Alan Shaju")

    @override_settings(CONTACT_RECIPIENT="owner@example.com", EMAIL_HOST="smtp.example.com")
    def test_contact_validation_csrf_and_mail(self):
        data = {"name": "Reader", "email": "reader@example.com", "message": "Hello Alan!"}
        self.assertEqual(self.client.post("/api/contact/", data).status_code, 403)
        invalid = self.client.post("/api/contact/", {"name": "Reader"}, HTTP_X_CSRFTOKEN=self.token)
        self.assertEqual(invalid.status_code, 400)
        response = self.client.post("/api/contact/", data, HTTP_X_CSRFTOKEN=self.token)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Contact.objects.get().emailed)
        self.assertEqual(mail.outbox[0].reply_to, ["reader@example.com"])
        self.assertEqual(mail.outbox[0].to, ["owner@example.com"])

    @override_settings(CONTACT_RECIPIENT="owner@example.com", RESEND_API_KEY="test-key")
    @patch("portfolio.views.urlopen", side_effect=OSError)
    def test_contact_is_retained_on_delivery_failure(self, _):
        response = self.client.post("/api/contact/", {
            "name": "Reader", "email": "reader@example.com", "message": "Hello Alan!",
        }, HTTP_X_CSRFTOKEN=self.token)
        self.assertEqual(response.status_code, 201)
        self.assertFalse(Contact.objects.get().emailed)

    @override_settings(GEOIP_PATH="/private/GeoLite2-City.mmdb", TRUSTED_PROXY_HOPS=1)
    @patch("portfolio.views.geoip")
    def test_visit_location_and_privacy_signal(self, geoip):
        geoip.return_value = Mock()
        geoip.return_value.city.return_value = {"city": "Example", "region": "Example region", "country_name": "Example country"}
        headers = {
            "HTTP_X_CSRFTOKEN": self.token, "HTTP_X_FORWARDED_FOR": "192.0.2.1, 8.8.8.8",
            "HTTP_USER_AGENT": "Example browser", "HTTP_ACCEPT_LANGUAGE": "en",
        }
        self.client.post("/api/visit/", HTTP_SEC_GPC="1", **headers)
        self.assertFalse(Visit.objects.exists())
        response = self.client.post("/api/visit/", {"referrer": "https://example.com/path?q=private"}, **headers)
        self.assertEqual(response.status_code, 200)
        visit = Visit.objects.get()
        self.assertEqual((visit.ip, visit.city, visit.referrer_host), ("8.8.8.8", "Example", "example.com"))
        self.assertEqual((visit.device, visit.language), ("Example browser", "en"))
