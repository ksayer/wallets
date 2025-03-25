from django.contrib import admin
from django.urls import include, path

from wallets.api.v1.urls import router as wallets_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include(wallets_router.urls)),
]
