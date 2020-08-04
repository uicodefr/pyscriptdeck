from datetime import datetime, date
from tests.test_base import app, client, login
from pyscriptdeck.dao import ExecutionHistory, ExecutionHistoryDao


_SCRIPT_ID = "pyscriptdeck.base.execution.CleanHistory"

def test_clean_history(app, client):
    with app.app_context():
        for _ in range(25):
            ExecutionHistoryDao.insert(ExecutionHistory(
                script_id="fakeNumber",
                run_at=datetime.now(),
                executed_by_id=1,
                execution_success=False,
                execution_message="Message for clean by number"
            ))

        ExecutionHistoryDao.insert(ExecutionHistory(
            script_id="fakeDate",
            run_at=datetime(year=2020, month=1, day=1),
            executed_by_id=1,
            execution_success=False,
            execution_message="Message for clean by date"
        ))
        ExecutionHistoryDao.insert(ExecutionHistory(
            script_id="fakeDate",
            run_at=datetime(year=2020, month=2, day=1),
            executed_by_id=1,
            execution_success=False,
            execution_message="Message for clean by date"
        ))
        ExecutionHistoryDao.insert(ExecutionHistory(
            script_id="fakeDate",
            run_at=datetime.now(),
            executed_by_id=1,
            execution_success=False,
            execution_message="Message for clean by date"
        ))

    login(client)
    response = client.get("/api/executions")
    assert response.status_code == 200
    # 25 fakeNumber + 3 fakeDate
    assert len(response.json) == 28

    data = {"clean_type": "incorrect"}
    response = client.post("/api/scripts/" + _SCRIPT_ID + "/_run", json=data)
    assert not response.json["success"]
    assert response.json["message"] == "Unknown clean_type : incorrect"
    response = client.get("/api/executions")
    # 25 fakeNumber + 3 fakeDate + 1 CleanHistory
    assert len(response.json) == 29

    data = {"clean_type": "by_number", "clean_number": 10}
    response = client.post("/api/scripts/" + _SCRIPT_ID + "/_run", json=data)
    assert response.json["success"]
    assert response.json["message"] == "Clean {} by number with the value : {}".format(15, 10)
    response = client.get("/api/executions")
    # 10 fakeNumber + 3 fakeDate + 2 CleanHistory
    assert len(response.json) == 15

    clean_date = date.today().isoformat()
    data = {"clean_type": "by_date", "clean_date": clean_date}
    response = client.post("/api/scripts/" + _SCRIPT_ID + "/_run", json=data)
    assert response.json["success"]
    assert response.json["message"] == "Clean {} by date with the value : {}".format(2, clean_date)
    response = client.get("/api/executions")
    # 10 fakeNumber + 1 fakeDate + 3 CleanHistory
    assert len(response.json) == 14
