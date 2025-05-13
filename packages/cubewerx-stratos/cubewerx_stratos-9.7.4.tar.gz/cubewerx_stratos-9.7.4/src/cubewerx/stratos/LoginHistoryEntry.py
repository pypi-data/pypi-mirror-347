# $Id: LoginHistoryEntry.py 78570 2025-01-23 18:57:06Z pomakis $

import datetime

from .OidUser import OidUser


class LoginHistoryEntry:
    """An entry of the login history.
    """

    def __init__(self, jsonRep: dict):
        timestampStr = jsonRep.get("timestamp")
        self.__timestamp = datetime.datetime.fromisoformat(timestampStr)
        self.__ipAddress = jsonRep.get("ipAddress")
        authUserVal = jsonRep.get("authUser")
        oidUserVal = jsonRep.get("oidUser")
        self.__user = authUserVal if authUserVal else OidUser(oidUserVal)

    @property
    def timestamp(self) -> datetime.datetime:
        """the date and time (in the server's time zone) of the login"""
        return self.__timestamp

    @property
    def ipAddress(self) -> str | None:
        """the IP address of the login, or None if unknown"""
        return self.__ipAddress

    @property
    def user(self) -> str | OidUser:
        """the user account the login, either a string representing the
        username of a CwAuth User or an OidUser object representing an
        OpenID Connect user"""
        return self.__user
