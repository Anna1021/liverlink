from django import forms
from django.db.models import Case, When, Value, IntegerField
from .form_choices import SORT_USER_CHOICES

class SortPeerForm(forms.Form):
    """Form enabling the sorting of users"""

    sort_by = forms.ChoiceField(choices=SORT_USER_CHOICES,required=False,label="Sort by")
    
    def calculate_user_type_score(self,current_user,other_user,weighting,score):
        """Calculates user type specific score"""
        if hasattr(current_user, 'patient') and hasattr(other_user, 'patient'):
            score+=1* weighting['user_type']
            if current_user.patient.condition == other_user.patient.condition:
                score += 1*weighting['condition']
            if abs(current_user.patient.age_of_diagnosis-other_user.patient.age_of_diagnosis)<5:
                score += 1*weighting['age_of_diagnosis']           
        elif hasattr(current_user, 'parent') and hasattr(other_user, 'parent'):
            score+=1* weighting['user_type']
            if current_user.parent.child_condition == other_user.parent.child_condition:
                score += 1*weighting['child_condition']
            if abs(current_user.parent.child_age_of_diagnosis-other_user.parent.child_age_of_diagnosis)<5:
                score += 1*weighting['child_age_of_diagnosis'] 
        return score

    def calculate_age_score(self,current_user,other_user,weighting,score):
        """Calclates score based on age proximity"""
        if current_user.date_of_birth and other_user.date_of_birth:
            age_difference = abs(current_user.date_of_birth.year - other_user.date_of_birth.year)
            if age_difference <= 5:
                score += 1*weighting['age']
        return score

    def calculate_match_score(self, current_user, other_user):
        """Calculates the score of each user in relation to the current user """
        score = 0
        weighting = {"user_type":1,"age":0.4,"gender":0.2,
                     "language":0.9,"ethnicity":0.2,"country":1,
                     "hospital":1,"age_of_diagnosis":0.2,"condition":1,
                     "child_age_of_diagnosis":0.2,"child_condition":1}
        score = self.calculate_user_type_score(current_user,other_user,weighting,score)
        score = self.calculate_age_score(current_user,other_user,weighting,score)
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
    
    def mark_users_if_dob_exists(self,users):
        users = users.annotate(
            dob_is_null=Case(
                When(date_of_birth=None, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        )
        return users
    
    def sort_users(self, users, current_user):
        """Sorts users based on the selected criterion."""
        cleaned_data = self.cleaned_data 
        sort_by = cleaned_data.get('sort_by')
        if sort_by == 'username_asc':
            users = users.order_by('username')
        elif sort_by == 'username_desc':
            users = users.order_by('-username')
        elif sort_by == 'age_asc':
            users = self.mark_users_if_dob_exists(users).order_by('dob_is_null', '-date_of_birth')
        elif sort_by == 'age_desc':
            users =  self.mark_users_if_dob_exists(users).order_by('dob_is_null', 'date_of_birth')
        elif sort_by == '' and current_user:
            user_scores = [(user, self.calculate_match_score(current_user, user)) for user in users]
            sorted_users = sorted(user_scores, key=lambda x: x[1], reverse=True)
            users = [user_score[0] for user_score in sorted_users]
        return users
    