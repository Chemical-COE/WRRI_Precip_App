import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Welcome to the WRRI Precipitation Agreeability App')
st.info('This app is currently static.')
st.write('Over the course of the next year please expect updates.')
st.write('For more information reach out or requests to the author cfirkins@unm.edu')

@st.cache_data
def read_data():
    grouped_data = pd.read_csv('grouped_data.csv')
    return grouped_data

grouped_data = read_data()
    
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

daily_grouped = grouped_data.groupby(['source', 'obs_date'], as_index=False)['mm'].sum()

all_sources = daily_grouped['source'].unique()
full_date_range = pd.date_range(
    start=daily_grouped['obs_date'].min(),
    end=daily_grouped['obs_date'].max(),
    freq='D'
)
full_grid = pd.MultiIndex.from_product(
    [all_sources, full_date_range], 
    names=['source', 'obs_date']
).to_frame(index=False)

full_grid['obs_date'] = pd.to_datetime(full_grid['obs_date']).dt.date
daily_grouped['obs_date'] = pd.to_datetime(daily_grouped['obs_date']).dt.date

complete_daily = pd.merge(full_grid, daily_grouped, on=['source', 'obs_date'], how='left')
complete_daily = complete_daily.sort_values(['obs_date', 'source']).reset_index(drop=True)
plot_df = complete_daily.copy()
plot_df['obs_date_dt'] = pd.to_datetime(plot_df['obs_date'])


source_offsets = {
    'Traditional Gauge': pd.Timedelta(hours=9),
    'IoT': pd.Timedelta(hours=10),
    'Commercial Gauge': pd.Timedelta(hours=11),
    'MRMS': pd.Timedelta(hours=12)
}

plot_df['plot_date'] = plot_df['obs_date_dt'] + plot_df['source'].map(source_offsets)

fig = px.scatter(
    plot_df,
    x='plot_date',
    y='mm',
    color='source',
    symbol='source',  # Assigns a unique marker shape (circle, square, diamond, etc.) per source
    labels={'plot_date': 'Manual Rain Gauge Observation Date', 'mm': 'Accumulated Rain (mm)'},
    title='Precipitation Grouped by Day (Offset)'
)

fig.update_traces(marker=dict(size=6, opacity=0.8))


fig.add_hline(y=25.4, line_width=2, line_dash="dash", line_color="red")

fig.update_yaxes(range=[None, 30])
fig.write_html('Precipitation Grouped by Day.html')
st.plotly_chart(fig)

st.info('Current data can be downloaded by clicking the button below.')

csv_data = grouped_data.to_csv(index=False).encode('utf-8')

st.download_button(
    label='Click Here To Download Data',
    data=csv_data,
    file_name='grouped_precipitation_data.csv',
    mime='text/csv'
)
st.dataframe(grouped_data)
