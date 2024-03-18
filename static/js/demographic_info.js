var colours = ["#55efc4","#81ecec","#a29bfe","#ffeaa7","#fab1a0","#ff7675","#fd79a8"];

//Change the label colouring based on theme
document.getElementById('theme').addEventListener('click', function() {
    let label_colour = getThemeColors() === "#ffffff" ? "#000000" : "#ffffff";
    let ChartOptions = updateChartOptions(label_colour); 
    bar_chart.options = ChartOptions;
    bar_chart.update();
    pieChart.options = ChartOptions;
    pieChart.update();
});

function getThemeColors() {
    let storedTheme = localStorage.getItem("currentTheme"); 
    return storedTheme === "light-theme" ? "#000000" : "#ffffff"; 
}

function updateChartOptions(label_colour) {
    return {scales: {y: {beginAtZero: true,
                ticks: {color: label_colour, }},
            x: {ticks: { color: label_colour,},}},
        plugins: {legend: {labels: {color: label_colour
                }}, }};}
                
let label_colour = getThemeColors();
let ChartOptions = updateChartOptions(label_colour);

//Charts information
let user_type_data={
    labels:user_types_labels,
    datasets:[{
            label: "User Types",
            backgroundColor: colours,
            data: user_types_count}],
    title:"Types of users"
};

let user_ages_data ={
    labels:age_range_labels,
    datasets:[{
            label:"User Ages",
            backgroundColor:colours,
            data:age_range_counts
        }],
    title: "User Age Distribution"
};

let ethnicity_data = {
    labels: ethnicities, 
    datasets: [{
        label: "Ethnicity Distribution",
        backgroundColor: colours, 
        data: ethnicity_count
    }],
    title: "User Ethnicity among users"
};

let patient_condition_data = {
    labels: patient_condition_labels, 
    datasets: [{
        label: "Liver Disease Distribution",
        backgroundColor: colours,
        data: patient_condition_count 
    }],
    title: "Liver Disease among Users"
};

let parent_child_condition_data = {
    labels: parent_child_condition_labels, 
    datasets: [{
        label: "Liver Disease Distribution",
        backgroundColor: colours,
        data: parent_child_condition_count 
    }],
    title: "Liver Disease among Users"
};

let user_gender_data={
    labels:gender_labels,
    datasets:[{
            label: "Number of Users",
            backgroundColor: colours,
            data: gender_count
        }],
    title:"Genders among Users"
};

let user_location_data={
    labels:location_labels,
    datasets:[{
            label: "Number of Users",
            backgroundColor: colours,
            data: location_count
        }],
    title:"Genders among Users"
};

let user_location_south_america_data={
    labels:south_america_labels,
    datasets:[{
            label: "Number of Users",
            backgroundColor: colours,
            data: south_america_count
        }],
    title:"Users within South America"
};

let user_location_europe_data = {
    labels: europe_labels,
    datasets: [{
        label: "Number of Users",
        backgroundColor: colours,
        data: europe_count
    }],
    title: "Users within Europe"
};

let user_location_north_america_data = {
    labels: north_america_labels,
    datasets: [{
        label: "Number of Users",
        backgroundColor: colours,
        data: north_america_count
    }],
    title: "Users within North America"
};

let user_location_asia_data = {
    labels: asia_labels,
    datasets: [{
        label: "Number of Users",
        backgroundColor: colours,
        data: asia_count
    }],
    title: "Users within Asia"
};

let user_location_africa_data = {
    labels: africa_labels,
    datasets: [{
        label: "Number of Users",
        backgroundColor: colours,
        data: africa_count
    }],
    title: "Users within Africa"
};

let user_location_oceania_data = {
    labels: oceania_labels,
    datasets: [{
        label: "Number of Users",
        backgroundColor: colours,
        data: oceania_count
    }],
    title: "Users within Australia"
};

let user_location_antarctica_data = {
    labels: antarctica_labels,
    datasets: [{
        label: "Number of Users",
        backgroundColor: colours,
        data: antarctica_count
    }],
    title: "Users within Antarctica"
};

//Charts
let bar_chart_id = document.getElementById("barChart").getContext("2d");

let bar_chart = new Chart(bar_chart_id, {
    type: "bar",
    data: {labels: [], datasets: [{label: "", backgroundColor: [], borderColor: [], data: []}]},
    options: ChartOptions 
});


function update_bar_chart_data(selectedData) {
    bar_chart.data.labels =selectedData.labels;
    bar_chart.data.datasets[0].data=selectedData.datasets[0].data;
    bar_chart.data.datasets[0].label =selectedData.datasets[0].label;
    bar_chart.data.datasets[0].backgroundColor=selectedData.datasets[0].backgroundColor;
    bar_chart.data.datasets[0].borderColor= selectedData.datasets[0].borderColor;
    bar_chart.options.plugins.title.text=selectedData.title;
    bar_chart.update();
}

