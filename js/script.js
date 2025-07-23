// Frontend/js/script.js - Enhanced version with API integration
// Variáveis globais
let cart = [];
let modalQt = 1;
let modalKey = 0;
let doceJson = []; // Will be populated from API
let useAPI = true; // Flag to toggle between API and local data

// Check if API is available
async function checkAPIAvailability() {
    try {
        const response = await api.getProducts();
        return response.success;
    } catch (error) {
        console.warn('API not available, using local data');
        return false;
    }
}

// Load products from API or fallback to local data
async function loadProductsData() {
    if (useAPI) {
        const isAPIAvailable = await checkAPIAvailability();
        
        if (isAPIAvailable) {
            const response = await api.getProducts();
            if (response.success) {
                doceJson = api.transformProductData(response.data);
                console.log('Products loaded from API');
                return;
            }
        }
    }
    
    // Fallback to local data
    doceJson = doceData; // From doce.js
    console.log('Using local product data');
}

// Extrair categorias únicas dos produtos
function getCategorias() {
    return [...new Set(doceJson.map(doce => doce.category).filter(cat => cat))];
}

// Criar botões de filtro dinamicamente
function criarBotoesFiltro() {
    const categorias = getCategorias();
    const containerFiltros = document.querySelector('.categories');
    containerFiltros.innerHTML = ''; // Limpa botões existentes
    
    // Adiciona botão "Todos"
    const botaoTodos = document.createElement("button");
    botaoTodos.className = "category-btn active";
    botaoTodos.textContent = "Todos";
    botaoTodos.setAttribute('data-category', 'todos');
    botaoTodos.addEventListener("click", () => {
        filtrarPorCategoria('todos');
        atualizarBotaoAtivo(botaoTodos);
    });
    containerFiltros.appendChild(botaoTodos);
    
    // Adiciona botão para cada categoria
    categorias.forEach(categoria => {
        const botao = document.createElement("button");
        botao.className = "category-btn";
        botao.textContent = formatarNomeCategoria(categoria);
        botao.setAttribute('data-category', categoria);
        botao.addEventListener("click", () => {
            filtrarPorCategoria(categoria);
            atualizarBotaoAtivo(botao);
        });
        containerFiltros.appendChild(botao);
    });
}

// Formatar nome da categoria para exibição
function formatarNomeCategoria(categoria) {
    const nomes = {
        'brigadeiros': 'Brigadeiros',
        'coxinhas': 'Coxinhas de Morango',
        'tortas': 'Tortas no Pote',
        'kits': 'Kits Festa'
    };
    return nomes[categoria] || categoria;
}

