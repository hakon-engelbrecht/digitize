from fastapi import FastAPI, UploadFile, File
import matplotlib.image as mpimg
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from main import calculate_sums, process_accounting_data, check_database_data, load_data_from_database, process_file, save_data_to_database, validate_data, detect_duplicates, correct_data, process_excel_to_db, visualize_data

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/get_data")
async def get_data():
    data = load_data_from_database()
    data = validate_data(data)
    data = detect_duplicates(data)
    data = correct_data(data)
    return data.to_dict(orient='records')

@app.get("/get_plot")
async def get_plot():
    data = load_data_from_database()
    sums = calculate_sums(data)
    return sums.to_dict()

@app.post("/upload_data")
async def post_data(file: UploadFile):
    print(file.filename)
    process_file(file)

if __name__ == "__main__":
    process_excel_to_db('Buchhaltungsdaten.xlsx')
    uvicorn.run(app, host="0.0.0.0", port=5000)
