// cart-complete-fixed.js - SISTEMA COMPLETO FUNCIONAL
class CartManager {
    constructor() {
        this.initialized = false;
    }
    
    init() {
        if (this.initialized) return;
        
        console.log('🚀 Inicializando CartManager Completo...');
        this.bindAddToCartButtons();
        this.bindCartUpdateEvents();
        this.initialized = true;
    }
    
    bindAddToCartButtons() {
        // Botones de agregar al carrito
        document.querySelectorAll('.add-to-cart-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.handleAddToCart(e, button);
            });
        });
        
        // Botón de detalle de producto
        document.querySelectorAll('.add-to-cart-btn-detail').forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.handleAddToCartDetail(e, button);
            });
        });
    }
    
    bindCartUpdateEvents() {
        const quantityForms = document.querySelectorAll('.quantity-form');
        if (!quantityForms.length) return;
        
        console.log('🛒 Inicializando eventos del carrito...');
        
        // Botones de cantidad en el carrito
        document.querySelectorAll('.quantity-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                
                const action = button.dataset.action;
                const input = button.closest('.input-group').querySelector('.quantity-input');
                const form = button.closest('.quantity-form');
                
                if (!input || !form) return;
                
                let currentValue = parseInt(input.value);
                const max = parseInt(input.max) || 999;
                const min = parseInt(input.min) || 1;
                
                if (action === 'increase' && currentValue < max) {
                    input.value = currentValue + 1;
                } else if (action === 'decrease' && currentValue > min) {
                    input.value = currentValue - 1;
                } else {
                    return;
                }
                
                console.log('📤 Enviando formulario con cantidad:', input.value);
                form.submit();
            });
        });
        
        // Inputs directos
        document.querySelectorAll('.quantity-input').forEach(input => {
            input.addEventListener('change', function() {
                const form = this.closest('.quantity-form');
                if (form) {
                    console.log('📤 Enviando formulario con cambio manual:', this.value);
                    form.submit();
                }
            });
        });
    }
    
    handleAddToCart(e, button) {
        const productId = button.dataset.productId;
        console.log(`🛒 Click en agregar producto ID: ${productId}`);
        
        if (!productId) {
            console.error('❌ No se encontró product-id');
            this.showErrorState(button, button.innerHTML, 'Error: ID de producto no válido');
            return;
        }
        
        this.addProductToCart(productId, 1, button);
    }
    
    handleAddToCartDetail(e, button) {
        const productId = button.dataset.productId;
        const quantityInput = document.getElementById('quantity');
        const quantity = quantityInput ? parseInt(quantityInput.value) : 1;
        
        console.log(`🛒 Click en agregar producto detalle - ID: ${productId}, Cantidad: ${quantity}`);
        
        if (!productId) {
            console.error('❌ No se encontró product-id');
            this.showErrorState(button, button.innerHTML, 'Error: ID de producto no válido');
            return;
        }
        
        this.addProductToCart(productId, quantity, button);
    }
    
    addProductToCart(productId, quantity, button) {
        const originalText = button.innerHTML;
        
        // Validar cantidad
        if (quantity < 1) {
            this.showErrorState(button, originalText, 'La cantidad debe ser al menos 1');
            return;
        }
        
        this.showLoadingState(button);
        
        console.log(`📤 Enviando AJAX - Producto: ${productId}, Cantidad: ${quantity}`);
        
        // URL CORREGIDA - sin template string
        const url = `/carrito/agregar/${productId}/`;
        console.log(`🔗 URL: ${url}`);
        
        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': this.getCookie('csrftoken'),
            },
            body: new URLSearchParams({
                'quantity': quantity.toString(),
                'csrfmiddlewaretoken': this.getCookie('csrftoken')
            })
        })
        .then(response => {
            console.log(`📥 Respuesta recibida: ${response.status}`);
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('📊 Datos recibidos:', data);
            if (data.success) {
                this.showSuccessState(button, originalText, data);
            } else {
                this.showErrorState(button, originalText, data.message);
            }
        })
        .catch(error => {
            console.error('❌ Error en la petición:', error);
            this.showErrorState(button, originalText, 'Error de conexión. Intenta nuevamente.');
        });
    }
    
    showLoadingState(button) {
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Agregando...';
        button.disabled = true;
        button.classList.add('btn-loading');
    }
    
    showSuccessState(button, originalText, data) {
        console.log('✅ Producto agregado exitosamente');
        this.showToast(data.message, 'success');
        this.updateCartCounter(data.cart_total_items);
        
        button.innerHTML = '<i class="fas fa-check me-2"></i>¡Agregado!';
        button.classList.remove('btn-loading');
        button.classList.add('btn-success');
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
            button.classList.remove('btn-success');
        }, 2000);
    }
    
    showErrorState(button, originalText, message) {
        console.error('❌ Error:', message);
        button.innerHTML = originalText;
        button.disabled = false;
        button.classList.remove('btn-loading');
        this.showToast(message, 'error');
    }
    
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    showToast(message, type = 'info') {
        // Toast mejorado
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        
        const icon = type === 'success' ? 'check-circle' : 
                    type === 'error' ? 'exclamation-triangle' : 'info-circle';
        
        toast.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${icon} me-2"></i>
                <span class="flex-grow-1">${message}</span>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 4000);
    }
    
    updateCartCounter(count) {
        const cartBadge = document.querySelector('.cart-badge');
        if (cartBadge) {
            cartBadge.textContent = count;
            // Efecto de animación
            cartBadge.style.transform = 'scale(1.3)';
            setTimeout(() => {
                cartBadge.style.transform = 'scale(1)';
            }, 300);
        }
    }
}

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Iniciando CartManager Completo...');
    window.cartManager = new CartManager();
    window.cartManager.init();
});