document.getElementById("continentSelectBar").addEventListener("change", function() {
    let selectedValue = this.value; 
    switch(selectedValue) {
        case "europe":
            update_bar_chart_data(user_location_europe_data);
            break;
        case "north_america":
            update_bar_chart_data(user_location_north_america_data);
            break;
        case "south_america":
            update_bar_chart_data(user_location_south_america_data);
            break;
        case "asia":
            update_bar_chart_data(user_location_asia_data);
            break;
        case "africa":
            update_bar_chart_data(user_location_africa_data);
            break;
        case "oceania":
            update_bar_chart_data(user_location_oceania_data);
            break;
        case "antarctica":
            update_bar_chart_data(user_location_antarctica_data);
            break;
        default:
            update_bar_chart_data(user_location_data);
    }
})

document.getElementById("barChartDataSelect").addEventListener("change", function() {
    let selectedValue = this.value; 
    switch(selectedValue) {
        case "user_age":
            update_bar_chart_data(user_ages_data);
            break;
        case "ethnicity":
            update_bar_chart_data(ethnicity_data);
            break;
        case "patient_condition":
            update_bar_chart_data(patient_condition_data);
            break;
        case "parent_child_condition":
            update_bar_chart_data(parent_child_condition_data);
            break;
        case "user_gender":
            update_bar_chart_data(user_gender_data);
            break;
        case "user_location":
            update_bar_chart_data(user_location_data);
            break;
        default:
            update_bar_chart_data(user_type_data);
    }
});
 
update_bar_chart_data(user_type_data);

let ctxPie = document.getElementById("ethnicityChart").getContext("2d");
let pieChart = new Chart(ctxPie, {
    type: "pie",
    data: {labels: [], datasets: [{label: "", backgroundColor: [], borderColor: [], data: []}]},
    options: ChartOptions 
});

function update_pie_chart_data(selectedData) {
    pieChart.data.labels = selectedData.labels;
    pieChart.data.datasets[0].data = selectedData.datasets[0].data;
    pieChart.data.datasets[0].backgroundColor = selectedData.datasets[0].backgroundColor;
    pieChart.options.plugins.title.text = selectedData.title;
    pieChart.update();
}

document.getElementById("continentSelectPie").addEventListener("change", function() {
    let selectedValue = this.value; 
    switch(selectedValue) {
        case "europe":
            update_pie_chart_data(user_location_europe_data);
            break;
        case "north_america":
            update_pie_chart_data(user_location_north_america_data);
            break;
        case "south_america":
            update_pie_chart_data(user_location_south_america_data);
            break;
        case "asia":
            update_pie_chart_data(user_location_asia_data);
            break;
        case "africa":
            update_pie_chart_data(user_location_africa_data);
            break;
        case "oceania":
            update_pie_chart_data(user_location_oceania_data);
            break;
        case "antarctica":
            update_pie_chart_data(user_location_antarctica_data);
            break;
        default:
            update_pie_chart_data(user_location_data);
    }
})


document.getElementById("pieChartDataSelect").addEventListener("change", function() {
    let selectedValue = this.value;
    switch(selectedValue) {
        case "user_age":
            update_pie_chart_data(user_ages_data);
            break;
        case "ethnicity":
            update_pie_chart_data(ethnicity_data);
            break;
        case "patient_condition":
            update_pie_chart_data(patient_condition_data);
            break;
        case "parent_child_condition":
            update_pie_chart_data(parent_child_condition_data);
            break;
        case "user_gender":
            update_pie_chart_data(user_gender_data);
            break;
        case "user_location":
            update_pie_chart_data(user_location_data);
            break;
        default:
            update_pie_chart_data(user_type_data);
    }
});

update_pie_chart_data(user_type_data);

//Loading continets
document.addEventListener('DOMContentLoaded', function () {
    var dataSelect = document.getElementById('barChartDataSelect');
    var continentSelect = document.getElementById('continentSelectBar');
    function toggleContinentDropdown() {
        if (dataSelect.value === "user_location") {
            continentSelect.style.display = 'block'; 
        } else {
            continentSelect.style.display = 'none'; 
        }
    }
    toggleContinentDropdown();
    dataSelect.addEventListener('change', toggleContinentDropdown);
});

document.addEventListener('DOMContentLoaded', function () {
    var dataSelect = document.getElementById('pieChartDataSelect');
    var continentSelect = document.getElementById('continentSelectPie');
    function toggleContinentDropdown() {
        if (dataSelect.value === "user_location") {
            continentSelect.style.display = 'block'; 
        } else {
            continentSelect.style.display = 'none'; 
        }
    }
    toggleContinentDropdown();
    dataSelect.addEventListener('change', toggleContinentDropdown);
});



