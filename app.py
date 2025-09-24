import sys
import os
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run


from src.CysProject.exception.exception import NetworkSecurityException
from src.CysProject.logging.logger import logging
from src.CysProject.pipeline.training_pipeline import TrainingPipeline
from src.CysProject.utils.gen_functions import load_object
from src.CysProject.utils.ml_utils.model.estimator import NetworkModel
from sqlalchemy import create_engine

# --- SQLite with SQLAlchemy ---
DB_PATH = "network_data.db"
TABLE_NAME = "NetworkData"
engine = create_engine(f"sqlite:///{DB_PATH}")

# --- FastAPI app ---
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        # (Optional) Example: fetch data from SQLite before training
        df = pd.read_sql_table(TABLE_NAME, con=engine)
        logging.info(f"Loaded {len(df)} records from SQLite for training")

        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        # Load model + preprocessor
        preprocessor = load_object("final_models/preprocessor.pkl")
        final_model = load_object("final_models/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        # Predict
        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred

        # Save prediction
        df.to_csv('prediction_output/output.csv', index=False)
        table_html = df.to_html(classes='table table-striped')

        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        raise NetworkSecurityException(e, sys)

if __name__=="__main__":
    app_run(app, host="0.0.0.0", port=8000)
