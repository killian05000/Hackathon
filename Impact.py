
# https://upload.wikimedia.org/wikipedia/commons/0/00/Mercator-proj.jpg
# https://docs.python.org/3.5/library/collections.html#collections.namedtuple
# https://docs.python.org/3.5/library/csv.html#module-csv

import collections
from abc import ABC, abstractmethod
import csv

Impact = collections.namedtuple('Impact', ['x', 'y', 'strength', 'when'])

fname = "database.csv"
table = []
with open (fname) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        print(row['lat']," | ",row['lon'])
        #table.append(Impact(row['lat'],row['lon'],"0000",row['date'])
#return table

class ImpactReader(ABC):
    @abstractmethod
    def getImpacts(self):
        pass

class ImpactZone(ABC):
    @abstractmethod
    def applyImpact(self, impact):
        pass

class FakeImpactReader(ImpactReader):
    def getImpacts(self):
        impacts = []
        max = 10
        for i in range(max):
            impacts.append(Impact(i/max, i/max, i/max, i/max))
        return impacts

class FakeImpactZone(ImpactZone):
    def applyImpact(self, impact):
        print(impact)

class CSVImpactReader(ImpactReader):
    def read(fileName):
        with open(fileName) as csvfile:
            minImpact = Impact(x = -180, y = -90, strength = -1, when = -1)
            maxImpact = Impact(x = 180, y = 90, strength = 0, when = 0)
            for impact in map(Impact._make, csv.reader(csvfile)):
                # lattitude = impact.y
                # longitude = impact.x
                latitude_percent = y

                print(emp.name, emp.title)
