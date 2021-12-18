from django.urls import path

from .api.urls import urlpatterns as api_urls

app_name = "users"

urlpatterns = [

] + api_urls
