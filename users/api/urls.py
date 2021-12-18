from django.urls import path

from .views import user_views

urlpatterns = [
    path('get_token/', user_views.CreateTokenView),
    path('sign_up/', user_views.CreateUserView),
]
