from __future__ import annotations
import os
from maleo_foundation.managers.client.base import ClientManager, ClientHTTPControllerManager, ClientControllerManagers
from maleo_foundation.types import BaseTypes
from maleo_foundation.utils.logging import SimpleConfig
from maleo_token.client.controllers.http import MaleoTokenHTTPController
from maleo_token.client.controllers import MaleoTokenControllers
from maleo_token.client.services import MaleoTokenServices

class MaleoTokenManager(ClientManager):
    def __init__(
            self,
            log_config:SimpleConfig,
            service_key:BaseTypes.OptionalString=None,
            url:BaseTypes.OptionalString=None
        ):
        key = "token-manager"
        name = "TokenManager"
        url = url or os.getenv("TOKEN_MANAGER_URL")
        if url is None:
            raise ValueError("'TOKEN_MANAGER_URL' variable must be set if 'url' is set to None")
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
        http_controller = MaleoTokenHTTPController(manager=self._controller_managers.http)
        self._controllers = MaleoTokenControllers(http=http_controller)

    @property
    def controllers(self) -> MaleoTokenControllers:
        return self._controllers

    def _initialize_services(self):
        self._services = MaleoTokenServices(logger=self._logger, controllers=self._controllers)

    @property
    def services(self) -> MaleoTokenServices:
        return self._services