import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. Configuración de la Página ---
st.set_page_config(page_title="Tracker de Ingresos", layout="centered")

# --- 2. Gestión del Estado ---
if 'registros' not in st.session_state:
    st.session_state['registros'] = []

# --- 3. Título y Métricas (Dashboard) ---
st.title("💰 Control de Ingresos")

# Cálculos de totales en tiempo real
total_bruto = sum(item['bruto'] for item in st.session_state['registros'])
total_neto = sum(item['neto'] for item in st.session_state['registros'])
total_estudio = sum(item['estudio'] for item in st.session_state['registros'])

# Mostramos 3 columnas de métricas
col1, col2, col3 = st.columns(3)
col1.metric("Total Bruto", f"${total_bruto:,.2f}")
col2.metric("Tu Parte (Neto)", f"${total_neto:,.2f}", delta_color="normal")
col3.metric("Parte Estudio", f"${total_estudio:,.2f}", delta_color="off") 

st.divider()

# --- 4. Formulario de Entrada ---
with st.expander("➕ Añadir Nuevo Ingreso", expanded=True):
    c1, c2 = st.columns(2)
    
    with c1:
        bruto = st.number_input("Importe Bruto ", min_value=0.0, step=10.0)
    with c2:
        # El usuario introduce SU porcentaje
        porc_usuario = st.number_input("Tu Porcentaje (%)", min_value=0.0, max_value=100.0, value=70.0)

    btn_agregar = st.button("Registrar Ingreso", use_container_width=True)

    if btn_agregar:
        if bruto > 0:
            # --- LÓGICA DE NEGOCIO ---
            # 1. Tu parte
            neto_usuario = bruto * (porc_usuario / 100)
            
            # 2. Parte del estudio (El restante)
            porc_estudio = 100 - porc_usuario
            neto_estudio = bruto * (porc_estudio / 100)
            
            nuevo_registro = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "bruto": bruto,
                "porc_usuario": porc_usuario,
                "neto": neto_usuario,
                "porc_estudio": porc_estudio, # Guardamos el % del estudio
                "estudio": neto_estudio       # Guardamos el $ del estudio
            }
            
            st.session_state['registros'].insert(0, nuevo_registro)
            st.success(f"Registrado: Tú ${neto_usuario:.2f} | Estudio ${neto_estudio:.2f}")
            st.rerun()
        else:
            st.error("El importe debe ser mayor a 0.")

# --- 5. Visualización de Datos (Tabla) ---
st.subheader("Historial de Registros")

if len(st.session_state['registros']) > 0:
    df = pd.DataFrame(st.session_state['registros'])
    
    st.dataframe(
        df,
        column_config={
            "fecha": "Fecha",
            "bruto": st.column_config.NumberColumn("Bruto", format="$%.2f"),
            "porc_usuario": st.column_config.NumberColumn("Tu %", format="%.0f%%"),
            "neto": st.column_config.NumberColumn("Tuyo ($)", format="$%.2f"),
            # Nuevas columnas para el estudio
            "porc_estudio": st.column_config.NumberColumn("% Est.", format="%.0f%%"),
            "estudio": st.column_config.NumberColumn("Estudio ($)", format="$%.2f"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    if st.button("Borrar todo el historial"):
        st.session_state['registros'] = []
        st.rerun()
else:
    st.info("No hay registros todavía.")

