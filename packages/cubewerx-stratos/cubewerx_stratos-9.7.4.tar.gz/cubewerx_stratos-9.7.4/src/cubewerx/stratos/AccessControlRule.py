# $Id: AccessControlRule.py 78774 2025-03-13 16:39:46Z pomakis $

import datetime
import json
from enum import StrEnum
from shapely import Polygon, from_geojson, to_geojson


class OperationClass(StrEnum):
    """An enumeration of the operation classes that can be access controlled.
    """

    GET_MAP               = "GetMap"
    GET_FEATURE_INFO      = "GetFeatureInfo"
    GET_FEATURE           = "GetFeature"
    INSERT_FEATURE        = "InsertFeature"
    UPDATE_FEATURE        = "UpdateFeature"
    DELETE_FEATURE        = "DeleteFeature"
    MANAGE_FEATURE_SETS   = "ManageFeatureSets"
    MANAGE_STORED_QUERIES = "ManageStoredQueries"
    MANAGE_STYLES         = "ManageStyles"
    EXECUTE_PROCESS       = "ExecuteProcess"
    MANAGE_PROCESSES      = "ManageProcesses"
    GET_RECORD            = "GetRecord"
    INSERT_RECORD         = "InsertRecord"
    UPDATE_RECORD         = "UpdateRecord"
    DELETE_RECORD         = "DeleteRecord"
    GET_ENTRY             = "GetEntry"
    INSERT_ENTRY          = "InsertEntry"
    UPDATE_ENTRY          = "UpdateEntry"
    DELETE_ENTRY          = "DeleteEntry"
    MANAGE_PUBLICATIONS   = "ManagePublications"
    MANAGE_SUBSCRIPTIONS  = "ManageSubscriptions"
    MANAGE_CHANGES        = "ManageChanges"


class AreaSource:
    """A reference to a source of polygons, multi-surfaces and/or
    envelopes to be used for access control.

    ARGUMENTS:
        urlOrFilePath - a URL or local file path (absolute or relative
            to the deployment URL or directory) to the source, or None
            (but then required to be set via the property)
        format - the name of the convert-library driver that should be
            used to read this source (e.g., "GeoJSON", "shape"), or
            None; if None an attempt will be made to sniff the format
        where - a CQL2 WHERE clause filter to select a subset of the
            geometries, or None to apply no filter
    """

    def __init__(self, urlOrFilePath: str | None = None,
                 format: str | None = None,
                 where: str = None):
        self.__urlOrFilePath = urlOrFilePath if urlOrFilePath else None
        self.__format = format if format else None
        self.__where = where if where else None

    @staticmethod
    def _fromJsonRep(jsonRep: dict):
        return AreaSource(jsonRep.get("urlOrFilePath"),
            jsonRep.get("format"), jsonRep.get("where"))

    @property
    def urlOrFilePath(self) -> str | None:
        """a URL or local file path (absolute or relative to the
        deployment URL or directory) to the source, or None"""
        return self.__urlOrFilePath

    @urlOrFilePath.setter
    def urlOrFilePath(self, value: str | None):
        self.__urlOrFilePath = value if value else None

    @property
    def format(self) -> str | None:
        """the name of the convert-library driver that should be used to
        read this source (e.g., "GeoJSON", "shape"), or None; if None an
        attempt will be made to sniff the format"""
        return self.__format

    @format.setter
    def format(self, value: str | None):
        self.__format = value if value else None

    @property
    def where(self) -> str | None:
        """a CQL2 WHERE clause filter to select a subset of the
        geometries, or None to apply no filter"""
        return self.__where

    @where.setter
    def where(self, value: str | None):
        self.__where = value if value else None

    @property
    def _jsonRep(self) -> dict:
        jsonRep = {}
        if self.__urlOrFilePath:
            jsonRep["urlOrFilePath"] = self.__urlOrFilePath
        if self.__format:
            jsonRep["format"] = self.__format
        if self.__where:
            jsonRep["where"] = self.__where
        return jsonRep

    def __repr__(self):
        return repr(self._jsonRep)


class WatermarkLocation(StrEnum):
    """An enumeration of where watermarks can be applied in rendered maps.
    """

    NOWHERE       = "nowhere"
    TOP_LEFT      = "top left"
    TOP_CENTER    = "top center"
    TOP_RIGHT     = "top right"
    CENTER_LEFT   = "center left"
    CENTER        = "center"
    CENTER_RIGHT  = "center right"
    BOTTOM_LEFT   = "bottom left"
    BOTTOM_CENTER = "bottom center"
    BOTTOM_RIGHT  = "bottom right"
    TILED         = "tiled"


