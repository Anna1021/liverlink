from django import forms

class SortPeerForm(forms.Form):
    """Form enabling the sorting of users"""
    SORT_CHOICES = [
        ('', 'Best Match'),  # Assuming '' signifies default sorting or 'Best Match'
        ('username_asc', 'Username Ascending'),
        ('username_desc', 'Username Descending'),
        ('age_asc', 'Age Ascending'),
        ('age_desc', 'Age Descending'),
    ]

    sort_by = forms.ChoiceField(choices=SORT_CHOICES,required=False,label="Sort by")

    
    def calculate_match_score(current_user, other_user):
        """
        Calculate a 'match score' based on the location of current_user and other_user.
        """
        score = 0
        # Increment score if both users are in the same location
        if current_user.location == other_user.location:
            score += 1
        return score
    
    def sort_users(self, users):
        """Sorts users based on the selected criterion."""
        cleaned_data = self.cleaned_data 
        sort_by = cleaned_data.get('sort_by')

        if sort_by == 'username_asc':
            users = users.order_by('username')
        elif sort_by == 'username_desc':
            users = users.order_by('-username')
        elif sort_by == 'age_asc':
            users = users.order_by('-date_of_birth')
        elif sort_by == 'age_desc':
            users = users.order_by('date_of_birth')
        elif sort_by == '' and current_user:
            users = list(users)  # Convert queryset to list for custom sorting
            for user in users:
                user.match_score = calculate_match_score(current_user, user)
            users.sort(key=lambda user: user.match_score, reverse=True)

        return users