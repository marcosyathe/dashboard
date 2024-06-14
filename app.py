import dash
from  dash import dcc, html, dash_table
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=['assets/style.css'])

server = app.server

# Carrega os dados do CSV
df = pd.read_csv('data.csv')

df['Porcentagem Afetada'] = df['Porcentagem'].apply(lambda x: f'{x:.2f}%')

columns = ['Classe','Área (m²)','Porcentagem Afetada']
# Define o layout do dashboard
app.layout = [
    html.Header(className='header', children=[
           
        html.Div(className='logo-container',children=[
            html.Img(className='logo',src='assets/logo.png'),
        ]), 
        #html.H1(className='title',children='Dashboard')
    ]),

    html.Div(
    className='grid-container',
    children=[
        # Primeira linha: imagens
        html.Div(
            className='grid-item img-container',
            children=[
                html.H2(className='chart-title',children='Imageamento'),
                html.Img(src='assets/plantacao1.png', alt='Plantacao 1', style={'width': '500px', 'height': '500px'}),
            ]
        ),
        html.Div(
            className='grid-item img-container',
            children=[
                html.H2(className='chart-title',children='Imagem Gerada pela ETKHA Plantas Daninhas'),

                html.Img(src='assets/plantacao1.png', alt='Plantacao 2', style={'width': '500px', 'height': '500px'}),
            ]
        ),
        # Segunda linha: tabela e gráfico
        html.Div(
            className='grid-item table-container',
            children=[
                html.H2(className='chart-title',children='Classe, Área e Porcentagem Afetada'),
                dash_table.DataTable(
                    
                    id='table',
                    columns=[{'id': c, 'name': c} for c in columns],
                    data=df.to_dict('records'),
                    style_table={'overflowX': 'auto'},
                    style_cell_conditional=[
                        {
                        'if':{'column_id':c},
                        'textAlign': 'center'
                        } for c in ['Classe','Porcentagem Afetada','Área (m²)']
                        ],
                    style_as_list_view=True
                                    )
            ]
        ),
        html.Div(
            className='grid-item',
            children=[
                html.H2(className='chart-title',children='Porcentagem da Área Afetada'),
                dcc.Graph(id='pie-chart')
            ]
        ),
       
    ]
)]


# Callback para atualizar o gráfico de pizza
@app.callback(
    dash.Output('pie-chart', 'figure'),
    dash.Input('table', 'data')
)

def update_pie_chart(data):
    df = pd.DataFrame(data)
    fig = go.Figure(data=[go.Pie(labels=df['Classe'], values=df['Porcentagem'], hole=0.3)])
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
