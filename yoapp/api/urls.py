from django.conf.urls import re_path, include, url
from .views import UserViewSet, Logout
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserViewSet, CategoryViewSet #, UserLoginView
from django.contrib.auth import views
#from django.views.decorators.csrf import csrf_exempt
#from rest_framework_jwt.views import obtain_jwt_token



router = routers.DefaultRouter()
router.include_format_suffixes = False
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns = router.urls

# urlpatterns += [
#     re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
# ]

login_kwargs = {}
urlpatterns += [
    # url(r'^user/login/$', UserLoginView.as_view(), login_kwargs, name='login'),
    # url(r'^logout/$', views.logout, name='logout'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    #url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^logout/', Logout.as_view()),
    #url(r'^account/', include('account.urls')),
]




#urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

#print (router.urls)

