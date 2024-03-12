from django import forms
from django.db.models import Case, When, Value, IntegerField
from .form_choices import SORT_USER_CHOICES

class SortPeerForm(forms.Form):
    """Form enabling the sorting of users"""

    sort_by = forms.ChoiceField(choices=SORT_USER_CHOICES,required=False,label="Sort by")
    
    def sort_users(self, users, current_user):
        """Sorts users based on the selected criterion."""
        
        cleaned_data = self.cleaned_data
        sort_by = cleaned_data.get('sort_by')
        sort_options = {
            'username_asc': lambda qs: qs.order_by('username'),
            'username_desc': lambda qs: qs.order_by('-username'),
            'age_asc': lambda qs: qs.order_by('-date_of_birth'),
            'age_desc': lambda qs: qs.order_by('date_of_birth'),
        }
        if sort_by in sort_options:
            users = sort_options[sort_by](users)
        elif sort_by == '' and current_user:
            user_scores = [(user, self.calculate_match_score(current_user, user)) for user in users]
            sorted_users = sorted(user_scores, key=lambda x: x[1], reverse=True)
            users = [user_score[0] for user_score in sorted_users]
        return users
    
    def calculate_match_score(self, current_user, other_user):
        """Calculates the score of each user in relation to the current user """

        score = 0
        weighting_types = {"user_type":1,"age":0.4,"hospital":1,"age_of_diagnosis":0.2,"condition":1,
                     "child_age_of_diagnosis":0.2,"child_condition":1}
        score = self.calculate_user_type_score(current_user,other_user,weighting_types,score)
        score = self.calculate_age_score(current_user,other_user,weighting_types,score)
        weighting_user = {"gender": 0.2, "language": 0.9, "ethnicity": 0.2, "location": 1, "hospital": 1,}
        matches = {
            attribute: getattr(current_user, attribute, None) == getattr(other_user, attribute, None)
            for attribute in weighting_user}
        score += sum(weight for attribute, weight in weighting_user.items() if matches[attribute])
        return score

    def calculate_age_score(self,current_user,other_user,weighting,score):
        """Calclates score based on age proximity"""

        age_difference = abs(current_user.date_of_birth.year - other_user.date_of_birth.year)
        if age_difference <= 5:
            score += 1*weighting['age']
        return score
    
    def calculate_user_type_score(self, current_user, other_user, weighting,score):
        """Calculates user type specific score."""
        
        if hasattr(current_user, 'patient') and hasattr(other_user, 'patient'):
            score += 1 * weighting['user_type']
            score += self.calculate_condition_match(current_user.patient, other_user.patient, weighting['condition'], weighting['age_of_diagnosis'])
        elif hasattr(current_user, 'parent') and hasattr(other_user, 'parent'):
            score += 1 * weighting['user_type']
            score += self.calculate_condition_match(current_user.parent, other_user.parent, weighting['child_condition'], weighting['child_age_of_diagnosis'])
        elif hasattr(current_user, 'mentor') and hasattr(other_user, 'patient'):
            score += 1 * weighting['user_type']
            score += self.calculate_condition_match(current_user.mentor, other_user.patient, weighting['condition'], weighting['age_of_diagnosis'])
        return score
    
    def calculate_condition_match(self,user_type_1, user_type_2, condition_weight, age_diagnosis_weight):
        score=0
        if getattr(user_type_1, 'condition', None) == getattr(user_type_2, 'condition', None):
            score += condition_weight
        age_of_diagnosis_1 = getattr(user_type_1, 'age_of_diagnosis', None)
        age_of_diagnosis_2 = getattr(user_type_2, 'age_of_diagnosis', None)
        if age_of_diagnosis_1 and age_of_diagnosis_2:
            if abs(age_of_diagnosis_1 - age_of_diagnosis_2) < 5:
                score += age_diagnosis_weight
        return score


    