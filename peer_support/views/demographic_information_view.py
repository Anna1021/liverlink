from .helpers import  calculate_age, country_to_continent, country_to_continent_specific, map_blank_key
from peer_support.models import Mentor, Professional, User, Patient, Parent
from django.contrib import messages
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from collections import defaultdict
from collections import Counter

class DemographicInformationView(LoginRequiredMixin, View):
    """Displays demographic inforamtion for all users to staff"""

    def get(self, request):
        current_user = request.user
        if not current_user.is_staff:
            messages.error(request, "You do not have access to this view.")
            return redirect(reverse('feed'))
        context = {
            'user_types_labels': list(self.get_user_types().keys()),
            'user_types_count': list(self.get_user_types().values()),
            'ethnicities': list(self.get_user_ethnicities().keys()),
            'ethnicity_count': list(self.get_user_ethnicities().values()),
            'age_range_labels': list(self.get_age_ranges().keys()), 
            'age_range_counts': list(self.get_age_ranges().values()),
            'patient_condition_labels': list(self.get_patient_conditions().keys()), 
            'patient_condition_count' :list(self.get_patient_conditions().values()),
            'mentor_condition_labels': list(self.get_mentor_conditions().keys()), 
            'mentor_condition_count' :list(self.get_mentor_conditions().values()),
            'professional_expertise_labels': list(self.get_professional_expertise().keys()), 
            'professional_expertise_count' :list(self.get_professional_expertise().values()),
            'gender_labels': list(self.get_genders().keys()), 
            'gender_count' :list(self.get_genders().values()),
            'parent_child_condition_labels': list(self.get_parent_child_conditions().keys()), 
            'parent_child_condition_count' :list(self.get_parent_child_conditions().values()),
            'location_labels': list(self.get_locations().keys()), 
            'location_count' :list(self.get_locations().values()),
            'europe_labels': list(self.get_locations_specific().get("Europe", {}).keys()),
            'europe_count': list(self.get_locations_specific().get("Europe", {}).values()),
            'north_america_labels': list(self.get_locations_specific().get("North America", {}).keys()),
            'north_america_count': list(self.get_locations_specific().get("North America", {}).values()),
            'south_america_labels': list(self.get_locations_specific().get("South America", {}).keys()),
            'south_america_count': list(self.get_locations_specific().get("South America", {}).values()),
            'asia_labels': list(self.get_locations_specific().get("Asia", {}).keys()),
            'asia_count': list(self.get_locations_specific().get("Asia", {}).values()),
            'africa_labels': list(self.get_locations_specific().get("Africa", {}).keys()),
            'africa_count': list(self.get_locations_specific().get("Africa", {}).values()),
            'oceania_labels': list(self.get_locations_specific().get("Oceania", {}).keys()),
            'oceania_count': list(self.get_locations_specific().get("Oceania", {}).values()),
            'antarctica_labels': list(self.get_locations_specific().get("Antarctica", {}).keys()),
            'antarctica_count': list(self.get_locations_specific().get("Antarctica", {}).values())
        }
        return render(request, 'demographic_information.html', context)
    
    def get_professional_expertise(self):
        professional_expertise = Professional.objects.values_list('expertise', flat=True)
        professional_expertise = [map_blank_key(expertise) for expertise in professional_expertise]
        return Counter(professional_expertise) 
    
    def get_mentor_conditions(self):
        mentor_conditions = Mentor.objects.values_list('condition', flat=True)
        mentor_conditions = [map_blank_key(condition) for condition in mentor_conditions]
        return Counter(mentor_conditions) 
    
    def get_age_ranges(self):
        users_ages = [calculate_age(user.date_of_birth) for user in User.objects.all() if user.date_of_birth is not None]
        age_ranges = {"13-20": 0, "21-30": 0, "31-40": 0, "41-50": 0, "51-60": 0, "61-70": 0, "71+":0}
        for age in users_ages:
            if 13 <= age <= 20:
                age_ranges["13-20"]+=1
            elif 21 <= age <= 30:
                age_ranges["21-30"]+=1
            elif 31 <= age <= 40:
                age_ranges["31-40"]+=1
            elif 41 <= age <= 50:
                age_ranges["41-50"]+=1
            elif 51 <= age <= 60:
                age_ranges["51-60"]+=1
            elif 61 <= age <= 70:
                age_ranges["61-70"]+=1
            else:
                age_ranges["71+"]+=1
        return age_ranges

    def get_user_types(self):
        patients = Patient.objects.count()
        parents = Parent.objects.count()
        mentors = Mentor.objects.count()
        professionals = Professional.objects.count()
        return {'patients': patients,
            'parents': parents, 'mentors': mentors, 'professional': professionals}

    def get_user_ethnicities(self):
        users = User.objects.all()
        ethnicity_names = [user.ethnicity_name() for user in users]
        ethnicity_names = [map_blank_key(user.ethnicity_name()) for user in users]
        return Counter(ethnicity_names)

    def get_patient_conditions(self):
        patient_conditions = Patient.objects.values_list('condition', flat=True)
        patient_conditions = [map_blank_key(condition) for condition in patient_conditions]
        return Counter(patient_conditions) 

    def get_parent_child_conditions(self):
        parent_child_conditions = Parent.objects.values_list('child_condition', flat=True)
        parent_child_conditions = [map_blank_key(child_condition) for child_condition in parent_child_conditions]
        return Counter(parent_child_conditions) 

    def get_genders(self):
        genders = User.objects.values_list('gender', flat=True)
        genders = [map_blank_key(gender) for gender in genders]
        return Counter(genders) 

    def get_locations(self):
        """Returns set of all continets and number of users in each"""

        country_codes = User.objects.values_list('location', flat=True)
        continents = [country_to_continent(code) for code in country_codes if country_to_continent(code) is not None]
        return Counter(continents) 

    def get_locations_specific(self):
        """Returns set of all countries for each continent and number of users in each"""

        country_codes = User.objects.values_list('location', flat=True)
        continent_to_countries = defaultdict(list)
        for code in country_codes:
            continent, country = country_to_continent_specific(code)
            continent_to_countries[continent].append(country)
        continent_counts = {continent: Counter(countries) for continent, countries in continent_to_countries.items()}
        return(continent_counts)
