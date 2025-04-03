var donutChart = null; // Variável global inicializada


document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript carregado, tentando renderizar o gráfico...");
    
    var ctx = document.getElementById('donutChart');
    
    if (!ctx) {
        console.error("Erro: Elemento 'donutChart' não encontrado!");
        return;
    }

     // Verifica se o gráfico já existe e destrói antes de recriar
     if (donutChart) {
        donutChart.destroy();
        }

    donutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Alimentação', 'Entretenimento','Mobilidade','Saúde'],
            datasets: [{
                data: [50, 30,20,20],
                backgroundColor: ['#663399', '#0000FF','#00FA9A', '#DC143C']
            }]
        }
    });
});


window.onload = function () {
    console.log("window.onload foi chamado!");
    console.log(document.getElementById("donutChart").getContext('2d'));
};


// Função para buscar e atualizar os dados do gráfico
function filtrarGastos(periodo) {
        var ctx = document.getElementById('donutChart').getContext('2d');

        $.getJSON(`/filtrarGastos/${periodo}`, function(dados) {

                const mensagem = document.getElementById("mensagem");

                if (dados.length === 0) {
                    mensagem.innerHTML = "Nenhum gasto encontrado para esse período.";
                    mensagem.style.display = "block"; // Exibe a mensagem
                    // atualizarGrafico([], []); // Limpa o gráfico    
                }
                else {
                    mensagem.style.display = "none";
                    let categorias = dados.map(item => item.categoria);
                    let valores = dados.map(item => item.valor);
                    
                    donutChart.data.labels = categorias;
                    donutChart.data.datasets[0].data = valores;
                    donutChart.update();
                    //drawDonutChart(dados);
                }    
                });

}

