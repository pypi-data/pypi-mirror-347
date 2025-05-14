from __future__ import annotations
from pydantic import Field
from maleo_foundation.managers.client.base import ClientServiceControllers, ClientControllers

from maleo_access.token.controllers.http.authentication import MaleoAccessAuthenticationHTTPController
class MaleoAccessAuthenticationControllers(ClientServiceControllers):
    http:MaleoAccessAuthenticationHTTPController = Field(..., description="Authentication's http controller")

class MaleoAccessControllers(ClientControllers):
    authentication:MaleoAccessAuthenticationControllers = Field(..., description="Authentication's controllers")