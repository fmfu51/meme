from django.urls import path
from articles import views

app_name = "article"

urlpatterns = [
    path('', views.index, name='index'),
    path('article/create/', views.article_create, name='create'),
    path('<int:article_id>/', views.article_detail, name='detail'),
    path('delete/<int:article_id>/', views.article_delete, name='delete'),
    path('update/<int:article_id>/', views.article_update, name='update'),
    path('comment/create/article/<int:article_id>/', views.comment_create, name='comment_create'),
    path('comment/update/article/<int:comment_id>/', views.comment_update, name='comment_update'),
    path('comment/delete/article/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('like/article/<int:article_id>/', views.like_article, name='like_article')
]
