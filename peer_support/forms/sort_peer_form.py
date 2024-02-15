from django import forms
from peer_support.models import Parent, Patient, User
from .form_choices import SORT_USER_CHOICES

class SortPeerForm(forms.Form):
    """Form enabling the sorting of users"""

    sort_by = forms.ChoiceField(choices=SORT_USER_CHOICES,required=False,label="Sort by")
    
    def calculate_match_score(self, current_user, other_user):
        score = 0
        weighting = {"user_type":0.7,"age":0.4,"gender":0.25,
                     "language":0.9,"ethnicity":0.2,"country":1,
                     "hospital":1,"age_of_diagnosis":0.2,"condition":1,
                     "child_age_of_diagnosis":0.2,"child_condition":1}

        current_user = User.objects.select_related().get(id=current_user.id)
        other_user = User.objects.select_related().get(id=other_user.id)

        if isinstance(current_user, Patient) and isinstance(other_user, Patient):
            score+=1* weighting['user_type']
            if current_user.condition == other_user.condition:
                score += 1*weighting['condition']
            if abs(current_user.age_of_diagnosis-other_user.age_of_diagnosis)<5:
                score += 1*weighting['gender']           
        elif isinstance(current_user, Parent) and isinstance(other_user, Parent):
            score+=1* weighting['user_type']
            if current_user.child_condition == other_user.child_condition:
                score += 1*weighting['child_condition']
            if abs(current_user.child_age_of_diagnosis-other_user.child_age_of_diagnosis)<5:
                score += 1*weighting['child_gender']  

        if current_user.date_of_birth and other_user.date_of_birth:
            age_difference = abs(current_user.date_of_birth.year - other_user.date_of_birth.year)
            if age_difference <= 5:
                score += 1*weighting['age']

        if current_user.gender == other_user.gender:
            score += 1*weighting['gender']        
        if current_user.language == other_user.language:
            score += 1*weighting['language']
        if current_user.ethnicity == other_user.ethnicity:
            score += 1*weighting['ethnicity']
        if current_user.location == other_user.location:
            score += 1*weighting['country']
        if current_user.hospital == other_user.hospital:
            score += 1*weighting['hospital']
        return score
    
    def sort_users(self, users, current_user):
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
            user_scores = [(user, self.calculate_match_score(current_user, user)) for user in users]
            sorted_users = sorted(user_scores, key=lambda x: x[1], reverse=True)
            users = [user_score[0] for user_score in sorted_users]
        return users
    