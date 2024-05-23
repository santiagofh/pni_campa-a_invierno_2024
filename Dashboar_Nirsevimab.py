#%%
import streamlit as st
import pandas as pd
from datetime import date, timedelta
import plotly.express as px

# Carga los datos procesados y rellenados
data = pd.read_csv("nirsevimab_analizado.csv")
df_establecimientos = pd.read_csv("data/Establecimientos Nirsevimab.csv", sep=";", usecols=[0,1])
#%%
# 'Clínica Juan Pablo II'- No tiene vacunatorio
# 'Clínica Santa Rosa'- No tiene vacunatorio
df_establecimientos.replace('Centro Médico HTS SpA','Vacunatorio Centro Médico ACHS',inplace=True)
df_establecimientos_maternidad=df_establecimientos.loc[df_establecimientos.Maternidad==1]
no_vacunatorios=[
    'Clínica Juan Pablo II',
    'Clínica Santa Rosa',
]


df_establecimientos_vacunatorio=df_establecimientos.loc[~(df_establecimientos['Todos los establecimientos'].isin(no_vacunatorios))]
df_establecimientos_vacunatorio=df_establecimientos_vacunatorio.drop_duplicates(subset=['Todos los establecimientos'])
#%%
# Convertir las fechas a datetime si no lo están ya
data['Dia del reporte'] = pd.to_datetime(data['Dia del reporte'])

# Título y selección de la fecha
st.title('📊 Análisis de Campaña de Vacunación Nirsevimab 2024')
yesterday = date.today() - timedelta(days=1)
selected_date = st.date_input('📅 Selecciona un día para el informe:', value=yesterday)
st.write(f"## 📆 Análisis correspondiente a la fecha: {selected_date.strftime('%d/%m/%Y')}")

# Filtrar los datos para el día seleccionado
data_filtered = data[data['Dia del reporte'] == pd.Timestamp(selected_date)]
data_vac=data_filtered.loc[data_filtered['Lugar de administración Nirsevimab']=='Vacunatorio']
data_mat=data_filtered.loc[data_filtered['Lugar de administración Nirsevimab']=='Maternidad o neonatologia o sala cuna']

# Resumen de vacunatorios que contestaron

total_vacunatorios_maternindad = str(len(df_establecimientos_maternidad))
total_vacunatorios_respondieron_maternidad = len(data_mat['Vacunatorio'].unique())
total_vacunatorios_respondieron = len(data_vac['Vacunatorio'].unique())
total_vacunatorios = str(len(df_establecimientos_vacunatorio))
st.write("### Total de vacunatorios en la campaña de invierno")

# Calcula los totales para los gráficos
total_vacunatorios = len(df_establecimientos_vacunatorio)
total_vacunatorios_maternidad = len(df_establecimientos_maternidad)

total_vacunatorios_respondieron = len(data_vac['Vacunatorio'].unique())
total_vacunatorios_respondieron_maternidad = len(data_mat['Vacunatorio'].unique())
st.write("---")
st.write(f"**🏥 Total de vacunatorios en la campaña:** {total_vacunatorios}")
st.write(f"**🏥 Total de vacunatorios de maternidad en la campaña:** {total_vacunatorios_maternindad}")
st.write("---")
st.write("### Analisis de vacunatorios del formulario")
st.write(f"**🏥 Total de vacunatorios que respondieron para el día:** {total_vacunatorios_respondieron}")
data_vac_no_respondieron=df_establecimientos_vacunatorio.loc[~(df_establecimientos_vacunatorio['Todos los establecimientos'].isin(list(data_vac['Vacunatorio'].unique())))]
data_vac_no_respondieron=data_vac_no_respondieron.reset_index()
st.write(f"**🏥 Listado de vacunatorios que no respondieron. Total: {str(len(data_vac_no_respondieron))}**")
data_vac_no_respondieron['Todos los establecimientos']
st.write(f"**🏥 Total de vacunatorios de maternidad que respondieron para el día:** {total_vacunatorios_respondieron_maternidad}")
# Maternidad
data_mat_no_respondieron=df_establecimientos_maternidad.loc[~(df_establecimientos_maternidad['Todos los establecimientos'].isin(list(data_mat['Vacunatorio'].unique())))]
data_mat_no_respondieron=data_mat_no_respondieron.reset_index()
st.write(f"**🏥 Listado de vacunatorios de maternidad que no respondieron. Total: {str(len(data_mat_no_respondieron))}**")
data_mat_no_respondieron['Todos los establecimientos']

