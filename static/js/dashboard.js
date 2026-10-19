
// SPACE LAGOON DASHBOARD
// Actual analytics supplied by Flask + Apache Spark

Chart.defaults.color = "#BCE9DE";
Chart.defaults.font.family = "'Playfair Display', Georgia, serif";

const gridColor = "rgba(188, 233, 222, 0.12)";

const palette = [
    "#54B7BE",
    "#BCE9DE",
    "#216B78",
    "#A88BFA",
    "#F48FB1",
    "#73D7C0",
    "#F6C177",
    "#7DA7F7"
];


// 1. ACCIDENT SEVERITY

new Chart(document.getElementById("severityChart"), {
    type: "doughnut",

    data: {
        labels: dashboardData.severity.map(item => item.name),

        datasets: [{
            data: dashboardData.severity.map(item => item.count),
            backgroundColor: palette,
            borderColor: "#071923",
            borderWidth: 3,
            hoverOffset: 10
        }]
    },

    options: {
        responsive: true,
        maintainAspectRatio: false,

        plugins: {
            legend: {
                position: "bottom"
            }
        }
    }
});


// 2. STATE-WISE ANALYSIS

new Chart(document.getElementById("stateChart"), {
    type: "bar",

    data: {
        labels: dashboardData.states.map(item => item.name),

        datasets: [{
            label: "Total Accidents",
            data: dashboardData.states.map(item => item.count),
            backgroundColor: "#54B7BE",
            borderRadius: 7
        }]
    },

    options: {
        responsive: true,
        maintainAspectRatio: false,

        scales: {
            x: {
                ticks: { color: "#BCE9DE" },
                grid: { display: false }
            },

            y: {
                beginAtZero: true,
                ticks: { color: "#BCE9DE" },
                grid: { color: gridColor }
            }
        },

        plugins: {
            legend: { display: false }
        }
    }
});


// 3. WEATHER ANALYSIS

new Chart(document.getElementById("weatherChart"), {
    type: "pie",

    data: {
        labels: dashboardData.weather.map(item => item.name),

        datasets: [{
            data: dashboardData.weather.map(item => item.count),
            backgroundColor: palette,
            borderColor: "#071923",
            borderWidth: 3
        }]
    },

    options: {
        responsive: true,
        maintainAspectRatio: false,

        plugins: {
            legend: {
                position: "bottom"
            }
        }
    }
});


// 4. ACCIDENT HOTSPOTS

new Chart(document.getElementById("hotspotChart"), {
    type: "bar",

    data: {
        labels: dashboardData.hotspots.map(item => item.city),

        datasets: [{
            label: "Accidents",
            data: dashboardData.hotspots.map(item => item.count),
            backgroundColor: "#73D7C0",
            borderRadius: 7
        }]
    },

    options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,

        scales: {
            x: {
                beginAtZero: true,
                ticks: { color: "#BCE9DE" },
                grid: { color: gridColor }
            },

            y: {
                ticks: { color: "#BCE9DE" },
                grid: { display: false }
            }
        },

        plugins: {
            legend: { display: false }
        }
    }
});