class Watermark:
    """A watermark to apply for map layer rendering.

    ARGUMENTS:
        urlOrFilePath - a URL or local file path (absolute or relative
            to the deployment URL or directory) to an image to use as
            the watermark, or None (but then required to be set via
            the property); PNG is preferred, but JPEG, GIF and TIFF will
            also work
        location - where the watermark should be applied in the rendered
            map; the only location suitable for tiled maps is TILED
        opacity - the opacity (0...1) of the watermark (subject to the
            opacity of the image itself
    """

    def __init__(self, urlOrFilePath: str | None = None,
                 location: WatermarkLocation=WatermarkLocation.TILED,
                 opacity: float=1.0):
        self.__urlOrFilePath = urlOrFilePath if urlOrFilePath else None
        self.__location = location
        self.__opacity = min(max(float(opacity), 0.0), 1.0)

    @staticmethod
    def _fromJsonRep(jsonRep: dict):
        urlOrFilePath = jsonRep.get("urlOrFilePath")
        try:
            location = WatermarkLocation(jsonRep.get("location", "tiled"))
        except ValueError as e:
            location = WatermarkLocation.TILED # rather than failing
        opacity = min(max(jsonRep.get("opacity", 1.0), 0.0), 1.0)
        return Watermark(urlOrFilePath, location, opacity)

    @property
    def urlOrFilePath(self) -> str | None:
        """a URL or local file path (absolute or relative to the
        deployment URL or directory) to an image to use as the
        watermark, or None; PNG is preferred, but JPEG, GIF and
        TIFF will also work"""
        return self.__urlOrFilePath

    @urlOrFilePath.setter
    def urlOrFilePath(self, value: str | None):
        self.__urlOrFilePath = value if value else None

    @property
    def location(self) -> WatermarkLocation:
        """where the watermark should be applied in the rendered map;
        the only location suitable for tiled maps is TILED"""
        return self.__location

    @location.setter
    def location(self, value: WatermarkLocation):
        self.__location = value if value else WatermarkLocation.TILED

    @property
    def opacity(self) -> float:
        """the opacity (0...1) of the watermark (subject to the
        opacity of the image itself"""
        return self.__opacity

    @opacity.setter
    def opacity(self, value: float):
        self.__opacity = min(max(float(value), 0.0), 1.0)

    @property
    def _jsonRep(self) -> dict:
        jsonRep = {}
        if self.__urlOrFilePath:
            jsonRep["urlOrFilePath"] = self.__urlOrFilePath
        if self.__location != WatermarkLocation.TILED:
            jsonRep["location"] = str(self.__location)
        if self.__opacity != 1.0:
            jsonRep["opacity"] = self.__opacity
        return jsonRep

    def __repr__(self):
        return repr(self._jsonRep)

