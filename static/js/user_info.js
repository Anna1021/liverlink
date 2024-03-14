var colours = ["#55efc4","#81ecec","#a29bfe","#ffeaa7","#fab1a0","#ff7675","#fd79a8"];

let user_type_data={
    labels:["Patients", "Parents", "Mentors"],
    datasets:[{
            label: "User Types",
            backgroundColor: colours,
            data: [num_patients, num_parents, num_mentors]}],
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

let bar_chart_id = document.getElementById("barChart").getContext("2d");

let bar_chart = new Chart(bar_chart_id, {
    type: "bar",
    data: {labels: [],datasets: [{label: "",backgroundColor: [],borderColor: [],data: []}]},
    options: {scales: {y: {beginAtZero: true}},
        plugins: {title:{display: true,text: ""}}}
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

document.getElementById("barChartDataSelect").addEventListener("change", function() {
    let selectedValue = this.value; 
    console.log("Mentor Condition Labels: 1")
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
        case "mentor_condition":
            console.log("Mentor Condition Labels: 2")
            console.log("Mentor Condition Labels:", mentor_condition_labels); // Debugging: Print labels
            console.log("Mentor Condition Count:", mentor_condition_count); // Debugging: Print counts
            
            let mentorConditionData = {
                labels: mentor_condition_labels,
                datasets: [{
                    label: "Mentor Conditions",
                    backgroundColor: colours,
                    data: mentor_condition_count
                }],
                title: "Mentor Condition Distribution"
            };
            update_bar_chart_data(mentorConditionData);
            break;
        default:
            update_bar_chart_data(user_type_data);
    }
});


update_bar_chart_data(user_type_data);

let ctxPie = document.getElementById("ethnicityChart").getContext("2d");
let pieChart = new Chart(ctxPie, {
    type: "pie",
    data: {labels: [],datasets: [{label: "",backgroundColor: [],borderColor: [],data: []}]},
    options: {scales: {y: {beginAtZero: true}},
        plugins: {title:{display: true,text: ""}}}
});

function update_pie_chart_data(selectedData) {
    pieChart.data.labels = selectedData.labels;
    pieChart.data.datasets[0].data = selectedData.datasets[0].data;
    pieChart.data.datasets[0].backgroundColor = selectedData.datasets[0].backgroundColor;
    pieChart.options.plugins.title.text = selectedData.title;
    pieChart.update();
}

document.getElementById("pieChartDataSelect").addEventListener("change", function() {
    let selectedValue = this.value;
    switch(selectedValue) {
        case "parent_child_condition":
            update_pie_chart_data(parent_child_condition_data);
            break;
        case "user_type":
            update_pie_chart_data(user_type_data);
            break;
        case "user_age":
            update_pie_chart_data(user_ages_data);
            break;
        case "user_gender":
            update_pie_chart_data(user_gender_data);
            break;
        case "user_location":
            update_pie_chart_data(user_location_data);
            break;
        case "mentor_condition":
            update_pie_chart_data({
                labels: mentor_condition_labels,
                datasets: [{
                    backgroundColor: colours.slice(0, mentor_condition_labels.length), // Ensure there are enough colors
                    data: mentor_condition_count
                }],
                title: "Mentor Condition Distribution"
            });
            break;
        default:
            update_pie_chart_data(patient_condition_data);
    }
});

update_pie_chart_data(ethnicity_data);


