# $Id: Role.py 78570 2025-01-23 18:57:06Z pomakis $

import validators

from .OidUser import OidUser


class Role:
    """A CubeWerx Stratos CwAuth role.

    Roles are a convenient way of assigning tasks to users, allowing
    access to be granted to particular data and/or operations based on
    users' roles rather than having to manage access-control rules at a
    per-user level.

    Roles can be assigned to CubeWerx Stratos CwAuth users and OpenID
    Connect users.

    A special built-in "Administrator" role allows full
    administraton access to a CubeWerx Stratos deployment.  This role
    is hardcoded-assigned to the "admin" CwAuth user, but is also
    assignable to other users to grant them full administraton access.
    This role cannot be removed.

    To create a new role, create a new Role object (specifying the
    desired role name), set any other desired properties, and call the
    addOrReplaceRole() method of the Stratos object.

    To change the details of an existing role, fetch the role object via
    the getRoles() or getRole() method of the Stratos object, update
    one or more properties of that role, and call the updateRole()
    method of the Stratos object to commit those changes.

    To remove a role, call the removeRole() method of the Stratos object.

    ARGUMENTS:
        name - the name of the role; each role must have a unique name;
            required unless supplied via the dictionary parameter
        dictionary - a dictionary supplying properties; do not specify;
            for internal use only
    """

    def __init__(self, name: str=None, dictionary: dict={}):
        if name:
            if not "name" in dictionary: dictionary["name"] = name
        elif not "name" in dictionary:
            raise Exception("name needs to be specified")
        self._dict = dictionary

        # Keep track of the properties that are programmatically changed
        # so that an appropriate patch dictionary can be constructed.
        self.__descriptionChanged = False
        self.__contactChanged = False
        self.__authUsersChanged = False
        self.__oidUsersChanged = False

    @property
    def name(self):
        """the unique name of this role"""
        return self._dict.get("name")

    @property
    def description(self) -> str | None:
        """a brief textual description of this role, or None"""
        return self._dict.get("description")

    @description.setter
    def description(self, value: str | None):
        if value:
            self._dict["description"] = value
        else:
            del self._dict["description"]
        self.__descriptionChanged = True

    @property
    def contactEmail(self) -> str | None:
        """the e-mail address to contact regarding this role, or None"""
        return self._dict.get("contact")

    @contactEmail.setter
    def contactEmail(self, value: str | None):
        if value:
            if not validators.email(value):
                raise ValueError("Invalid emailAddress")
            self._dict["contact"] = value
        else:
            del self._dict["contact"]
        self.__contactChanged = True

    @property
    def isBuiltin(self) -> bool:
        """is this a non-removable built-in role?"""
        return self._dict.get("builtin", true)

    @property
    def authUsers(self) -> list[str]:
        """the list of CubeWerx Stratos CwAuth user accounts that have
        this role; these are the usernames only; to get the full User
        objects (for full names and e-mail addresses, etc.), pass
        this list to the getAuthUsers() method of the Stratos object; this
        list of users can be re-specified with a role.authUsers = [...]
        assignment; however, to add or remove a user to/from the existing
        list, use the addAuthUser() or removeAuthUser() methods rather
        than role.authUsers.append() or role.authUsers.remove()"""
        return self._dict.get("authUsers", [])

    @authUsers.setter
    def authUsers(self, value: list[str]):
        self._dict["authUsers"] = value if value else []
        self.__authUsersChanged = True

    def addAuthUser(self, username: str):
        """Add a CubeWerx Stratos CwAuth user to this role.

        ARGUMENTS:
            username - the username of the CubeWerx Stratos CwAuth user
                account to add this role to; the specified user must
                exist; if the user already has this role, this is a no-op
        RETURNS:
            (nothing)
        """
        if username:
            if not self._dict.get("authUsers"): self._dict["authUsers"] = []
            if not username in self._dict["authUsers"]:
                self._dict["authUsers"].append(username)
            self.__authUsersChanged = True

    def removeAuthUser(self, username: str):
        """Remove a CubeWerx Stratos CwAuth user from this role.

        ARGUMENTS:
            username - the username of the CubeWerx Stratos CwAuth user
                account to remove (revoke) this role from; if the user
                doesn't have this role, this is a no-op
        RETURNS:
            (nothing)
        """
        if self._dict["authUsers"] and username and \
                username in self._dict["authUsers"]:
            self._dict["authUsers"].remove(username)
            self.__authUsersChanged = True

    @property
    def oidUsers(self) -> list[OidUser]:
        """the list of OpenID Connect user identities that have this role;
        this list of users can be re-specified with a role.oidUsers = [...]
        assignment; however, to add or remove a user to/from the existing
        list, use the addOidUser() or removeOidUser() methods rather
        than role.oidUsers.append() or role.oidUsers.remove()"""
        return self._dict.get("oidUsers", [])

    @oidUsers.setter
    def oidUsers(self, value: list[OidUser]):
        self._dict["oidUsers"] = value if value else []
        self.__oidUsersChanged = True

    def addOidUser(self, oidUser: OidUser):
        """Add an OpenID Connect user to this role.

        ARGUMENTS:
            oidUser - the OpenID Connect user identity to add this role
                to; if the user already has this role, this is a no-op
        RETURNS:
            (nothing)
        """
        if oidUser:
            if not self._dict.get("oidUsers"): self._dict["oidUsers"] = []
            self._dict["oidUsers"].append(oidUser)
            self.__oidUsersChanged = True

    def removeOidUser(self, oidUser: OidUser):
        """Remove an OpenID Connect user from this role.

        ARGUMENTS:
            oidUser - the OpenID Connect user identity to remove (revoke)
                this role from; if the user doesn't have this role, this
                is a no-op
        RETURNS:
            (nothing)
        """
        if self._dict["oidUsers"] and oidUser and \
                oidUser in self._dict["oidUsers"]:
            self._dict["oidUsers"].remove(oidUser)
            self.__oidUsersChanged = True

    @property
    def _patchDict(self) -> dict:
        patch = {}
        if self.__descriptionChanged:
            patch["description"] = self.description
        if self.__contactChanged:
            patch["contact"] = self.contactEmail
        if self.__authUsersChanged:
            patch["authUsers"] = self.authUsers
        if self.__oidUsersChanged:
            patch["oidUsers"] = self.oidUsers
        return patch
