from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.views.generic.edit import FormView
from peer_support.models import Post
from peer_support.forms import PostForm

class CreatePostView(LoginRequiredMixin,FormView):
    
    def get(self,request):
        form = PostForm()
        return render(request, 'create_post.html', {'form': form})

    def post(self,request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed') 
        
