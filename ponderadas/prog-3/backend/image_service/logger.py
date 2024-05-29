import requests
import datetime
from decouple import config
from pydantic import BaseModel


class LogEntry(BaseModel):
    service: str
    user_id: str
    action: str
    result: str
    cause: str = None
    timestamp: datetime.datetime = None


class LoggerClient:
    def __init__(self, service: str, route: str):
        self._serverOk = False
        self._first_logged = False
        self.url = config("LOG_SERVICE_URL", default="")
        self.service = service
        self.route = route

    async def _first_log(self):
        await self._verify_server_ok()

        print("First logging...")
        log_entry = LogEntry(
            service=self.service,
            user_id="System",
            action="Starting_logger",
            result="Success",
            cause=None,
        )

        await self._request(log_entry=log_entry)
        self._first_logged = True

    async def log(
        self,
        user_id: str,
        action: str,
        result: str = "Success",
        cause: str = None,
    ) -> None:
        """make a log

        Args:
            user_id (str): responsible of the log
            action (str): action to be performed
            result (str, optional): result of the action. Defaults to "Success".
            cause (str, optional): cause of error (if result is'n "Success"). Defaults to None.
        """
        if not self._first_logged:
            await self._first_log()

        log_entry = LogEntry(
            service=self.service,
            user_id=user_id,
            action=action,
            result=result,
            cause=cause,
        )

        if self._serverOk:
            await self._request(log_entry=log_entry)
        else:
            await self._verify_server_ok()

        print("server_status: ", self._serverOk, " log: ", log_entry)

    async def _request(self, log_entry: LogEntry):
        """Make a request to the logger server and

        Args:
            log_entry (LogEntry): log_entry.

        Returns:
            json: response form the logger server
        """
        response = requests.post(
            f"{self.url}/{self.route}",
            json=log_entry.dict(),
        )

        if response.status_code != 200:
            print(f"Failed to log action: {response.content}")
            await self._verify_server_ok()

        return response

    async def _ping(self):
        """Ping the logger server

        Returns:
            dict: response from the server
        """
        response = requests.post(f"{self.url}/ping")
        return response

    async def _verify_server_ok(self) -> None:
        """verify if has a logger server

        Returns:
            bool: true if server is ok, otherwise false
        """
        print("Pinging...")
        response = await self._ping()

        self._serverOk = True if response.status_code == 200 else False
