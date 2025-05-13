# $Id: Stats.py 79029 2025-05-01 15:39:41Z pomakis $

class Stats:
    """System statistics.
    """

    def __init__(self, jsonRep: dict):
        self.__nActiveUsers = jsonRep.get("nActiveUsers")
        self.__loadAverage = tuple(jsonRep.get("loadAverage"))
        self.__nCpus = jsonRep.get("nCpus")
        memory = jsonRep.get("memory")
        self.__memoryUsed = memory.get("used") if memory else -1
        self.__memoryTotal = memory.get("total") if memory else -1

    @property
    def nActiveUsers(self) -> list[int]:
        """the number of unique users that have used the product per
        specified time period, for the last specified number of time
        periods, in forward chronological order; for example, if the
        request was for nPeriods=24 and nSecondsPerPeriod=3600, then
        this list would contain 24 items with the last item indicating
        the number of unique users that have used the product within
        the past hour and the previous item indicating the number of
        unique users that have used the product during the hour before
        that, etc."""
        return self.__nActiveUsers

    @property
    def loadAverage(self) -> tuple[float, float, float]:
        """the current load average of the system over the last 1, 5 and
        15 minutes, respectively; for a normalized system load, divide
        by the number of CPUs on the system"""
        return self.__loadAverage

    @property
    def nCpus(self) -> float:
        """the number of CPUs on the system"""
        return self.__nCpus

    @property
    def memoryUsed(self) -> int:
        """the number of bytes of physical memory on the system that are
        currently being used"""
        return self.__memoryUsed

    @property
    def memoryTotal(self) -> int:
        """the number of bytes of physical memory on the system"""
        return self.__memoryTotal