// Filtrar produtos por categoria
function filtrarPorCategoria(categoria) {
    const itensDoces = document.querySelectorAll('.doce-area .doce-item:not(.models .doce-item)');
    
    itensDoces.forEach((item, index) => {
        const doceIndex = index;
        const doce = doceJson[doceIndex];
        
        if (categoria === 'todos' || (doce && doce.category === categoria)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

// Atualizar botão ativo
function atualizarBotaoAtivo(botaoSelecionado) {
    document.querySelectorAll('.category-btn').forEach(btn => btn.classList.remove('active'));
    botaoSelecionado.classList.add('active');
}

// Show loading state
function showLoading() {
    const doceArea = document.querySelector('.doce-area');
    doceArea.innerHTML = '<div class="loading">Carregando produtos...</div>';
}

// Hide loading state
function hideLoading() {
    const loadingElement = document.querySelector('.loading');
    if (loadingElement) {
        loadingElement.remove();
    }
}

// Carregar os doces na página
function carregarDoces() {
    const doceArea = document.querySelector('.doce-area');
    
    // Clear existing products (except models)
    const existingItems = doceArea.querySelectorAll('.doce-item:not(.models .doce-item)');
    existingItems.forEach(item => item.remove());
    
    doceJson.forEach((item, index) => {
        // Skip inactive products
        if (item.is_active === false) {
            return;
        }
        
        let doceItem = document.querySelector('.models .doce-item').cloneNode(true);
        doceArea.appendChild(doceItem);
        
        // Preencher os dados de cada doce
        doceItem.querySelector('.doce-item--img img').src = item.img;
        
        // Tratar preços - padronizar para usar 'prices' sempre
        let preco = item.prices ? item.prices[0] : (item.price ? (Array.isArray(item.price) ? item.price[0] : item.price) : 0);
        
        if (!isNaN(preco) && preco > 0) {
            doceItem.querySelector('.doce-item--price').innerHTML = `R$ ${preco.toFixed(2)}`;
        } else {
            doceItem.querySelector('.doce-item--price').innerHTML = 'Consulte preço';
        }

        doceItem.querySelector('.doce-item--name').innerHTML = item.name;
        doceItem.querySelector('.doce-item--desc').innerHTML = item.description;

        // Add stock indicator if low
        if (item.stock !== undefined && item.stock < 10) {
            const stockIndicator = document.createElement('div');
            stockIndicator.className = 'stock-indicator';
            stockIndicator.innerHTML = `Estoque: ${item.stock}`;
            doceItem.appendChild(stockIndicator);
        }

        // Evento para abrir o modal
        doceItem.querySelector('a').addEventListener('click', (e) => {
            e.preventDefault();
            openModal(index);
        });
    });
}

// Inicializar página
async function inicializar() {
    showLoading();
    await loadProductsData();
    hideLoading();
    carregarDoces();
    criarBotoesFiltro();
}

// Botão voltar ao topo
document.getElementById('topBtn').addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Abrir modal
function openModal(index) {
    modalQt = 1;
    modalKey = index;

    let doce = doceJson[index];

    document.querySelector('.doceBig img').src = doce.img;
    document.querySelector('.doceInfo h1').innerHTML = doce.name;
    document.querySelector('.doceInfo--desc').innerHTML = doce.description;

    // Preencher tamanhos
    const sizesContainer = document.querySelector('.doceInfo--sizes');
    sizesContainer.innerHTML = '';

    // Verificar se tem tamanhos disponíveis
    if (doce.sizes && doce.sizes.length > 0) {
        doce.sizes.forEach((label, idx) => {
            const sizeBtn = document.createElement('div');
            sizeBtn.classList.add('doceInfo--size');
            if (idx === 0) sizeBtn.classList.add('selected');
            sizeBtn.setAttribute('data-size', idx);

            const span = document.createElement('span');
            span.innerText = label;
            sizeBtn.appendChild(span);
            sizesContainer.appendChild(sizeBtn);

            sizeBtn.addEventListener('click', () => {
                document.querySelectorAll('.doceInfo--size').forEach(s => s.classList.remove('selected'));
                sizeBtn.classList.add('selected');
                updateModalPrice();
            });
        });
    }

    updateModalPrice();

    document.querySelector('.doceInfo--qt').innerHTML = modalQt;
    document.querySelector('.doceWindowArea').style.display = 'flex';
    setTimeout(() => {
        document.querySelector('.doceWindowArea').style.opacity = 1;
    }, 10);
}

// Atualizar preço no modal
function updateModalPrice() {
    const selectedBtn = document.querySelector('.doceInfo--size.selected');
    const doce = doceJson[modalKey];
    
    if (!selectedBtn) {
        // Se não há tamanho selecionado, usar primeiro preço disponível
        let preco = doce.prices ? doce.prices[0] : (doce.price ? (Array.isArray(doce.price) ? doce.price[0] : doce.price) : 0);
        if (!isNaN(preco) && preco > 0) {
            document.querySelector('.doceInfo--actualPrice').innerHTML = `R$ ${preco.toFixed(2)}`;
        } else {
            document.querySelector('.doceInfo--actualPrice').innerHTML = 'Consulte preço';
        }
        return;
    }

    const selectedSizeIdx = parseInt(selectedBtn.getAttribute('data-size'));
    let price = 0;
    
    // Padronizar acesso aos preços
    if (doce.prices && doce.prices[selectedSizeIdx] !== undefined) {
        price = doce.prices[selectedSizeIdx];
    } else if (doce.price) {
        if (Array.isArray(doce.price)) {
            price = doce.price[selectedSizeIdx] || doce.price[0];
        } else {
            price = doce.price;
        }
    }

    if (!isNaN(price) && price > 0) {
        document.querySelector('.doceInfo--actualPrice').innerHTML = `R$ ${price.toFixed(2)}`;
    } else {
        document.querySelector('.doceInfo--actualPrice').innerHTML = 'Consulte preço';
    }
}

// Fechar modal
function closeModal() {
    document.querySelector('.doceWindowArea').style.opacity = 0;
    setTimeout(() => {
        document.querySelector('.doceWindowArea').style.display = 'none';
    }, 500);
}

// Eventos do modal
document.querySelectorAll('.doceInfo--cancelButton, .doceInfo--cancelMobileButton').forEach(item => {
    item.addEventListener('click', closeModal);
});

document.querySelector('.doceInfo--qtmenos').addEventListener('click', () => {
    if (modalQt > 1) {
        modalQt--;
        document.querySelector('.doceInfo--qt').innerHTML = modalQt;
    }
});

document.querySelector('.doceInfo--qtmais').addEventListener('click', () => {
    modalQt++;
    document.querySelector('.doceInfo--qt').innerHTML = modalQt;
});

// Adicionar ao carrinho
document.querySelector('.doceInfo--addButton').addEventListener('click', () => {
    const selectedSizeBtn = document.querySelector('.doceInfo--size.selected');
    const selectedSize = selectedSizeBtn ? selectedSizeBtn.getAttribute('data-size') : 0;
    const doce = doceJson[modalKey];
    const identifier = `${doce.id}-${selectedSize}`;

    // Calcular preço do item
    let itemPrice = 0;
    if (doce.prices && doce.prices[selectedSize] !== undefined) {
        itemPrice = doce.prices[selectedSize];
    } else if (doce.price) {
        itemPrice = Array.isArray(doce.price) ? doce.price[selectedSize] || doce.price[0] : doce.price;
    }

    const key = cart.findIndex(item => item.identifier === identifier);
    if (key > -1) {
        cart[key].qt += modalQt;
    } else {
        cart.push({
            identifier,
            id: doce.id,
            size: selectedSize,
            qt: modalQt,
            name: doce.name,
            sizeName: doce.sizes ? doce.sizes[selectedSize] : 'Padrão',
            price: itemPrice
        });
    }

    updateCart();
    closeModal();
});

// Atualizar carrinho
function updateCart() {
    document.querySelector('.menu-openner span').innerHTML = cart.length;
    
    if (cart.length > 0) {
        document.querySelector('aside').classList.add('show');
        document.querySelector('.cart').innerHTML = '';

        let subtotal = 0;

        cart.forEach((item, index) => {
            let doceItem = doceJson.find(doce => doce.id == item.id);
            
            let cartItem = document.querySelector('.models .cart--item').cloneNode(true);
            cartItem.querySelector('img').src = doceItem.img;
            cartItem.querySelector('.cart--item-nome').innerHTML = `${item.name} (${item.sizeName})`;
            cartItem.querySelector('.cart--item--qt').innerHTML = item.qt;

            cartItem.querySelector('.cart--item-qtmenos').addEventListener('click', () => {
                if (cart[index].qt > 1) {
                    cart[index].qt--;
                } else {
                    cart.splice(index, 1);
                }
                updateCart();
            });

            cartItem.querySelector('.cart--item-qtmais').addEventListener('click', () => {
                cart[index].qt++;
                updateCart();
            });

            document.querySelector('.cart').append(cartItem);
            subtotal += item.price * item.qt;
        });

        // Atualizar totais
        document.querySelector('.subtotal span:last-child').innerHTML = `R$ ${subtotal.toFixed(2)}`;
        document.querySelector('.total span:last-child').innerHTML = `R$ ${subtotal.toFixed(2)}`;
        
    } else {
        document.querySelector('aside').classList.remove('show');
    }
}

// Abrir/fechar carrinho
document.querySelector('.menu-openner').addEventListener('click', () => {
    if (cart.length > 0) {
        document.querySelector('aside').classList.add('show');
    }
});

document.querySelector('.menu-closer').addEventListener('click', () => {
    document.querySelector('aside').classList.remove('show');
});

// Enhanced checkout function with API integration
async function finalizarCompra() {
    if (cart.length === 0) {
        alert('Seu carrinho está vazio!');
        return;
    }

    // Show loading state
    const finalizarBtn = document.querySelector('.cart--finalizar');
    const originalText = finalizarBtn.innerHTML;
    finalizarBtn.innerHTML = 'Processando...';
    finalizarBtn.style.opacity = '0.7';

    try {
        if (useAPI) {
            // Try to submit order via API
            const purchaseData = api.transformCartForAPI(cart);
            const response = await api.createPurchase(purchaseData);
            
            if (response.success) {
                alert('Pedido enviado com sucesso! Entraremos em contato em breve.');
                cart = [];
                updateCart();
            } else {
                throw new Error(response.error || 'Erro ao processar pedido');
            }
        } else {
            // Fallback: Generate WhatsApp message
            generateWhatsAppOrder();
        }
    } catch (error) {
        console.error('Error processing order:', error);
        
        // Fallback to WhatsApp
        alert('Ocorreu um erro ao processar o pedido online. Redirecionando para WhatsApp...');
        generateWhatsAppOrder();
    } finally {
        // Reset button
        finalizarBtn.innerHTML = originalText;
        finalizarBtn.style.opacity = '1';
    }
}

// Generate WhatsApp order message
function generateWhatsAppOrder() {
    let message = '🍰 *Pedido Terapia Doce* 🍰\n\n';
    let total = 0;

    cart.forEach(item => {
        const itemTotal = item.price * item.qt;
        total += itemTotal;
        message += `• ${item.name}\n`;
        message += `  Tamanho: ${item.sizeName}\n`;
        message += `  Quantidade: ${item.qt}\n`;
        message += `  Preço: R$ ${itemTotal.toFixed(2)}\n\n`;
    });

    message += `*Total: R$ ${total.toFixed(2)}*\n\n`;
    message += 'Gostaria de confirmar este pedido, por favor! 😊';

    const encodedMessage = encodeURIComponent(message);
    const whatsappURL = `https://wa.me/5561920015630?text=${encodedMessage}`;
    
    window.open(whatsappURL, '_blank');
    
    // Clear cart after sending to WhatsApp
    cart = [];
    updateCart();
}

// Update finalizar compra event listener
document.querySelector('.cart--finalizar').addEventListener('click', finalizarCompra);

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', inicializar);