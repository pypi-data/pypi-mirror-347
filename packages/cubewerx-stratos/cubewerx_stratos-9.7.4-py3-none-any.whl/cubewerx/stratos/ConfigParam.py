# $Id: ConfigParam.py 78752 2025-03-10 20:24:19Z pomakis $

import requests
import math
from enum import StrEnum

from .MultilingualString import *
from .CwException import *


class ConfigParamType(StrEnum):
    """An enumeration of the configuration parameter types.
    """

    BOOLEAN             = "Boolean"
    NUMBER              = "Number"
    STRING              = "String"
    PASSWORD            = "Password"
    PERCENTAGE          = "Percentage"
    URL                 = "URL"
    DURATION            = "Duration"
    ENUMERATED          = "Enumerated"
    MULTILINGUAL_STRING = "MultilingualString"
    STRING_LIST         = "StringList"
    STRING_MAP          = "StringMap"
    JSON                = "JSON"

    # ugly hack to handle case insensitive parsing from server
    @staticmethod
    def _parse(typeStr: str):
        lowerTypeStr = typeStr.lower()
        if lowerTypeStr == "boolean":
            return ConfigParamType.BOOLEAN
        elif lowerTypeStr == "number":
            return ConfigParamType.NUMBER
        elif lowerTypeStr == "string":
            return ConfigParamType.STRING
        elif lowerTypeStr == "password":
            return ConfigParamType.PASSWORD
        elif lowerTypeStr == "percentage":
            return ConfigParamType.PERCENTAGE
        elif lowerTypeStr == "url":
            return ConfigParamType.URL
        elif lowerTypeStr == "duration":
            return ConfigParamType.DURATION
        elif lowerTypeStr == "multilingualstring":
            return ConfigParamType.MULTILINGUAL_STRING
        elif lowerTypeStr == "stringlist":
            return ConfigParamType.STRING_LIST
        elif lowerTypeStr == "stringmap":
            return ConfigParamType.STRING_MAP
        elif lowerTypeStr == "json":
            return ConfigParamType.JSON
        else:
            return ConfigParamType.STRING


