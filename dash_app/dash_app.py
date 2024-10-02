import dash
from dash import html, dcc
import plotly.express as px
from flask import Flask
from app.models import db, EmotionData, User
import pandas as pd

def create_dash_app(server):
    dash_app = dash.Dash(
        server=server,
        name="Dashboard",
        url_base_pathname='/dash/'
    )

    with server.app_context():
        # ดึงข้อมูลจากฐานข้อมูล
        data = EmotionData.query.all()
        if data:
            emotions = [d.emotion for d in data]
            df = pd.DataFrame({'emotion': emotions})
            # สร้างกราฟ
            fig = px.histogram(df, x='emotion', title='Emotion Distribution')
        else:
            # เมื่อไม่มีข้อมูล ให้สร้างกราฟเปล่าพร้อมแสดงข้อความ
            df = pd.DataFrame({'emotion': ['No Data Available']})
            fig = px.histogram(df, x='emotion', title='No Data Available')

    dash_app.layout = html.Div([
        html.H1('Emotion Statistics'),
        dcc.Graph(figure=fig)
    ])
    return dash_app
