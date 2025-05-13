# $Id: ApiKey.py 78570 2025-01-23 18:57:06Z pomakis $

import datetime
import validators


class ApiKey:
    """An API key.

    To create a new API key, create a new ApiKey object (either specifying
    the desired key string or letting the server auto-generate one for you),
    set any other desired properties, and call the addOrReplaceApiKey()
    method of the Stratos object.

    To change the details of an existing API key, fetch the ApiKey
    object via the getApiKeys() or getApiKey() method of the Stratos
    object, update one or more properties of tha API key, and call the
    updateApiKey() method of the Stratos object to commit those changes.

    To remove an API key, call the removeApiKey() method of the Stratos
    object.

    ARGUMENTS:
        key - the desired API key string, or ""/None to let the server
            auto-generate one
        dictionary - a dictionary supplying properties; do not specify;
            for internal use only
    """

    def __init__(self, key: str=None, dictionary: dict={}):
        if key:
            if not "apiKey" in dictionary: dictionary["apiKey"] = key
        self._dict = dictionary

        # Keep track of the properties that are programmatically changed
        # so that an appropriate patch dictionary can be constructed.
        self.__descriptionChanged = False
        self.__contactChanged = False
        self.__expiresAtChanged = False
        self.__isEnabledChanged = False

    @property
    def key(self):
        """the API key string
        """
        return self._dict.get("apiKey")

    @property
    def description(self) -> str | None:
        """a brief textual description of this API key, or None
        """
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
        """the e-mail address to contact regarding this API key, or None
        """
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
    def expiresAt(self) -> datetime.datetime | None:
        """the date and time (UTC) that this API key expires (after which
        time it's effectively disabled), or None if this API key never
        expires
        """
        dateTimeStr = self._dict.get("expiresAt")
        return datetime.datetime.fromisoformat(dateTimeStr) \
            if dateTimeStr else None

    @expiresAt.setter
    def expiresAt(self, value: datetime.datetime | None):
        if value:
            self._dict["expiresAt"] = value.isoformat()
        else:
            del self._dict["expiresAt"]
        self.__expiresAtChanged = True

    @property
    def isEnabled(self) -> bool:
        """is this API key enabled (subject to expiresAt)?
        """
        return self._dict.get("isEnabled", true)

    @isEnabled.setter
    def isEnabled(self, value: bool):
        self._dict["isEnabled"] = bool(value)
        self.__isEnabledChanged = True

    @property
    def _patchDict(self) -> dict:
        patch = {}
        if self.__descriptionChanged:
            patch["description"] = self.description
        if self.__contactChanged:
            patch["contact"] = self.contactEmail
        if self.__expiresAtChanged:
            patch["expiresAt"] = self._dict.get("expiresAt")
        if self.__isEnabledChanged:
            patch["isEnabled"] = self.isEnabled
        return patch

