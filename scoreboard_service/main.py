from fastapi import FastAPI

app = FastAPI()

# Some minimal endpoint
@app.get("/")
def root():
    return {"message": "Scoreboard service up!"}
