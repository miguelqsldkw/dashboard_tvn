
import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Dashboard TVN", layout="wide")

st.title("📊 Dashboard Estratégico – TVN")
st.markdown("Este panel permite visualizar el cumplimiento de indicadores estratégicos de Televisión Nacional de Chile bajo el modelo CMI.")

# Cargar datos
file = st.file_uploader("Sube el archivo Excel con la base de datos", type=["xlsx"])
if file:
    df = pd.read_excel(file, sheet_name="Base de datos")

    # Evaluar cumplimiento
    def evaluar_cumplimiento(row):
        if row['Resultado'] >= row['Meta']:
            return 'Cumplido'
        elif row['Resultado'] >= 0.8 * row['Meta']:
            return 'En riesgo'
        else:
            return 'No cumplido'

    df['Evaluación'] = df.apply(evaluar_cumplimiento, axis=1)

    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        anio = st.selectbox("Selecciona el año", sorted(df['Año/Periodo'].unique()))
    with col2:
        perspectivas = st.multiselect("Filtra por perspectiva", df['Perspectiva'].unique(), default=list(df['Perspectiva'].unique()))

    # Filtrado de datos
    df_filtrado = df[(df['Año/Periodo'] == anio) & (df['Perspectiva'].isin(perspectivas))]

    # Gráfico de barras
    st.subheader("📍 Resultados por Indicador")
    fig_bar = px.bar(
        df_filtrado, x="Indicador", y="Resultado", color="Evaluación",
        color_discrete_map={"Cumplido": "green", "En riesgo": "orange", "No cumplido": "red"},
        labels={"Resultado": "Valor alcanzado"},
        height=450
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

    # Gráfico de líneas por perspectiva
    st.subheader("📈 Comparación de Resultados y Metas por Perspectiva")
    fig_line = px.line(
        df_filtrado, x="Indicador", y=["Resultado", "Meta"], color="Perspectiva",
        markers=True, labels={"value": "Valor", "variable": "Tipo"},
        height=450
    )
    fig_line.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_line, use_container_width=True)

    # Tabla con resultados
    st.subheader("📋 Detalle de Indicadores")
    st.dataframe(df_filtrado[["Perspectiva", "Indicador", "Resultado", "Meta", "Unidad", "Evaluación"]])

else:
    st.info("Por favor, sube un archivo Excel con la hoja 'Base de datos'.")
