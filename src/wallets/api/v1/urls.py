from rest_framework import routers

from wallets.api.v1.views import WalletViewSet, TransactionViewSet


router = routers.DefaultRouter()
router.register(r"wallets", WalletViewSet)
router.register(r"transactions", TransactionViewSet)

urlpatterns = router.urls
