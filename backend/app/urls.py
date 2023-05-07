from django.urls import include, path

urlpatterns = [
    path("v1/", include("app.user.v1.urls")),
]
