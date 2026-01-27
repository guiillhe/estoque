document.addEventListener('DOMContentLoaded', function() {
    
    const formsetContainer = document.getElementById('formset-container');
    const addMoreButton = document.getElementById('add-more');
    
    // Encontrar o management_form dinamicamente
    const totalForms = document.querySelector('[name$="TOTAL_FORMS"]');
    
    if (!formsetContainer || !addMoreButton || !totalForms) {
        console.warn('Elementos do formset não encontrados');
        return;
    }
    
    // Obter o prefixo do formset (orderitem_set, items, etc)
    const formsetPrefix = totalForms.name.split('-')[0];
    
    // Função para obter o número do formulário a partir do nome do campo
    function getFormIndex(name) {
        const match = name.match(new RegExp(`${formsetPrefix}-(\\d+)-`));
        return match ? parseInt(match[1]) : -1;
    }
    
    // Função para atualizar índices dos campos
    function updateFormIndices() {
        const formRows = formsetContainer.querySelectorAll('.formset-row');
        formRows.forEach((row, index) => {
            row.querySelectorAll('input, select, textarea').forEach(field => {
                if (field.name) {
                    field.name = field.name.replace(new RegExp(`${formsetPrefix}-\\d+`), `${formsetPrefix}-${index}`);
                    if (field.id) {
                        field.id = field.id.replace(new RegExp(`id_${formsetPrefix}_\\d+`), `id_${formsetPrefix}_${index}`);
                    }
                }
            });
            // Atualizar labels
            row.querySelectorAll('label').forEach(label => {
                if (label.htmlFor) {
                    label.htmlFor = label.htmlFor.replace(new RegExp(`id_${formsetPrefix}_\\d+`), `id_${formsetPrefix}_${index}`);
                }
            });
        });
        totalForms.value = formRows.length;
    }
    
    // Adicionar nova linha
    addMoreButton.addEventListener('click', function() {        
        const formRows = formsetContainer.querySelectorAll('.formset-row');
        if (formRows.length > 0) {
            const lastRow = formRows[formRows.length - 1];
            const newRow = lastRow.cloneNode(true);
            
            // Limpar valores dos campos
            newRow.querySelectorAll('input, select, textarea').forEach(field => {
                if (field.type !== 'hidden') {
                    field.value = '';
                }
                // Limpar erros
                field.classList.remove('is-invalid');
            });
            
            // Remover mensagens de erro
            newRow.querySelectorAll('.text-danger').forEach(error => {
                error.remove();
            });
            
            // Garantir que o botão de remover existe e fica visível
            let removeButton = newRow.querySelector('.remove-form-row');
            if (!removeButton) {
                // Se não existe, criar o botão
                const buttonCol = newRow.querySelector('.col-md-2');
                if (buttonCol) {
                    const btn = document.createElement('button');
                    btn.type = 'button';
                    btn.className = 'btn btn-outline-danger btn-sm remove-form-row';
                    btn.innerHTML = '<i class="bi bi-dash-circle"></i> Remover';
                    buttonCol.innerHTML = '';
                    buttonCol.appendChild(btn);
                }
            } else {
                removeButton.style.display = 'block';
            }
            
            formsetContainer.appendChild(newRow);
            updateFormIndices();
        }
    });
    
    // Remover linha (usando delegação de eventos)
    formsetContainer.addEventListener('click', function(e) {
        if (e.target.closest('.remove-form-row')) {
            const formRows = formsetContainer.querySelectorAll('.formset-row');
            if (formRows.length > 1) { // Manter pelo menos 1 linha
                e.target.closest('.formset-row').remove();
                updateFormIndices();
            }
        }
    });
    
    // Inicializar índices
    updateFormIndices();
});