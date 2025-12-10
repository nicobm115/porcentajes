import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. Configuración de la Página ---
st.set_page_config(page_title="Tracker de Ingresos", layout="centered")

# --- 2. Gestión del Estado (Persistencia temporal) ---
# Como Streamlit recarga todo el script en cada interacción, 
# guardamos los datos en la caché de sesión.
if 'registros' not in st.session_state:
    st.session_state['registros'] = []

# --- 3. Título y Métricas ---
st.title("💰 Control de Ingresos")

# Cálculo de totales en tiempo real
total_neto = sum(item['neto'] for item in st.session_state['registros'])
total_bruto = sum(item['bruto'] for item in st.session_state['registros'])

# Usamos columnas para mostrar métricas tipo dashboard
col_met1, col_met2 = st.columns(2)
col_met1.metric("Total Acumulado (Neto)", f"${total_neto:,.2f}")
col_met2.metric("Total Facturado (Bruto)", f"${total_bruto:,.2f}")

st.divider()

# --- 4. Formulario de Entrada (Sidebar o Principal) ---
with st.expander("➕ Añadir Nuevo Ingreso", expanded=True):
    c1, c2 = st.columns(2)
    
    with c1:
        bruto = st.number_input("Importe Bruto ($)", min_value=0.0, step=10.0)
    with c2:
        # Dejamos 70% como default, pero editable
        porcentaje = st.number_input("Porcentaje a retener (%)", min_value=0.0, max_value=100.0, value=70.0)

    btn_agregar = st.button("Registrar Ingreso", use_container_width=True)

    # Lógica al pulsar el botón
    if btn_agregar:
        if bruto > 0:
            neto = bruto * (porcentaje / 100)
            nuevo_registro = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "bruto": bruto,
                "porcentaje": porcentaje,
                "neto": neto
            }
            # Insertamos al principio (0) para que salga el más reciente arriba
            st.session_state['registros'].insert(0, nuevo_registro)
            st.success("Ingreso registrado correctamente.")
            st.rerun() # Forzamos recarga para actualizar la tabla inmediatamente
        else:
            st.error("El importe debe ser mayor a 0.")

# --- 5. Visualización de Datos ---
st.subheader("Historial de Registros")

if len(st.session_state['registros']) > 0:
    # Convertimos la lista de diccionarios a DataFrame de Pandas
    df = pd.DataFrame(st.session_state['registros'])
    
    # Configuración de columnas para visualización limpia
    st.dataframe(
        df,
        column_config={
            "fecha": "Fecha",
            "bruto": st.column_config.NumberColumn("Bruto", format="$%.2f"),
            "porcentaje": st.column_config.NumberColumn("% Retenido", format="%.0f%%"),
            "neto": st.column_config.NumberColumn("Neto (Tuyo)", format="$%.2f"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Botón para limpiar historial
    if st.button("Borrar todo el historial"):
        st.session_state['registros'] = []
        st.rerun()
else:
    st.info("No hay registros todavía. Añade uno arriba.")