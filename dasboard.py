import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
import numpy as np

#df_orders = pd.read_csv('https://raw.githubusercontent.com/WuCandice/Superstore-Sales-Analysis/refs/heads/main/dataset/Superstore%20Dataset.csv')

def cargar_datos():
    data = pd.read_csv('https://raw.githubusercontent.com/WuCandice/Superstore-Sales-Analysis/refs/heads/main/dataset/Superstore%20Dataset.csv')
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    return data

df_orders = cargar_datos()

def generate_age(segment):
    if segment == 'Consumer':
        return np.random.randint(18, 36)
    elif segment == 'Corporate':
        return np.random.randint(36, 56)
    else:  # Home Office
        return np.random.randint(56, 71)

df_orders['customer_age'] = df_orders['Segment'].apply(generate_age)
#print("Muestra de datos con la edad generada:")
#print(df_orders[['Segment', 'customer_age']].head())

#df_orders
all_data = df_orders.copy()

all_data = all_data.dropna(how="any")

all_data['Category'] = all_data['Category'].apply(lambda x: str(x))
all_data['Year'] = all_data['Order Date'].apply(lambda x: str(x)[0:4])
sales_by_category = all_data[['Category', 'Sales']].groupby(['Category']).sum()
sales_by_category.head(10)
sales_by_region = all_data[['Region', 'Sales']].groupby(['Region']).sum()
sales_by_region.head()
sales_by_subcategory = all_data[['Sub-Category', 'Sales']].groupby(['Sub-Category']).sum()
sales_by_subcategory.head()
sales_by_year = all_data[['Year', 'Sales', 'Profit']].groupby('Year').sum()
sales_by_year.head()
sales_by_age = all_data[['customer_age', 'Sales', 'Profit']].groupby('customer_age').sum()
sales_by_age.head()


#st.title("Reporte de ventas")
#st.header("Super Store")

#fig = px.bar(sales_by_category,x = sales_by_category.index,
#             y='Sales',
#             title="Nro de Ventas",
#             )
#fig.update_layout(xaxis_title="Categoria",yaxis_title="ventas")
#st.plotly_chart(fig,use_container_width=True)

#st.markdown("---")


st.sidebar.header("Filtros del dashboard")
min_date = df_orders['Order Date'].min()
max_date = df_orders['Order Date'].max()
print(min_date)
print(type(min_date))
fecha_inicial,fecha_final = st.sidebar.date_input(
    "Selecciona un rango de fechas",
    value=[min_date,max_date],
    min_value=min_date,
    max_value=max_date
)
df_filtrado = df_orders[df_orders['Order Date'].between(pd.to_datetime(fecha_inicial),pd.to_datetime(fecha_final))]

st.title("Super Store Dashboard")
st.markdown('##')

ventas_totales = df_orders['Sales'].sum()
utilidad_totales = df_orders['Profit'].sum()
ordenes_totales = df_orders['Order ID'].nunique()
clientes_totales = df_orders['Customer ID'].nunique()

col1,col2,col3,col4 = st.columns(4)
with col1:
    st.metric(label="Ventas Totales",value=f"${ventas_totales}")
with col2:
    st.metric(label="Utilidad Total",value=f"${utilidad_totales}")    
with col3:
    st.metric(label="Ordenes Totales",value=f"{ordenes_totales}")
with col4:
    st.metric(label="Clientes Totales",value=f"{clientes_totales}")

st.header("Ventas y utilidades a lo largo del tiempo")
ventas_por_utilidad = df_filtrado.set_index('Order Date').resample('M').agg({'Sales': 'sum','Profit':'sum'}).reset_index()
fig_area= px.area(
    ventas_por_utilidad,
    x='Order Date',
    y=['Sales','Profit'],
    title="Evolucion de ventas y utilidades en el tiempo"
)
st.plotly_chart(fig_area,use_container_width=True)
st.markdown('---')

colpie,coldona = st.columns(2)

with colpie:
    ventas_by_region = df_filtrado.groupby('Region')['Sales'].sum().reset_index()
    fig_pie_region = px.pie(
        ventas_by_region,
        names='Region',
        values='Sales',
        title="Ventas por Región"
    )
    st.plotly_chart(fig_pie_region,use_container_width=True)
    