class ConfigParam:
    """The details of a CubeWerx Stratos configuration parameter.
    """

    def __init__(self, jsonRep: dict, configUrl: str, authorizationToken: str):
        self.__initFromJsonRep(jsonRep)
        self.__configParamUrl = configUrl + "/" + self.__name
        self.__authorizationToken = authorizationToken

    def __initFromJsonRep(self, jsonRep: dict):
        self.__name = jsonRep.get("name")
        self.__description = jsonRep.get("description")
        self.__type = ConfigParamType._parse(jsonRep.get("type", "String"))
        self.__range = jsonRep.get("range")
        self.__isGlobal = jsonRep.get("isGlobal", False)
        self.__defaultValueStr = jsonRep.get("defaultValueStr")
        self.__explicitValueStr = jsonRep.get("explicitValueStr")

        if "defaultValue" in jsonRep.keys():
            rawDefaultVal = jsonRep.get("defaultValue")
            if self.__type == ConfigParamType.NUMBER:
                self.__defaultValue = \
                    math.inf if rawDefaultVal is None else rawDefaultVal
            elif self.__type == ConfigParamType.MULTILINGUAL_STRING:
                self.__defaultValue = MultilingualString(rawDefaultVal)
            else:
                self.__defaultValue = rawDefaultVal
        else:
            self.__defaultValue = None

        if "explicitValue" in jsonRep.keys():
            rawExplicitVal = jsonRep.get("explicitValue")
            if self.__type == ConfigParamType.NUMBER:
                self.__explicitValue = \
                    math.inf if rawExplicitVal is None else rawExplicitVal
            elif self.__type == ConfigParamType.MULTILINGUAL_STRING:
                self.__explicitValue = MultilingualString(rawExplicitVal)
            else:
                self.__explicitValue = rawExplicitVal
        else:
            self.__explicitValue = None

    @property
    def name(self) -> str:
        """the name of this configuration parameter"""
        return self.__name

    @property
    def description(self) -> str | None:
        """a description of this configuration parameter, or None"""
        return self.__description

    @property
    def type(self) -> ConfigParamType:
        """the type of this configuration parameter"""
        return self.__type

    @property
    def range(self) -> list[str]:
        """the list of allowed case-insensitive values of this configuration
        parameter if of type ENUMERATED, or None otherwise"""
        return self.__range

    @property
    def isGlobal(self) -> bool:
        """whether or not this is a global configuration parameter that
        affects all deployments"""
        return self.__isGlobal

    @property
    def defaultValueStr(self) -> str:
        """the string representation of the default value of this
        configuration parameter"""
        return self.__defaultValueStr

    @property
    def defaultValue(self):
        """the default value of this configuration parameter, expressed as
        the appropriate Python type according to the following table

        Config Param Type    Python type
        -----------------    -----------
        BOOLEAN              bool
        NUMBER               float (can be math.inf)
        STRING               str
        PASSWORD             str
        PERCENTAGE           float (0..100)
        URL                  str
        DURATION             float (in seconds)
        ENUMERATED           str
        MULTILINGUAL_STRING  cubewerx.stratos.MultilingualString
        STRING_LIST          list[str]
        STRING_MAP           dict[str,str]
        JSON                 bool|int|float|str|list|dict
        """
        return self.__defaultValue

    @property
    def explicitValueStr(self) -> str | None:
        """the string representation of the value that's explicitly set
        for this configuration parameter, or None if the default value
        is active; setting this (or clearing it by setting it to None)
        will automatically update the server"""
        return self.__explicitValueStr

    @explicitValueStr.setter
    def explicitValueStr(self, valueStr: str):
        paramUrl = self.__configParamUrl;
        if valueStr is None:
            requestHeaders = {
                "Authorization": "CwAuth " + self.__authorizationToken
            }
            response = requests.delete(paramUrl, headers=requestHeaders)
            ServerException.raise_for_status(response)
            self.__explicitValue = None
            self.__explicitValueStr = None
        else:
            requestHeaders = {
                "Content-Type": "text/plain; charset=utf-8",
                "Accept": "application/json",
                "Authorization": "CwAuth " + self.__authorizationToken
            }
            response = requests.put(paramUrl, headers=requestHeaders,
                data=str(valueStr).encode('utf-8'))
            ServerException.raise_for_status(response)
            responseJson = response.json()
            self.__initFromJsonRep(response.json())

    @property
    def explicitValue(self):
        """the value that's explicitly set for this configuration
        parameter, expressed as the appropriate Python type, or None if
        the default value is active; setting this (or clearing it by
        setting it to None) will automatically update the server

        Config Param Type    Python type
        -----------------    -----------
        BOOLEAN              bool
        NUMBER               float (can be math.inf)
        STRING               str
        PASSWORD             str
        PERCENTAGE           float (0..100)
        URL                  str
        DURATION             float (in seconds)
        ENUMERATED           str
        MULTILINGUAL_STRING  cubewerx.stratos.MultilingualString
        STRING_LIST          list[str]
        STRING_MAP           dict[str,str]
        JSON                 bool|int|float|str|list|dict
        """
        return self.__explicitValue

    @explicitValue.setter
    def explicitValue(self, value):
        paramUrl = self.__configParamUrl;
        if value is None:
            requestHeaders = {
                "Authorization": "CwAuth " + self.__authorizationToken
            }
            response = requests.delete(paramUrl, headers=requestHeaders)
            ServerException.raise_for_status(response)
            self.__explicitValue = None
            self.__explicitValueStr = None
        else:
            # Convert the value to the appropriate JSON type if necessary.
            try:
                if self.__type == ConfigParamType.BOOLEAN:
                    jsonRep = bool(value)
                elif self.__type == ConfigParamType.NUMBER:
                    jsonRep = float(value)
                    if (math.isinf(jsonRep)): jsonRep = None
                elif self.__type == ConfigParamType.STRING:
                    jsonRep = str(value)
                elif self.__type == ConfigParamType.PASSWORD:
                    jsonRep = str(value)
                elif self.__type == ConfigParamType.PERCENTAGE:
                    jsonRep = max(min(float(value), 100), 0)
                elif self.__type == ConfigParamType.URL:
                    jsonRep = str(value)
                elif self.__type == ConfigParamType.DURATION:
                    jsonRep = max(float(value), 0)
                elif self.__type == ConfigParamType.ENUMERATED:
                    jsonRep = str(value)
                elif self.__type == ConfigParamType.MULTILINGUAL_STRING:
                    jsonRep = value._jsonRep
                elif self.__type == ConfigParamType.STRING_LIST:
                    jsonRep = []
                    for strVal in value:
                        jsonRep.append(str(strVal))
                elif self.__type == ConfigParamType.STRING_MAP:
                    jsonRep = {}
                    for key, value in dict(value).items():
                        jsonRep[str(key)] = str(value)
                else:
                    jsonRep = value
            except TypeError as e:
                raise TypeError("type of value must be compatible with " +
                    "configuration parameter type")

            requestHeaders = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "CwAuth " + self.__authorizationToken
            }
            response = requests.put(paramUrl, headers=requestHeaders,
                json=jsonRep)
            ServerException.raise_for_status(response)
            responseJson = response.json()
            self.__initFromJsonRep(response.json())

