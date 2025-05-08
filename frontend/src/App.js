// src/App.js
import React, { useState } from "react";
import ScreenshotTracker from "./ScreenShotTracker/ScreenshotTracker";

const products = [
      { id: 1, name: "Classic White T-Shirt", price: "$20", img: "https://c.media-amazon.com/images/I/51Y6ryllCsL._AC_SX679_.jpg", hasSizeChart: false },
      { id: 2, name: "Black Hoodie", price: "$40", img: "https://c.media-amazon.com/images/I/61C+zURu0EL._AC_SX679_.jpg", hasSizeChart: true },
      { id: 3, name: "Blue Jeans", price: "$60", img: "https://c.media-amazon.com/images/I/51GkgJfInTL._AC_SY879_.jpg", hasSizeChart: true },
      { id: 4, name: "Sneakers", price: "$80", img: "https://c.media-amazon.com/images/I/61oa+rlwTiL._AC_SY695_.jpg", hasSizeChart: false },
      { id: 5, name: "Summer Dress", price: "$45", img: "https://c.media-amazon.com/images/I/81EYjmptifL._AC_SY879_.jpg", hasSizeChart: true },
      { id: 6, name: "Cap", price: "$15", img: "https://c.media-amazon.com/images/I/71eHXFsetiS._AC_SX679_.jpg", hasSizeChart: false },
      { id: 7, name: "Blue Denim T-Shirt", price: "$20", img: "https://c.media-amazon.com/images/I/71nwNJMLSSL._AC_SY879_.jpg", hasSizeChart: false },
      { id: 8, name: "Yellow Hoodie", price: "$40", img: "https://c.media-amazon.com/images/I/61VNNqXvirL._AC_SX679_.jpg", hasSizeChart: true },
      { id: 9, name: "Black Towel", price: "$60", img: "https://c.media-amazon.com/images/I/91VyEHJ5ndL.__AC_SX300_SY300_QL70_FMwebp_.jpg", hasSizeChart: true },
      { id: 10, name: "Sandals", price: "$80", img: "https://c.media-amazon.com/images/I/91UzoqnwFZL._AC_SY695_.jpg", hasSizeChart: false },
      { id: 11, name: "Shorts", price: "$45", img: "https://c.media-amazon.com/images/I/51Jb15RPOfL._AC_SY879_.jpg", hasSizeChart: true },
      { id: 12, name: "Keychain", price: "$15", img: "https://c.media-amazon.com/images/I/51GSHPQqsRL._AC_SX679_.jpg", hasSizeChart: false },
    ];

function App() {
  const [cart, setCart] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);

  const addToCart = (product) => {
    setCart([...cart, product]);
    alert(`${product.name} added to cart!`);
    setSelectedProduct(null);
  };

  const removeFromCart = (index) => {
    const updatedCart = [...cart];
    updatedCart.splice(index, 1);
    setCart(updatedCart);
  };

  const renderCatalog = () => (
    <div style={{ padding: "20px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>Product Catalog</h1>
        <button onClick={() => setSelectedProduct("cart")} style={{ padding: "10px", background: "green", color: "white", border: "none", borderRadius: "5px" }}>
          🛒 View Cart ({cart.length})
        </button>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: "20px" }}>
        {products.map(product => (
          <div key={product.id} onClick={() => setSelectedProduct(product)} style={{ border: "1px solid #ddd", padding: "15px", cursor: "pointer" }}>
            <img src={product.img} alt={product.name} style={{ width: "100%", height: "150px", objectFit: "cover" }} />
            <h3>{product.name}</h3>
            <p>{product.price}</p>
          </div>
        ))}
      </div>
    </div>
  );

  const renderProductPage = (product) => (
    <div style={{ padding: "20px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>{product.name}</h1>
        <button onClick={() => setSelectedProduct("cart")} style={{ padding: "10px", background: "green", color: "white", border: "none", borderRadius: "5px" }}>
          🛒 View Cart ({cart.length})
        </button>
      </div>
      <img src={product.img} alt={product.name} style={{ width: "300px", height: "auto" }} />
      <p>Price: {product.price}</p>
      <label htmlFor="size">Select Size:</label>
      <select id="size">
        <option value="">Choose</option>
        <option value="S">Small</option>
        <option value="M">Medium</option>
        <option value="L">Large</option>
      </select>
      <br /><br />
      <button onClick={() => addToCart(product)}>Add to Cart</button>
      <button disabled>Save for Later</button>
      <br />
      {!product.hasSizeChart ? (
        <div style={{ color: "gray", fontSize: "0.9em" }}>Size chart not found</div>
      ) : (
        <a href="#">View size chart</a>
      )}
      <br /><br />
      <button onClick={() => setSelectedProduct(null)}>⬅️ Back to Catalog</button>
    </div>
  );

  const renderCart = () => (
    <div style={{ padding: "20px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>Your Cart</h1>
        <button onClick={() => setSelectedProduct(null)} style={{ padding: "10px", background: "gray", color: "white", border: "none", borderRadius: "5px" }}>
          ⬅️ Back to Catalog
        </button>
      </div>
      <ul>
        {cart.map((item, index) => (
          <li key={index}>
            {item.name} - {item.price}
            <button onClick={() => removeFromCart(index)}>Remove</button>
          </li>
        ))}
      </ul>
      <br />
      <button onClick={() => alert("Order Placed")}>Place Order</button>
    </div>
  );

  if (selectedProduct === "cart") return renderCart();
  if (selectedProduct) return renderProductPage(selectedProduct);
  return (
    <>
      {renderCatalog()}
      <ScreenshotTracker />
    </>
  );
}

export default App;