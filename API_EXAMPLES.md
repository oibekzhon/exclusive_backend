# JSON API Response Examples

## Product List Endpoint: `/api/products/`

### Full Product Response (with all fields):
```json
[
  {
    "id": 1,
    "image": "http://localhost:8000/media/products/logo.avif",
    "name": "Pro Gaming Laptop RTX 4080",
    "description": "High-performance gaming laptop with RTX 4080 graphics card",
    "price": "2499.99",
    "oldPrice": "3299.99",
    "discount": 24,
    "rating": "4.75",
    "reviews": 250,
    "temporaryDiscount": 10,
    "category": "Laptop",
    "colors": [
      {
        "id": 1,
        "name": "Qora (Black)",
        "hexCode": "#000000"
      },
      {
        "id": 2,
        "name": "Oq (White)",
        "hexCode": "#FFFFFF"
      }
    ],
    "sizes": [
      {
        "id": 1,
        "name": "15.6 inch"
      },
      {
        "id": 2,
        "name": "17.3 inch"
      }
    ],
    "images": [
      "http://localhost:8000/media/products/laptop_1.jpg",
      "http://localhost:8000/media/products/laptop_2.jpg",
      "http://localhost:8000/media/products/laptop_3.jpg"
    ],
    "isBestSelling": true,
    "isFlashSale": true
  }
]
```

### Minimal Product Response (only required fields):
```json
[
  {
    "id": 2,
    "image": null,
    "name": "Budget T-Shirt",
    "description": "Comfortable cotton t-shirt",
    "price": "15.99",
    "oldPrice": null,
    "discount": 0,
    "rating": "0.00",
    "reviews": 0,
    "temporaryDiscount": 0,
    "category": "Shirt",
    "colors": [],
    "sizes": [],
    "images": [],
    "isBestSelling": false,
    "isFlashSale": false
  }
]
```

### Multiple Products:
```json
[
  {
    "id": 1,
    "name": "Pro Gaming Laptop RTX 4080",
    "isBestSelling": true,
    "isFlashSale": true,
    "reviews": 250,
    "rating": "4.75"
  },
  {
    "id": 3,
    "name": "Gaming Mouse Logitech G502",
    "isBestSelling": true,
    "isFlashSale": false,
    "reviews": 500,
    "rating": "4.50"
  },
  {
    "id": 4,
    "name": "USB-C Cable",
    "isBestSelling": false,
    "isFlashSale": true,
    "reviews": 5,
    "rating": "3.50"
  }
]
```

---

## Frontend Usage Examples

### React Component - Display Products:
```jsx
function ProductCard({ product }) {
  return (
    <div className="product-card">
      <img src={product.image} alt={product.name} />
      
      {product.isBestSelling && (
        <span className="badge badge-success">Best Selling</span>
      )}
      
      {product.isFlashSale && (
        <span className="badge badge-danger">Flash Sale</span>
      )}
      
      <h3>{product.name}</h3>
      <p>{product.description}</p>
      
      <div className="price">
        <span className="current-price">${product.price}</span>
        {product.oldPrice && (
          <span className="old-price">${product.oldPrice}</span>
        )}
        {product.discount > 0 && (
          <span className="discount">-{product.discount}%</span>
        )}
      </div>
      
      {product.temporaryDiscount > 0 && (
        <div className="temp-discount">
          Extra {product.temporaryDiscount}% off!
        </div>
      )}
      
      <div className="rating">
        ⭐ {product.rating} ({product.reviews} reviews)
      </div>
      
      {product.colors.length > 0 && (
        <div className="colors">
          <label>Colors:</label>
          {product.colors.map(color => (
            <div 
              key={color.id} 
              className="color-option"
              style={{ backgroundColor: color.hexCode }}
              title={color.name}
            />
          ))}
        </div>
      )}
      
      {product.sizes.length > 0 && (
        <div className="sizes">
          <label>Sizes:</label>
          <select>
            <option>Select Size</option>
            {product.sizes.map(size => (
              <option key={size.id} value={size.id}>{size.name}</option>
            ))}
          </select>
        </div>
      )}
      
      {product.images.length > 1 && (
        <div className="image-gallery">
          {product.images.map((img, idx) => (
            <img key={idx} src={img} alt={`${product.name} ${idx + 1}`} />
          ))}
        </div>
      )}
    </div>
  );
}
```

