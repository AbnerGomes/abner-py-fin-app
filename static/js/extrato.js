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

// const hoje = new Date();
// const primeiroDiaMes = new Date(hoje.getFullYear(), hoje.getMonth(), 1);


// Pega os valores do input oculto vindo do backend
// const dataInicioInput = document.querySelector('input[name="data_inicio"]').value;
// const dataFimInput = document.querySelector('input[name="data_fim"]').value;

// const parseData = (str) => {
//     const [ano, mes, dia] = str.split('-');
//     return new Date(ano, mes - 1, dia);
// };

// const dataInicio = dataInicioInput ? parseData(dataInicioInput) : new Date(new Date().getFullYear(), new Date().getMonth(), 1);
// const dataFim = dataFimInput ? parseData(dataFimInput) : new Date();


// // Pega as datas do formulário (em formato yyyy-mm-dd)
// const dataInicioInput = document.getElementById('data_inicio').value;
// const dataFimInput = document.getElementById('data_fim').value;

// // Converte para objeto Date
// const startDate = new Date(dataInicioInput);
// const endDate = new Date(dataFimInput);




// const picker = new Litepicker({
//     element: document.getElementById('periodo-picker'),
//     singleMode: false,
//     format: 'DD/MM/YYYY',
//     lang: 'pt-BR',
//     autoApply: true,
//     numberOfMonths: 1,
//     numberOfColumns: 1,
//     startDate: startDate,
//     endDate: endDate,
//     setup: (picker) => {
//         picker.on('selected', (start, end) => {
//             document.getElementById('data_inicio').value = start.format('YYYY-MM-DD');
//             document.getElementById('data_fim').value = end.format('YYYY-MM-DD');
//         });

//         // document.addEventListener('click', function(event) {
//         //     const target = event.target;
//         //     if (!picker.ui.contains(target) && target !== document.getElementById('periodo-picker')) {
//         //         picker.hide();
//         //     }
//         // });
//     }
// });


//    //Preenche os campos ocultos com os valores iniciais (1º dia até hoje)
//    document.addEventListener('DOMContentLoaded', function () {
//     // const hoje = new Date();
//     // const primeiroDiaMes = new Date(hoje.getFullYear(), hoje.getMonth(), 1);

//     const hoje = new Date(dataFimInput);
//     const primeiroDiaMes = new Date(dataInicioInput);


//     const formatarData = (data) => {
//         return data.toISOString().split('T')[0]; // yyyy-mm-dd
//     };

//     document.getElementById('data_inicio').value = formatarData(primeiroDiaMes);
//     document.getElementById('data_fim').value = formatarData(hoje);

//     // Atualiza o texto no botão do período
//     const formatarVisual = (data) => {
//         return ('0' + data.getDate()).slice(-2) + '/' + ('0' + (data.getMonth() + 1)).slice(-2) + '/' + data.getFullYear();
//     };

//     // document.getElementById('periodo-picker').value = formatarVisual(primeiroDiaMes) + ' a ' + formatarVisual(hoje);
//     document.getElementById('periodo-picker').value = formatarVisual(dataInicio) + ' a ' + formatarVisual(dataFim);

// });



document.addEventListener('DOMContentLoaded', function () {
    // Pega as datas do formulário
    const dataInicioStr = document.getElementById('data_inicio')?.value;
    const dataFimStr = document.getElementById('data_fim')?.value;

    // Se vierem vazias, usa primeiro dia do mês até hoje
    const hoje = new Date();
    const primeiroDiaMes = new Date(hoje.getFullYear(), hoje.getMonth(), 1);

    // Converte para datas no fuso local (sem subtrair 1 dia)
    const parseDate = (str) => {
        if (!str) return null;
        const parts = str.split('-'); // "YYYY-MM-DD"
        return new Date(parts[0], parts[1] - 1, parts[2]); // mês começa em 0
    };

    const startDate = parseDate(dataInicioStr) || primeiroDiaMes;
    const endDate = parseDate(dataFimStr) || hoje;

    // Atualiza visualmente o texto no botão
    const pickerInput = document.getElementById('periodo-picker');
    pickerInput.textContent = `${startDate.toLocaleDateString()} até ${endDate.toLocaleDateString()}`;

    // Inicializa o picker
    const picker = new Litepicker({
        element: pickerInput,
        singleMode: false,
        numberOfMonths: 1,
        numberOfColumns: 2,
        format: "DD/MM/YYYY",
        lang: "pt-BR",
        startDate: startDate,
        endDate: endDate,
        autoApply: true,
        setup: (picker) => {
            picker.on('selected', (startDate, endDate) => {
                document.querySelector('input[name="data_inicio"]').value = startDate.format('YYYY-MM-DD');
                document.querySelector('input[name="data_fim"]').value = endDate.format('YYYY-MM-DD');
                pickerInput.textContent = `${startDate.format('DD/MM/YYYY')} até ${endDate.format('DD/MM/YYYY')}`;
            });
        }
    });
});
