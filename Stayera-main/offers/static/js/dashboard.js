var xValues = ["Food", "House Rent ", "Educational fees", "Transportation", "Saving"];
var yValues = [30, 25, 20, 10, 15];
var barColors = [
  "#F9C80E",
  "#F86624",
  "#00F0B5",
  "#3777FF",
  "#FF0F80"
];

const piechart = document.getElementById('myChart').getContext('2d');

new Chart(piechart, {
  type: "doughnut",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
    responsive: true,
    plugins: {
        tooltip: {
            titleColor: 'white',   // Set tooltip title color
            bodyColor: 'white'   // Set tooltip body color
        },
        legend: {
            labels: {
                color: 'white' // Set legend label color
            }
        },
        datalabels: {
            color: 'white', // Set color of the segment labels if using chartjs-plugin-datalabels
            anchor: 'center',
            align: 'center',
            formatter: (value, context) => {
                return context.chart.data.labels[context.dataIndex] + ': ' + value; // Customize label text
            }
        }
    }
}
});


const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct", "Nov", "Dec"];


const line = document.getElementById('myLineChart').getContext('2d');
 new Chart(line, {
        type: 'line', // Specify the type of chart
        data: {
            labels: months,
            datasets: [{
                label: 'Food', // Name of the dataset
                data: [15000, 14500, 15000, 14000, 10000, 14200, 14000 , 15200 , 14100 , 13800 , 14520 , 15050 ,14860], // Y-axis data
                borderColor: "#F9C80E" , // Line color
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // Fill color
                borderWidth: 2, // Width of the line
                pointBackgroundColor: '#F9C80E', // Point color
                pointBorderColor: '#fff', // Point border color
                pointRadius: 5, // Point size
                },
                {
                  label: 'House Rent', // Name of the dataset
                  data: [10000 , 10000 , 10000 ,10000 , 11000 , 11000 ,11000, 12000 , 12000 , 12000 ,12900 , 12900 ,12900 ], // Y-axis data
                  borderColor: '#F86624', // Line color
                  backgroundColor: 'rgba(75, 192, 192, 0.2)', // Fill color
                  borderWidth: 2, // Width of the line
                  pointBackgroundColor: '#F86624', // Point color
                  pointBorderColor: '#fff', // Point border color
                  pointRadius: 5, // Point size
                },
                {
                  label: 'Educational Fees', // Name of the dataset
                  data: [7000,7200,7200,7700,7800,7950,7950,8000,8250,8400,8500,8500], // Y-axis data
                  borderColor: "#00F0B5", // Line color
                  backgroundColor: 'rgba(75, 192, 192, 0.2)', // Fill color
                  borderWidth: 2, // Width of the line
                  pointBackgroundColor: '#00F0B5', // Point color
                  pointBorderColor: '#fff', // Point border color
                  pointRadius: 5, // Point size
                },
                {
                  label: 'Transportation', // Name of the dataset
                  data: [3500 , 5100 , 3900 , 4200 , 2500 , 3300 , 4400 , 3950, 3570 , 4000, 3050 , 3700], // Y-axis data
                  borderColor:  "#3777FF", // Line color
                  backgroundColor: 'rgba(75, 192, 192, 0.2)', // Fill color
                  borderWidth: 2, // Width of the line
                  pointBackgroundColor: '#3777FF', // Point color
                  pointBorderColor: '#fff', // Point border color
                  pointRadius: 5, // Point size
                },
                {
                  label: 'Saving', // Name of the dataset
                  data: [6000 , 5700 , 6000 , 5900 , 6100 , 6020 ,3500 , 7000 , 4500 , 5000 , 4200 , 4350 ,], // Y-axis data
                  borderColor: "#FF0F80", // Line color
                  backgroundColor: 'rgba(75, 192, 192, 0.2)', // Fill color
                  borderWidth: 2, // Width of the line
                  pointBackgroundColor: '#FF0F80', // Point color
                  pointBorderColor: '#fff', // Point border color
                  pointRadius: 5, // Point size
                }]
        },
        options: {
            responsive: true, // Make the chart responsive
            scales: {
              x: {
                  ticks: {
                      color: 'white', // Change x-axis label color
                  },
                  grid: {
                      color: 'rgba(107,204,94,0.35)' // Change x-axis grid line color
                  }
              },
              y: {
                  ticks: {
                      color: 'white', // Change y-axis label color
                  },
                  grid: {
                      color: 'rgba(107,204,94,0.35)' // Change y-axis grid line color
                  }
              }
          },
            plugins: {
              legend: {
                  labels: {
                      color: '#fff', // Change legend label color
                      
                  },
                  
                  position: 'top', // Position of the legend
              },
                tooltip: {
                    mode: 'index', // Tooltip mode
                    intersect: false // Do not require intersection for tooltips
                }
            }
        }
    });