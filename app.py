import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# --- 1. PAGE INITIALIZATION ---
st.set_page_config(
    page_title="Luxury Interiors",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THEME STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .luxury-title {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        margin: 0;
    }
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .product-card {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
    }
    .price-tag {
        background: #ffd700;
        color: #1a1a1a;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. PERSISTENT DATA STATE ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# Product Catalog Dataset
PRODUCTS = [
    {"id": 1, "name": "Velvet Chesterfield Sofa", "price": 2999, "category": "sofas", "image": "🛋️", "stock": 12},
    {"id": 2, "name": "Modern L-Shape Sofa", "price": 2499, "category": "sofas", "image": "🛋️", "stock": 8},
    {"id": 3, "name": "Luxury Leather Sectional", "price": 4999, "category": "sofas", "image": "🛋️", "stock": 5},
    {"id": 4, "name": "Marble Coffee Table", "price": 899, "category": "tables", "image": "☕", "stock": 15},
    {"id": 5, "name": "Oak Dining Table", "price": 1799, "category": "tables", "image": "🍽️", "stock": 10},
    {"id": 6, "name": "Glass Side Table", "price": 299, "category": "tables", "image": "☕", "stock": 20},
    {"id": 7, "name": "Eames Lounge Chair", "price": 1299, "category": "chairs", "image": "🪑", "stock": 18},
    {"id": 8, "name": "Velvet Armchair", "price": 799, "category": "chairs", "image": "🪑", "stock": 25},
    {"id": 9, "name": "Bar Stool Set", "price": 599, "category": "chairs", "image": "🪑", "stock": 30},
    {"id": 10, "name": "Crystal Chandelier", "price": 2499, "category": "lighting", "image": "💡", "stock": 6},
    {"id": 11, "name": "Modern Floor Lamp", "price": 399, "category": "lighting", "image": "💡", "stock": 22},
    {"id": 12, "name": "Wall Sconces (Pair)", "price": 299, "category": "lighting", "image": "💡", "stock": 15},
    {"id": 13, "name": "Persian Rug 8x10", "price": 2999, "category": "decor", "image": "🧳", "stock": 4},
    {"id": 14, "name": "Wall Art Set", "price": 599, "category": "decor", "image": "🎨", "stock": 12},
    {"id": 15, "name": "Marble Vase", "price": 199, "category": "decor", "image": "🪴", "stock": 35}
]

# Calculate Shopping Aggregations Safely
cart_item_count = sum(st.session_state.cart.values())
cart_total_price = sum(next(p['price'] for p in PRODUCTS if p['id'] == pid) * qty for pid, qty in st.session_state.cart.items())

# --- 4. NAVIGATION BAR ---
with st.sidebar:
    st.markdown("## 🏠 Navigation")
    selected = option_menu(
        menu_title=None,
        options=["Catalog", "Cart", "Checkout", "Dashboard"],
        icons=["house", "cart", "credit-card", "bar-chart"],
        default_index=0
    )

# --- 5. HEADER BRANDING ---
st.markdown("""
    <div class="main-header">
        <h1 class="luxury-title">Luxury Interiors</h1>
        <p class="subtitle">Premium Furniture & Home Decor for Discerning Tastes</p>
    </div>
""", unsafe_allow_html=True)

# --- 6. TOP APP METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Unique Items", len(PRODUCTS))
m2.metric("Items in Cart", cart_item_count)
m3.metric("Current Total", f"${cart_total_price:,.2f}")
m4.metric("Total Warehouse Stock", sum(p['stock'] for p in PRODUCTS))
st.markdown("---")

# --- 7. APPLICATIVE INTERFACE CORE ROUTING ---
if selected == "Catalog":
    st.header("✨ Premium Collection")
    
    # Filter Controls
    f_col1, f_col2 = st.columns([2, 1])
    with f_col1:
        search_query = st.text_input("🔍 Search our inventory...", "").strip().lower()
    with f_col2:
        price_bounds = st.slider("💰 Price Window ($)", 0, 5000, (0, 5000))

    # Real-Time Data Filtration
    filtered = [
        p for p in PRODUCTS 
        if (not search_query or search_query in p['name'].lower()) and 
           (price_bounds[0] <= p['price'] <= price_bounds[1])
    ]

    # Category Separation Tabs
    t_sofa, t_table, t_chair, t_light, t_decor = st.tabs(["🛋️ Sofas", "☕ Tables", "🪑 Chairs", "💡 Lighting", "🎨 Decor"])
    categories = {"sofas": t_sofa, "tables": t_table, "chairs": t_chair, "lighting": t_light, "decor": t_decor}

    for cat_slug, tab_obj in categories.items():
        with tab_obj:
            cat_items = [p for p in filtered if p['category'] == cat_slug]
            if not cat_items:
                st.info("No items match your selected filter parameters in this category.")
            for item in cat_items:
                with st.container():
                    c1, c2, c3 = st.columns([1, 4, 2])
                    c1.markdown(f"## {item['image']}")
                    c2.markdown(f'<div class="product-card"><h3>{item["name"]}</h3><p>Availability: <b>{item["stock"]} units left</b></p></div>', unsafe_allow_html=True)
                    with c3:
                        st.markdown(f'<div class="price-tag">${item["price"]:,.2f}</div>', unsafe_allow_html=True)
                        if st.button("Add To Cart", key=f"btn_add_{item['id']}", use_container_width=True):
                            st.session_state.cart[item['id']] = st.session_state.cart.get(item['id'], 0) + 1
                            st.toast(f"Added {item['name']} to cart!")
                            st.rerun()

elif selected == "Cart":
    st.header("🛒 Your Shopping Cart")
    if not st.session_state.cart:
        st.info("Your shopping cart is currently empty.")
    else:
        for pid, qty in list(st.session_state.cart.items()):
            item_details = next(p for p in PRODUCTS if p['id'] == pid)
            cc1, cc2, cc3, cc4 = st.columns([3, 1, 1, 1])
            cc1.write(f"**{item_details['name']}**")
            cc2.write(f"Quantity: {qty}")
            cc3.write(f"${item_details['price'] * qty:,.2f}")
            if cc4.button("❌ Remove", key=f"del_{pid}"):
                del st.session_state.cart[pid]
                st.rerun()

elif selected == "Checkout":
    st.header("💳 Complete Your Order")
    if not st.session_state.cart:
        st.warning("Your cart is empty. Please add products before checking out.")
    else:
        st.subheader(f"Grand Total Bill: ${cart_total_price:,.2f}")
        if st.button("Confirm and Pay", type="primary", use_container_width=True):
            st.session_state.cart = {}
            st.balloons()
            st.success("Thank you! Your order has been securely processed.")
            st.rerun()

elif selected == "Dashboard":
    st.header("📊 Inventory & Business Analytics")
    df = pd.DataFrame(PRODUCTS)
    
    fig_scatter = px.scatter(df, x='price', y='stock', size='price', color='category', hover_name='name', title="Price vs Stock Inventory Scatter")
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.plotly_chart(px.pie(df, names='category', values='stock', title="Total Stock Volume Breakdown"), use_container_width=True)
    with col_g2:
        st.plotly_chart(px.bar(df, x='category', y='price', color='category', title="Average Valuation Profiles"), use_container_width=True)
