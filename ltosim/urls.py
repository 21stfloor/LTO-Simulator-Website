from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from system import views
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.views import LogoutView
from system.views import MyLoginView, QuestionViewSet, ReviewerViewSet
from django.urls import include, re_path
from system.admin import admin_site

router = routers.DefaultRouter()
router.register(r'scores', views.ScoreViewSet)
router.register(r'reviewers', ReviewerViewSet)
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    path('', include('system.urls', namespace='system')),
    path('api/', include((router.urls, 'app_name'), namespace='instance_name')),
    path('admin/', admin_site.urls),
    # path("admin-users/", views.user_list, name="users"),
    path('accounts/login/',
        MyLoginView.as_view(),
        name='login',
    ),
    path(
        'accounts/logout/',
        LogoutView.as_view(),
        name='logout',
    ),
    path("accounts/register", views.register_request, name="register")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)