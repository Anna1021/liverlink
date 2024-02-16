# from django.urls import reverse
# from django.shortcuts import render

# class ReferralView():
#     def referral_link(request):
#         mentor_id = request.user.id
#         referral_link = request.build_absolute_uri(reverse('register')) + '?ref=' + str(mentor_id)
#         return render(request, 'referral_link.html', {'referral_link': referral_link})