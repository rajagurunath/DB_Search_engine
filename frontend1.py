# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 20:56:46 2018

@author: welcome
"""

import dash
import dash_html_components as html
#import dash_core_components as dcc
#import plotly


app=dash.Dash()


app.layout=html.Div([
                     
                     html.Div('Search engine')
                     
                     
                     ])


if __name__=='__main__':
    app.run_server(debug=True)