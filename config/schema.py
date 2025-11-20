from django.urls import path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class HttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Spy Cat Agency API",
        default_version="v1",
        description="Api description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="khasanjon.dev@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    generator_class=HttpAndHttpsSchemaGenerator,
    permission_classes=[permissions.AllowAny],
)

swagger_urlpatterns = [
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
