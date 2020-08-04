from datetime import date, timedelta
from pyscriptdeck.common import ScriptDeck, ScriptDescription, ScriptResult
from pyscriptdeck.dao import ExecutionHistoryDao


class CleanHistory(ScriptDeck):
    """ Clean the history of the execution """
    def __init__(self):
        super(CleanHistory, self).__init__(__name__)

    def get_description(self):
        return ScriptDescription(
            group="base", name="Clean execution history",
            description="Clean by number OR by date",
            params=[{
                "id": "clean_type",
                "type": "radio",
                "label": "Clean by number or by date",
                "values": [
                    {"value": "by_number", "label": "By number"},
                    {"value": "by_date", "label": "By date"}
                ],
                "default": "by_number"
            }, {}, {
                "id": "clean_number",
                "type": "number",
                "label": "Execution history to keep by script (older are deleted)",
                "default": "20"
            }, {
                "id": "clean_date",
                "type": "date",
                "label": "Execution history to delete older than a date",
                "default": (date.today() - timedelta(days=30)).isoformat()
            }]
        )

    def run(self, data_input):
        clean_type = data_input["clean_type"]

        if clean_type == "by_number":
            clean_number = data_input["clean_number"]
            script_id_list = ExecutionHistoryDao.find_distinct_script_id()
            deleted_count = 0
            for script_id in script_id_list:
                result_to_keep = ExecutionHistoryDao.findall_by_script_id(script_id, clean_number)
                ids_to_keep = list(map(lambda exec_history: exec_history.id, result_to_keep))
                if ids_to_keep:
                    deleted_count += ExecutionHistoryDao.delete_for_number(script_id, ids_to_keep)

            message = "Clean {} by number with the value : {}".format(deleted_count, clean_number)
            return ScriptResult(success=True, message=message)

        if clean_type == "by_date":
            clean_date = data_input["clean_date"]
            deleted_count = ExecutionHistoryDao.delete_older_than(clean_date)
            message = "Clean {} by date with the value : {}".format(deleted_count, clean_date)
            return ScriptResult(success=True, message=message)

        return ScriptResult(success=False, message="Unknown clean_type : {}".format(clean_type))
