from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

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

]