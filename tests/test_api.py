from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

import app.main as main_module


client = TestClient(main_module.app)


@pytest.fixture
def mock_table(monkeypatch):
    table = MagicMock()

    monkeypatch.setattr(
        main_module,
        "table",
        table
    )

    return table


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_invalid_application_status():
    response = client.post(
        "/applications",
        json={
            "company": "National Grid",
            "role": "Python Developer",
            "status": "Waiting",
            "location": "UK",
            "date_applied": "2026-10-04"
        }
    )

    assert response.status_code == 422


def test_create_application(mock_table):
    response = client.post(
        "/applications",
        json={
            "company": "National Grid",
            "role": "Python Developer",
            "status": "Applied",
            "location": "UK",
            "date_applied": "2026-10-04"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Application created successfully"

    assert data["application"]["company"] == "National Grid"

    assert data["application"]["status"] == "Applied"

    assert "id" in data["application"]

    mock_table.put_item.assert_called_once()


def test_get_applications(mock_table):
    mock_table.scan.return_value = {
        "Items": [
            {
                "id": "123",
                "company": "National Grid",
                "role": "Python Developer",
                "status": "Applied",
                "location": "UK",
                "date_applied": "2026-10-04"
            }
        ]
    }

    response = client.get("/applications")

    assert response.status_code == 200

    data = response.json()

    assert len(data["applications"]) == 1

    assert data["applications"][0]["company"] == "National Grid"

    mock_table.scan.assert_called_once()


def test_get_application_by_id(mock_table):
    mock_table.get_item.return_value = {
        "Item": {
            "id": "123",
            "company": "National Grid",
            "role": "Python Developer",
            "status": "Applied",
            "location": "UK",
            "date_applied": "2026-10-04"
        }
    }

    response = client.get("/applications/123")

    assert response.status_code == 200

    assert response.json()["application"]["id"] == "123"

    mock_table.get_item.assert_called_once_with(
        Key={"id": "123"}
    )


def test_update_application(mock_table):
    mock_table.get_item.return_value = {
        "Item": {
            "id": "123",
            "company": "National Grid",
            "role": "Python Developer",
            "status": "Applied"
        }
    }

    response = client.put(
        "/applications/123",
        json={
            "company": "National Grid",
            "role": "Python Developer",
            "status": "Interview",
            "location": "UK",
            "date_applied": "2026-10-04"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Application updated successfully"

    assert data["application"]["status"] == "Interview"

    mock_table.put_item.assert_called_once()


def test_delete_application(mock_table):
    mock_table.get_item.return_value = {
        "Item": {
            "id": "123",
            "company": "National Grid"
        }
    }

    response = client.delete("/applications/123")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Application deleted successfully"
    }

    mock_table.delete_item.assert_called_once_with(
        Key={"id": "123"}
    )