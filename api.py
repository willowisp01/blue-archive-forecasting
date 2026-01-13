from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

with open('data/results/six_month_forecast.json', 'r') as file:
    six_month_forecast = json.load(file)

@app.get('/')
def root():
    return {'message': 'Blue Archive 6-month Forecast API'}

@app.get('/six_month_forecast')
def get_six_month_forecast():
    if six_month_forecast:
        return six_month_forecast
    else:
        raise HTTPException(status_code=404, detail="Six-month forecast data not found")