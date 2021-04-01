from django.conf.urls import url
from jobapp import views

urlpatterns = [
    url(r'job_info/', views.Job_infoView.as_view()),
    url(r'job_add/', views.Job_addView.as_view()),
    url(r'job_detail/', views.Job_detailView.as_view()),
    url(r'user/', views.UserView.as_view()),
    url(r'my_publish/', views.My_publishView.as_view()),
    url(r'my_collect/', views.My_collectView.as_view()),
    url(r'my_collectList/', views.My_collectListView.as_view()),
    url(r'sign/', views.SignView.as_view()),
    url(r'search/', views.SearchView.as_view()),
]
