from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils import timezone

from articles.forms import ArticleForm, CommentForm
from articles.models import Article, Comment


def index(request):
    # 페이징 입력 파라미터
    page = request.GET.get('page', '1')

    # 조회
    article_list = Article.objects.order_by('-reg_date')

    # 페이징 처리
    paginator = Paginator(article_list, 1)
    page_obj = paginator.get_page(page)

    context = {'article_list': page_obj}
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
    article = Article.objects.get(pk=article_id)
    context = {'article': article}
    return render(request, 'articles/article_detail.html', context)


@login_required(login_url='accounts:login')
def article_delete(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user != article.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('article:detail', article_id=article.id)
    article.delete()
    return redirect('article:index')


@login_required(login_url='accounts:login')
def article_update(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user != article.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('article:detail', article_id=article.id)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.update_date = timezone.now()
            article.save()
            return redirect('article:detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    context = {'form': form}
    return render(request, 'articles/article_update.html', context)


def comment_create(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.reg_date = timezone.now()
            comment.article = article
            comment.save()
            return redirect('article:detail', article_id=article.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'articles/comment_form.html')


@login_required(login_url='accounts:login')
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글 수정 권한이 없습니다.')
        return redirect('article:detail', article_id=comment.article.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.update_date = timezone.now()
            comment.save()
            return redirect('article:detail', article_id=comment.article.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'articles/comment_form.html', context)


@login_required(login_url='accounts:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글 삭제 권한이 없습니다')
        return redirect('article:detail', article_id=comment.article.id)
    else:
        comment.delete()
    return redirect('article:detail', article_id=comment.article.id)
