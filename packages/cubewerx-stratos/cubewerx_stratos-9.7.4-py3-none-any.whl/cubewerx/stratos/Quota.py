# $Id: Quota.py 78570 2025-01-23 18:57:06Z pomakis $

import datetime
from enum import StrEnum, auto


class QuotaIdentityType(StrEnum):
    """An enumeration of the identity types that a quota can be on.
    """
    USERNAME = auto()
    ROLE     = auto()
    API_KEY  = auto()


class QuotaField(StrEnum):
    """An enumeration of the things that a quota can be on.
    """
    N_REQUESTS         = auto()
    DURATION           = auto()
    CPU_SECONDS        = auto()
    N_RESPONSE_BYTES   = auto()
    N_FEATURES         = auto()
    N_POINTS           = auto()
    N_PIXELS           = auto()
    N_NONEMPTY_PIXELS  = auto()
    N_FEATURE_BYTES    = auto()
    N_COVERAGE_BYTES   = auto()
    N_DOWNLOAD_BYTES   = auto()
    N_PROCESSING_UNITS = auto()


class QuotaGranularity(StrEnum):
    """An enumeration of granularity of a quota (i.e., what unit of time
    it applies to).
    """
    UNBOUNDED    = auto()
    ANNUALLY     = auto()
    SEMIANNUALLY = auto()
    BIMONTHLY    = auto()
    MONTHLY      = auto()
    WEEKLY       = auto()
    DAILY        = auto()


class Quota:
    """A quota.

    Do not instantiate directly.  To get a list of quotas or a specific
    quota, call the getQuotas() ot getQuota() methods of the Stratos
    object respectively.  To create, update or remove a quota, call the
    addQuota(), updateQuota() or removeQuota() methods of the Stratos
    object respectively.
    """

    def __init__(self, jsonRep: dict):
        self.__id = jsonRep.get("quotaId")
        self.__identityType = QuotaIdentityType(jsonRep.get("identityType"))
        self.__identity = jsonRep.get("identity")
        self.__field = QuotaField(jsonRep.get("field"))

        service = jsonRep.get("service")
        self.__service = service if service else "*"

        operation = jsonRep.get("operation")
        self.__operation = operation if operation else "*"

        self.__granularity = QuotaGranularity(jsonRep.get("granularity"))
        self.__fromDate = datetime.date.fromisoformat(jsonRep.get("fromDate"))
        self.__toDate = datetime.date.fromisoformat(jsonRep.get("toDate"))
        self.__limit = int(jsonRep.get("limit"))
        self.__usage = int(jsonRep.get("usage"))

        warningNumSent = jsonRep.get("warningNumSent")
        self.__warningNumSent = int(warningNumSent) if warningNumSent else 0

    @property
    def id(self) -> str:
        """the ID of this quota"""
        return self.__id

    @property
    def identityType(self) -> QuotaIdentityType:
        """the type of identity that this quota is on"""
        return self.__identityType

    @property
    def identity(self) -> str:
        """the identity (username, role or API key) that this quota is on"""
        return self.__identity

    @property
    def field(self) -> QuotaField:
        """the thing being quotad"""
        return self.__field

    @property
    def service(self) -> str:
        """the service (as known by CubeWerx Stratos Analytics) that this
        quota applies to (e.g., "WMS", "WMTS", "WCS", "WFS", "WPS", "CSW"),
        or "*" if the quota applies to all services"""
        return self.__service

    @property
    def operation(self) -> str:
        """the operation (as known by CubeWerx Stratos Analytics) that
        this quota applies to. (e.g., "GetMap", "GetFeature"), or "*"
        if the quota applies to all operations"""
        return self.__operation

    @property
    def granularity(self) -> QuotaGranularity:
        """the granularity of this quota (i.e., what unit of time it
        applies to)"""
        return self.__granularity

    @property
    def fromDate(self) -> datetime.date:
        """the start date (inclusive, in the server's time zone) of the
        current time window of this quota; this will be automatically
        adjusted at the beginning of every unit of time specified by
        the granularity field"""
        return self.__fromDate

    @property
    def toDate(self) -> datetime.date:
        """the end date (inclusive, in the server's time zone) of the
        current time window of this quota; this will be automatically
        adjusted at the beginning of every unit of time specified by
        the granularity field"""
        return self.__toDate

    @property
    def limit(self) -> int:
        """the limit that this quota imposes"""
        return self.__limit

    @property
    def usage(self) -> int:
        """the current usage (which will be automatically reset at the
        beginning of every unit of time specified by the granularity
        field)"""
        return self.__usage

    @property
    def warningNumSent(self) -> int:
        """the highest warning level (typically 1 to 3, or 0 for no
        warning) that the user, role maintainer or API key maintainer
        has been e-mailed about regarding the current usage level; this
        will be automatically reset at the beginning of every unit of
        time specified by the granularity field"""
        return self.__warningNumSent

