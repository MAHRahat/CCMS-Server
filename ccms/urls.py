from django.conf.urls import url

from ccms import views

urlpatterns = [
    url(r'^citizens$', views.citizens_list),
    url(r'^employees$', views.employees_list),
    url(r'^users$', views.users_list),
    url(r'^users/(?P<pk>\d+)$', views.user_details),
    url(r'^categories$', views.categories_list),
    url(r'^categories/(?P<pk>\d+)$', views.categories_details),
    url(r'^complaints$', views.complaints_list),
    url(r'^complaints(?P<cs>\w+)$', views.complaints_list),
    url(r'^complaints/(?P<pk>\d+)$', views.complaints_details),
    url(r'^complaints/user/(?P<cid>\d+)$', views.complaints_of_citizen),
]
