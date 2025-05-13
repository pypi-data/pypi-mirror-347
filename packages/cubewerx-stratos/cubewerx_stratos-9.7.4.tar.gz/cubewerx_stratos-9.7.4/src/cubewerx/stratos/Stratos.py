# $Id: Stratos.py 78775 2025-03-13 21:14:08Z pomakis $

import validators
import requests
import datetime
from urllib.parse import quote

from .Stats import *
from .RequestHistory import *
from .LoginHistoryEntry import *
from .ConfigParam import *
from .AuthUser import *
from .OidUser import *
from .Role import *
from .ApiKey import *
from .Quota import *
from .CubeSTOR import *
from .DataStore import *
from .CwException import *


class Stratos:
    """The CubeWerx Stratos Administration Interface.

    ARGUMENTS:
        deploymentUrl - the URL of a CubeWerx Stratos deployment; e.g.,
            "https://somewhere.com/cubewerx/"
        username - the username (with an Administrator role) to log in as
        password - the password of the specified username
        authUrl (optional) - the URL of the CubeWerx Stratos Authentication
            Server to use, if not the one provided by the specified
            deployment; e.g., "https://somewhereelse.com/cubewerx/auth"
    NOTABLE RAISES:
        LoginException - the login is unsuccessful; subclasses are:
            NotAStratosException - the specified deploymentUrl is not a
                CubeWerx Stratos deployment
            IncompatibleStratosVersionException - the CubeWerx Stratos
                deployment is not of a compatible version
            NotAnAuthServerException - the specified authUrl is not a
                CubeWerx Stratos Authentication Server
            AuthServerVersionTooLowException - the version number of the
                CubeWerx Stratos Authentication Server is too low
            InvalidCredentialsException - invalid username or password
            NotAdministratorException - the user does not have
                Administrator privileges
            LoginAttemptsTooFrequentException - login attempts are being
                made too frequently
            NoMoreSeatsException - no more seats are available for the
                user (not applicable for most deployments)
        (and many others)
    """

    def __init__(self, deploymentUrl: str, username: str, password: str,
                 authUrl: str=None):
        # Append a trailing "/" to the deployment URL if necessary.
        if not deploymentUrl.endswith("/"): deploymentUrl += "/"

        # Verify arguments.
        if not validators.url(deploymentUrl):
            raise ValueError("Invalid deployment URL")
        if authUrl and not validators.url(authUrl):
            raise ValueError("Invalid authentication-server URL")
        if not username:
            raise ValueError("No username provided")

        # Verify that the specified deploymentUrl actually points to a
        # CubeWerx Stratos of a compatible version.  Since there's no
        # guarantee that future versions of CubeWerx Stratos will behave
        # the same way as 9.8 (or the 9.7 development stream leading up
        # to it), we have little choice but to only consider 9.7.x or
        # 9.8.x as compatible versions.
        response = requests.get(deploymentUrl + "cubeserv/default/alive")
        if response.status_code != 200: raise NotAStratosException()
        cwVersion = response.headers.get("CubeWerx-Stratos-Version")
        if not cwVersion:
            cwVersion = response.headers.get("CubeWerx-Suite-Version")
        if not cwVersion:  # earlier versions didn't provide this header
            raise IncompatibleStratosVersionException(None, "9.8.x")
        else:
            xyzList = cwVersion.split(".")
            versionNumInt = int(xyzList[0]) * 1000000 \
                + int(xyzList[1]) * 1000 \
                + int(xyzList[2])
            if versionNumInt < 9007002 or versionNumInt >= 9009000:
                raise IncompatibleStratosVersionException(cwVersion, "9.8.x")

        # Log in.
        authUrl = authUrl.rstrip("/") if authUrl else deploymentUrl + "auth"
        credentials, authorizationToken = \
            self.__login(authUrl, username, password)

        # Assign object values.
        # (NOTE: deploymentUrl has a trailing slash, but
        # cubeservUrl and adminUrl do not.)
        self.deploymentUrl = deploymentUrl
        self.cubeservUrl = deploymentUrl + "cubeserv/default"
        self.adminUrl = self.cubeservUrl + "/admin"
        self.credentials = credentials
        self.__authorizationToken = authorizationToken
        self.__requestHeaders = {
            "Accept": "application/json",
            "Authorization": "CwAuth " + authorizationToken
        }

        self.__versionObj = None

    def getVersion(self) -> str:
        """Return the x.y.z version number of the CubeWerx Stratos.
        """
        self.__fetchVersionObj()
        return self.__versionObj.get("versionNumber")

    def getVersionFull(self) -> str:
        """Return the full version string of the CubeWerx Stratos.
        """
        self.__fetchVersionObj()
        return self.__versionObj.get("fullStr")

    def getLicenseExpirationDate(self) -> datetime.date | None:
        """Return the license expiry date of the CubeWerx Stratos.

        ARGUMENTS:
            (none)
        RETURNS:
            the license expiry date of the CubeWerx Stratos deployment,
            or None if the license has no expiry date
        """
        self.__fetchVersionObj()
        dateStr = self.__versionObj.get("licenseExpiration")
        return datetime.date.fromisoformat(dateStr) if dateStr else None

    def getStats(self, nPeriods: int=24,
            nSecondsPerPeriod: int=3600) -> Stats:
        """Fetch current system statistics.

        ARGUMENTS:
            nPeriods - the number of time periods to return in the
                nActiveUsers list (default: 24)
            nSecondsPerPeriod - the duration in seconds of each time period
                in the nActiveUsers list (default: 3600 (one hour))
        RETURNS:
            a Stats object providing current system statistics
        """
        statsUrl = self.adminUrl + "/stats"
        params = {
            "nPeriods": nPeriods,
            "periodDuration": nSecondsPerPeriod
        }
        response = requests.get(statsUrl, headers=self.__requestHeaders,
            params=params)
        ServerException.raise_for_status(response)
        return Stats(response.json())

    def getRequestHistory(self, maxPeriods: int=24) -> RequestHistory:
        """Fetch a summary of the recent request history.

        ARGUMENTS:
            maxPeriods - the maximum number of time periods (typically
                but not necessarily months) to return (default: 24)
        RETURNS:
            a summary of the recent request history
        """
        requestHistoryUrl = self.adminUrl + "/requestHistory"
        params = { "maxPeriods": maxPeriods }
        response = requests.get(requestHistoryUrl,
            headers=self.__requestHeaders, params=params)
        ServerException.raise_for_status(response)
        return RequestHistory(response.json())

    def getLoginHistory(self,
            username: str | None = None,
            ipAddress: str | None = None,
            fromTime: datetime.datetime | None = None,
            toTime: datetime.datetime | None = None,
            order: str = "forward",
            num: int = 100) -> list[LoginHistoryEntry]:
        """Fetch a login history.

        ARGUMENTS:
            username - the CwAuth user to fetch the login history of,
                or None to fetch the login history of all users
            ipAddress - the IP address to fetch the login history of,
                or None to fetch the login history of all IP addresses;
                if an IPv4 address with less than four octets is specified,
                it matches all IP address beginning with the specified
                octets
            fromTime - the start date and time inclusive (in the server's
                time zone) of the login history to fetch, or None to fetch
                back indefinitely
            toTime - the end date and time inclusive (in the server's time
                zone) of the login history to fetch, or None to fetch to
                the current time
            order - the chronological order of the returned entries,
                one of "forward" or "reverse"
            num - the maximum number of most-recent entries to return
        RETURNS:
            a list of LoginHistoryEntry objects
        """
        loginHistoryUrl = self.adminUrl + "/loginHistory"
        params = {}
        if username: params["username"] = username
        if ipAddress: params["ipAddress"] = ipAddress
        if fromTime: params["from"] = fromTime.isoformat()
        if toTime: params["to"] = toTime.isoformat()
        params["order"] = order
        params["num"] = num
        response = requests.get(loginHistoryUrl,
            headers=self.__requestHeaders, params=params)
        ServerException.raise_for_status(response)
        loginHistory = []
        for entryJson in response.json():
            loginHistory.append(LoginHistoryEntry(entryJson))
        return loginHistory

    def getConfigParams(self) -> dict[str,ConfigParam]:
        """Fetch the available configuration parameters.

        ARGUMENTS:
            (none)
        RETURNS:
            a dictionary mapping configuration parameter names to
            ConfigParam obects
        """
        configUrl = self.adminUrl + "/config"
        response = requests.get(configUrl, headers=self.__requestHeaders)
        ServerException.raise_for_status(response)

        configParams = {}
        for configParamJson in response.json():
            configParam = ConfigParam(configParamJson, configUrl,
                self.__authorizationToken)
            configParams[configParam.name] = configParam

        return configParams

    def getAuthUsers(self, usernames: list=None) -> list[AuthUser]:
        """Fetch a list of CwAuth users.

        ARGUMENTS:
            usernames - a list of usernames to fetch, or None/[] to fetch
                all users; if specified, the users will be returned in the
                specified order; if a specified username doesn't exist,
                it's omitted from the returned list
        RETURNS:
            the list of all or selected CwAuth users of the CubeWerx Stratos
        """
        usersUrl = self.adminUrl + "/users"
        response = requests.get(usersUrl, headers=self.__requestHeaders)
        ServerException.raise_for_status(response)

        users = []
        if usernames:
            for username in usernames:
                for userJson in response.json():
                    if userJson.get("username") == username:
                        users.append(AuthUser(dictionary=userJson))
        else:
            for userJson in response.json():
                users.append(AuthUser(dictionary=userJson))

        return users

    def getAuthUser(self, username: str) -> AuthUser | None:
        """Fetch the specified CwAuth user.

        ARGUMENTS:
            username - a username
        RETURNS:
            the CwAuth user with the specified username, or None if no
            such user exists
        """
        userUrl = self.adminUrl + "/users/" + quote(username)
        response = requests.get(userUrl, headers=self.__requestHeaders)
        if response.status_code == 404: return None
        ServerException.raise_for_status(response)
        return AuthUser(dictionary=response.json())

    def addOrReplaceAuthUser(self, user: AuthUser) -> bool:
        """Add a CwAuth user or replace an existing user's definition.

        Adds a new CwAuth user to the CubeWerx Stratos.  If a user with
        the same username already exists, that user's definition is
        replaced.

        ARGUMENTS:
            user - a CwAuth user definition; must have an e-mail address
                and a password set
        RETURNS:
            True if an existing user was replaced, or False if a new user
            was added
        """
        # Validate requirements of AuthUser object
        if not user.emailAddress:
            raise ValueError("E-mail address of user not specified")
        if user.password is None:
            raise ValueError("Password of user not specified")

        userUrl = self.adminUrl + "/users/" + quote(user.username)
        response = requests.put(userUrl, headers=self.__requestHeaders,
            json=user._dict)
        ServerException.raise_for_status(response)
        existingReplaced = (response.status_code == 200)
        return existingReplaced

    def updateAuthUser(self, user: AuthUser):
        """Update the definition of a CwAuth user.

        Commits a CwAuth user update to the CubeWerx Stratos.  The intended
        flow is 1) fetch the definition of a user with getAuthUsers() or
        getAuthUser(), 2) update one or more properties of that user, and
        3) call this method to commit those changes.

        ARGUMENTS:
            user - a modified CwAuth user definition
        RETURNS:
            (nothing)
        """
        userUrl = self.adminUrl + "/users/" + quote(user.username)
        response = requests.patch(userUrl, headers=self.__requestHeaders,
            json=user._patchDict)
        ServerException.raise_for_status(response)

    def removeAuthUser(self, user: AuthUser | str) -> bool:
        """Remove a CwAuth user.

        Removes the specified CwAuth user from the CubeWerx Stratos.  The
        special "admin" user cannot be removed.

        Note that if this AuthUser is in an AuthUser list that was fetched
        via a call to getAuthUsers(), the object isn't automatically
        removed from the list.  It's up to the caller to do that if
        necessary.

        ARGUMENTS:
            user - a CwAuth user definition or username
        RETURNS:
            True if the user was removed, or False if the user didn't exist
        """
        username = user.username if isinstance(user, AuthUser) else user
        # TODO: reject attempt to remove "admin" here?
        userUrl = self.adminUrl + "/users/" + quote(username)
        response = requests.delete(userUrl, headers=self.__requestHeaders)
        existingRemoved = True
        if response.status_code == 404:
            existingRemoved = False
        else:
            ServerException.raise_for_status(response)
        return existingRemoved

    def getRoles(self, roleNames: list=None) -> list[Role]:
        """Fetch a list of roles.

        ARGUMENTS:
            roleNames - a list of role names to fetch, or None/[] to fetch
                all roles; if specified, the roles will be returned in the
                specified order; if a specified role name doesn't exist,
                it's omitted from the returned list
        RETURNS:
            the list of all or selected roles of the CubeWerx Stratos
        """
        rolesUrl = self.adminUrl + "/roles"
        response = requests.get(rolesUrl, headers=self.__requestHeaders)
        ServerException.raise_for_status(response)

        roles = []
        if roleNames:
            for roleName in roleNames:
                for roleJson in response.json():
                    if roleJson.get("name") == roleName:
                        roles.append(Role(dictionary=roleJson))
        else:
            for roleJson in response.json():
                roles.append(Role(dictionary=roleJson))

        return roles

    def getRole(self, roleName: str) -> Role | None:
        """Fetch the specified role.

        ARGUMENTS:
            roleName - a role name
        RETURNS:
            the role with the specified name, or None if no such
            role exists
        """
        roleUrl = self.adminUrl + "/roles/" + quote(roleName)
        response = requests.get(roleUrl, headers=self.__requestHeaders)
        if response.status_code == 404: return None
        ServerException.raise_for_status(response)
        return Role(dictionary=response.json())

    def addOrReplaceRole(self, role: Role) -> bool:
        """Add a role or replace an existing role's definition.

        Adds a new role to the CubeWerx Stratos.  If a role with the
        same name already exists, that role's definition is replaced.

        ARGUMENTS:
            role - a role definition
        RETURNS:
            True if an existing role was replaced, or False if a new role
            was added
        """
        roleUrl = self.adminUrl + "/roles/" + quote(role.name)
        response = requests.put(roleUrl, headers=self.__requestHeaders,
            json=role._dict)
        ServerException.raise_for_status(response)
        existingReplaced = (response.status_code == 200)
        return existingReplaced

    def updateRole(self, role: Role):
        """Update the definition of a role.

        Commits a CwAuth role update to the CubeWerx Stratos.  The intended
        flow is 1) fetch the definition of a role with getRoles() or
        getRole(), 2) update one or more properties of that role, and 3)
        call this method to commit those changes.

        ARGUMENTS:
            role - a modified role definition
        RETURNS:
            (nothing)
        """
        roleUrl = self.adminUrl + "/roles/" + quote(role.name)
        response = requests.patch(roleUrl, headers=self.__requestHeaders,
            json=role._patchDict)
        ServerException.raise_for_status(response)

    def removeRole(self, role: Role | str) -> bool:
        """Remove a role.

        Removes the specified role from the CubeWerx Stratos.  Built-in
        roles such as "Administrator" cannot be removed.  (This can be
        checked with role.isBuiltin.)

        ARGUMENTS:
            role - a role definition or role name
        RETURNS:
            True if the role was removed, or False if the role didn't exist
        """
        # Reject attempts to remove built-in roles.  (Although, if the
        # caller provides just a role name, then only the well-known
        # role name "Administrator" can be checked here.)
        if ((isinstance(role, Role) and role.isBuiltin) or
                (isinstance(role, str) and role.name == "Administrator")):
            raise ValueError('Built-in role "%s" cannot be removed' %
                role.name)

        rolename = role.name if isinstance(role, Role) else role
        roleUrl = self.adminUrl + "/roles/" + quote(rolename)
        response = requests.delete(roleUrl, headers=self.__requestHeaders)
        existingRemoved = True
        if response.status_code == 404:
            existingRemoved = False
        else:
            ServerException.raise_for_status(response)
        return existingRemoved

    def getApiKeys(self) -> list[ApiKey]:
        """Fetch the list of API keys.

        ARGUMENTS:
            (none)
        RETURNS:
            the list of all API keys of the CubeWerx Stratos
        """
        apiKeysUrl = self.adminUrl + "/apiKeys"
        response = requests.get(apiKeysUrl, headers=self.__requestHeaders)
        ServerException.raise_for_status(response)

        apiKeys = []
        for apiKeyJson in response.json():
            apiKeys.append(ApiKey(dictionary=apiKeyJson))

        return apiKeys

    def getApiKey(self, key: str) -> ApiKey | None:
        """Fetch the specified API key.

        ARGUMENTS:
            key - an API key string
        RETURNS:
            the API key with the specified key string, or None if no
            such API key exists
        """
        apiKeyUrl = self.adminUrl + "/apiKeys/" + quote(key)
        response = requests.get(apiKeyUrl, headers=self.__requestHeaders)
        if response.status_code == 404: return None
        ServerException.raise_for_status(response)
        return ApiKey(dictionary=response.json())

    def addOrReplaceApiKey(self, apiKey: ApiKey) -> bool:
        """Add an API key or replace an existing API key's definition.

        Adds a new API key to the CubeWerx Stratos.  If an API key with
        the same key string already exists, that API key's definition
        is replaced.  If apiKey.key isn't set, the server will
        auto-generate a key string and set apiKey.key accordingly.

        ARGUMENTS:
            apiKey - an API key definition
        RETURNS:
            True if an existing API key was replaced, or False if a new
            API key was added
        """
        apiKeysUrl = self.adminUrl + "/apiKeys"
        if apiKey.key:
            apiKeyUrl = apiKeysUrl + "/" + quote(apiKey.key)
            response = requests.put(apiKeyUrl, headers=self.__requestHeaders,
                json=apiKey._dict)
            ServerException.raise_for_status(response)
            existingReplaced = (response.status_code == 200)
            return existingReplaced
        else:
            response = requests.post(apiKeysUrl,
                headers=self.__requestHeaders, json=apiKey._dict)
            ServerException.raise_for_status(response)
            responseJson = response.json()
            apiKey._dict["apiKey"] = responseJson.get("apiKey")
            return False

    def updateApiKey(self, apiKey: ApiKey):
        """Update the definition of an API key.

        Commits an API key update to the CubeWerx Stratos.  The intended
        flow is 1) fetch the definition of an API key with getApiKeys()
        or getApiKey(), 2) update one or more properties of that API key,
        and 3) call this method to commit those changes.

        ARGUMENTS:
            apiKey - a modified API key definition
        RETURNS:
            (nothing)
        """
        apiKeyUrl = self.adminUrl + "/apiKeys/" + quote(apiKey.key)
        response = requests.patch(apiKeyUrl, headers=self.__requestHeaders,
            json=apiKey._patchDict)
        ServerException.raise_for_status(response)

    def removeApiKey(self, apiKey: ApiKey | str) -> bool:
        """Remove an API key.

        Removes the specified API key from the CubeWerx Stratos.

        ARGUMENTS:
            apiKey - an API key definition or key string
        RETURNS:
            True if the API key was removed, or False if the API key
            didn't exist
        """
        key = apiKey.key if isinstance(apiKey, ApiKey) else apiKey
        apiKeyUrl = self.adminUrl + "/apiKeys/" + quote(key)
        response = requests.delete(apiKeyUrl, headers=self.__requestHeaders)
        existingRemoved = True
        if response.status_code == 404:
            existingRemoved = False
        else:
            ServerException.raise_for_status(response)
        return existingRemoved

    def getQuotas(self) -> list[Quota]:
        """Fetch the list of quotas.

        ARGUMENTS:
            (none)
        RETURNS:
            the list of all quotas of the CubeWerx Stratos
        """
        quotasUrl = self.adminUrl + "/quotas"
        response = requests.get(quotasUrl, headers=self.__requestHeaders)
        ServerException.raise_for_status(response)

        quotas = []
        for quotaJson in response.json():
            quotas.append(Quota(quotaJson))

        return quotas

    def getQuota(self, id: str) -> Quota | None:
        """Fetch the specified quota.

        ARGUMENTS:
            id - a quota ID
        RETURNS:
            the quota with the specified ID, or None if no such quota exists
        """
        quotaUrl = self.adminUrl + "/quotas/" + quote(id)
        response = requests.get(quotaUrl, headers=self.__requestHeaders)
        if response.status_code == 404: return None
        ServerException.raise_for_status(response)
        return Quota(response.json())

    def addQuota(self, identityType: QuotaIdentityType, identity: str,
                 field: QuotaField, service: str, operation: str,
                 granularity: QuotaGranularity, limit: int,
                 usage: int = 0) -> Quota:
        """Add a new quota.

        ARGUMENTS:
            identityType - the type of identity that this quota is on
            identity - the identity (username, role or API key) that this
                quota is on; the specified username, role or API key must
                exist
            field - the thing being quotad
            service - the service (as known by CubeWerx Stratos Analytics)
                that this quota applies to. E.g., "WMS", "WMTS", "WCS",
                "WFS", "WPS", "CSW", or "*" if the quota applies to all
                services
            operation - the operation (as known by CubeWerx Stratos
                Analytics) that this quota applies to. (e.g., "GetMap",
                "GetFeature"), or "*" if the quota applies to all
                operations
            granularity - the granularity of this quota (i.e., what unit
                of time it applies to
            limit - the limit that this quota imposes
            usage - the current usage (which will be automatically
                reset at the beginning of every unit of time specified
                by the granularity field)
        RETURNS:
            the new quota
        """
        quotasUrl = self.adminUrl + "/quotas"
        postDict = {
            "identityType": str(identityType),
            "identity": str(identity),
            "field": str(field),
            "service": str(service) if service else "*",
            "operation": str(operation) if operation else "*",
            "granularity": str(granularity),
            "limit": max(int(limit), 0),
            "usage": max(int(usage), 0)
        }
        response = requests.post(quotasUrl, headers=self.__requestHeaders,
            json=postDict)
        ServerException.raise_for_status(response)
        return Quota(response.json())

    def updateQuota(self, quota: Quota | str,
                    limit: int | None = None, usage: int | None = None):
        """Update the limit and/or usage of a quota.

        ARGUMENTS:
            quota - a quota definition or ID
            limit - the new limit that this quota imposes, or None to
                not change
            usage - the new current usage (which will be automatically
                reset at the beginning of every unit of time specified
                by the granularity field), or None to not change
        RETURNS:
            (nothing)
        """
        if limit is None and usage is None: return
        isObject = isinstance(quota, Quota)
        id = quota.id if isObject else quota
        quotaUrl = self.adminUrl + "/quotas/" + quote(id)
        patchDict = {}
        if limit is not None:
            limit = max(int(limit), 0)
            patchDict["limit"] = limit
            if isObject: quota._Quota__limit = limit
        if usage is not None:
            usage = max(int(usage), 0)
            patchDict["usage"] = usage
            if isObject: quota._Quota__usage = usage
        response = requests.patch(quotaUrl, headers=self.__requestHeaders,
            json=patchDict)
        ServerException.raise_for_status(response)

    def removeQuota(self, quota: Quota | str) -> bool:
        """Remove a quota.

        Removes the specified quota from the CubeWerx Stratos.

        ARGUMENTS:
            quota - a quota definition or ID
        RETURNS:
            True if the quota was removed, or False if the quota
            didn't exist
        """
        id = quota.id if isinstance(quota, Quota) else quota
        quotaUrl = self.adminUrl + "/quotas/" + quote(id)
        response = requests.delete(quotaUrl, headers=self.__requestHeaders)
        existingRemoved = True
        if response.status_code == 404:
            existingRemoved = False
        else:
            ServerException.raise_for_status(response)
        return existingRemoved

    def getCubeSTORs(self) -> list[CubeSTOR]:
        """Fetch the list of CubeSTOR database details.

        ARGUMENTS:
            (none)
        RETURNS:
            the list of all CubeSTOR databases of the CubeWerx Stratos
        """
        cubestorsUrl = self.adminUrl + "/cubestors"
        response = requests.get(cubestorsUrl, headers=self.__requestHeaders)
        ServerException.raise_for_status(response)

        cubestors = []
        for cubestorJson in response.json():
            cubestors.append(CubeSTOR(cubestorJson))

        return cubestors

    def getCubeSTOR(self, dbName: str) -> CubeSTOR | None:
        """Fetch the details specified CubeSTOR database.

        ARGUMENTS:
            dbName - a CubeSTOR database name
        RETURNS:
            the details of the CubeSTOR database with the specified name,
            or None if no such database exists
        """
        cubestorUrl = self.adminUrl + "/cubestors/" + quote(dbName)
        response = requests.get(cubestorUrl, headers=self.__requestHeaders)
        if response.status_code == 404: return None
        ServerException.raise_for_status(response)
        return CubeSTOR(response.json())

    def addCubeSTOR(self, dbName: str, title: str | None,
                    description: str | None) -> CubeSTOR:
        """Add a CubeSTOR database.

        Adds a new CubeSTOR database to the CubeWerx Stratos.

        ARGUMENTS:
            dbName - the CubeSTOR database name to use; can be no longer
                than 64 characters
            title - the title of the database, or None
            description - a short description of the database, or None
        RETURNS:
            the new CubeSTOR database details
        """
        cubestorUrl = self.adminUrl + "/cubestors/" + quote(dbName)
        putDict = {}
        if title: putDict["title"] = title
        if description: putDict["description"] = description
        response = requests.put(cubestorUrl, headers=self.__requestHeaders,
            json=putDict)
        ServerException.raise_for_status(response)
        return CubeSTOR(response.json())

    def updateCubeSTOR(self, cubestor: CubeSTOR | str,
                       title: str | None = None,
                       description: str | None = None):
        """Update the title and/or description of a CubeSTOR database.

        ARGUMENTS:
            cubestor - a CubeSTOR details object or database name
            title - the new title of the database, "" to clear the title,
                or None to not change
            description - the new short description of the database, ""
                to clear the description, or None to not change
        RETURNS:
            (nothing)
        """
        if title is None and description is None: return
        isObject = isinstance(cubestor, CubeSTOR)
        dbName = cubestor.dbName if isObject else cubestor
        cubestorUrl = self.adminUrl + "/cubestors/" + quote(dbName)
        patchDict = {}
        if title is not None:
            title = str(title)
            patchDict["title"] = title
            if isObject:
                cubestor._CubeSTOR__title = title if title else None
        if description is not None:
            description = str(description)
            patchDict["description"] = description
            if isObject:
                cubestor._CubeSTOR__description = \
                    description if description else None
        response = requests.patch(cubestorUrl, headers=self.__requestHeaders,
            json=patchDict)
        ServerException.raise_for_status(response)

    def removeCubeSTOR(self, cubestor: CubeSTOR | str) -> bool:
        """Remove a CubeSTOR database.

        Removes the specified CubeSTOR database from the CubeWerx
        Stratos.  WARNING: This will remove any and all data that has
        been loaded into this database.  Some databases cannot be removed
        (determinable by the canDelete property of the CubeSTOR details
        object).  One such situation is if the CubeSTOR database is
        currently the source of of a data store.  In this situation, the
        database must first be removed as the source of the data store
        (via a call to updateDataStore() or removeDataStore()).

        Note that if this CubeSTOR is in a CubeSTOR list that was fetched
        via a call to getCubeSTORs(), the object isn't automatically
        removed from the list.  It's up to the caller to do that if
        necessary.

        ARGUMENTS:
            cubestor - a CubeSTOR details object or database name
        RETURNS:
            True if the CubeSTOR database was removed, or False if the
            CubeSTOR database didn't exist
        """
        isObject = isinstance(cubestor, CubeSTOR)
        dbName = cubestor.dbName if isObject else cubestor
        cubestorUrl = self.adminUrl + "/cubestors/" + quote(dbName)
        response = requests.delete(cubestorUrl, headers=self.__requestHeaders)
        existingRemoved = True
        if response.status_code == 404:
            existingRemoved = False
        else:
            ServerException.raise_for_status(response)
        return existingRemoved

    def getDataStores(self) -> list[DataStore]:
        """Fetch the list of CubeWerx Stratos data stores

        ARGUMENTS:
            (none)
        RETURNS:
            the list of all data stores of the CubeWerx Stratos
        """
        dataStoresUrl = self.adminUrl + "/dataStores"
        response = requests.get(dataStoresUrl, headers=self.__requestHeaders)
        ServerException.raise_for_status(response)

        dataStores = []
        for dataStoreJson in response.json():
            dataStore = DataStore(jsonRep=dataStoreJson)
            dataStoreUrl = dataStoresUrl + "/" + quote(dataStore.name)
            ogcApiLandingPageUrl = (self.cubeservUrl + "/ogcapi/" +
                quote(dataStore.name))
            dataStore._setServerAssociation(dataStoreUrl,
                ogcApiLandingPageUrl, self.__authorizationToken)
            dataStores.append(dataStore)

        return dataStores

    def getDataStore(self, name: str) -> DataStore | None:
        """Fetch the specified CubeWerx Stratos data store.

        ARGUMENTS:
            name - a data store name
        RETURNS:
            the CubeWerx Stratos data store with the specified name,
            or None if no such data store exists
        """
        dataStoreUrl = self.adminUrl + "/dataStores/" + quote(name)
        response = requests.get(dataStoreUrl, headers=self.__requestHeaders)
        if response.status_code == 404: return None
        ServerException.raise_for_status(response)

        dataStore = DataStore(jsonRep=response.json())
        ogcApiLandingPageUrl = (self.cubeservUrl + "/ogcapi/" +
            quote(dataStore.name))
        dataStore._setServerAssociation(dataStoreUrl,
            ogcApiLandingPageUrl, self.__authorizationToken)
        return dataStore

    def addOrReplaceDataStore(self, dataStore: DataStore) -> bool:
        """Add a data store or replace an existing data store's definition.

        Adds a new data store to the CubeWerx Stratos.  If a data store
        with the same name already exists, that data store's definition
        is replaced.

        ARGUMENTS:
            dataStore - a data store definition; must have a data store
                type and source set
        RETURNS:
            True if an existing data store was replaced, or False if a
            new data store was added
        """
        # Validate requirements of DataStore object.
        if not dataStore.type:
            raise ValueError("Type of data store not specified")
        if not dataStore.source:
            raise ValueError("Source of data store not specified")

        # Add or replace this data store.
        # TODO: Should this be allowed for an existing data store that
        # already has layers?  Probably not.
        dataStoreUrl = self.adminUrl + "/dataStores/" + quote(dataStore.name)
        response = requests.put(dataStoreUrl, headers=self.__requestHeaders,
            json=dataStore._jsonRep)
        ServerException.raise_for_status(response)
        existingReplaced = (response.status_code == 200)

        ogcApiLandingPageUrl = (self.cubeservUrl + "/ogcapi/" +
            quote(dataStore.name))
        dataStore._setServerAssociation(dataStoreUrl,
            ogcApiLandingPageUrl, self.__authorizationToken)

        return existingReplaced

    def updateDataStore(self, dataStore: DataStore):
        """Update the definition of a data store.

        Commits a data store update to the CubeWerx Stratos.  The intended
        flow is 1) fetch the definition of a data store with getDataStores()
        or getDataStore(), 2) update one or more properties of that data
        store, and 3) call this method to commit those changes.

        ARGUMENTS:
            dataStore - a modified data store definition
        RETURNS:
            (nothing)
        """
        dataStoreUrl = self.adminUrl + "/dataStores/" + quote(dataStore.name)
        response = requests.patch(dataStoreUrl, headers=self.__requestHeaders,
            json=dataStore._patchDict)
        ServerException.raise_for_status(response)

    def removeDataStore(self, dataStore: DataStore | str) -> bool:
        """Remove a data store.

        Removes the specified data store from the CubeWerx Stratos.  Some
        data stores cannot be removed (determinable by the canDelete
        property of the data store object).

        Note that if this DataStore is in an DataStore list that
        was fetched via a call to getDataStores(), the object isn't
        automatically removed from the list.  It's up to the caller to
        do that if necessary.

        ARGUMENTS:
            dataStore - a data store definition or name
        RETURNS:
            True if the data store was removed, or False if the data
            store didn't exist
        """
        name = dataStore.name \
            if isinstance(dataStore, DataStore) else dataStore
        dataStoreUrl = self.adminUrl + "/dataStores/" + quote(name)
        response = requests.delete(dataStoreUrl, headers=self.__requestHeaders)
        existingRemoved = True
        if response.status_code == 404:
            existingRemoved = False
        else:
            ServerException.raise_for_status(response)

        dataStore._setServerAssociation(None, None, None)

        return existingRemoved

    @staticmethod
    def __login(authUrl: str, username: str, password: str):
        # Try to log in to the specified deployment.
        # (see "https://requests.readthedocs.io/en/latest/")
        loginUrl = authUrl + "/login"
        headers = { "Accept": "application/json" }
        data = { "username": username, "password": password }
        response = requests.post(loginUrl, headers=headers, data=data)
        ServerException.raise_for_status(response)

        # Make sure this is a CubeWerx Stratos version 9.7.x or higher.
        cwVersion = response.headers.get("CubeWerx-Stratos-Version")
        if not cwVersion:
            cwVersion = response.headers.get("CubeWerx-Suite-Version")
        if not cwVersion:
            raise NotAnAuthServerException()
        else:
            xyzList = cwVersion.split(".")
            versionNumInt = int(xyzList[0]) * 1000000 \
                + int(xyzList[1]) * 1000 \
                + int(xyzList[2])
            if versionNumInt < 9007002:
                raise AuthServerVersionTooLowException(cwVersion, "9.7.2")

        # Verify that the authentication server returned a status of
        # "loginSuccessful".
        authStatus = response.headers.get("CwAuth-Status", "unknown")
        if authStatus == "loginFailed":
            raise InvalidCredentialsException()
        elif authStatus == "loginAttemptsTooFrequent":
            raise LoginAttemptsTooFrequentException()
        elif authStatus == "noMoreSeats":
            raise NoMoreSeatsException(username)
        elif authStatus != "loginSuccessful":
            raise LoginException() # catch-all for other auth statuses

        responseJson = response.json()
        credentials = responseJson.get("credentials")
        authorizationToken = responseJson.get("authorizationToken")

        # Verify that the user has the Administrator role.
        roles = credentials.get("roles", [])
        if not "Administrator" in roles:
            raise NotAdministratorException(username)

        # We're done!
        return credentials, authorizationToken

    def __fetchVersionObj(self):
        if not self.__versionObj:
            response = requests.get(self.adminUrl + "/version",
                headers=self.__requestHeaders)
            ServerException.raise_for_status(response)
            self.__versionObj = response.json()

