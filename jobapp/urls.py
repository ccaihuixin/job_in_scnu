from django.conf.urls import url
from jobapp import views
urlpatterns =[
    url(r'job_info/',views.Job_infoView.as_view()),
    url(r'job_add/',views.Job_addView.as_view()),
    url(r'job_detail/', views.Job_detailView.as_view()),
]