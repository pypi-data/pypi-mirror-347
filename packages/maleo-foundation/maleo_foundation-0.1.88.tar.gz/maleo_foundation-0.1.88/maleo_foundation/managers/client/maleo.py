from pydantic import Field
from maleo_foundation.types import BaseTypes
from maleo_foundation.managers.client.base import ClientManager, ClientHTTPControllerManager, ClientControllerManagers, ClientHTTPController, ClientServiceControllers, ClientControllers
from maleo_foundation.managers.service import ServiceManager

class MaleoClientHTTPController(ClientHTTPController):
    def __init__(self, service_manager:ServiceManager, manager:ClientHTTPControllerManager):
        self._service_manager = service_manager
        super().__init__(manager)

    @property
    def service_manager(self) -> ServiceManager:
        return self._service_manager

class MaleoClientServiceControllers(ClientServiceControllers):
    http:MaleoClientHTTPController = Field(..., description="Maleo's HTTP Client Controller")

    class Config:
        arbitrary_types_allowed=True

class MaleoClientManager(ClientManager):
    def __init__(
        self,
        key:str,
        name:str,
        service_manager:ServiceManager,
        url:BaseTypes.OptionalString = None
    ):
        self._url = url
        self._service_manager = service_manager
        super().__init__(key, name, service_manager.log_config, service_manager.configs.service.key)

    @property
    def service_manager(self) -> ServiceManager:
        return self._service_manager

    def _initialize_controllers(self) -> None:
        if self._url is None:
            raise ValueError("'URL' must not be None if initializing controllers")
        #* Initialize managers
        http_controller_manager = ClientHTTPControllerManager(url=self._url)
        self._controller_managers = ClientControllerManagers(http=http_controller_manager)
        #* Initialize controllers
        #! This initialied an empty controllers. Extend this function in the actual class to initialize all controllers.
        self._controllers = ClientControllers()

    @property
    def controllers(self) -> ClientControllers:
        return self._controllers

    async def dispose(self) -> None:
        self._logger.info("Disposing client manager")
        if self._controller_managers is not None:
            if self._controller_managers.http is not None:
                await self._controller_managers.http.dispose()
        self._logger.info("Client manager disposed successfully")