from django.shortcuts import render
from peer_support.models import Post
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class SearchView(LoginRequiredMixin, View):
    """View to search for posts."""

    def search_post(request):
        if request.method == 'POST':
            search_query = request.POST['search_query']
            posts = Post.objects.filter(content__contains=search_query)
            return render(request, 'feed.html', {'query':search_query, 'posts':posts})
        else:
            return render(request, 'feed.html',{})