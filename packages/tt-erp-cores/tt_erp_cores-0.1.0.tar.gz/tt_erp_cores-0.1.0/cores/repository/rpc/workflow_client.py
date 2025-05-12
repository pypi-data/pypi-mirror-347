import json

from cores.component.client import ClientBase
from cores.helpers import helper


class WorkflowClient(ClientBase):
    async def get_by_type(self):
        f = helper.open_file_as_root_path("workflow.json")
        # f = open('workflow.json')
        data = json.load(f)
        f.close()
        return data
        # return await self.curl_api('GET', '/api/current-user')