class ContentRef:
    """"The content that's being granted (or excepted in the case of
    an "except" clause).

    Within a "grant" clause, content is all-inclusive by default.  That
    is, if no spatial area is specified, it means "everywhere", if no
    feature filters are specified, it means "all features", and if no
    property names are specified, it means "all properties".  Within an
    "except" clause, however, content is all-inclusive by default only
    if it's empty (other than the required "name" property).  Otherwise
    it only includes (excepts) the mentioned thing(s).

    ARGUMENTS:
        name - the name/ID of the feature set, layer or process that's
            being granted (or excepted in the case of an "except"
            clause), or "*" for all; required unless supplied via the
            dictionary parameter
        jsonRep - a dictionary supplying properties; do not specify;
            for internal use only
    """

    def __init__(self, name: str=None, jsonRep: dict={}):
        self.__name = jsonRep.get("name")
        if not self.__name:
            self.__name = name
        if not self.__name:
            raise Exception("name needs to be specified")

        self.__areas = []
        self.__minScaleDenominator = None
        self.__finestResolution = None
        self.__where = None
        self.__properties = []
        self.__watermark = None

        if jsonRep:
            areasJson = jsonRep.get("areas")
            if isinstance(areasJson, list):
                for areaJson in areasJson:
                    if "urlOrFilePath" in areaJson:
                        self.__areas.append(AreaSource._fromJsonRep(areaJson))
                    else:
                        polygon = from_geojson(json.dumps(areaJson))
                        self.__areas.append(polygon)

            minScaleDenominator = jsonRep.get("minScaleDenominator")
            if minScaleDenominator:
                self.__minScaleDenominator = minScaleDenominator

            finestResolution = jsonRep.get("finestResolution")
            if finestResolution:
                self.__finestResolution = finestResolution

            where = jsonRep.get("where")
            if where:
                self.__where = where

            propertiesJson = jsonRep.get("properties")
            if isinstance(propertiesJson, list):
                for propertyJson in propertiesJson:
                  self.__properties.append(str(propertyJson))

            watermarkJson = jsonRep.get("watermark")
            if watermarkJson:
                self.__watermark = Watermark._fromJsonRep(watermarkJson)

    @property
    def name(self) -> str:
        """the name/ID of the feature set, layer or process that's
        being granted (or excepted in the case of an "except" clause),
        or "*" for all"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = str(value) if value else "*"

    @property
    def areas(self) -> list[Polygon|AreaSource]:
        """the spatial areas that are being granted (or excepted in the
        case of an \"except\" clause)"""
        return self.__areas

    @property
    def minScaleDenominator(self) -> float | None:
        """the level of detail to grant access to, expressed as a
        minimum scale denominator (e.g., a minimum scale denominator of
        100000 indicates that no detail finer than a scale of 1/100000
        should be granted), or None to not limit level of detail in this
        way; the lower the specified number, the more detail is granted;
        mutually exclusive with the finestResolution property (i.e.,
        setting this property, even to None, automatically sets the
        finestResolution property to None)"""
        return self.__minScaleDenominator

    @minScaleDenominator.setter
    def minScaleDenominator(self, value: float | None):
        if value is not None and value <= 0:
            raise ValueError("minScaleDenominator must be a positive number")
        self.__minScaleDenominator = float(value) if value else None
        self.__finestResolution = None

    @property
    def finestResolution(self) -> dict | None:
        """the level of detail to grant access to, expressed as a
        dictionary with a "resolution" field indicating a resolution
        (i.e., units per pixel) and a "crs" field indicating the
        coordinate reference system that the resolution should be
        interpreted with respect to (e.g., { "resolution": 10000, "crs":
        "EPSG:3857" }), or None to not limit level of detail in this
        way; the lower the specified number, the more detail is granted;
        mutually exclusive with the minScaleDenominator property (i.e.,
        setting this property, even to None, automatically sets the
        minScaleDenominator property to None)"""
        return self.__finestResolution

    @finestResolution.setter
    def finestResolution(self, value: dict | None):
        if value:
            if not isinstance(value, dict):
                raise TypeError("dict or None expected")
            if not "resolution" in value:
                raise ValueError("missing required 'resolution' field")
            resolution = float(value["resolution"])
            if resolution < 0:
                raise ValueError("resolution must be a non-negative number")
            if not "crs" in value:
                raise ValueError("missing required 'crs' field")
            crs = str(value["crs"])
            if not crs:
                raise ValueError("missing 'crs' value")
            self.__finestResolution = { "resolution": resolution, "crs": crs }
        else:
            self.__finestResolution = None
        self.__minScaleDenominator = None

    @property
    def where(self) -> str | None:
        """a CQL2 WHERE clause filter that limits feature-set content
        to only those features that pass through the filter, or None
        to apply no filter"""
        return self.__where

    @where.setter
    def where(self, value: str | None):
        self.__where = str(value) if value else None

    @property
    def properties(self) -> list[str]:
        """the set of feature-set properties to grant access to (or
        except in the case of an "except" clause); if no properties
        are specified, it means "all properties" """
        return self.__properties

    @property
    def watermark(self) -> Watermark | None:
        """a watermark to apply for map layer rendering, or None"""
        return self.__watermark

    @watermark.setter
    def watermark(self, value: Watermark | None):
        self.__watermark = value

    @property
    def _jsonRep(self) -> dict:
        jsonRep = {}

        jsonRep["name"] = self.__name

        if self.__areas:
            jsonRep["areas"] = areasJson = []
            for area in self.__areas:
                if isinstance(area, AreaSource):
                    if area.urlOrFilePath:
                        areasJson.append(area._jsonRep)
                else:
                    geoJsonStr = to_geojson(area)
                    areasJson.append(json.loads(geoJsonStr))

        if self.__minScaleDenominator:
            jsonRep["minScaleDenominator"] = self.__minScaleDenominator

        if self.__finestResolution:
            jsonRep["finestResolution"] = self.__finestResolution

        if self.__where:
            jsonRep["where"] = self.__where

        if self.__properties:
            jsonRep["properties"] = self.__properties

        if self.__watermark:
            jsonRep["watermark"] = self.__watermark._jsonRep

        return jsonRep

    def __repr__(self):
        return repr(self._jsonRep)


class AccessControlRuleClause:
    """A CubeWerx Access Control Rule Clause.

    There are two types of rule clauses: "grant" and "except".
    A "grant" clause specifies the operation classes that are being
    granted, and the content that is being granted for those operations.
    If no operation classes are specified, it means "all operations".
    Similarly, if no content is specified, it means "all content".  Some
    operation classes (such as GET_RECORD) are independent of content.
    Access can be granted to such operation classes by simply referring
    to them in the operationClasses property of a "grant" rule clause,
    independent of what content is referred to in the "content" property.

    An "except" clause specifies exceptions to what's being granted by
    the rule.  It does not cause the rule to revoke any access that may
    be granted by another rule.

    ARGUMENTS:
        jsonRep - a dictionary supplying properties; do not specify;
            for internal use only
    """

    def __init__(self, jsonRep: dict={}):
        self.__operationClasses = []
        self.__content = []

        if jsonRep:
            operationClassesJson = jsonRep.get("operationClasses")
            if isinstance(operationClassesJson, list) \
                    and "*" not in operationClassesJson:
                for operationClassStr in operationClassesJson:
                    operationClass = OperationClass(operationClassStr)
                    self.__operationClasses.append(operationClass)

            contentJson = jsonRep.get("content")
            if isinstance(contentJson, list):
                for contentRefJson in contentJson:
                    self.__content.append(ContentRef(None, contentRefJson))

    @property
    def operationClasses(self) -> list[OperationClass]:
        """the operation classes that are being granted (or excepted in
        the case of an "except" clause); if empty, all operation classes
        are granted (or excepted)"""
        return self.__operationClasses

    @property
    def content(self) -> list[ContentRef]:
        """the content that's being granted (or excepted in the case
        of an "except" clause); if empty, all content is granted (or
        excepted)"""
        return self.__content

    @property
    def _jsonRep(self) -> dict:
        jsonRep = {}

        if self.__operationClasses:
            jsonRep["operationClasses"] = operationClassesJson = []
            for operationClass in self.__operationClasses:
                operationClassesJson.append(str(operationClass))

        if self.__content:
            jsonRep["content"] = contentJson = []
            for contentRef in self.__content:
                contentJson.append(contentRef._jsonRep)

        return jsonRep

    def __repr__(self):
        return repr(self._jsonRep)


class AccessControlRule:
    """A CubeWerx Access Control Rule.

    A rule grants whatever is specified by the "grant" clauses minus
    whatever is specified by the "except" clauses.

    ARGUMENTS:
        jsonRep - a dictionary supplying properties; do not specify;
            for internal use only
    """

    def __init__(self, jsonRep: dict={}):
        self.__appliesTo = []
        self.__expiresAt = None
        self.__grants = []
        self.__excepts = []

        if jsonRep:
            appliesTo = jsonRep.get("appliesTo")
            if isinstance(appliesTo, list):
                self.__appliesTo = appliesTo # future compatibility
            else:
                self.__appliesTo = str(appliesTo).split(",")

            expiresAtStr = jsonRep.get("expiresAt")
            if expiresAtStr:
                self.__expiresAt = \
                    datetime.datetime.fromisoformat(expiresAtStr)

            grantsJson = jsonRep.get("grants")
            if isinstance(grantsJson, list):
                for grantJson in grantsJson:
                    self.__grants.append(AccessControlRuleClause(grantJson))

            exceptsJson = jsonRep.get("excepts")
            if isinstance(exceptsJson, list):
                for exceptJson in exceptsJson:
                    self.__excepts.append(AccessControlRuleClause(exceptJson))

    @property
    def appliesTo(self) -> list[str]:
        """the identities that this rule applies to; a specific syntax
        is required for each identity (e.g., "cwAuth{*}", "cwAuth{jsmith}",
        "cwAuth{%Analyst}", "oidConnect{mySub@https://myIssuer.com}",
        "oidConnect{https://myIssuer.com}", "ipAddress{20.76.201.171}",
        ipAddress{20.76.201}", "everybody")"""
        return self.__appliesTo

    # TODO: Hide the ugly string-encoded syntax for the different identity
    # types.  Perhaps we should tie the AuthUser and OidUser classes together
    # with an Identity base class, and add AuthRole IpAddress and Everybody
    # classes.

    @property
    def expiresAt(self) -> datetime.datetime | None:
        """when this rule expires, or None for never; after this date and
        time, the rule ceases to grant access"""
        return self.__expiresAt

    @expiresAt.setter
    def expiresAt(self, value: datetime.datetime | None):
        self.__expiresAt = value

    @property
    def grants(self) -> list[AccessControlRuleClause]:
        """the clauses that indicate what's being granted by this rule"""
        return self.__grants

    @property
    def excepts(self) -> list[AccessControlRuleClause]:
        """the clauses that indicate exceptions to what's being granted
        by this rule; note that these clauses do not revoke any access
        that may be granted by another rule"""
        return self.__excepts

    @property
    def _jsonRep(self) -> dict:
        jsonRep = {}
        jsonRep["appliesTo"] = ",".join(self.__appliesTo)
        if (self.__expiresAt):
            jsonRep["expiresAt"] = self.__expiresAt.isoformat()

        jsonRep["grants"] = grants = []
        for grantClause in self.__grants:
            grants.append(grantClause._jsonRep)

        if self.__excepts:
            jsonRep["excepts"] = excepts = []
            for exceptClause in self.__excepts:
                excepts.append(exceptClause._jsonRep)

        return jsonRep

    def __repr__(self):
        return repr(self._jsonRep)
