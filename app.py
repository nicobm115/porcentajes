import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. Configuración de la Página ---
st.set_page_config(page_title="Tracker de Ingresos", layout="centered")

st.title("💰 Control de Ingresos")

if 'df' not in st.session_state:
    # Creamos un DataFrame vacío con las columnas necesarias
    st.session_state.df = pd.DataFrame(columns=[ "fecha", "Bruto", "neto", "notas"])



# --- 4. Formulario de Entrada ---
with st.form("➕ Añadir Nuevo Ingreso"):
    
    bruto = st.number_input("Importe Bruto ", min_value=0, step=10,value=60)
    
    porc_usuario = st.selectbox("Tu Porcentaje % ", options=[ 60, 70,], index=1)

    Nota = st.text_input("Nota ")

    submitted= st.form_submit_button('añadir')

if submitted:
   
    hoy= datetime.now().strftime("%m-%d-%Y")
    df_new = pd.DataFrame(
        [
            {
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


