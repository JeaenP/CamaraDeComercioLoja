
document.addEventListener('DOMContentLoaded', function() {
  const coloresSocios = [
      'rgba(23, 107, 160, 0.6)',   
      'rgba(25, 170, 222, 0.6)',    
      'rgba(26, 201, 230, 0.6)',  
      'rgba(27, 212, 212, 0.6)',   
  ];

var oroSocios75AniosCtx = document.getElementById('oroSocios75AniosChart').getContext('2d');
var oroSocios75AniosChart = new Chart(oroSocios75AniosCtx, {
  type: 'doughnut',
  data: {
      labels: ['Socios Oro con 75 Años', 'Otros Socios Oro'],
      datasets: [{
          data: dataoroSocios75Anios,
          backgroundColor: coloresSocios,
          borderColor: coloresSocios.map(color => color.replace('0.6', '1')),
          borderWidth: 1
      }]
  },
  options: {
      responsive: true,
      maintainAspectRatio: false,  
      plugins: {
          legend: {
              position: 'top',
              align: 'start'
          },
          title: {
              display: true,
              text: 'Proporción de Socios Oro con 75 Años'
          }
      }
  }
});

  var sociosPorTipoCtx = document.getElementById('sociosPorTipoChart').getContext('2d');
  var sociosPorTipoChart = new Chart(sociosPorTipoCtx, {
      type: 'bar',
      data: {
          labels: tiposSocios,
          datasets: [{
              label: 'Cantidad de Socios',
              data: cantidadSocios,
              backgroundColor: coloresSocios,
              borderColor: coloresSocios.map(color => color.replace('0.6', '1')),
              borderWidth: 2,
              borderRadius: 5,
              borderSkipped: false,
          }]
      },
      options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: true,  
          plugins: {
              legend: {
                  display: true,
                  
                 
                  labels: {
                      usePointStyle: true,
                      generateLabels: function(chart) {
                          var data = chart.data;
                          if (data.labels.length && data.datasets.length) {
                              return data.labels.map(function(label, index) {
                                  var dataset = data.datasets[0];
                                  var pointStyle = 'rect';
                                  return {
                                      text: label,
                                      fillStyle: dataset.backgroundColor[index],
                                      strokeStyle: dataset.borderColor[index],
                                      lineWidth: dataset.borderWidth,
                                      pointStyle: pointStyle,
                                      hidden: false,
                                      datasetIndex: 0,
                                      index: index,
                                  };
                              });
                          }
                          return [];
                      },
                  },
                  
              },
              title: {
                  display: true,
                  text: 'SOCIOS POR TIPO',
              },
          },
          scales: {
              y: {
                  ticks: {
                      display: false,
                  },
              },
          },
          
      },
  });


  var anios30aporteCtx = document.getElementById('anios30aporteChart').getContext('2d');
  var anios30aporteChart = new Chart(anios30aporteCtx, {
      type: 'bar',
      data: {
          labels: ['Cumplidos', 'Cumple este año', 'Cumple este mes'],
          datasets: [{
              data: [socios_30_anios_aporte_cumplidos, socios_30_anios_aporte_este_anio, socios_30_anios_aporte_este_mes],
              backgroundColor: coloresSocios,
              borderColor: coloresSocios.map(color => color.replace('0.6', '1')),
              borderWidth: 2,
              borderRadius: 5,
              borderSkipped: false,
          }]
      },
      options: {
          indexAxis: 'x',
          responsive: true,
          maintainAspectRatio: true,  
          plugins: {
              legend: {
                  display: true,
                  labels: {
                      usePointStyle: true,
                      generateLabels: function(chart) {
                          var data = chart.data;
                          if (data.labels.length && data.datasets.length) {
                              return data.labels.map(function(label, index) {
                                  var dataset = data.datasets[0];
                                  var pointStyle = 'rect';
                                  return {
                                      text: label,
                                      fillStyle: dataset.backgroundColor[index],
                                      strokeStyle: dataset.borderColor[index],
                                      lineWidth: dataset.borderWidth,
                                      pointStyle: pointStyle,
                                      hidden: false,
                                      datasetIndex: 0,
                                      index: index,
                                  };
                              });
                          }
                          return [];
                      },
                  },
                  
              },
              title: {
                  display: true,
                  text: '30 AÑOS DE APORTE',
              },
          },
          scales: {
              x: {
                  ticks: {
                      display: false,
                  },
              },
          },
          
      },
  });

  var sociosPorGeneroCtx = document.getElementById('sociosPorGeneroChart').getContext('2d');
  var sociosPorGeneroChart = new Chart(sociosPorGeneroCtx, {
      type: 'pie',
      data: {
          labels: generoSocios,
          datasets: [{
              label: 'Cantidad de Socios',
              data: cantidadSociosGenero,
              backgroundColor: coloresSocios,
              borderColor: coloresSocios.map(color => color.replace('0.6', '1')),
              borderWidth: 2,
              borderRadius: 5,
              borderSkipped: false,
          }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,  
        plugins: {
            legend: {
                position: 'top',
                align: 'start'
            },
            title: {
                display: true,
                text: 'Proporción de Socios Oro con 75 Años'
            }
        }
    }
  });

  var lineChartCtx = document.getElementById('lineChart').getContext('2d');
  var lineChart = new Chart(lineChartCtx, {
    type: 'line',
    data: {
        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        datasets: [{
            label: 'Pagos Mensuales',
            data: datosLineChart,
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            fill: false,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
});