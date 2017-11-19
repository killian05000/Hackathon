import bpy

# Impact file

import collections
from abc import ABC, abstractmethod
import csv
import random

for k in ["hack_width", "hack_height", "hack_strength", "hack_z", "hack_frame"]:
    if not k in bpy.context.object.keys():
        bpy.context.object[k] = 0

Impact = collections.namedtuple('Impact', ['x', 'y', 'strength', 'when'])

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
            minImpact = Impact(x = -180, y = -90, strength = -1, time = -1)
            maxImpact = Impact(x = 180, y = 90, strength = 0, time = 0)
            for impact in map(Impact._make, csv.reader(csvfile)):
                print(emp.name, emp.title)

class FakeImpactReader(ImpactReader):
    def getImpacts(self):
        impacts = []
        max = 10
        for i in range(max):
            impacts.append(Impact(random.random(), random.random(), random.random(), random.random()))
        return impacts


class BlenderImpactZone(ImpactZone):
    def __init__(self):
        self.g = bpy.data.groups.new('hack')
        self.width = bpy.context.object["hack_width"]
        self.height = bpy.context.object["hack_height"]
        self.strength = bpy.context.object["hack_strength"]
        self.z = bpy.context.object["hack_z"]
        self.frame = bpy.context.object["hack_frame"]

    def applyImpact(self, impact):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, size=impact.strength*self.strength, location=(impact.x*self.width, impact.y*self.height, 0))
        o = bpy.context.scene.objects.active
        self.g.objects.link(o)
        f = impact.when*self.frame
        o.keyframe_insert(data_path="location", frame=f, index=2)
        o.location[2] = self.z
        o.keyframe_insert(data_path="location", frame=f-1, index=2)

def main(context):
    ir = FakeImpactReader()
    iz = BlenderImpactZone()
    impacts = ir.getImpacts()
    for impact in impacts:
        iz.applyImpact(impact)

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    width = bpy.props.FloatProperty(name="Width", default=bpy.context.object["hack_width"])
    height = bpy.props.FloatProperty(name="Height", default=bpy.context.object["hack_height"])
    strength = bpy.props.FloatProperty(name="Strength", default=bpy.context.object["hack_strength"])
    z = bpy.props.FloatProperty(name="Z", default=bpy.context.object["hack_z"])
    frame = bpy.props.FloatProperty(name="Frame", default=bpy.context.object["hack_frame"])

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.context.object["hack_width"] = self.width
        bpy.context.object["hack_height"] = self.height
        bpy.context.object["hack_strength"] = self.strength
        bpy.context.object["hack_z"] = self.z
        bpy.context.object["hack_frame"] = self.frame

        main(context)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

def register():
    bpy.utils.register_class(SimpleOperator)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)

if __name__ == "__main__":
    register()
