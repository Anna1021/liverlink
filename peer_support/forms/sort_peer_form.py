from django import forms

class SortPeerForm(forms.Form):
    """Form enabling the sorting of users"""
    ALL_CHOICE = [('', 'None')]
    Username = forms.ChoiceField(choices=ALL_CHOICE+[('asc', 'Ascending'), ('desc', 'Descending')], required=False, label="Username")
    Age = forms.ChoiceField(choices=ALL_CHOICE+[('asc', 'Ascending'), ('desc', 'Descending')], required=False, label="Age")

    def clean(self):
        cleaned_data = super().clean()
        username_order = cleaned_data.get('Username')
        age_order = cleaned_data.get('Age')

        if username_order and age_order:
            self.add_error(None, 'Please choose only one sorting criterion: either Username or Age.')
        elif username_order == '' and age_order == '':
            pass
        return cleaned_data

    def sort_users(self, users):
        """Sorts users based on the selected criterion."""
        cleaned_data = self.cleaned_data 
        username_order = cleaned_data.get('Username')
        age_order = cleaned_data.get('Age')

        if username_order == 'asc':
            users = users.order_by('username')
        elif username_order == 'desc':
            users = users.order_by('-username')
        elif age_order == 'asc':
            users = users.order_by('-date_of_birth')
        elif age_order == 'desc':
            users = users.order_by('date_of_birth')

        return users
