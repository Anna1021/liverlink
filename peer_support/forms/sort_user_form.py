from django import forms
from .form_choices import SORT_USER_CHOICES

class SortUserForm(forms.Form):
    """Form enabling the sorting of users"""

    sort_by = forms.ChoiceField(choices=SORT_USER_CHOICES, required=False,label="Sort by")
    weighting_types = {"user_type": 1,"age": 0.4, "hospital": 1, "age_of_diagnosis": 0.2, "condition": 1,
                     "child_age_of_diagnosis": 0.2, "child_condition": 1, "expertise": 2}
    
    def sort_by_username(self, users, order):
        return users.order_by(order + 'username')

    def sort_by_age(self, users, order):
        return users.order_by(order + 'date_of_birth')

    def sort_by_match_score(self, users, current_user):
        user_scores = [(user, self.calculate_match_score(current_user, user)) for user in users]
        sorted_users = sorted(user_scores, key=lambda x: x[1], reverse=True)
        return [user_score[0] for user_score in sorted_users]

    def get_sort_option(self, sort_by):
        sort_options = {
            'username_asc': lambda users: self.sort_by_username(users, ''),
            'username_desc': lambda users: self.sort_by_username(users, '-'),
            'age_asc': lambda users: self.sort_by_age(users, '-'),
            'age_desc': lambda users: self.sort_by_age(users, ''),
        }
        return sort_options.get(sort_by)

    def sort_users(self, users, current_user):
        """Sorts users based on the selected criterion."""
        
        cleaned_data = self.cleaned_data
        sort_by = cleaned_data.get('sort_by')
        sort_option = self.get_sort_option(sort_by)
        if sort_option:
            users = sort_option(users)
        elif sort_by == '' and current_user:
            users = self.sort_by_match_score(users, current_user)
        return users
    
    def calculate_match_score(self, current_user, other_user):
        """Calculates the score of each user in relation to the current user """

        score = 0
        
        score = self.calculate_user_type_score(current_user, other_user, score)
        score = self.calculate_age_score(current_user, other_user,score)
        weighting_user = {"gender": 0.2, "language": 0.9, "ethnicity": 0.2, "location": 1, "hospital": 1,}
        matches = {
            attribute: getattr(current_user, attribute, None) == getattr(other_user, attribute, None)
            for attribute in weighting_user}
        score += sum(weight for attribute, weight in weighting_user.items() if matches[attribute])
        return score

    def calculate_age_score(self, current_user, other_user, score):
        """Calclates score based on age proximity"""

        age_difference = abs(current_user.date_of_birth.year - other_user.date_of_birth.year)
        if age_difference <= 5:
            score += 1 * self.weighting_types['age']
        return score
    
    def calculate_user_type_score(self, current_user, other_user, score):
        """Calculates user type specific score."""
        
        if hasattr(current_user, 'patient') and hasattr(other_user, 'patient'):
            score += 1 * self.weighting_types['user_type']
            score += self.calculate_condition_match(current_user.patient, other_user.patient, self.get_key_value_pair('condition'), self.get_key_value_pair('age_of_diagnosis'))
        elif hasattr(current_user, 'parent') and hasattr(other_user, 'parent'):
            score += 1 * self.weighting_types['user_type']
            score += self.calculate_condition_match(current_user.parent, other_user.parent, self.get_key_value_pair('child_condition'), self.get_key_value_pair('child_age_of_diagnosis'))
        elif hasattr(current_user, 'mentor') and hasattr(other_user, 'patient'):
            score += 1 * self.weighting_types['user_type']
            score += self.calculate_condition_match(current_user.mentor, other_user.patient, self.get_key_value_pair('condition'), self.get_key_value_pair('age_of_diagnosis'))
        elif hasattr(current_user, 'professional') and hasattr(other_user, 'patient'):
            score += 1 * self.weighting_types['user_type']
            condition = self.get_key_value_pair('expertise')
            new_condition = (condition[0], 'condition', condition[2])
            score += self.calculate_condition_match(current_user.professional, other_user.patient, new_condition, None)
        return score
    
    def calculate_condition_match(self,user_type_1, user_type_2, condition, age_of_diagnosis):
        score=0
        condition_1 = getattr(user_type_1, condition[0], None) 
        condition_2 = getattr(user_type_2, condition[1], None)
        if condition_1 and condition_2 and (condition_1==condition_2):
            score += condition[2]
        if not age_of_diagnosis:
            return score
        age_of_diagnosis_1 = getattr(user_type_1, age_of_diagnosis[0], None)
        age_of_diagnosis_2 = getattr(user_type_2, age_of_diagnosis[1], None)
        if age_of_diagnosis_1 and age_of_diagnosis_2 and (abs(age_of_diagnosis_1 - age_of_diagnosis_2) < 5):
                score += age_of_diagnosis[2]
        return score

    def get_key_value_pair(self, key_value):
        value = self.weighting_types[key_value]
        return (key_value, key_value ,value)