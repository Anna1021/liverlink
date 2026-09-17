document.addEventListener('DOMContentLoaded', function () {    
    var timeframeDropdown = document.getElementById('notification_timeframe');
    var typeDropdown = document.getElementById('notification_type');

    timeframeDropdown.addEventListener('change', handleDropdownChange);
    typeDropdown.addEventListener('change', handleDropdownChange);

    function handleDropdownChange() {
        var selectedTimeframe = timeframeDropdown.value;
        var selectedType = typeDropdown.value;
        var url = window.location.pathname;

        var queryParams = [];
        if (selectedTimeframe !== "") {
            queryParams.push('timeframe=' + selectedTimeframe);
        }
        if (selectedType !== "") {
            queryParams.push('type=' + selectedType);
        }

        if (queryParams.length > 0) {
            url += '?' + queryParams.join('&');
        }

        window.location.href = url;
    }
});
