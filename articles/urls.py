from config.settings import dev as settings
from django.conf.urls.static import static
from django.urls import path
from articles import views

app_name = "article"

urlpatterns = [
    path('', views.index, name='index'),
    path('article/create/', views.article_create, name='article_create'),
    path('<int:article_id>', views.article_detail, name='article_detail'),
    path('delete/<int:article_id>', views.article_delete, name='article_delete'),
    path('update/<int:article_id>', views.article_update, name='article_update'),
]

