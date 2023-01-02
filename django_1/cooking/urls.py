from django.urls import path, re_path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from django.views.generic import TemplateView

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title='Главный дед мороз',
        default_version='v 0.0.1',
        description='Документация по API к ресурсу кулинария',
        terms_of_service='https://www.google.com/policies/terms',
        contact=openapi.Contact(email='khasan@uzmobile.uz'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)


urlpatterns = [
    # path('', index, name='index'),
    path('', Index.as_view(), name='index'),
    # path('category/<int:pk>/', category_list, name='category_list'),
    path('category/<int:pk>/', ArticleByCategory.as_view(), name='category_list'),
    # path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/', ArticleDetail.as_view(), name='post_detail'),
    path('add_article/', add_post, name='add'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('post/<int:pk>/update/', ArticleUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', ArticleDelete.as_view(), name='post_delete'),

    # API
    path('posts/api/', CookingAPI.as_view(), name='CookingAPI'),
    path('posts/api/<int:pk>', CookingAPIDetail.as_view(), name='CookingAPIDetail'),
    path('categories/api/', CookingCategoryAPI.as_view(), name='CookingCategoryAPI'),
    path('categories/api/<int:pk>', CookingCategoryAPIDetail.as_view(), name='CookingCategoryAPIDetail'),
    # Doc: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#installation
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path(
        'swagger-ui/',
        TemplateView.as_view(
            template_name='swagger/swagger_ui.html',
            extra_context={'schema_url': 'openapi-schema'},
        ),
        name='swagger-ui',

    ),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=1),
        name='schema-json'
    )
]