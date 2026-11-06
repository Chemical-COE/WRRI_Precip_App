import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Welcome to the WRRI Precipitation App')
grouped_data = pd.read_csv('grouped_data.csv')

daily = grouped_data.groupby(['source', 'hr bucket', 'day'], as_index = False)['mm'].sum()

fig = px.scatter(
    daily,
    x='hr bucket',
    y='mm',
    labels={'hr bucket': 'Mountain Time (Grouped by Hour)', 'mm': 'Accumulated Rain (mm)'},
    color = 'source',
    title = 'Precipitation Grouped by Hour'
)

fig.add_hline(y= 25.4, line_width=2, line_dash="dash", line_color="red")
#fig.add_hline(y= 2*25.4, line_width=2, line_dash="dash", line_color="red")
fig.write_html('Precipitation Grouped by Hour.html')
st.plotly_chart(fig)
