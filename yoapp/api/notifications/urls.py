from django.conf.urls import  url
from .views import test_func
from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet
urlpatterns = [
    url(r'^reg-device/fcm/$',GCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='reg_fcm_device'),
    url(r'^reg-device/test/$', test_func, name='reg_fcm_device'),

]