from django.urls import path

from django.conf.urls import url
from uploadapp import views


app_name= 'uploadapp'

urlpatterns = [
    url(r'upload-file/', views.BgFileUploadView.as_view()),
    url(r'images/', views.BgFileListView.as_view()),
]
#
