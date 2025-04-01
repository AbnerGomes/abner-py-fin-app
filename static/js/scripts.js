// Função para desenhar o gráfico de donut
function drawDonutChart(dados) {
    var ctx = document.getElementById('donutChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: dados.map(item => item[0]), // Categorias
            datasets: [{
                label: 'Gastos',
                data: dados.map(item => item[1]), // Valores
                backgroundColor: ['#ffcc00', '#ff9900', '#ff6600', '#ff3300'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return tooltipItem.label + ': R$ ' + tooltipItem.raw.toFixed(2);
                        }
                    }
                }
            }
        });
}

// Carregar os dados do servidor
document.addEventListener('DOMContentLoaded', function() {
    var dados = {{ dados_grafico | tojson }};  // Recebe os dados do Flask
    drawDonutChart(dados);
});

