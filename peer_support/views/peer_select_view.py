from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from peer_support.forms import SortPeerForm, FilterPeerForm,SearchPeerForm
from peer_support.models import User
from django.contrib import messages


class PeerView(LoginRequiredMixin, View):
    """Displays the page for viewing all users on network."""

    template_name = 'peer_select.html'

    def get(self, request):
        users = User.objects.exclude(is_staff=True).exclude(id=request.user.id).distinct()
        formSearch=SearchPeerForm(data=request.GET)
        formSort = SortPeerForm( data=request.GET)
        formFilter = FilterPeerForm( data=request.GET)
        if formSearch.is_valid():
            users =formSearch.search_users(users)
        if formFilter.is_valid():
            users =formFilter.filter_users(users)
        if formSort.is_valid():
            users = formSort.sort_users(users)
        else:
            messages.add_message(request, messages.ERROR, "Please choose only one sorting criterion: either Username or Age.")
        

        return render(request, self.template_name, {'users': users, 'formSort': formSort, 'formFilter': formFilter, 'formSearch': formSearch})
