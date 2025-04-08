document.addEventListener("DOMContentLoaded", function () {
        console.log("EXTRATO carregado, tentando renderizar o gráfico...");
});


// const picker = new Litepicker({
//     element: document.getElementById('periodo-picker'),
//     singleMode: false, // MUITO IMPORTANTE: desativa modo "1 data só"
//     format: 'DD/MM/YYYY',
//     lang: 'pt-BR',
//     autoApply: true, // aplica automaticamente após escolher data final
//     numberOfMonths: 1,
//     numberOfColumns: 1,
//     setup: (picker) => {
//         picker.on('selected', (start, end) => {
//             // Define os valores ocultos para o formulário
//             document.getElementById('data_inicio').value = start.format('YYYY-MM-DD');
//             document.getElementById('data_fim').value = end.format('YYYY-MM-DD');
//         });

//     }
// });

const hoje = new Date();
const primeiroDiaMes = new Date(hoje.getFullYear(), hoje.getMonth(), 1);

const picker = new Litepicker({
    element: document.getElementById('periodo-picker'),
    singleMode: false,
    format: 'DD/MM/YYYY',
    lang: 'pt-BR',
    autoApply: true,
    numberOfMonths: 1,
    numberOfColumns: 1,
    startDate: primeiroDiaMes,
    endDate: hoje,
    setup: (picker) => {
        picker.on('selected', (start, end) => {
            document.getElementById('data_inicio').value = start.format('YYYY-MM-DD');
            document.getElementById('data_fim').value = end.format('YYYY-MM-DD');
        });

        document.addEventListener('click', function(event) {
            const target = event.target;
            if (!picker.ui.contains(target) && target !== document.getElementById('periodo-picker')) {
                picker.hide();
            }
        });
    }
});


   // Preenche os campos ocultos com os valores iniciais (1º dia até hoje)
   document.addEventListener('DOMContentLoaded', function () {
    const hoje = new Date();
    const primeiroDiaMes = new Date(hoje.getFullYear(), hoje.getMonth(), 1);

    const formatarData = (data) => {
        return data.toISOString().split('T')[0]; // yyyy-mm-dd
    };

    document.getElementById('data_inicio').value = formatarData(primeiroDiaMes);
    document.getElementById('data_fim').value = formatarData(hoje);

    // Atualiza o texto no botão do período
    const formatarVisual = (data) => {
        return ('0' + data.getDate()).slice(-2) + '/' + ('0' + (data.getMonth() + 1)).slice(-2) + '/' + data.getFullYear();
    };

    document.getElementById('periodo-picker').value = formatarVisual(primeiroDiaMes) + ' a ' + formatarVisual(hoje);
});