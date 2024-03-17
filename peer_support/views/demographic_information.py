from peer_support.models import Mentor,Parent,Patient
from .helpers import get_user_ethnicities, get_age_ranges, get_patient_conditions, get_genders, get_locations, get_parent_child_conditions, get_mentor_conditions
from django.contrib import messages
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required

@login_required
def demographic_information(request):
    """Displays demographic inforamtion for all users to staff"""

    current_user = request.user
    if not current_user.is_staff:
        messages.error(request, "You do not have access to this view.")
        return redirect(reverse('dashboard'))
    num_patients = Patient.objects.count()
    num_parents = Parent.objects.count()
    num_mentors = Mentor.objects.count()
    ethnicities = get_user_ethnicities()
    patient_conditions = get_patient_conditions()
    parent_child_conditions = get_parent_child_conditions()
    age_ranges = get_age_ranges()
    genders = get_genders()
    locations = get_locations()
    context = {
        'num_patients': num_patients,
        'num_parents': num_parents,
        'num_mentors': num_mentors,
        'ethnicities': list(ethnicities.keys()),
        'ethnicity_count': list(ethnicities.values()),
        'age_range_labels': list(age_ranges.keys()), 
        'age_range_counts': list(age_ranges.values()),
        'patient_condition_labels': list(patient_conditions.keys()), 
        'patient_condition_count' :list(patient_conditions.values()),
        'gender_labels': list(genders.keys()), 
        'gender_count' :list(genders.values()),
        'parent_child_condition_labels': list(parent_child_conditions.keys()), 
        'parent_child_condition_count' :list(parent_child_conditions.values()),
        'location_labels': list(locations.keys()), 
        'location_count' :list(locations.values()),
    }
    return render(request, 'demographic_information.html', context)

