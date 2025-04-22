document.addEventListener("DOMContentLoaded", function () {
        console.log("EXTRATO carregado, tentando renderizar o gráfico...");
});



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
        numberOfColumns: 1,
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


//modal edição
document.addEventListener('click', function (event) {
    // Verifica se o evento foi disparado por um botão de edição
    if (event.target && event.target.classList.contains('edit-icon')) {
      const data = event.target.getAttribute('data-data');
      const categoria = event.target.getAttribute('data-categoria');
      const descricao = event.target.getAttribute('data-descricao');
      const valor = event.target.getAttribute('data-valor');
      
      const id = event.target.getAttribute('data-id');

    const dataFormatada = formatarDataManual(data);
    document.getElementById('editar-data').value = dataFormatada;
    

      document.getElementById('editar-categoria').value = categoria;
      document.getElementById('editar-descricao').value = descricao;
      document.getElementById('editar-valor').value = valor;
  
      document.getElementById('editar-id').value = id;

      const modal = document.getElementById('modal-editar');
      modal.style.display = 'block';
    }
  
    // Fechar o modal quando clicar no botão de fechar ou fora do modal
    const fecharModal = document.getElementById('fechar-modal');
    if (event.target === fecharModal) {
      const modal = document.getElementById('modal-editar');
      modal.style.display = 'none';
    }
  
    const modal = document.getElementById('modal-editar');
    if (event.target === modal) {
      modal.style.display = 'none';
    }


    //deletar
     // Clique no ícone de deletar
  
     if (event.target && event.target.classList.contains('fa-trash')) {
        const modal = document.getElementById('modal-confirmar-exclusao');
        const fecharModal = document.getElementById('fechar-modal-excluir');
        const confirmarBtn = document.getElementById('confirmar-exclusao');

        let idSelecionado = null;

        // Abre o modal ao clicar na lixeira
        
        idSelecionado = event.target.getAttribute('data-id');
        modal.style.display = 'block';
                
        //setar no campo id hidden o id para delecao
        document.getElementById('id-gasto-excluir').value = idSelecionado;


        // // Confirma exclusão
        // confirmarBtn.addEventListener('click', function () {
        //     if (idSelecionado) {
        //     fetch(`/deletar_gasto/${idSelecionado}`, {
        //         method: 'POST'
        //     })
        //     .then(res => {
        //         if (res.ok) {
        //         window.location.reload(); // Atualiza a página
        //         } else {
        //         alert("Erro ao excluir gasto.");
        //         }
        //     });
        //     }
        // });

     }
  });
  

  function formatarDataManual(dataBr) {
    const partes = dataBr.split('/');
    if (partes.length === 3) {
      const [dia, mes, ano] = partes;
      return `${ano}-${mes.padStart(2, '0')}-${dia.padStart(2, '0')}`;
    }
    return '';
  }
  



  //modal delecao

  let idParaExcluir = null;

