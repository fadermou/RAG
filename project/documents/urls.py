from django.urls import path
from .views import DocumentUploadAPIView, DocumentListAPIView
from .views import *

urlpatterns = [
    path("upload/", DocumentUploadAPIView.as_view(), name="upload-document"),
    path("list/", DocumentListAPIView.as_view(), name="list-documents"),

]
