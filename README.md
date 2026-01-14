# Blue Archive Revenue Forecasting Model

## About this Project

Blue Archive is a role-playing game (RPG) about helping students from various academies resolve problems through story-driven narratives and combat scenarios. The aim of this notebook is to predict the 6-month future revenue of this game using features such as character banners (opportunities to obtain characters), events, and story releases. 

Data from various fan sites, online forums, and unofficial APIs were used to collate training data. A hybrid model consisting of spline + XGB (Extreme Gradient Boosting) is used. The spline models the overall trend in revenue, whereas XGB captures all other information apart from the trend. For instance, cycles and seasonality. 

There are 2 features of this project: a Jupyter notebook that predicts the revenue for the next 6 months, and an API that simply returns that 6-month forecast.


## How to Run (Docker)

This is the suggested run option for maximum compatibility. 

First, clone this repo, and ensure you have Docker installed.

Simply input this command:
* `docker-compose up --build`

This will download pre-built images from Docker Hub and do the necessary setup.
   
To use the API, type in the following commands from within the conda environment: 
* `curl http://127.0.0.1:8000/six_month_forecast`
(or you can just type http://127.0.0.1:8000/six_month_forecast into your web browser too.)

To view and run the `analysis.ipynb` notebook, type http://127.0.0.1:8888 into your browser.

## How to Run (Self-Setup)

First, clone this repo.

Using Anaconda, set up a conda environment using the `environment.yml` file. After which, it should be as simple as running all cells in the notebook `analysis.ipynb`. Doing that will 
* load in data from the API
* format raw data 
* train the model
* produce results and visualizations (etc). 

If any 3rd-party API cannot be reached, or the data is invalid for whatever reason, a serialized record of the API data will be loaded instead (see `*.pkl` files.) For reproducability, trained models have also be serialized (see `trend_model.joblib` and `xgb_residual_model.joblib`).

The 6-month forecast created by my model can also be obtained through an API. 

`six_month_forecast`: gives a six month forecast of revenue based on last available existing data.

To use the API, type in the following commands from within the `ba-forecasting` conda environment: 
* `uvicorn api:app --reload --host 127.0.0.1 --port 8000`
* `curl http://127.0.0.1:8000/six_month_forecast`
(or you can just type http://127.0.0.1:8000/six_month_forecast into your web browser too.)

## How to Test 

After setting up and activating the conda environment, you can run the command `pytest` from the root directory of this project. It should activate all tests. 

Please make you are in the right environment (`ba-forecasting`) before running `pytest`!

## Summary of Results

The hybrid model predicted a 6 month forecast accurately (with an outlier of the first month forecast). The MAE was 1.2 million excluding that forecast, about 6% of the maximum observed monthly revenue of 19 million. The model also achieved directional accuracy of 100% (i.e. the model correctly predicts whether revenue will go up or down) for that forecast of 6 months.

For more details, please refer to `analysis.ipynb`.

## Resources Used

The 3rd party API used to collate some features was https://api.ennead.cc/buruaka/banner. For collated data from fan sites and forums, you may refer to the sources listed in each individual `.xlsx` file. 
