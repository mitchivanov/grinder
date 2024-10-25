from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'strategies', views.TradingStrategyViewSet, basename='strategy')

urlpatterns = [
    # Web interface URLs
    path('', views.StrategyListView.as_view(), name='strategy_list'),
    path('strategy/create/', views.StrategyCreateView.as_view(), name='strategy_create'),
    path('strategy/<int:pk>/', views.StrategyDetailView.as_view(), name='strategy_detail'),
    
    # API URLs
    path('api/', include(router.urls)),
]
