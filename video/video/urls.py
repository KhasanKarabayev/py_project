from django.urls import path
from .views import  *

urlpatterns = [
    path('v/<lesson_id>', generate_video ),
]