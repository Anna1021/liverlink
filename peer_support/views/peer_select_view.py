from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from peer_support.forms import SortUserForm, FilterUserForm, SearchUserForm
from .helpers import get_addable_peers, get_user_type, get_page


class PeerSelectView(LoginRequiredMixin, View):
    """Displays the page for viewing users on network."""

    template_name = "peer_select.html"

    def get(self, request):
        users = get_addable_peers(request.user)
        form_search = SearchUserForm(data=request.GET)
        form_sort = SortUserForm(data=request.GET)
        form_filter = FilterUserForm(data=request.GET)
        users = self.process_search(users, form_search)
        users = self.process_filter(users, form_filter)
        users = self.process_sort(users, form_sort, request.user)
        users_with_types = [{'user': user, 'user_type': get_user_type(user)} for user in users]
        users_with_types = get_page(request,users_with_types)
        context = {'users': users_with_types, 'form_sort': form_sort, 'form_filter': form_filter, 'form_search': form_search}
        return render(request, self.template_name, context)

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
