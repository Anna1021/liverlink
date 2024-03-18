from .helpers import get_user_ethnicities, get_age_ranges, get_patient_conditions, get_genders, get_locations, get_parent_child_conditions, get_locations_specific, get_user_types
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
    context = {
        'user_types_labels': list(get_user_types().keys()),
        'user_types_count': list(get_user_types().values()),
        'ethnicities': list(get_user_ethnicities().keys()),
        'ethnicity_count': list(get_user_ethnicities().values()),
        'age_range_labels': list(get_age_ranges().keys()), 
        'age_range_counts': list(get_age_ranges().values()),
        'patient_condition_labels': list(get_patient_conditions().keys()), 
        'patient_condition_count' :list(get_patient_conditions().values()),
        'gender_labels': list(get_genders().keys()), 
        'gender_count' :list(get_genders().values()),
        'parent_child_condition_labels': list(get_parent_child_conditions().keys()), 
        'parent_child_condition_count' :list(get_parent_child_conditions().values()),
        'location_labels': list(get_locations().keys()), 
        'location_count' :list(get_locations().values()),
        'europe_labels': list(get_locations_specific().get("Europe", {}).keys()),
        'europe_count': list(get_locations_specific().get("Europe", {}).values()),
        'north_america_labels': list(get_locations_specific().get("North America", {}).keys()),
        'north_america_count': list(get_locations_specific().get("North America", {}).values()),
        'south_america_labels': list(get_locations_specific().get("South America", {}).keys()),
        'south_america_count': list(get_locations_specific().get("South America", {}).values()),
        'asia_labels': list(get_locations_specific().get("Asia", {}).keys()),
        'asia_count': list(get_locations_specific().get("Asia", {}).values()),
        'africa_labels': list(get_locations_specific().get("Africa", {}).keys()),
        'africa_count': list(get_locations_specific().get("Africa", {}).values()),
        'oceania_labels': list(get_locations_specific().get("Oceania", {}).keys()),
        'oceania_count': list(get_locations_specific().get("Oceania", {}).values()),
        'antarctica_labels': list(get_locations_specific().get("Antarctica", {}).keys()),
        'antarctica_count': list(get_locations_specific().get("Antarctica", {}).values()),
    }
    return render(request, 'demographic_information.html', context)

