from django.urls import path, include
from accounts.api.v1.views import ProfileApiView

urlpatterns = [
    # profile
    path("profile/", ProfileApiView.as_view(), name="profile")
]
