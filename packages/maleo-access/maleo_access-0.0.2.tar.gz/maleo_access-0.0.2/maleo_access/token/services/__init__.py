from __future__ import annotations
from pydantic import Field
from maleo_foundation.managers.client.base import ClientServices
from maleo_access.token.services.authentication import MaleoAccessAuthenticationClientService

class MaleoAccessServices(ClientServices):
    authentication:MaleoAccessAuthenticationClientService = Field(..., description="Authentication's service")