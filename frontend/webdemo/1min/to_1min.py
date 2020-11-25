import pandas as pd 
import re
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
rating_year = pd.read_csv('1min/run_omdb_rating.csv')
years=rating_year.groupby("Released")["imdbRating"].mean().reset_index()
px.scatter(years,x="Released", y="imdbRating").show()