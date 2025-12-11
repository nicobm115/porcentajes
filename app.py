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


st.divider()

# --- 4. Formulario de Entrada ---
with st.form("➕ Añadir Nuevo Ingreso"):
    
    bruto = st.number_input("Importe Bruto ", min_value=0, step=10,value=60)
    
    porc_usuario = st.selectbox("Tu Porcentaje % ", options=[ 60, 70,], index=1)

    Nota = st.text_input("Nota ")

    submitted= st.form_submit_button('añadir')

if submitted:
    recent_ticket_number= int(max(st.session_state.df.ID).split("-")[1])
    hoy= datetime.now().strftime("%m-%d-%Y")
    df_new = pd.DataFrame(
        [
            {
                "ID":f"nº-{recent_ticket_number+1}",
                'fecha': hoy,
                "Bruto": bruto,
                "neto": bruto*porc_usuario/100,
                "notas":Nota
                
            }
        ]
    )
    
st.write("Tattoo añadido !")
st.dataframe(df_new, use_container_width=True, hide_index=True)
st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

st.header("Tattoos")
st.write(f"nº: `{len(st.session_state.df)}`")
