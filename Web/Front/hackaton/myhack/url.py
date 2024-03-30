from django.urls import path
from . import views


urlpatterns = [
    path("", views.my_view, name="my_view"),
    path('upload_image', views.upload_image, name='upload_image'),
]
