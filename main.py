import dash
import dash_auth
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px

mapbox_access_token = "pk.eyJ1IjoicXV5bmhkbzIxOTEiLCJhIjoiY2tjNDJuYTZ0MDB5MDJ4cXN5cTVuMmE0ayJ9.QWeZb9STIOYfvmEUkDxoJw"
px.set_mapbox_access_token(mapbox_access_token)

df = pd.read_excel("sensor_data.xlsx")
df1 = pd.read_excel("vessel_data.xlsx")

vessel_name = df['vessel'].unique()

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'logistics': 'temp123'
}
#-------------------------------------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

#-------------------------------------------

app.layout = html.Div([
    dcc.Dropdown(id='my-dropdown',
                 options=[{'label': i, 'value': i} for i in vessel_name],
                 value='Santa Isabel'),

    html.Div([
        html.Div([dcc.Graph(id='my_graph1', figure={})],className='six columns'),
        html.Div([dcc.Graph(id='my_graph2', figure={})], className='six columns')
],className='row')

],
    style={
        # 'padding': 30,
        'marginLeft': 50, 'marginRight': 30,
    # 'marginTop': 50, 'marginBottom': 10
    }
)


@app.callback([Output(component_id='my_graph1', component_property='figure'),
               Output(component_id='my_graph2', component_property='figure')],

              [Input('my-dropdown', 'value')])
def update_rows(selected_value):
    df_fil = df[df['vessel'] == selected_value]

    fig1 = px.line(df_fil, x='time', y='sensor_temp', color='Serial_No')
    fig1.update_xaxes(title_text= 'Timestamp')
    fig1.update_yaxes(title_text='Sensor temperature')
    fig1.update_layout(plot_bgcolor="#FFF")

    df1_fil = df1[df1['vessel'] == selected_value]
    fig2 = px.scatter_mapbox(df1_fil,
                             lon='longitude',
                             lat='latitude',
                             hover_data=['Max sensor temp', 'Mean sensor temp', 'Min sensor temp'],
                             size='Wind temp',
                             color='Wind temp',
                             color_continuous_scale=px.colors.cyclical.IceFire
                             )

    fig2.update_layout(width=700, height=1000,
                       hovermode='closest', mapbox=dict(accesstoken=mapbox_access_token,
                                                        bearing=0, center=dict(lon=-17.91523, lat=22.12103), pitch=0,
                                                        zoom=2), showlegend=False)

    return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True, port=8055)