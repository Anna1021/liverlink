from django.shortcuts import render
from peer_support.forms import SortUserForm, FilterUserForm, SearchUserForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .helpers import get_user_type

class FriendsListView(LoginRequiredMixin, View):
    """Display the list of friends."""

    def get(self, request):
        """Display the list of friends."""

        friends = request.user.friends.all()
        friends_with_types = [{'friend': friend, 'user_type': get_user_type(friend)} for friend in friends]
        form_search, form_sort, form_filter = self.get_forms(request)
        friends = self.process_forms(friends, form_search, form_sort, form_filter, request.user)
        context = {'friends': friends_with_types, 'form_sort': form_sort, 'form_filter': form_filter, 'form_search': form_search}
        return render(request, 'friends_list.html', context)
        
    def get_forms(self, request):
        """Return the search, sort, and filter forms."""
        
        form_search = SearchUserForm(data=request.GET)
        form_sort = SortUserForm(data=request.GET)
        form_filter = FilterUserForm(data=request.GET)
        return form_search, form_sort, form_filter

    def process_forms(self, friends, form_search, form_sort, form_filter, user):
        """Process forms and return the filtered, sorted, and searched friends."""

        friends = self.process_search(friends, form_search)
        friends = self.process_filter(friends, form_filter)
        friends = self.process_sort(friends, form_sort, user)
        return friends

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