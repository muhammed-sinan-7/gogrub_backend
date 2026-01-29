from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from users.views import health

schema_view = get_schema_view(
    openapi.Info(
        title="GoGrub API Documentation",
        default_version="v1",
        description="API documentation for GoGrub E-commerce",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Health check endpoints (both with and without trailing slash)
    path("health/", health, name="health"),
    path("health", health, name="health-no-slash"),
    
    # Admin
    path("admin/", admin.site.urls),
    
    # API endpoints
    path("api/auth/", include("users.urls")),
    path("api/", include("chatbot.urls")),
    path("api/products/", include("products.urls")),
    path("api/cart/", include("cart.urls")),
    path("api/wishlist/", include("wishlist.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/admin/", include("admin.urls")),
    path("api/notifications/", include("notifications.urls")),
    
    # API documentation
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", 
        schema_view.with_ui("redoc", cache_timeout=0), 
        name="schema-redoc"
    ),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
