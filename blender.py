
# https://upload.wikimedia.org/wikipedia/commons/0/00/Mercator-proj.jpg
# https://docs.python.org/3.5/library/collections.html#collections.namedtuple
# https://docs.python.org/3.5/library/csv.html#module-csv

import collection
from abc import ABC, abstractmethod
import csv
import bpy

Impact = collection.namedtuple('Impact', ['x', 'y', 'strength', 'when'])

class ImpactReader(ABC):
    @abstractmethod
    def getImpacts(self):
        pass

class ImpactZone(ABC):
    @abstractmethod
    def applyImpact(self, impact):
        pass

class CSVImpactReader(ImpactReader):
    def read(fileName):
        with open(fileName) as csvfile:
            minImpact = Impact(x = -180, y = -90, strength = -1, when = -1)
            maxImpact = Impact(x = 180, y = 90, strength = 0, when = 0)
            for impact in map(Impact._make, csv.reader(csvfile)):
                print(emp.name, emp.title)

class BlenderImpactZone(ImpactZone):
    pass

# g = bpy.data.groups.new('supergroupe')
# g.objects.link(bpy.data.objects['Cube'])
#
# lamp_object.location = (5.0, 5.0, 5.0)

def main(context):
    #bpy.ops.object.effector_add()
    for ob in context.scene.objects:
        print(ob)

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleOperator)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()
