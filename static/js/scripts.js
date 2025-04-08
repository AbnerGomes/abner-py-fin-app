var donutChart = null; // Variável global inicializada

// Função para buscar e atualizar os dados do gráfico
function filtrarGastos(periodo) {
    var ctx = document.getElementById('donutChart').getContext('2d');

    $.getJSON(`/filtrarGastos/${periodo}`, function(dados) {

            
            const mensagem = document.getElementById("mensagem");

            const total = document.getElementById("total");

            if (dados.length === 0 || dados === null || dados === undefined ) {
                mensagem.innerHTML = "Nenhum gasto encontrado para esse período.";
                mensagem.style.display = "block"; // Exibe a mensagem
                // atualizarGrafico([], []); // Limpa o gráfico    
                total.style.display = "none"
            }
            else {
                console.log(periodo)
                console.log(dados)
                console.log('cai aqui')
                total.style.display = "block";
                mensagem.style.display = "none";
                let categorias = dados.map(item => item.categoria);
                let valores = dados.map(item => item.valor);
                
                donutChart.data.labels = categorias;
                donutChart.data.datasets[0].data = valores;
                donutChart.update();
                //drawDonutChart(dados);

                    // Calcula e mostra o total
                let totalGasto = valores.reduce((acc, val) => acc + parseFloat(val || 0), 0);
                let totalFormatado = totalGasto.toLocaleString('pt-BR', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                });
                document.getElementById("valor-total").innerText = totalFormatado;
            }    
            });

}



 document.addEventListener("DOMContentLoaded", function () {
    //document.getElementById('total').style.display='none'
    
filtrarGastos('mesatual');
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
            labels: ['Alimentação', 'Entretenimento','Mobilidade','Saúde','Moradia','Outros','Dívidas'],
            datasets: [{
                data: [0, 0,0,0,0,0],
                backgroundColor: ['#663399', '#0000FF','#00FA9A', '#DC143C','#FFFF00','#8B4513','#f59518']
            }]
        }
    });
 });


window.onload = function () {
    console.log("window.onload foi chamado!");
    console.log(document.getElementById("donutChart").getContext('2d'));
};



// data atual ja carregada no cadastro de gasto
document.addEventListener("DOMContentLoaded", function() {
    let hoje = new Date().toISOString().split('T')[0];
    let campoData = document.getElementById("data");
    if (campoData) {
        campoData.value = hoje;
    }
});