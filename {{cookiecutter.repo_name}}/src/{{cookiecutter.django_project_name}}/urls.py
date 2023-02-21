"""{{ cookiecutter.django_project_name }} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("{{ cookiecutter.django_app_name }}.urls")),
{%- if cookiecutter.worker == "rq" %}
    path("admin/rq/", include("django_rq.urls")),
{%- endif %}
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        path(r"rosetta/", include("rosetta.urls")),
    ]

try:
    import uwsgi  # noqa
except ImportError:
    pass
else:
    urlpatterns += [
        path("admin/uwsgi/", include("django_uwsgi.urls")),
    ]

if settings.DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
