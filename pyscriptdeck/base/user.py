import bcrypt
from pyscriptdeck.common import ScriptDeck, ScriptDescription, ScriptResult
from pyscriptdeck.dao import UserDao, db_commit


class ChangePassword(ScriptDeck):
    """ Change password for the main user """
    def __init__(self):
        super().__init__(__name__)

    def get_description(self):
        return ScriptDescription(
            group="base", name="Change main password",
            description="Change the password for the main user",
            params=[{
                "id": "password",
                "type": "password",
                "label": "New password",
                "default": ""
            }, {
                "id": "password_confirm",
                "type": "password",
                "label": "Confirm password",
                "default": ""
            }]
        )

    def run(self, data_input):
        password = data_input["password"]
        password_confirm = data_input["password_confirm"]

        if len(password) < 5:
            return ScriptResult(success=False, message="The minimum length is 5")
        if password != password_confirm:
            return ScriptResult(success=False, message="The passwords does not match")

        user = UserDao.find_by_username("admin")
        if user is None:
            return ScriptResult(success=False, message="User not found")

        user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        db_commit()

        return ScriptResult(success=True, message="Password Updated")
