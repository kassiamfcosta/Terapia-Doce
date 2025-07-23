class TerapiaDoceAPI {
    constructor() {
        this.baseURL = 'http://localhost:8000/api';
        this.endpoints = {
            products: '/core/products/',
            purchases: '/core/purchases/',
            clients: '/clients/clients/',
            admins: '/admins/admins/'
        };
    }

    // Generic API call method
    async apiCall(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            }
        };

        const finalOptions = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, finalOptions);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return { success: true, data };
        } catch (error) {
            console.error('API call failed:', error);
            return { success: false, error: error.message };
        }
    }

    // Get all products
    async getProducts() {
        return await this.apiCall(this.endpoints.products);
    }

    // Get single product
    async getProduct(id) {
        return await this.apiCall(`${this.endpoints.products}${id}/`);
    }

    // Create purchase
    async createPurchase(purchaseData) {
        return await this.apiCall(this.endpoints.purchases, {
            method: 'POST',
            body: JSON.stringify(purchaseData)
        });
    }

    // Create client (for registration)
    async createClient(clientData) {
        return await this.apiCall(this.endpoints.clients, {
            method: 'POST',
            body: JSON.stringify(clientData)
        });
    }

    // Transform API product data to match frontend format
    transformProductData(apiProducts) {
        return apiProducts.map(product => ({
            id: product.id,
            name: product.name,
            img: product.image || 'imagens/default-product.png',
            price: product.prices && product.prices.length > 0 ? product.prices : [product.price],
            prices: product.prices && product.prices.length > 0 ? product.prices : [product.price],
            sizes: product.sizes && product.sizes.length > 0 ? product.sizes : ['Padrão'],
            description: product.description,
            category: product.category,
            stock: product.stock,
            is_active: product.is_active
        }));
    }

    // Transform cart data for API
    transformCartForAPI(cart) {
        const items = cart.map(item => ({
            product_id: item.id,
            quantity: item.qt,
            price: item.price,
            size_selected: item.sizeName,
            size_index: item.size
        }));

        const total = cart.reduce((sum, item) => sum + (item.price * item.qt), 0);

        return {
            total: total.toFixed(2),
            notes: 'Pedido realizado pelo site',
            items: items
        };
    }
}

// Create global API instance
const api = new TerapiaDoceAPI();

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TerapiaDoceAPI;
}