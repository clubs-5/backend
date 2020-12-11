import plotly.express as px
import pandas as pd 
def runcoun():
    ratings = pd.read_csv('./counIMDB.csv')
    top_rated=ratings[0:10]
    fig =px.sunburst(
        top_rated,
        path=['Title','Country'],
        values='Rating',
        color='Rating')
    fig.show()
print('finish')
