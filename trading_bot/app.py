"""
Streamlit Web UI for Trading Bot
A professional web interface for placing orders on Binance Futures Testnet
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from decimal import Decimal
import os
from pathlib import Path
import json

# Import trading bot modules
from bot.client import BinanceClient, BinanceAPIError
from bot.orders import OrderManager
from bot.validators import ValidationError

# Page configuration
st.set_page_config(
    page_title="Trading Bot UI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    /* Ensure metric cards are readable regardless of Streamlit theme */
    div[data-testid="stMetric"] {
        background-color: #f0f2f6 !important;
        border: 1px solid #d9dee7;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    div[data-testid="stMetricLabel"] p,
    div[data-testid="stMetricValue"] {
        color: #111827 !important;
    }
    div[data-testid="stMetricDelta"] {
        color: #374151 !important;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "client" not in st.session_state:
    st.session_state.client = None
if "order_manager" not in st.session_state:
    st.session_state.order_manager = None
if "connection_status" not in st.session_state:
    st.session_state.connection_status = False
if "order_history" not in st.session_state:
    st.session_state.order_history = []

# Sidebar - Settings and Configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    st.subheader("API Credentials")
    
    api_key = st.text_input(
        "API Key",
        value=os.getenv("BINANCE_API_KEY", ""),
        type="password",
        help="Your Binance Futures Testnet API Key"
    )
    
    api_secret = st.text_input(
        "API Secret",
        value=os.getenv("BINANCE_API_SECRET", ""),
        type="password",
        help="Your Binance Futures Testnet API Secret"
    )
    
    # Connection test button
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔌 Connect", use_container_width=True):
            if not api_key or not api_secret:
                st.error("❌ Please enter both API Key and Secret")
            else:
                try:
                    st.session_state.client = BinanceClient(api_key, api_secret)
                    st.session_state.order_manager = OrderManager(st.session_state.client)
                    
                    # Test connection
                    server_time = st.session_state.client.get_server_time()
                    st.session_state.connection_status = True
                    st.success("✅ Connected to Binance Testnet!")
                    st.info(f"Server Time: {server_time}")
                    
                except BinanceAPIError as e:
                    st.session_state.connection_status = False
                    st.error(f"❌ Connection Failed: {str(e)}")
                except Exception as e:
                    st.session_state.connection_status = False
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        if st.button("🔓 Disconnect", use_container_width=True):
            st.session_state.client = None
            st.session_state.order_manager = None
            st.session_state.connection_status = False
            st.info("Disconnected")
    
    # Connection status
    st.divider()
    if st.session_state.connection_status:
        st.markdown('<div class="success-box">🟢 Status: Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-box">🔴 Status: Disconnected</div>', unsafe_allow_html=True)
    
    st.divider()
    st.subheader("ℹ️ Info")
    st.markdown("""
    **Testnet Only**
    - This bot connects to Binance Futures Testnet
    - No real money involved
    - For learning and testing only
    
    **Get Credentials:**
    1. Visit https://testnet.binancefuture.com
    2. Create account
    3. Go to API Management
    4. Create API key
    5. Copy here
    """)


# Main content area
st.title("🤖 Trading Bot - Web UI")
st.markdown("*Place orders on Binance Futures Testnet*")

# Check if connected
if not st.session_state.connection_status:
    st.warning("⚠️ Please connect to Binance in the sidebar first")
    st.info("1. Enter your API credentials in the sidebar\n2. Click 'Connect' button")
else:
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Dashboard", "🛒 Place Order", "📋 Order Status", "📜 Order History"]
    )
    
    # TAB 1: Dashboard
    with tab1:
        st.subheader("Dashboard")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Status", "🟢 Connected", help="Connected to Binance Testnet")
        
        with col2:
            try:
                server_time = st.session_state.client.get_server_time()
                st.metric("Server Time", datetime.fromtimestamp(server_time/1000).strftime("%H:%M:%S"))
            except:
                st.metric("Server Time", "N/A")
        
        with col3:
            st.metric("Orders Placed", len(st.session_state.order_history))
        
        st.divider()
        
        # Quick Links
        st.subheader("Quick Links")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📈 Market Buy (0.001 BTC)", use_container_width=True):
                st.session_state.place_order_symbol = "BTCUSDT"
                st.session_state.place_order_side = "BUY"
                st.session_state.place_order_type = "MARKET"
                st.session_state.place_order_qty = "0.001"
                st.success("Preset loaded. Open the '🛒 Place Order' tab to submit.")
        
        with col2:
            if st.button("📉 Market Sell (0.001 BTC)", use_container_width=True):
                st.session_state.place_order_symbol = "BTCUSDT"
                st.session_state.place_order_side = "SELL"
                st.session_state.place_order_type = "MARKET"
                st.session_state.place_order_qty = "0.001"
                st.success("Preset loaded. Open the '🛒 Place Order' tab to submit.")
        
        with col3:
            if st.button("💹 ETH Limit Buy", use_container_width=True):
                st.session_state.place_order_symbol = "ETHUSDT"
                st.session_state.place_order_side = "BUY"
                st.session_state.place_order_type = "LIMIT"
                st.session_state.place_order_qty = "0.1"
                st.success("Preset loaded. Open the '🛒 Place Order' tab to submit.")
        
        with col4:
            if st.button("💹 ETH Limit Sell", use_container_width=True):
                st.session_state.place_order_symbol = "ETHUSDT"
                st.session_state.place_order_side = "SELL"
                st.session_state.place_order_type = "LIMIT"
                st.session_state.place_order_qty = "0.1"
                st.success("Preset loaded. Open the '🛒 Place Order' tab to submit.")
    
    # TAB 2: Place Order
    with tab2:
        st.subheader("Place New Order")
        
        col1, col2 = st.columns(2)
        
        with col1:
            symbol = st.text_input(
                "Symbol",
                value=st.session_state.get("place_order_symbol", "BTCUSDT"),
                placeholder="e.g., BTCUSDT",
                help="Trading pair symbol"
            )
        
        with col2:
            side = st.selectbox(
                "Side",
                ["BUY", "SELL"],
                index=0 if st.session_state.get("place_order_side", "BUY") == "BUY" else 1,
                help="Buy or Sell"
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            order_type = st.selectbox(
                "Order Type",
                ["MARKET", "LIMIT"],
                index=0 if st.session_state.get("place_order_type", "MARKET") == "MARKET" else 1,
                help="Market or Limit order"
            )
        
        with col2:
            quantity = st.number_input(
                "Quantity",
                value=float(st.session_state.get("place_order_qty", 0.001)),
                min_value=0.0001,
                step=0.001,
                format="%.4f",
                help="Order quantity"
            )
        
        # Price field (only for LIMIT orders)
        if order_type == "LIMIT":
            price = st.number_input(
                "Price",
                value=0.0,
                min_value=0.0,
                step=100.0,
                format="%.2f",
                help="Order price (required for LIMIT orders)"
            )
        else:
            price = None
        
        # Order summary
        st.divider()
        st.subheader("Order Summary")
        
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        with summary_col1:
            st.metric("Symbol", symbol)
        with summary_col2:
            st.metric("Side", side)
        with summary_col3:
            st.metric("Type", order_type)
        with summary_col4:
            st.metric("Quantity", f"{quantity:.4f}")
        
        if order_type == "LIMIT":
            st.metric("Price", f"{price:.2f}")
        
        # Place order button
        st.divider()
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            if st.button("✅ Place Order", use_container_width=True, type="primary"):
                try:
                    with st.spinner(f"Placing {order_type} order..."):
                        response = st.session_state.order_manager.place_order(
                            symbol=symbol,
                            side=side,
                            order_type=order_type,
                            quantity=str(quantity),
                            price=str(price) if price else None
                        )
                        
                        # Add to history
                        order_entry = {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "symbol": symbol,
                            "side": side,
                            "type": order_type,
                            "quantity": quantity,
                            "price": price if order_type == "LIMIT" else "-",
                            "order_id": response.get("orderId"),
                            "status": response.get("status"),
                            "executed_qty": response.get("executedQty"),
                            "avg_price": response.get("avgPrice", "-")
                        }
                        st.session_state.order_history.append(order_entry)
                        
                        # Show success message
                        st.success("✅ Order Placed Successfully!")
                        
                        # Show order details
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.write(f"**Order ID:** {response.get('orderId')}")
                        st.write(f"**Status:** {response.get('status')}")
                        st.write(f"**Executed Qty:** {response.get('executedQty')}")
                        st.write(f"**Avg Price:** {response.get('avgPrice', 'N/A')}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                except ValidationError as e:
                    st.error(f"❌ Validation Error: {str(e)}")
                except BinanceAPIError as e:
                    st.error(f"❌ API Error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        with col2:
            if st.button("🔄 Reset Form", use_container_width=True):
                st.session_state.place_order_symbol = "BTCUSDT"
                st.session_state.place_order_side = "BUY"
                st.session_state.place_order_type = "MARKET"
                st.session_state.place_order_qty = "0.001"
                st.rerun()
        
        with col3:
            if st.button("❌ Clear", use_container_width=True):
                st.write("")
    
    # TAB 3: Order Status
    with tab3:
        st.subheader("Check Order Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            check_symbol = st.text_input(
                "Symbol",
                value="BTCUSDT",
                placeholder="e.g., BTCUSDT"
            )
        
        with col2:
            check_order_id = st.number_input(
                "Order ID",
                value=0,
                min_value=0,
                step=1,
                help="Order ID to check"
            )
        
        if st.button("🔍 Check Status", use_container_width=True, type="primary"):
            if not check_order_id:
                st.error("❌ Please enter an Order ID")
            else:
                try:
                    with st.spinner("Fetching order status..."):
                        order = st.session_state.client.get_order_status(
                            symbol=check_symbol,
                            order_id=int(check_order_id)
                        )
                        
                        # Display order details
                        st.success("✅ Order Found!")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Order ID", order.get("orderId"))
                        with col2:
                            st.metric("Status", order.get("status"))
                        with col3:
                            st.metric("Executed Qty", order.get("executedQty"))
                        with col4:
                            st.metric("Avg Price", order.get("avgPrice", "N/A"))
                        
                        # Full details
                        st.divider()
                        st.subheader("Full Details")
                        
                        details_df = pd.DataFrame([
                            {"Field": "Symbol", "Value": order.get("symbol")},
                            {"Field": "Side", "Value": order.get("side")},
                            {"Field": "Type", "Value": order.get("type")},
                            {"Field": "Status", "Value": order.get("status")},
                            {"Field": "Original Qty", "Value": order.get("origQty")},
                            {"Field": "Executed Qty", "Value": order.get("executedQty")},
                            {"Field": "Price", "Value": order.get("price")},
                            {"Field": "Avg Price", "Value": order.get("avgPrice")},
                            {"Field": "Time in Force", "Value": order.get("timeInForce")},
                            {"Field": "Update Time", "Value": datetime.fromtimestamp(int(order.get("updateTime", 0))/1000).strftime("%Y-%m-%d %H:%M:%S")},
                        ])
                        
                        st.dataframe(details_df, use_container_width=True, hide_index=True)
                        
                except BinanceAPIError as e:
                    st.error(f"❌ Error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # TAB 4: Order History
    with tab4:
        st.subheader("Order History")
        
        if not st.session_state.order_history:
            st.info("ℹ️ No orders yet. Place an order to see it here.")
        else:
            # Create DataFrame from order history
            df = pd.DataFrame(st.session_state.order_history)
            
            # Display stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Orders", len(st.session_state.order_history))
            with col2:
                buy_orders = len([o for o in st.session_state.order_history if o["side"] == "BUY"])
                st.metric("Buy Orders", buy_orders)
            with col3:
                sell_orders = len([o for o in st.session_state.order_history if o["side"] == "SELL"])
                st.metric("Sell Orders", sell_orders)
            with col4:
                filled_orders = len([o for o in st.session_state.order_history if o["status"] == "FILLED"])
                st.metric("Filled Orders", filled_orders)
            
            st.divider()
            
            # Display table
            st.subheader("All Orders")
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Export options
            col1, col2 = st.columns(2)
            
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                json_data = df.to_json(orient="records", indent=2)
                st.download_button(
                    label="📥 Download as JSON",
                    data=json_data,
                    file_name=f"orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            # Clear history
            if st.button("🗑️ Clear History", help="Clear all order history"):
                st.session_state.order_history = []
                st.rerun()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px;">
    Trading Bot v1.0 | Binance Futures Testnet | 
    <a href="https://testnet.binancefuture.com" target="_blank">Get Testnet Account</a>
</div>
""", unsafe_allow_html=True)
