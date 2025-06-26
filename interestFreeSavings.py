import streamlit as st

st.set_page_config(page_title="Simulador de Cuotas Sin Interés", layout="centered")

# --- Comercio preset ---
stores = {
    "Ningún comercio": {"price": 1_000_000, "months": None,"min_allowed_price" : 1},
    "📱 Samsung": {"price": 3_000_000, "months": [3, 6, 12],"min_allowed_price" : 1},
    "🛒 Mercado Libre": {"price": 1_200_000, "months": [2, 3, 6, 12],"min_allowed_price" : 1},
    "🎧 JBL": {"price": 500_000, "months": [3, 6, 12],"min_allowed_price" : 100_000},
    "🛏️ Emma Sleep": {"price": 1_800_000, "months": [2, 3, 6, 12],"min_allowed_price" : 1},
    "🥶 Electrolux": {"price": 2_500_000, "months": [3, 6],"min_allowed_price" : 400_000},
    "Specialized 🚴‍♂️": {"price": 5_000_000, "months": [6, 12],"min_allowed_price" : 5000000},
    "Xiaomi 🏠": {"price": 1_500_000, "months": [2,3, 6, 12],"min_allowed_price" : 1},
}

st.title("💸 Simulador de Ahorro en Cuotas Sin Interés")
resumen_pagina = """
### 💡 ¿Realmente te convienen las cuotas sin interés?

Cuando compras algo a cuotas, **normalmente pagas más** por intereses.  
Pero algunos comercios ofrecen **cuotas verdaderamente sin interés**. ¿Es una buena oportunidad?

✅ **Sí, incluso si ya tienes el dinero.**  
Al pagar en cuotas, conservas tu plata y puedes **invertirla o usarla para otras cosas**.

Este simulador asume que ese dinero lo inviertes mes a mes en una cuenta que te da rendimiento, como **Nu** o **RappiPay**.  
Te muestra **cuánto terminas ganando al usar cuotas sin interés inteligentemente**.
"""

st.markdown(resumen_pagina)
# --- Tienda preseleccionada ---
st.subheader("Elige un comercio (opcional)")
selected_store = st.selectbox("Selecciona un comercio", list(stores.keys()), index=0)
if selected_store:
    st.session_state["preset_price"] = stores[selected_store]["price"]
    st.session_state["preset_months"] = stores[selected_store]["months"][-1]
    st.markdown(f"**Precio seleccionado:** ${st.session_state['preset_price']:,.0f} en {st.session_state['preset_months']} meses")

# --- Inputs del usuario ---
st.subheader("Parámetros de la compra")

P = st.number_input("💰 Precio del producto (P)", min_value=0, value=st.session_state.get("preset_price", 1000000))
# n_months = st.number_input("📆 Meses para pagar", min_value=1, value=st.session_state.get("preset_months", 12))
if stores[selected_store]["months"] is None:
    n_months = st.number_input("📆 Meses para pagar", min_value=stores[selected_store]["min_allowed_price"], value=st.session_state.get("preset_months", stores[selected_store]["months"][-1]), step=1)
else:
    n_months = st.selectbox("📆 Meses para pagar", stores[selected_store]["months"], index=stores[selected_store]["months"].index(st.session_state.get("preset_months", stores[selected_store]["months"][-1])))
payment_interval_days = st.number_input("🕒 Días entre pagos", min_value=1, value=30)

rate_type = st.selectbox("📈 Tipo de tasa de interés", ["Anual", "Mensual", "Diaria"])
r_input = st.slider("Tasa de interés (%)", min_value=0.0, max_value=100.0, value=9.25, step=0.01)

# --- Conversión de tasa ---
def get_daily_rate(rate_type, rate_percent):
    if rate_type == "Anual":
        return rate_percent / 100 / 365
    elif rate_type == "Mensual":
        return (rate_percent / 100) * 12 / 365
    else:
        return rate_percent / 100

delta = get_daily_rate(rate_type, r_input)
a = P / n_months
B = P - a

for i in range(1, int(n_months)):
    B = B * (1 + delta) ** payment_interval_days - a

savings = B * (1 + delta) ** payment_interval_days
discount_pct = (1 - (P - savings) / P) * 100

# --- Resultados ---
st.subheader("📊 Resultados")
st.markdown(f"""
- 💵 Precio original del producto: **${P:,.0f}**
- 💳 Pago mensual sin interés: **${a:,.0f}**
- 📈 Total ahorrado al final: **${savings:,.0f}**
- 🎯 Descuento efectivo aproximado: **{discount_pct:.2f}%**
""")

st.markdown("""
### ⚠️ Advertencia

Esta estrategia **puede ayudarte a ahorrar**, pero sólo si evitas mezclar **compras con interés y sin interés**.  

En algunas compras, como las de comercios internacionales, las compras pueden diferirse automáticamente a cuotas **con interés**, lo cual **anula los beneficios** de mantener tu liquidez invertida.

💡 Verifica siempre las condiciones de diferido de cada compra. Algunas entidades permiten modificar las cuotas **antes del primer corte**, lo cual es clave si estás usando esta estrategia.""")
