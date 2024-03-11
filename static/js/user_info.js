var colours = ["#55efc4","#81ecec","#a29bfe","#ffeaa7","#fab1a0","#ff7675","#fd79a8"];
let barChartId = document.getElementById("barChart").getContext("2d");

let barChart = new Chart(barChartId, {
    type: "bar",
    data: {labels: [],datasets: [{label: "",backgroundColor: [],borderColor: [],data: []}]},
    options: {scales: {y: {beginAtZero: true}},
        plugins: {title:{display: true,text: ""}}}
});

let userTypesData={
    labels:["Patients", "Parents", "Mentors"],
    datasets:[{
            label: "Number of Users",
            backgroundColor: colours,
            data: [num_patients, num_parents, num_mentors]}],
    title:"User Demographics"
};

let userAgesData ={
    labels:age_range_labels,
    datasets:[{
            label:"Number of Users",
            backgroundColor:colours,
            data:age_range_counts
        }],
    title: "User Age Distribution"
};

function updateBarChartData(selectedData) {
    barChart.data.labels =selectedData.labels;
    barChart.data.datasets[0].data=selectedData.datasets[0].data;
    barChart.data.datasets[0].label =selectedData.datasets[0].label;
    barChart.data.datasets[0].backgroundColor=selectedData.datasets[0].backgroundColor;
    barChart.data.datasets[0].borderColor= selectedData.datasets[0].borderColor;
    barChart.options.plugins.title.text=selectedData.title;
    barChart.update();
}

document.getElementById("barChartDataSelect").addEventListener("change", function() {
    let selectedValue = this.value;
    if (selectedValue==="userTypes") {
        updateBarChartData(userTypesData);
    } else if (selectedValue==="userAges") {
        updateBarChartData(userAgesData);
    }
});

updateBarChartData(userTypesData);

let ctxPie = document.getElementById("ethnicityChart").getContext("2d");
let pieChart = new Chart(ctxPie, {
    type: "pie",
    data: {labels: [],datasets: [{label: "",backgroundColor: [],borderColor: [],data: []}]},
    options: {scales: {y: {beginAtZero: true}},
        plugins: {title:{display: true,text: ""}}}
});

let ethnicityData = {
    labels: ethnicities, 
    datasets: [{
        label: "Ethnicity Distribution",
        backgroundColor: colours, 
        data: ethnicity_count
    }],
    title: "User Ethnicity Distribution"
};

let liverDiseaseData = {
    labels: condition_labels, 
    datasets: [{
        label: "Liver Disease Distribution",
        backgroundColor: colours,
        data: condition_count 
    }],
    title: "Liver Disease Distribution among Users"
};

function updatePieChartData(selectedData) {
    pieChart.data.labels = selectedData.labels;
    pieChart.data.datasets[0].data = selectedData.datasets[0].data;
    pieChart.data.datasets[0].backgroundColor = selectedData.datasets[0].backgroundColor;
    pieChart.options.plugins.title.text = selectedData.title;
    pieChart.update();
}

document.getElementById("pieChartDataSelect").addEventListener("change", function() {
    let selectedValue = this.value;
    if (selectedValue === "ethnicity") {
        updatePieChartData(ethnicityData);
    } else if (selectedValue === "liverDisease") {
        updatePieChartData(liverDiseaseData);
    }
});

updatePieChartData(ethnicityData);


