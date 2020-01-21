from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Post
from marketing.models import Signup
from django.db.models import Count, Q


def get_category_count():
    query_set = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return query_set


def search(request):
    query = request.GET.get('q')
    query_set = Post.objects.all().order_by('-pk')

    if query:
        query_set = query_set.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'query_set':query_set
    }
    return render(request, 'search_result.html', context)


def index(request):
    querySet = Post.objects.filter(featured=True)
    all_posts = Post.objects.all().order_by('-timestamp')
    latest = Post.objects.all().order_by('-timestamp')[0:3]
    if request.method=='POST':
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
    context = {
        'object_list' : querySet,
        'latest': latest,
        'all_posts':all_posts
    }
    return render(request, 'index.html', context)


def post(request, id):
    query_set = Post.objects.all().filter(id=id)
    category_count = get_category_count()
    latest = Post.objects.all().order_by('-timestamp')[0:3]
    context = {
        'post':query_set,
        'latest':latest,
        'category_count':category_count

    }
    return render(request, 'post.html', context)


def blog(request):
    category_count = get_category_count()
    querySet = Post.objects.all().order_by('-pk')
    latest = Post.objects.all().order_by('-timestamp')[0:3]
    paginator = Paginator(querySet, 4)
    requested_page_var = "page"
    page = request.GET.get(requested_page_var)
    try:
        paginated_query = paginator.page(page)
    except PageNotAnInteger:
        paginated_query = paginator.page(1)
    except EmptyPage:
        paginated_query = paginator.page(paginator.num_pages)
    context = {
        'object_list' : paginated_query,
        'latest': latest,
        'requested_page_var': requested_page_var,
        'category_count':category_count
    }
    return render(request, 'blog.html', context)
