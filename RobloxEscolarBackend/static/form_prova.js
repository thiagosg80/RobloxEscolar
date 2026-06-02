document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('containerQuestoes');
    if (!container) return;

    for(let i = 1; i <= 10; i++) {
        container.innerHTML += `
          <div class="q-box">
            <h3 class="section-heading" style="margin-top:0;">Questão ${i}</h3>
            <input type="text" class="enunciado" placeholder="Enunciado da questão..." required style="width:100%; box-sizing:border-box; margin-bottom:16px;">
            <div class="alternativas-inputs">
               ${['A','B','C','D','E'].map((l, idx) => `
                 <div class="alt-row" style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                   <input type="radio" name="c_${i}" value="${idx}" required> 
                   <input type="text" class="alt-text" placeholder="Opção ${l}" style="flex:1; padding: 12px; border: 1px solid var(--border); border-radius: var(--radius-sm);">
                 </div>
               `).join('')}
            </div>
          </div>`;
    }

    // 2. Preencher com dados se for Edição (lê do data-prova)
    const divDados = document.getElementById('dados-edicao');
    if (divDados) {
        const prova = JSON.parse(divDados.dataset.prova);
        // Preenche o nome
        document.getElementById('nomeProva').value = prova.nome_prova;
        
        // Preenche cada questão
        document.querySelectorAll('.q-box').forEach((box, index) => {
            const q = prova.questoes[index];
            box.querySelector('.enunciado').value = q.enunciado;
            
            // Preenche alternativas
            box.querySelectorAll('.alt-text').forEach((inp, idx) => {
                inp.value = q.alternativas[idx];
            });
            
            // Seleciona a correta
            box.querySelectorAll('input[type="radio"]')[q.correta].checked = true;
        });
    }

    // 3. Enviar formulário
    document.getElementById('formProva').onsubmit = async (e) => {
        e.preventDefault();
        const questoes = Array.from(document.querySelectorAll('.q-box')).map(box => ({
            enunciado: box.querySelector('.enunciado').value,
            alternativas: Array.from(box.querySelectorAll('.alt-text')).map(i => i.value),
            correta: parseInt(box.querySelector('input[type="radio"]:checked').value)
        }));
        
        await fetch('/prova/criar', { 
            method: 'POST', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ nome_prova: document.getElementById('nomeProva').value, questoes })
        });
        window.location.href = '/trials/show-all';
    };
});