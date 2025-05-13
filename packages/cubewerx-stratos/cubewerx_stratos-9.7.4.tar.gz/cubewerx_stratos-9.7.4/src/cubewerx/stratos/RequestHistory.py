# $Id: RequestHistory.py 78570 2025-01-23 18:57:06Z pomakis $

# TODO: we need some general way of handling server-output-not-
# as-expected exceptions

import datetime


class RequestSummary:
    """A summary of requests made and response bytes sent.
    """

    def __init__(self, jsonRep: dict):
        self.__nRequests = jsonRep.get("nRequests")
        self.__nBytes = jsonRep.get("nBytes")

    @property
    def nRequests(self) -> int:
        """the number of requests made"""
        return self.__nRequests

    @property
    def nBytes(self) -> int:
        """the number of response bytes sent"""
        return self.__nBytes


class RequestSummaries:
    """Summaries of requests made and response bytes sent by category.
    """

    def __init__(self, jsonRep: dict):
        self.__coverages = RequestSummary(jsonRep.get("coverages"))
        self.__vectors = RequestSummary(jsonRep.get("vectors"))
        self.__maps = RequestSummary(jsonRep.get("maps"))
        self.__tiles = RequestSummary(jsonRep.get("tiles"))
        self.__offlineDownloads = RequestSummary(
            jsonRep.get("offlineDownloads"))
        self.__other = RequestSummary(jsonRep.get("other"))
        self.__total = RequestSummary(jsonRep.get("total"))

    @property
    def coverages(self) -> RequestSummary:
        """summary of the coverage data (excluding tile requests)"""
        return self.__coverages

    @property
    def vectors(self) -> RequestSummary:
        """summary of the vector data (excluding tile requests)"""
        return self.__vectors

    @property
    def maps(self) -> RequestSummary:
        """summary of the map data (excluding tile requests)"""
        return self.__maps

    @property
    def tiles(self) -> RequestSummary:
        """summary of the tile data"""
        return self.__tiles

    @property
    def offlineDownloads(self) -> RequestSummary:
        """summary of the offline downloads"""
        return self.__offlineDownloads

    @property
    def other(self) -> RequestSummary:
        """summary of all other requests"""
        return self.__other

    @property
    def total(self) -> RequestSummary:
        """summary of all requests"""
        return self.__total


class RequestPeriod:
    """A summary of the recent request history for a specific time period.
    """

    def __init__(self, jsonRep: dict):
        self.__fromDate = datetime.date.fromisoformat(jsonRep.get("fromDate"))
        self.__toDate = datetime.date.fromisoformat(jsonRep.get("toDate"))
        self.__summaries = RequestSummaries(jsonRep.get("summaries"))

    @property
    def fromDate(self) -> datetime.date:
        """the start date (inclusive) of the time period"""
        return self.__fromDate

    @property
    def toDate(self) -> datetime.date:
        """the end date (inclusive) of the time period"""
        return self.__toDate

    @property
    def summaries(self) -> RequestSummaries:
        """a summary of the recent request history for this time period"""
        return self.__summaries


class RequestHistory:
    """A summary of the recent request history.
    """

    def __init__(self, jsonRep: dict):
        periodType = jsonRep.get("periodType")
        self.__periodTypeNoun = periodType.get("noun")
        self.__periodTypeAdjective = periodType.get("adjective")

        self.__periods = []
        for periodJsonRep in jsonRep.get("periods"):
            self.__periods.append(RequestPeriod(periodJsonRep))

        self.__dailyAverages = RequestSummaries(jsonRep.get("dailyAverages"))

    @property
    def periodTypeNoun(self) -> str:
        """the granularity of the time periods, expressed as a noun"""
        return self.__periodTypeNoun

    @property
    def periodTypeAdjective(self) -> str:
        """the granularity of the time periods, expressed as an adjective"""
        return self.__periodTypeAdjective

    @property
    def periods(self) -> list[RequestPeriod]:
        """summaries per time period, in forward chronological order"""
        return self.__periods

    @property
    def dailyAverages(self) -> RequestSummaries:
        """daily averages of request activity"""
        return self.__dailyAverages
