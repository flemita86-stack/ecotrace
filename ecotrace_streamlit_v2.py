import streamlit as st
import pandas as pd
import datetime as dt
from io import BytesIO

# --------------------------------------------
# CONFIGURACIÓN GENERAL
# --------------------------------------------
st.set_page_config(
    page_title="EcoTrace — Sistema de Trazabilidad Ambiental",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de colores y estilo
st.markdown("""
    <style>
        .main {
            background-color: #ffffff;
            color: #1b5e20;
            font-family: 'Arial', sans-serif;
        }
        h1, h2, h3 {
            color: #2e7d32 !important;
        }
        .stButton>button {
            background-color: #2e7d32;
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 100%;
            border: none;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #43a047;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------
# INICIALIZACIÓN
# --------------------------------------------
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=[
        "Fecha", "Generador", "Tipo de Residuo", "Cantidad (kg)", "Destino", "Observaciones"
    ])

# --------------------------------------------
# SIDEBAR
# --------------------------------------------
st.sidebar.title("📘 EcoTrace")
menu = st.sidebar.radio("Navegación", ["🏠 Inicio", "🗂️ Registro de Residuos", "📊 Estadísticas", "⚙️ Exportar Datos"])

# --------------------------------------------
# PÁGINA: INICIO
# --------------------------------------------
if menu == "🏠 Inicio":
    st.title("🌿 EcoTrace — Sistema de Trazabilidad Ambiental")
    st.markdown("""
    Bienvenido al sistema **EcoTrace**, una herramienta para la **gestión y trazabilidad ambiental** de residuos.
    
    **Objetivos:**
    - Registrar y monitorear los residuos generados.
    - Evaluar la trazabilidad ambiental en cada etapa.
    - Facilitar reportes y análisis de datos ambientales.

    Desarrollado por **Carlos Matías Moya** · Licenciado en Gestión Ambiental  
    """)

# --------------------------------------------
# PÁGINA: REGISTRO
# --------------------------------------------
elif menu == "🗂️ Registro de Residuos":
    st.title("🗂️ Registro de Residuos")

    with st.form("formulario_residuos"):
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("📅 Fecha", dt.date.today())
            generador = st.text_input("🏢 Generador del Residuo")
            tipo = st.selectbox("♻️ Tipo de Residuo", [
                "Orgánico", "Inorgánico", "Peligroso", "Patogénico", "RAEE", "Otro"
            ])
        with col2:
            cantidad = st.number_input("⚖️ Cantidad (kg)", min_value=0.0, format="%.2f")
            destino = st.text_input("🚛 Destino del Residuo")
            observaciones = st.text_area("📝 Observaciones")

        submitted = st.form_submit_button("💾 Guardar Registro")

        if submitted:
            if generador and cantidad > 0:
                nuevo_registro = pd.DataFrame({
                    "Fecha": [fecha],
                    "Generador": [generador],
                    "Tipo de Residuo": [tipo],
                    "Cantidad (kg)": [cantidad],
                    "Destino": [destino],
                    "Observaciones": [observaciones]
                })
                st.session_state["data"] = pd.concat(
                    [st.session_state["data"], nuevo_registro],
                    ignore_index=True
                )
                st.success("✅ Registro guardado exitosamente.")
            else:
                st.error("⚠️ Complete todos los campos obligatorios y asegúrese de que la cantidad sea mayor a 0.")

    st.divider()
    st.subheader("📋 Registros recientes")
    st.dataframe(st.session_state["data"], use_container_width=True)

# --------------------------------------------
# PÁGINA: ESTADÍSTICAS
# --------------------------------------------
elif menu == "📊 Estadísticas":
    st.title("📊 Estadísticas Ambientales")
    df = st.session_state["data"]

    if not df.empty:
        total_residuos = df["Cantidad (kg)"].sum()
        st.metric("♻️ Total de Residuos Registrados (kg)", f"{total_residuos:.2f}")

        tipo_resumen = df.groupby("Tipo de Residuo")["Cantidad (kg)"].sum().reset_index()

        st.bar_chart(tipo_resumen.set_index("Tipo de Residuo"))
    else:
        st.info("Aún no hay datos registrados.")

# --------------------------------------------
# PÁGINA: EXPORTAR DATOS
# --------------------------------------------
elif menu == "⚙️ Exportar Datos":
    st.title("⚙️ Exportar Registros")

    df = st.session_state["data"]

    if not df.empty:
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Registros EcoTrace")

        st.download_button(
            label="📥 Descargar Excel",
            data=output.getvalue(),
            file_name=f"EcoTrace_Registros_{dt.date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("⚠️ No hay registros para exportar.")

# --------------------------------------------
# PIE DE PÁGINA
# --------------------------------------------
st.markdown("""
---
🪴 **EcoTrace — Gestión Ambiental Responsable**  
Desarrollado por **Carlos Matías Moya**
""")
