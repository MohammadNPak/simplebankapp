from rest_framework import routers
from django.urls import path, include
from .views import (TransactionViewSet, CategoryViewSet,
                    monthly_summary_report,current_balance)

router = routers.DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("report/monthly", monthly_summary_report,name="monthly_summary_report"),
    path("report/current_balance", current_balance, name="current_balance")
]
