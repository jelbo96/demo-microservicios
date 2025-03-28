from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime
from services.influx_service import fetch_data_from_influx
from models.database import database
from models.models import alerts, AlertType

router = APIRouter()

class ProcessRequest(BaseModel):
    version: Literal[1, 2]
    timeSearch: str

@router.post("/process")
async def process_alerts(request: ProcessRequest):
    tables, error = fetch_data_from_influx(request.version, request.timeSearch)
    
    if error:
        raise HTTPException(status_code=500, detail=f"Error al consultar InfluxDB: {error}")

    rows = []
    for table in tables:
        for record in table.records:
            value = float(record.get_value())
            timestamp = record.get_time()

            if request.version == 1:
                if value > 800:
                    alert_type = AlertType.ALTA
                elif value > 500:
                    alert_type = AlertType.MEDIA
                elif value > 200:
                    alert_type = AlertType.BAJA
                else:
                    continue
            else:  # Versión 2
                if value < 200:
                    alert_type = AlertType.ALTA
                elif value < 500:
                    alert_type = AlertType.MEDIA
                elif value < 800:
                    alert_type = AlertType.BAJA
                else:
                    continue

            rows.append({
                "datetime": timestamp,
                "value": value,
                "version": request.version,
                "type": alert_type,
                "sended": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            })

    if rows:
        query = alerts.insert().values(rows)
        await database.execute(query)

    return {"status": "ok"}


class SearchRequest(BaseModel):
    version: int
    type: Optional[Literal["BAJA", "MEDIA", "ALTA"]] = None
    sended: Optional[bool] = None


@router.post("/search")
async def search_alerts(request: SearchRequest):
    try:
        query = alerts.select().where(alerts.c.version == request.version)

        if request.type:
            query = query.where(alerts.c.type == request.type)
        if request.sended is not None:
            query = query.where(alerts.c.sended == request.sended)

        results = await database.fetch_all(query)

        alerts_list = [
            {
                "datetime": row["datetime"].strftime("%Y-%m-%d %H:%M:%S"),
                "value": row["value"],
                "version": row["version"],
                "type": row["type"],
                "sended": row["sended"],
            }
            for row in results
        ]

        return alerts_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
   
   
class SendRequest(BaseModel):
    version: int
    type: Literal["BAJA", "MEDIA", "ALTA"]
 
    
@router.post("/send")
async def send_alerts(request: SendRequest):
    try:
        query = alerts.select().where(
            (alerts.c.version == request.version) & 
            (alerts.c.type == request.type) & 
            (alerts.c.sended == False)  
        )

        results = await database.fetch_all(query)

        if not results:
            return {"status": "No hay alertas pendientes de envío"}

        update_query = (
            alerts.update()
            .where(
                (alerts.c.version == request.version) & 
                (alerts.c.type == request.type) & 
                (alerts.c.sended == False)
            )
            .values(sended=True)
        )

        await database.execute(update_query)

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")