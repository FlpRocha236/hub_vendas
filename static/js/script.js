/* ARQUIVO: static/js/script.js */

function toggleAdminModal() {
    const modal = document.getElementById('adminModal');
    const backdrop = document.getElementById('modalBackdrop');
    const content = document.getElementById('modalContent');
    
    if (modal.classList.contains('hidden')) {
        // ABRIR
        modal.classList.remove('hidden');
        
        // Pequeno delay para permitir que o navegador renderize antes da animação CSS
        setTimeout(() => {
            modal.classList.add('modal-open');
        }, 10);
    } else {
        // FECHAR
        modal.classList.remove('modal-open');
        
        // Espera a animação (300ms) terminar antes de esconder o elemento
        setTimeout(() => {
            modal.classList.add('hidden');
        }, 300);
    }
}