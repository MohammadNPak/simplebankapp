from rest_framework import routers

from .views import TransactionViewSet,CategoryViewSet

router = routers.DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'categories', CategoryViewSet)
urlpatterns = router.urls
