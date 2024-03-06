from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from peer_support.forms import SortPeerForm, FilterPeerForm,SearchPeerForm
from .helpers import get_addable_peers

class PeerView(LoginRequiredMixin, View):
    """Displays the page for viewing all users on network."""
    template_name = 'peer_select.html'
    def get(self, request):
        users = get_addable_peers(request.user)
        formSearch=SearchPeerForm(data=request.GET)
        formSort = SortPeerForm( data=request.GET)
        formFilter = FilterPeerForm( data=request.GET)
        if formSearch.is_valid():
            users =formSearch.search_users(users)
        if formFilter.is_valid():
            users =formFilter.filter_users(users)
        else:
            messages.add_message(request, messages.ERROR, "Age invalid")
        if formSort.is_valid():
            users = formSort.sort_users(users, request.user)     
        context = {'users': users, 'formSort': formSort, 'formFilter': formFilter, 'formSearch': formSearch}
        return render(request, self.template_name, context)
    