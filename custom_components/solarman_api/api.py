"""Solarman API."""

import hashlib
import time
from typing import Any, cast

import aiohttp


class SolarmanApiClient:
    """Solarman API client."""

    exiration_time: float
    access_token: str | None

    def __init__(
        self,
        session: aiohttp.ClientSession,
        email: str,
        password: str,
        application_id: str,
        application_secret: str,
    ) -> None:
        """Initialize."""
        self.session = session
        self.email = email
        self.password = password
        self.application_id = application_id
        self.application_secret = application_secret
        self.exiration_time = 0
        self.access_token = None

    async def fetch_token(self) -> None:
        """Fetch new authorization token."""

        passhash = hashlib.sha256(self.password.encode()).hexdigest()
        data = {
            "appSecret": self.application_secret,
            "email": self.email,
            "password": passhash,
        }
        async with self.session.post(
            f"https://globalapi.solarmanpv.com/account/v1.0/token?appId={self.application_id}",
            json=data,
        ) as response:
            json = await response.json()
            if not json["success"]:
                if json["code"] == "2101021":
                    raise InvalidApplicationIdError(json["msg"])
                if json["code"] == "2101019":
                    raise InvalidApplicationSecretError(json["msg"])
                if json["code"] == "2101025":
                    raise InvalidEmailOrPasswordSecretError
                raise ApiError(json["msg"])

            self.exiration_time = time.time() + float(json["expires_in"]) - 60
            self.access_token = json["access_token"]

    async def get_token(self) -> str:
        """Get a valid authorization token."""
        if time.time() >= self.exiration_time:
            await self.fetch_token()

        if self.access_token is None:
            status = "could not get access token"
            raise AuthenticationError(status)
        return self.access_token

    async def get_data(self, device_serial_number: str) -> dict[str, Any]:
        """Fetch data for device."""

        token = await self.get_token()
        data = {"deviceSn": device_serial_number}
        headers = {"Authorization": "Bearer " + token}
        async with self.session.post(
            "https://globalapi.solarmanpv.com/device/v1.0/currentData",
            json=data,
            headers=headers,
        ) as response:
            json = await response.json()
            if not json["success"]:
                if json["code"] == "2101008":
                    raise InvalidDeviceSerialNumberError(json["msg"])
                if json["code"] == "2101016":
                    raise InvalidDeviceSerialNumberError(json["msg"])
                raise ApiError(json["msg"])
            return cast(dict[str, Any], json)


class SolarmanError(Exception):
    """Base class for Solarman errors."""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status


class ApiError(SolarmanError):
    """Raised when Solarman API request ended in error."""


class AuthenticationError(ApiError):
    """Raised when on authentication failure."""


class InvalidApplicationIdError(AuthenticationError):
    """Raised when an invalid application ID is provided."""


class InvalidApplicationSecretError(AuthenticationError):
    """Raised when an invalid application secret is provided."""


class InvalidEmailOrPasswordSecretError(AuthenticationError):
    """Raised when an invalid email or password is provided."""

    def __init__(self) -> None:
        """Initialize."""
        super().__init__("invalid email or password")


class InvalidDeviceSerialNumberError(ApiError):
    """Raised when an invalid device serial number is provided."""
