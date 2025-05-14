import logging

import requests

logger = logging.getLogger(__name__)


class ModelManageClient:
    def __init__(self, base_url: str, client_token: str):
        self.base_url = base_url if base_url.endswith("/v1.0") else base_url + "/v1.0"
        self.client_token = client_token

    def _send_request(self, method, endpoint, json=None, params=None, stream=False):
        headers = {
            "Authorization": f"Bearer {self.client_token}",
            "Content-Type": "application/json",
        }
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, json=json, params=params, headers=headers, stream=stream)

        return response

    def register_agent(self, agent_name, agent_id, agent_url, **kargs):
        if not agent_name:
            raise ValueError("agent_name is required")
        if not agent_id:
            raise ValueError("agent_id is required")
        if not agent_url:
            raise ValueError("agent_url is required")

        args = {
            "agent_name": agent_name,
            "agent_id": agent_id,
            "agent_url": agent_url,
            **kargs,
        }
        response = self._send_request("POST", "/agents", json=args)
        if response.status_code != 200:
            raise ValueError(f"register agent failed: {response.text}")
        logger.info("register agent success......")

    def get_agent(self, agent_name):
        if not agent_name:
            raise ValueError("agent_name is required")

        response = self._send_request("GET", "/agents", params={"agent_name": agent_name})
        if response.status_code != 200 and response.status_code != 404:
            raise ValueError(f"get agent failed: {response.text}")
        if response.status_code == 404:
            return None
        return response.json()

    def delete_agent(self, agent_name):
        if not agent_name:
            raise ValueError("agent_name is required")

        response = self._send_request("DELETE", "/agents", params={"agent_name": agent_name})
        if response.status_code != 200:
            raise ValueError(f"delete agent failed: {response.text}")
        logging.info("delete agent success......")

    def get_model_credentials(self, provider: str, model_type: str) -> dict:
        if not provider:
            raise ValueError("provider is required")
        if not model_type:
            raise ValueError("model_type is required")
        response = self._send_request(
            "GET", f"/model-providers/{provider}", params={"model_type": model_type}
        )

        if response.status_code != 200:
            raise ValueError(f"get model credentials failed: {response.text}")
        return response.json()
