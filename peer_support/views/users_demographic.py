from django.shortcuts import render
from peer_support.models import Mentor,Parent,Patient,User
from .helpers import get_user_ethnicities,get_age_ranges,get_patient_conditions

def user_demographic(request):
    num_patients = Patient.objects.count()
    num_parents = Parent.objects.count()
    num_mentors = Mentor.objects.count()
    ethnicities = get_user_ethnicities()
    conditions = get_patient_conditions()
    age_ranges = get_age_ranges()
    context = {
        'num_patients': num_patients,
        'num_parents': num_parents,
        'num_mentors': num_mentors,
        'ethnicities': list(ethnicities.keys()),
        'ethnicity_count': list(ethnicities.values()),
        'age_range_labels': list(age_ranges.keys()), 
        'age_range_counts': list(age_ranges.values()),
        'condition_labels': list(conditions.keys()), 
        'condition_count' :list(conditions.values()),
    }
    return render(request, 'chart.html', context)

