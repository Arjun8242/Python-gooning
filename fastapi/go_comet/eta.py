from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/eta")
def calculate_eta(distance: float, average_speed: float, delay: int):
    if distance<0:
        return HTTPException(status_code = 400,
        detail= "Invalid distance")
    if average_speed<=0:
        return HTTPException(status_code=400,
        detail="Invalid average speed")
    if delay <0:
        return HTTPException(status_code=400,
        detail="Invalid delay")

    time = distance/average_speed
    delay_hours = delay/60
    total_hours = time+delay_hours
    hours = int(total_hours)
    minutes = int((total_hours-hours)*60)
    return {"eta": f"{hours} hours and {minutes} minutes",
    "status_code": 200}

    