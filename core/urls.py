from django.urls import path,include


from . import views
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register("tests",views.TestModelViewSet)

urlpatterns = [
    path('', views.HelloView.as_view(),name="hello"),
    path('api/',include(router.urls)),
     path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/tests/<int:test_pk>/questions',views.QuestionApiView.as_view(),name="question")
    
]
