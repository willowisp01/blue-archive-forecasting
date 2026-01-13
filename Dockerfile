# Use Miniconda as base image
FROM continuumio/miniconda3:latest

# Set working directory
WORKDIR /app

COPY environment.yml .

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "ba-forecasting", "/bin/bash", "-c"]

COPY . .

EXPOSE 8000

# Run Uvicorn inside the Conda environment
CMD ["conda", "run", "--no-capture-output", "-n", "ba-forecasting", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
