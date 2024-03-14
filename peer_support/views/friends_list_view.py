from django.shortcuts import render
from peer_support.forms import SortPeerForm, FilterPeerForm, SearchPeerForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class FriendsListView(LoginRequiredMixin, View):
    """Display the list of friends."""

    def get(self, request):
        user = request.user
        friends = user.friends.all()
        form_search = SearchPeerForm(data=request.GET)
        form_sort = SortPeerForm(data=request.GET)
        form_filter = FilterPeerForm(data=request.GET)
        friends = self.process_search(friends, form_search)
        friends = self.process_filter(friends, form_filter)
        friends = self.process_sort(friends, form_sort, request.user)
        context = {'friends': friends, 'formSort': form_sort, 'formFilter': form_filter, 'formSearch': form_search}
        return render(request, 'friends_list.html', context)

    def process_search(self, users, form_search):
        """Process search form."""

        if form_search.is_valid():
            users = form_search.search_users(users)
        return users

    def process_filter(self, users, form_filter):
        """Process filter form and handle validation."""

        if form_filter.is_valid():
            users = form_filter.filter_users(users)
            return users
        else:
            messages.add_message(self.request, messages.ERROR, "Age invalid")
            return users

    def process_sort(self, users, form_sort, current_user):
        """Process sort form if filter form is valid."""

        if form_sort.is_valid():
            users = form_sort.sort_users(users, current_user)
        return users
