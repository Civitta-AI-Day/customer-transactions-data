from django.urls import include, path

urlpatterns = [
    path("api/", include("apps.customers.urls")),
    path("api/", include("apps.transactions.urls")),
]