### Vue.js Component:
```vue
<template>
  <div class="product-container">
    <div v-for="product in products" :key="product.id" class="product-card">
      <img :src="product.image" :alt="product.name" />
      
      <div v-if="product.isBestSelling" class="badge best-selling">
        🏆 Best Seller
      </div>
      
      <div v-if="product.isFlashSale" class="badge flash-sale">
        ⚡ Flash Sale
      </div>
      
      <h3>{{ product.name }}</h3>
      <p>{{ product.description }}</p>
      
      <div class="pricing">
        <span class="price">${{ product.price }}</span>
        <span v-if="product.oldPrice" class="old-price">${{ product.oldPrice }}</span>
        <span v-if="product.discount > 0" class="discount">-{{ product.discount }}%</span>
      </div>
      
      <div v-if="product.temporaryDiscount > 0" class="temp-discount">
        Temporary discount: {{ product.temporaryDiscount }}% OFF
      </div>
      
      <div class="rating">
        Rating: {{ product.rating }} ⭐ ({{ product.reviews }} reviews)
      </div>
      
      <div v-if="product.colors.length > 0" class="colors-section">
        <label>Available Colors:</label>
        <div class="color-list">
          <span 
            v-for="color in product.colors" 
            :key="color.id"
            class="color-tag"
            :style="{ backgroundColor: color.hexCode }"
            :title="color.name"
          >
            {{ color.name }}
          </span>
        </div>
      </div>
      
      <div v-if="product.sizes.length > 0" class="sizes-section">
        <label>Available Sizes:</label>
        <select v-model="selectedSize">
          <option value="">Select Size</option>
          <option v-for="size in product.sizes" :key="size.id" :value="size.id">
            {{ size.name }}
          </option>
        </select>
      </div>
      
      <div v-if="product.images.length > 1" class="image-gallery">
        <img 
          v-for="(img, idx) in product.images" 
          :key="idx" 
          :src="img" 
          :alt="`${product.name} ${idx + 1}`"
          class="gallery-image"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      products: [],
      selectedSize: ''
    }
  },
  mounted() {
    this.fetchProducts();
  },
  methods: {
    fetchProducts() {
      fetch('/api/products/')
        .then(res => res.json())
        .then(data => {
          this.products = data;
        });
    }
  }
}
</script>
```

---

## Filtering & Search Examples

### Filter by Best Seller:
```javascript
const bestSellers = products.filter(p => p.isBestSelling);
```

### Filter by Flash Sale:
```javascript
const flashSales = products.filter(p => p.isFlashSale);
```

### Filter by Rating:
```javascript
const topRated = products.filter(p => parseFloat(p.rating) >= 4.0);
```

### Filter by Category:
```javascript
const laptops = products.filter(p => p.category === 'Laptop');
```

### Filter by Color:
```javascript
const blackProducts = products.filter(p => 
  p.colors.some(c => c.hexCode === '#000000')
);
```

### Filter by Size:
```javascript
const largeSizeProducts = products.filter(p =>
  p.sizes.some(s => s.name === 'L' || s.name === 'XL')
);
```

---

## Admin Panel Usage Examples

### Adding a Product with All Features:

1. **Step 1: Basic Info**
   - Name: "Gaming Mouse"
   - Description: "Professional gaming mouse with RGB"
   - Category: Select from dropdown
   - Image: Upload image

2. **Step 2: Pricing**
   - Price: 79.99
   - Old Price: 99.99
   - Discount: 20
   - Temporary Discount: 15

3. **Step 3: Ratings**
   - Rating: 4.5
   - Reviews: 250

4. **Step 4: Variants**
   - Colors: Select "Qora (Black)" and "Oq (White)"
   - Sizes: Leave empty (not applicable for mouse)

5. **Step 5: Images**
   - Add 3 product images in the "Product Images" section

6. **Click Save**
   - Product saved successfully
   - Auto badges appear:
     - "Best Selling" ✓ (rating 4.5 >= 4 AND reviews 250 >= 100)
     - "Flash Sale" ✓ (temporary discount 15 > 0)

---

## Data Validation Rules

### Best Selling Criteria:
- ✅ rating >= 4.0
- ✅ reviews >= 100
- ✅ Both conditions must be true

### Flash Sale Criteria:
- ✅ temporary_discount > 0
- ✅ Any positive number qualifies
- ❌ 0 or null = NOT a flash sale

### Optional Fields (can be empty):
- old_price (leave blank = no old price shown)
- discount (leave blank = defaults to 0)
- reviews (leave blank = defaults to 0)
- rating (leave blank = defaults to 0)
- colors (leave empty = no color options)
- sizes (leave empty = no size options)
- temporary_discount (leave blank = not a flash sale)
