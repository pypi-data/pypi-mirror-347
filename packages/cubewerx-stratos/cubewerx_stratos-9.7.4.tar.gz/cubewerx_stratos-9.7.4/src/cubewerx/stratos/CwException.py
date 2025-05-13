# $Id: CwException.py 78570 2025-01-23 18:57:06Z pomakis $

import requests


class CwException(Exception):
    """The base class for all CubeWerx-specific exceptions.
    """
    pass


class LoginException(CwException):
    """The base class for all exceptions related to logging in to a
    CubeWerx Stratos deployment.
    """
    pass


class NotAStratosException(LoginException):
    """Raised when an attempt is made to connect to a URL that doesn't
    appear to be a CubeWerx Stratos deployment.
    """
    def __init__(self):
        super().__init__("Not a CubeWerx Stratos deployment")


class IncompatibleStratosVersionException(LoginException):
    """Raised when an attempt is made to connect to a CubeWerx Stratos
    deployment whose version number is incompatible with this Python
    package.
    """
    def __init__(self, version: str, requiredVersion: str):
        parentheticalVersion = ("(%s) " % version) if version else ""
        super().__init__("Version number of CubeWerx Stratos deployment "
            "%sis too low; must be a %s" %
            (parentheticalVersion, requiredVersion))


class NotAnAuthServerException(LoginException):
    """Raised when the specified CubeWerx Stratos Authentication Server
    URL doesn't seem to point to a CubeWerx Stratos Authentication
    Server.
    """
    def __init__(self):
        super().__init__("Not a CubeWerx Stratos Authentication Server")


class AuthServerVersionTooLowException(LoginException):
    """Raised when an attempt is made to connect to a CubeWerx Stratos
    Authentication Server whose version number is too low.
    """
    def __init__(self, version: str, minVersion: str):
        parentheticalVersion = ("(%s) " % version) if version else ""
        super().__init__("Version number of CubeWerx Stratos Authentication "
            "Server %sis too low; must be at least %s" %
            (parentheticalVersion, minVersion))


class InvalidCredentialsException(LoginException):
    """Raised when an invalid CubeWerx Stratos username or password is
    provided.
    """
    def __init__(self):
        super().__init__("Invalid username or password")


class NotAdministratorException(LoginException):
    """Raised when the provided CubeWerx Stratos username and password
    is accepted, but the specified user doesn't have Administrator
    privileges.
    """
    def __init__(self, username: str):
        super().__init__('User "%s" does not have Administrator privileges' %
            username)


class LoginAttemptsTooFrequentException(LoginException):
    """Raised when login attempts to the specified username are being made
    too frequently.  Wait a few seconds and try again.
    """
    def __init__(self):
        super().__init__("Login attempts are being made too frequently")


class NoMoreSeatsException(LoginException):
    """Raised when no more seats are available for the specified username.
    Not applicable for most deployments.
    """
    def __init__(self, username: str):
        super().__init__('No more seats are available for user "%s"' %
            username)


class ServerException(CwException):
    """Raised when the CubeWerx Stratos deployment returns an error.
    Provides a detailed error report.
    """
    def __init__(self, httpError: requests.exceptions.HTTPError,
            title: str | None, httpStatus: int, details: list[str],
            moreInfoUrl: str | None):
        self.__httpError = httpError
        self.__title = title
        self.__httpStatus = httpStatus
        self.__details = details
        self.__moreInfoUrl = moreInfoUrl

    @property
    def httpError(self) -> requests.exceptions.HTTPError:
        """the HTTPError object describing the error response"""
        return self.__httpError

    @property
    def title(self) -> str | None:
        """the title of the error report, or None"""
        return self.__title

    @property
    def httpStatus(self) -> int:
        """the HTTP status code of the error"""
        return self.__httpStatus

    @property
    def details(self) -> list[str]:
        """an array of strings describing the error, from most general
        to most specific"""
        return self.__details

    @property
    def moreInfoUrl(self) -> str | None:
        """a URL that provides more information about the error and the
        request that triggered it, or None"""
        return self.__moreInfoUrl

    def __str__(self):
        exceptionText = str(self.httpError)
        for detail in self.details:
            exceptionText += ("\nDetail: %s" % detail)
        if self.moreInfoUrl:
            exceptionText += ('\nSee "%s" for more information' %
                              self.moreInfoUrl)
        return exceptionText

    @staticmethod
    def raise_for_status(response: requests.Response):
        httpError = None
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            httpError = e

        if httpError:
            contentType = response.headers['Content-Type']
            if contentType == "application/problem+json":
                responseJson = response.json()
                title = responseJson.get("title")
                httpStatus = responseJson.get("status")
                if not httpStatus: httpStatus = response.status_code
                details = []
                detailsObjs = responseJson.get("details")
                if detailsObjs:
                    for detailObj in detailsObjs:
                        detail = detailObj.get("description")
                        if detail: details.append(detail)
                else:
                    detail = responseJson.get("detail")
                    if detail: details.append(detail)
                instanceUrl = responseJson.get("instance")

                raise ServerException(httpError, title, httpStatus,
                    details, instanceUrl)
            else:
                raise httpError

