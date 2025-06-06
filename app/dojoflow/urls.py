from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .api_views import (
    ClubViewSet, AttestationLevelViewSet, StudentViewSet, UserProfileViewSet
)
# TODO: Заменить на новый StudentViewSet после исправления ошибок
# from .api.v1.views.student import StudentViewSet

# Создаем роутер для API
router = DefaultRouter()
router.register(r'clubs', ClubViewSet, basename='club')
router.register(r'attestation-levels', AttestationLevelViewSet, basename='attestationlevel')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'profile', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    # JWT аутентификация
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('api/', include(router.urls)),
] 