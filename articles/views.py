from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils import timezone

from articles.forms import ArticleForm
from articles.models import Article


def index(request):
    article_list = Article.objects.order_by('-reg_date')
    context = {'article_list': article_list}
    return render(request, 'articles/article_list.html', context)


def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.reg_date = timezone.now()
            article.save()
            return redirect('article:index')
    else:
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'articles/article_form.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    context = {'article': article}
    return render(request, 'articles/article_detail.html', context)


def article_delete(request):
    return HttpResponse("delete 구동 확인")


def article_update(request):
    return HttpResponse("update 구동 확인")