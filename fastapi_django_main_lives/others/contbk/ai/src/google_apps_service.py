from google_apps_script import GoogleAppsScript

class GoogleAppsService:
    def __init__(self, script_id):
        self.script = GoogleAppsScript(script_id)

    def execute_script(self, function_name, params):
        return self.script.execute_script(function_name, params)