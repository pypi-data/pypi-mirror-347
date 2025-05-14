from __future__ import annotations
from maleo_foundation.managers.client.maleo import MaleoClientManager
from maleo_foundation.managers.service import ServiceManager
from maleo_access.client.controllers.http.authentication import MaleoAccessAuthenticationHTTPController
from maleo_access.client.controllers import (
    MaleoAccessAuthenticationControllers,
    MaleoAccessControllers
)
from maleo_access.client.services import (
    MaleoAccessAuthenticationClientService,
    MaleoAccessServices
)

class MaleoAccessClientManager(MaleoClientManager):
    def __init__(self, service_manager:ServiceManager):
        key = service_manager.configs.client.maleo.access.key
        name = service_manager.configs.client.maleo.access.name
        url = service_manager.configs.client.maleo.access.url
        super().__init__(key, name, url, service_manager)
        self._initialize_controllers()
        self._initialize_services()
        self._logger.info("Client manager initialized successfully")

    def _initialize_controllers(self):
        super()._initialize_controllers()
        #* Authentication controllers
        authentication_http_controller = MaleoAccessAuthenticationHTTPController(service_manager=self.service_manager, manager=self._controller_managers.http)
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