import ipaddress
import json
import logging
from functools import lru_cache
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from django import forms
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception
from django.core.mail import EmailMessage
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from geoip2.errors import AddressNotFoundError

from .models import Contact, Experience, Profile, Project, Visit

logger = logging.getLogger(__name__)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "email", "message")


@require_GET
@ensure_csrf_cookie
def home(request):
    return render(request, "index.html")


@require_GET
@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({"ok": True})


@require_GET
def content(request):
    profile = Profile.objects.first() or Profile()
    fields = ("name", "headline", "intro", "about", "github", "linkedin", "focus")
    projects = Project.objects.filter(published=True).values("id", "title", "description", "stack", "url")
    experience = Experience.objects.filter(published=True).values(
        "id", "title", "organization", "period", "location", "description",
    )
    return JsonResponse({
        "profile": model_to_dict(profile, fields=fields), "projects": list(projects),
        "experience": list(experience),
    })


@lru_cache(maxsize=1)
def geoip():
    return GeoIP2(settings.GEOIP_PATH)


@require_POST
def visit(request):
    if request.headers.get("DNT") == "1" or request.headers.get("Sec-GPC") == "1":
        return JsonResponse({"ok": True})
    ip = request.META.get("REMOTE_ADDR", "")
    forwarded = request.headers.get("X-Forwarded-For", "").split(",")
    hops = settings.TRUSTED_PROXY_HOPS
    if hops > 0 and len(forwarded) >= hops:
        ip = forwarded[-hops].strip()
    try:
        address = ipaddress.ip_address(ip)
    except ValueError:
        return JsonResponse({"ok": True})
    location = {}
    if address.is_global and settings.GEOIP_PATH:
        try:
            location = geoip().city(str(address))
        except AddressNotFoundError:
            pass
        except (GeoIP2Exception, OSError):
            logger.exception("GeoIP database unavailable")
    try:
        host = urlsplit(request.POST.get("referrer", "")).hostname or ""
    except ValueError:
        host = ""
    Visit.objects.create(
        ip=str(address), city=(location.get("city") or "")[:120],
        region=(location.get("region") or "")[:120],
        country=(location.get("country_name") or "")[:120],
        referrer_host=host[:253], device=request.headers.get("User-Agent", "")[:300],
        language=request.headers.get("Accept-Language", "")[:100],
    )
    return JsonResponse({"ok": True})


@require_POST
def contact(request):
    if request.POST.get("website"):
        return JsonResponse({"ok": True})
    form = ContactForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)
    submission = form.save()
    recipient = settings.CONTACT_RECIPIENT or ("owner@localhost" if settings.DEBUG else "")
    if recipient:
        try:
            submission.emailed = send_contact_email(submission, recipient)
            if submission.emailed:
                submission.save(update_fields=["emailed"])
        except (OSError, URLError, ValueError):
            logger.warning("Unable to mail portfolio contact %s", submission.pk)
    return JsonResponse({"ok": True}, status=201)


def send_contact_email(submission, recipient):
    subject = "New portfolio message"
    body = f"From {submission.name} <{submission.email}>\n\n{submission.message}"
    if settings.RESEND_API_KEY:
        payload = json.dumps({
            "from": settings.DEFAULT_FROM_EMAIL, "to": [recipient],
            "subject": subject, "text": body, "reply_to": submission.email,
        }).encode()
        request = Request("https://api.resend.com/emails", data=payload, headers={
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "alan-portfolio/1.0",
        })
        with urlopen(request, timeout=settings.EMAIL_TIMEOUT) as response:
            return 200 <= response.status < 300
    if settings.DEBUG or settings.EMAIL_HOST:
        return bool(EmailMessage(subject, body, to=[recipient], reply_to=[submission.email]).send())
    return False
