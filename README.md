# Blue Archive Revenue Forecasting Model

# About this Project

Blue Archive is a role-playing game (RPG) about helping students from various academies resolve problems through story-driven narratives and combat scenarios. The aim of this notebook is to predict the 6-month future revenue of this game using features such as character banners (opportunities to obtain characters), events, and story releases. 

Data from various fan sites, online forums, and unofficial APIs were used to collate training data. A hybrid model consisting of spline + XGB (Extreme Gradient Boosting) is used. The spline models the overall trend in revenue, whereas XGB captures all other information apart from the trend. For instance, cycles and seasonality. 

# How to Run 

Using Anaconda, set up a conda environment using the `environment.yml` file. After which, it should be as simple as running all cells in the notebook `analysis.ipynb`. Doing that will 
* load in data from the API
* format raw data 
* train the model
* produce results and visualizations (etc). 

If any API cannot be reached, or the data is invalid for whatever reason, a serialized record of the API data will be loaded instead (see `*.pkl` files.) For reproducability, trained models have also be serialized (see `trend_model.joblib` and `xgb_residual_model.joblib`).

# Summary of Results

The hybrid model predicted a 6 month forecast accurately (with an outlier of the first month forecast). The MAE was 1.2 million excluding that forecast, about 6% of the maximum observed monthly revenue of 19 million. The model also achieved directional accuracy of 100% (i.e. the model correctly predicts whether revenue will go up or down) for that forecast of 6 months.

# Resources Used

The API used was https://api.ennead.cc/buruaka/banner. For collated data from fan sites and forums, you may refer to the sources listed in each individual `.xlsx` file. 
