from fastapi import FastAPI, HTTPException
from uuid import uuid4
from mangum import Mangum

from app.models import JobApplication
from app.database import table


app = FastAPI(
    title="Job Application Tracker API",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/applications")
def create_application(application: JobApplication):

    application_id = str(uuid4())

    item = {
        "id": application_id,
        "company": application.company,
        "role": application.role,
        "status": application.status,
        "location": application.location,
        "date_applied": application.date_applied
    }

    try:
        table.put_item(Item=item)

        return {
            "message": "Application created successfully",
            "application": item
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.get("/applications")
def get_applications():

    try:
        response = table.scan()

        return {
            "applications": response.get("Items", [])
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
    
@app.get("/applications/{application_id}")
def get_application(application_id: str):

    try:
        response = table.get_item(
            Key={
                "id": application_id
            }
        )

        item = response.get("Item")

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Application not found"
            )

        return {
            "application": item
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
    
@app.put("/applications/{application_id}")
def update_application(
    application_id: str,
    application: JobApplication
):
    try:
        existing = table.get_item(
            Key={"id": application_id}
        ).get("Item")

        if not existing:
            raise HTTPException(
                status_code=404,
                detail="Application not found"
            )

        updated_item = {
            "id": application_id,
            "company": application.company,
            "role": application.role,
            "status": application.status,
            "location": application.location,
            "date_applied": application.date_applied
        }

        table.put_item(Item=updated_item)

        return {
            "message": "Application updated successfully",
            "application": updated_item
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
    
@app.delete("/applications/{application_id}")
def delete_application(application_id: str):
    try:
        existing = table.get_item(
            Key={"id": application_id}
        ).get("Item")

        if not existing:
            raise HTTPException(
                status_code=404,
                detail="Application not found"
            )

        table.delete_item(
            Key={"id": application_id}
        )

        return {
            "message": "Application deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

handler = Mangum(app)