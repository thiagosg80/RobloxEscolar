/* ─────────────────────────────────────────────
   RobloxEscolarBackend — show_all.js
   Comportamentos interativos da página de resultados
───────────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', () => {
  animateProgressBars();
  bindCardToggles();
});

/**
 * Anima as barras de progresso após o carregamento da página.
 * Os valores reais ficam em data-acertos e data-total nos elementos.
 */
function animateProgressBars() {
  document.querySelectorAll('.progress-acertos').forEach(el => {
    const pct = parseFloat(el.dataset.pct ?? 0);
    setTimeout(() => { el.style.width = pct + '%'; }, 150);
  });

  document.querySelectorAll('.progress-erros').forEach(el => {
    const pct = parseFloat(el.dataset.pct ?? 0);
    setTimeout(() => { el.style.width = pct + '%'; }, 150);
  });
}

/**
 * Abre/fecha o painel de detalhes de cada card de aluno.
 * O clique pode vir do header inteiro ou do botão dedicado.
 */
function bindCardToggles() {
  document.querySelectorAll('.aluno-header').forEach(header => {
    header.addEventListener('click', () => {
      const card = header.closest('.aluno-card');
      card.classList.toggle('open');
    });
  });
}
