import bpy

# Impact file

import collections
from abc import ABC, abstractmethod
import csv
import random

saveObject = bpy.context.scene.world

bpy.data.groups.new('explosion')
for k in ["hack_width", "hack_height", "hack_strength", "hack_z", "hack_frame"]:
    if not k in saveObject.keys():
        saveObject[k] = 0

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
    def __init__(self):
        self.array = []

    def getImpacts(self):
        return self.array

    def read(self, fileName):
        self.array = []
        with open (fileName) as csvfile:
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
                self.array.append(Impact(x,y,rad,year))

class FakeImpactReader(ImpactReader):
    def getImpacts(self):
        impacts = []
        x = [0.617, 0.497, 0.34,0.509,0.583,0.262,0.55,0.645,0.761,0.194,0.583,0.326,0.816,0.886,0.602,0.534,0.485,0.32,0.511,0.555,0.703,0.618,0.204,0.81,0.112,0.899,0.754,0.586,0.223,0.295,0.845,0.857,0.495,0.239,0.872,0.662,0.775,0.241,0.493,0.586,0.509]
        y = [0.4,0.4,0.522,0.329,0.407,0.371,0.555,0.223,0.257,0.309,0.524,0.627,0.238,0.375,0.462,0.315,0.352,0.575,0.442,0.474,0.4,0.235,0.286,0.412,0.219,0.19,0.341,0.545,0.429,0.504,0.229,0.32,0.286,0.21,0.593,0.348,0.268,0.3,0.458,0.306,0.435]
        for i in range(41):
            impacts.append(Impact(x[i], y[i], random.uniform(0.2, 0.4), random.random()))
        return impacts


class BlenderImpactZone(ImpactZone):
    def __init__(self):
        self.g = bpy.data.groups.new('hack')
        self.width = saveObject["hack_width"]
        self.height = saveObject["hack_height"]
        self.strength = saveObject["hack_strength"]
        self.z = saveObject["hack_z"]
        self.frame = saveObject["hack_frame"]

    def applyImpact(self, impact):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, size=impact.strength*self.strength, location=(impact.x*self.width, impact.y*self.height, 0))
        o = bpy.context.scene.objects.active
        self.g.objects.link(o)
        f = impact.when*self.frame
        o.keyframe_insert(data_path="location", frame=f, index=2)
        o.location[2] = self.z
        o.keyframe_insert(data_path="location", frame=f-1, index=2)

        bpy.ops.object.modifier_add(type='DYNAMIC_PAINT')
        o.modifiers['Dynamic Paint'].ui_type = 'BRUSH'
        bpy.ops.dpaint.type_toggle(type='BRUSH')

        bpy.ops.object.particle_system_add()
        s = bpy.context.scene.objects.active.modifiers['ParticleSystem 1'].particle_system.settings
        s.count = 50
        s.frame_end = f
        s.frame_start = f
        s.normal_factor = 5
        s.object_align_factor[2] = 10
        s.use_rotations = True
        s.phase_factor_random = 2
        s.use_render_emitter = False
        s.size_random = 0.9
        s.render_type = 'GROUP'
        s.dupli_group = bpy.data.groups['explosion']

def main(context):
    # ir = CSVImpactReader()
    # ir.read("database.csv")
    ir = FakeImpactReader()
    iz = BlenderImpactZone()
    impacts = ir.getImpacts()
    for impact in impacts:
        iz.applyImpact(impact)

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    width = bpy.props.FloatProperty(name="Width", default=saveObject["hack_width"])
    height = bpy.props.FloatProperty(name="Height", default=saveObject["hack_height"])
    strength = bpy.props.FloatProperty(name="Strength", default=saveObject["hack_strength"])
    z = bpy.props.FloatProperty(name="Z", default=saveObject["hack_z"])
    frame = bpy.props.FloatProperty(name="Frame", default=saveObject["hack_frame"])

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        saveObject["hack_width"] = self.width
        saveObject["hack_height"] = self.height
        saveObject["hack_strength"] = self.strength
        saveObject["hack_z"] = self.z
        saveObject["hack_frame"] = self.frame

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
