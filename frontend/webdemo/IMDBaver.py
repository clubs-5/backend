import pandas as pd 
import re
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

def runPy():
    rating_year = pd.read_csv('./run_omdb_rating.csv')
    years=rating_year.groupby("Released")["imdbRating"].mean().reset_index()
    px.scatter(years,x="Released", y="imdbRating").show()
    print('finish')