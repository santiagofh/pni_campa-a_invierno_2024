#%%
import pandas as pd
df=pd.read_excel("Campaña Invierno Nirsevimab 2024.xlsx")
df.columns = [col.replace('\xa0', ' ') for col in df.columns]
df.columns = [col.replace('\u00A0', ' ') for col in df.columns]

df_filled = df.fillna(0)
# Define a function to check if the final dose count is correct based on initial doses, administered, wastage, and transfers
def check_final_dose(row):
    expected_final = (row['Nª de dosis de Nirsevimab 50 mg al inicio de la jornada'] 
                      - row['Nª de dosis administradas de Nirsevimab 50 mg']
                      - (row.get('Nª de dosis mermas de Nirsevimab 50 mg') or 0)
                      + (row.get('Nº de dosis Nirsevimab 50 mg ingresadas') or 0)
                      - (row.get('Nº de dosis Nirsevimab 50 mg traspasadas a un servicio u otra institución') or 0))
    return expected_final == row['Nª de dosis de Nirsevimab 50 mg al final de la jornada']

# Apply the function to each row
df_filled['Final_Dose_Check_50mg'] = df_filled.apply(check_final_dose, axis=1)

# Identify the vacunatorios that have responded (have a report) and those that have not
responded_50mg = df_filled[df_filled['Final_Dose_Check_50mg']]['Nombre del Vacunatorio'].unique()
not_responded_50mg = df_filled[~df_filled['Final_Dose_Check_50mg']]['Nombre del Vacunatorio'].unique()

# Identify if there were any transfers made for 50mg doses
transfers_50mg = df_filled[df_filled['Nº de dosis Nirsevimab 50 mg traspasadas a un servicio u otra institución'].notnull()]['Nombre del Vacunatorio'].unique()

# Now repeat the same for 100mg doses
def check_final_dose_100mg(row):
    expected_final_100mg = (row['Nª de dosis de Nirsevimab 100 mg al inicio de la jornada'] 
                            - row['Nª de dosis administradas de Nirsevimab 100 mg'] 
                            - (row.get('Nª de dosis mermas de Nirsevimab 100 mg') or 0)
                            + (row.get('Nº de dosis Nirsevimab 100 mg ingresadas') or 0)
                            - (row.get('Nº de dosis Nirsevimab 100 mg traspasadas a un servicio u otra institución') or 0))
    return expected_final_100mg == row['Nª de dosis de Nirsevimab 100 mg al final de la jornada']

df_filled['Final_Dose_Check_100mg'] = df_filled.apply(check_final_dose_100mg, axis=1)

responded_100mg = df_filled[df_filled['Final_Dose_Check_100mg']]['Nombre del Vacunatorio'].unique()
not_responded_100mg = df_filled[~df_filled['Final_Dose_Check_100mg']]['Nombre del Vacunatorio'].unique()

transfers_100mg = df_filled[df_filled['Nº de dosis Nirsevimab 100 mg traspasadas a un servicio u otra institución'].notnull()]['Nombre del Vacunatorio'].unique()

# Return the summary for 50mg and 100mg
(responded_50mg, not_responded_50mg, transfers_50mg, responded_100mg, not_responded_100mg, transfers_100mg)
#%%
rename_columns = {
    'Nombre del Vacunatorio': 'Vacunatorio',
    'Nª de dosis de Nirsevimab 50 mg al inicio de la jornada': 'Dosis inicio 50 mg',
    'Nª de dosis administradas de Nirsevimab 50 mg': 'Dosis admin. 50 mg',
    'Nª de dosis mermas de Nirsevimab 50 mg': 'Dosis mermas 50 mg',
    'Nº de dosis Nirsevimab 50 mg traspasadas a un servicio u otra institución': 'Dosis traspaso salida 50 mg',
    'Nº de dosis Nirsevimab 50 mg ingresadas (en caso de realizar retiro o recibir por traspaso)': 'Dosis traspaso entrada 50 mg',
    'Nº de dosis Nirsevimab 50 mg ingresadas': 'Dosis traspaso entrada 50 mg',
    'Nª de dosis de Nirsevimab 50 mg al final de la jornada': 'Dosis final 50 mg',
    'Nª de dosis de Nirsevimab 100 mg al inicio de la jornada': 'Dosis inicio 100 mg',
    'Nª de dosis administradas de Nirsevimab 100 mg': 'Dosis admin. 100 mg',
    'Nª de dosis mermas de Nirsevimab 100 mg': 'Dosis mermas 100 mg',
    'Nº de dosis Nirsevimab 100 mg traspasadas a un servicio u otra institución': 'Dosis traspaso salida 100 mg',
    'Nº de dosis Nirsevimab 100 mg ingresadas (en caso de realizar retiro o recibir por traspaso)': 'Dosis traspaso entrada 100 mg',
    'Nº de dosis Nirsevimab 100 mg ingresadas':'Dosis traspaso entrada 100 mg',
    'Nª de dosis de Nirsevimab 100 mg al final de la jornada': 'Dosis final 100 mg'
}
df_filled.rename(columns=rename_columns, inplace=True)
df_filled.to_excel("nirsevimab_analizado.xlsx")
df_filled.to_csv("nirsevimab_analizado.csv")
# %%
