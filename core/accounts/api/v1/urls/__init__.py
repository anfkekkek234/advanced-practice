from django.urls import include, path

urlpatterns = [
    path("", include("accounts.api.v1.urls.accounts")),
    path("", include("accounts.api.v1.urls.profiles")),
]
