from __future__ import annotations
import os
from maleo_foundation.managers.client.base import ClientManager, ClientHTTPControllerManager, ClientControllerManagers
from maleo_foundation.types import BaseTypes
from maleo_foundation.utils.logging import SimpleConfig
from maleo_access.token.controllers.http.authentication import MaleoAccessAuthenticationHTTPController
from maleo_access.token.controllers import (
    MaleoAccessAuthenticationControllers,
    MaleoAccessControllers
)
from maleo_access.token.services import (
    MaleoAccessAuthenticationClientService,
    MaleoAccessServices
)

class MaleoAccessTokenManager(ClientManager):
    def __init__(self, log_config:SimpleConfig, service_key:BaseTypes.OptionalString=None):
        key = "token-manager"
        name = "TokenManager"
        url = os.getenv("TOKEN_MANAGER_URL")
        if url is None:
            raise ValueError("'TOKEN_MANAGER_URL' variable must be set")
        self._url = url
        super().__init__(key, name, log_config, service_key)
        self._initialize_controllers()
        self._initialize_services()
        self._logger.info("Client manager initialized successfully")

    def _initialize_controllers(self):
        #* Initialize managers
        http_controller_manager = ClientHTTPControllerManager(url=self._url)
        self._controller_managers = ClientControllerManagers(http=http_controller_manager)
        #* Initialize controllers
        #* Authentication controllers
        authentication_http_controller = MaleoAccessAuthenticationHTTPController(manager=self._controller_managers.http)
        authentication_controllers = MaleoAccessAuthenticationControllers(http=authentication_http_controller)
        #* All controllers
        self._controllers = MaleoAccessControllers(
            authentication=authentication_controllers,
        )

    @property
    def controllers(self) -> MaleoAccessControllers:
        return self._controllers

    def _initialize_services(self):
        super()._initialize_services()
        authentication_service = MaleoAccessAuthenticationClientService(logger=self._logger, controllers=self._controllers.authentication)
        self._services = MaleoAccessServices(
            authentication=authentication_service,
        )

    @property
    def services(self) -> MaleoAccessServices:
        return self._services