
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
    reader = csv.DictReader(csvfile, delimiter=',')
    higher = 2005
    i =0
    for row in reader:
        i=i+1
        x = float(row['Latitude'])/180
        y = float(row['Longitude'])/90
        rad = float(row['Radius'])/2000
        year = (int(row['Year'])-1945)/60
        print(i, " : ",x,y,rad,year)
        table.append(Impact(x,y,rad,year))
        compare = int(row['Year'])
        if compare < higher:
            higher = int(row['Year'])
    print("higher:",higher)

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
        fname = "database.csv"
        table = []
        with open (fname) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            #higher = 2005
            #i =0
            for row in reader:
                #i=i+1
                x = float(row['Latitude'])/180
                y = float(row['Longitude'])/90
                rad = float(row['Radius'])/2000
                year = (int(row['Year'])-1945)/60
                #print(i, " : ",x,y,rad,year)
                table.append(Impact(x,y,rad,year))
        return table
