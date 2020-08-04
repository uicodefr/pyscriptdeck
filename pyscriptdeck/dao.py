from typing import List, Dict
from datetime import datetime
import bcrypt
from pyscriptdeck.config import getconfig
from pyscriptdeck import db


def db_commit():
    db.session.commit()

def _join_sql_for_list(sql_check, join_operator, data_list) -> str:
    sql = "( "
    sql += join_operator.join([sql_check + "_" + str(i) for i, data in enumerate(data_list)])
    sql += " )"
    return sql

def _get_param_for_list(param_name, data_list) -> Dict:
    params_sql = {}
    for i, data in enumerate(data_list):
        params_sql[param_name + "_" + str(i)] = data
    return params_sql

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)

class UserDao:
    @staticmethod
    def create_adminuser_if_necessary():
        admin = User.query.filter_by(username="admin").first()
        if admin is None:
            password = bcrypt.hashpw(getconfig()["app.defaultPassword"].encode(), bcrypt.gensalt())
            admin = User(username="admin", password=password, created_at=datetime.now())
            db.session.add(admin)
            db.session.commit()

    @staticmethod
    def find_by_username(username: str) -> User:
        return User.query.filter_by(username=username).first()

class ExecutionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    script_id = db.Column(db.String(255), nullable=False, index=True)
    run_at = db.Column(db.DateTime(), nullable=False, index=True)
    executed_by_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    executed_by = db.relationship(User)
    execution_success = db.Column(db.Boolean(), nullable=False)
    execution_message = db.Column(db.String(512), nullable=False)

    def dict(self) -> Dict:
        return {
            "id": self.id,
            "scriptId": self.script_id,
            "runAt": self.run_at.timestamp(),
            "executedBy": self.executed_by.username,
            "success": self.execution_success,
            "message": self.execution_message
        }

class ExecutionHistoryDao:
    @staticmethod
    def insert(execution_history: ExecutionHistory):
        db.session.add(execution_history)
        db.session.commit()

    @staticmethod
    def findall() -> List[ExecutionHistory]:
        return ExecutionHistory.query.order_by(ExecutionHistory.run_at.desc()).all()

    @staticmethod
    def findall_by_script_id(script_id: str, limit: int) -> List[ExecutionHistory]:
        return ExecutionHistory.query.filter_by(script_id=script_id) \
        .order_by(ExecutionHistory.run_at.desc()).limit(limit).all()

    @staticmethod
    def delete_older_than(date) -> int:
        sql = "DELETE FROM execution_history WHERE run_at < :date"
        return db.session.execute(sql, {"date": date}).rowcount

    @staticmethod
    def find_distinct_script_id() -> List[str]:
        sql = "SELECT DISTINCT script_id FROM execution_history"
        result = db.session.execute(sql)
        return list(map(lambda line: line[0], result))

    @staticmethod
    def delete_for_number(script_id: str, ids_to_keep: List[int]) -> int:
        sql = "DELETE FROM execution_history WHERE script_id = :script_id AND "
        sql += _join_sql_for_list("id != :ids_to_keep", " AND ", ids_to_keep)
        params = _get_param_for_list("ids_to_keep", ids_to_keep)
        params["script_id"] = script_id
        return db.session.execute(sql, params).rowcount

class Parameter(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255), nullable=False)

class ParameterDao:
    @staticmethod
    def init():
        if ParameterDao.find_by_id("general.status") is None:
            status_parameter = Parameter(id="general.status", value="true")
            db.session.add(status_parameter)
            db.session.commit()

    @staticmethod
    def find_by_id(id: str) -> Parameter:
        return Parameter.query.filter_by(id=id).first()
