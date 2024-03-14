from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from peer_support.forms import SortPeerForm, FilterPeerForm,SearchPeerForm
from django.contrib import messages

@login_required
def friends_list(request):
    """Display the list of friends."""
    user = request.user
    friends = user.friends.all()
    formSearch= SearchPeerForm(data=request.GET)
    formSort = SortPeerForm( data=request.GET)
    formFilter = FilterPeerForm( data=request.GET)
    if formSearch.is_valid():
        friends = formSearch.search_users(friends)
    if formFilter.is_valid():
        friends = formFilter.filter_users(friends)
    else:
        messages.add_message(request, messages.ERROR, "Age invalid")
    if formSort.is_valid():
        friends = formSort.sort_users(friends, request.user)     
    context = {'friends': friends, 'formSort': formSort, 'formFilter': formFilter, 'formSearch': formSearch}
    return render(request, 'friends_list.html', context)