from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

from portfolio import views

urlpatterns = [
    path("", views.home),
    path("admin/", admin.site.urls),
    path("api/content/", views.content),
    path("api/csrf/", views.csrf),
    path("api/visit/", views.visit),
    path("api/contact/", views.contact),
    path("health/", lambda request: JsonResponse({"ok": True})),
]