# Sección de respuestas duplicadas
duplicated = data_filtered[data_filtered.duplicated(['Vacunatorio', 'Lugar de administración Nirsevimab'], keep=False)]
vacunatorio_dup = duplicated[duplicated['Lugar de administración Nirsevimab'] == 'Vacunatorio']
otros_dup = duplicated[duplicated['Lugar de administración Nirsevimab'] != 'Vacunatorio']

st.write("### Analisis de incongruencias")
# Resumen de incongruencias
incongruencias_50mg = len(data_filtered[~data_filtered['Final_Dose_Check_50mg']]['Vacunatorio'].unique())
incongruencias_100mg = len(data_filtered[~data_filtered['Final_Dose_Check_100mg']]['Vacunatorio'].unique())
st.write(f"**❗ Cantidad de vacunatorios con incongruencias en dosis de 50 mg:** {incongruencias_50mg}")
st.write(f"**❗ Cantidad de vacunatorios con incongruencias en dosis de 100 mg:** {incongruencias_100mg}")

# Asumiendo que 'vacunatorio_dup' y 'otros_dup' ya están definidos correctamente arriba en el script:
st.write(f"**❗ Cantidad de vacunatorios con respuestas duplicadas (Vacunatorio):** {len(vacunatorio_dup)}")
st.write(f"**❗ Cantidad de vacunatorios con respuestas duplicadas (Otros lugares de administración):** {len(otros_dup)}")

st.subheader('🔂 Respuestas duplicadas (Vacunatorio)')
st.dataframe(vacunatorio_dup[['Vacunatorio', 'Lugar de administración Nirsevimab']], use_container_width=True)

st.subheader('🔂 Respuestas duplicadas (Otros lugares de administración)')
st.dataframe(otros_dup[['Vacunatorio', 'Lugar de administración Nirsevimab']], use_container_width=True)

st.subheader('Vacunatorios con discrepancias (50 mg)')
# Filtrar por Final_Dose_Check_50mg False y seleccionar columnas relevantes
incorrect_50mg = data_filtered[~data_filtered['Final_Dose_Check_50mg']][[
    'Vacunatorio',
    'Dosis inicio 50 mg',
    'Dosis admin. 50 mg',
    'Dosis mermas 50 mg',
    'Dosis traspaso salida 50 mg',
    'Dosis traspaso entrada 50 mg',
    'Dosis final 50 mg'
]]
st.dataframe(incorrect_50mg, use_container_width=True)

st.subheader('Vacunatorios con discrepancias (100 mg)')
# Filtrar por Final_Dose_Check_100mg False y seleccionar columnas relevantes
incorrect_100mg = data_filtered[~data_filtered['Final_Dose_Check_100mg']][[
    'Vacunatorio',
    'Dosis inicio 100 mg',
    'Dosis admin. 100 mg',
    'Dosis mermas 100 mg',
    'Dosis traspaso salida 100 mg',
    'Dosis traspaso entrada 100 mg',
    'Dosis final 100 mg'
]]
st.dataframe(incorrect_100mg, use_container_width=True)
# %%
st.subheader('Total de nirsevimab al finalizar la jornada de los establecimientos reportados para 50 y 100 mg')

# %%
# Calculate total final doses for 50 mg and 100 mg
final_doses = data_filtered.groupby('Lugar de administración Nirsevimab').agg({
    'Dosis final 50 mg': 'sum',
    'Dosis final 100 mg': 'sum'
}).reset_index()

# Rename columns for clarity
final_doses.rename(columns={
    'Lugar de administración Nirsevimab': 'Tipo de Establecimiento',
    'Dosis final 50 mg': 'Total Final Dosis 50 mg',
    'Dosis final 100 mg': 'Total Final Dosis 100 mg'
}, inplace=True)

# Display the dataframe in Streamlit
st.subheader('Stock Final de Nirsevimab por Tipo de Establecimiento')
st.dataframe(final_doses, use_container_width=True)
