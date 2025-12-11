import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. Configuración de la Página ---
st.set_page_config(page_title="Tracker de Ingresos", layout="centered")

st.title("💰 Control de Ingresos")

# --- 2. Conexión con Google Sheets ---
# Conectamos con la hoja. ttl=0 asegura que no guarde caché y siempre muestre datos frescos.
conn = st.connection("gsheets", type=GSheetsConnection)

# Intentamos leer los datos existentes
try:
    # Ajusta "Hoja 1" al nombre real de tu pestaña en Google Sheets
    existing_data = conn.read(worksheet="Hoja 1", usecols=list(range(4)), ttl=0)
    # Si hay vacíos (NaN), los limpiamos para evitar errores
    existing_data = existing_data.dropna(how="all")
except:
    # Si la hoja está totalmente vacía o nueva, creamos el DataFrame base
    existing_data = pd.DataFrame(columns=["fecha", "Bruto", "neto", "notas"])

# --- 3. Formulario de Entrada ---
with st.form("➕ Añadir Nuevo Ingreso"):
    
    # He añadido step=5 para que sea más cómodo en móvil
    bruto = st.number_input("Importe Bruto", min_value=0, step=5, value=60)
    
    porc_usuario = st.selectbox("Tu Porcentaje %", options=[60, 70], index=1)
    
    Nota = st.text_input("Nota")

    submitted = st.form_submit_button('Añadir')

if submitted:
    # Calculamos el neto
    neto_calc = bruto * porc_usuario / 100
    hoy = datetime.now().strftime("%d-%m-%Y") # Cambié a Dia-Mes-Año (más común aquí)
    
    # Creamos el registro nuevo
    df_new = pd.DataFrame(
        [
            {
                "fecha": hoy,
                "Bruto": bruto,
                "neto": neto_calc,
                "notas": Nota
            }
        ]
    )
    
    # --- 4. ACTUALIZACIÓN EN LA NUBE ---
    # Unimos lo que ya había en Sheets con lo nuevo
    updated_df = pd.concat([existing_data, df_new], ignore_index=True)
    
    # Escribimos todo de vuelta a Google Sheets
    conn.update(worksheet="Hoja 1", data=updated_df)
    
    st.success("¡Tattoo guardado en la nube!")
    
    # IMPORTANTE: st.rerun() recarga la app para que veas el dato nuevo en la tabla de abajo inmediatamente
    st.rerun()

# --- 5. Mostrar Historial ---
st.header("Historial de Tattoos")

if not existing_data.empty:
    st.write(f"nº trabajos: `{len(existing_data)}`")
    
    # Calculamos el total ganado (suma de la columna neto)
    total_ganado = existing_data["neto"].sum()
    st.metric(label="Total Ganado (Neto)", value=f"{total_ganado:,.2f} €")

    # Mostramos la tabla (ordenada para ver el último primero, opcional)
    # create una copia para no alterar el orden al guardar
    st.dataframe(existing_data.sort_index(ascending=False), use_container_width=True, hide_index=True)
else:
    st.info("Aún no hay registros en la hoja.")
