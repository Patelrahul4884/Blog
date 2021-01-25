from django.urls import path
from . import views

urlpatterns = [
    path('create',views.api_blog_post_create,name='create'),
    path('<int:pk>/',views.api_blog_post_detail,name='detail'),
    path('<int:pk>/update',views.api_blog_post_update,name='update'),
    path('<int:pk>/delete',views.api_blog_post_delete,name='delete'),
]