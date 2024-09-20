bl_info = {
    "name": "STOOL",
    "author": "ST",
    "version": (3, 36),
    "blender": (2, 90, 0),
}

import bpy
from bpy.types import Operator
from bpy.props import (
        StringProperty,
        BoolProperty,
        EnumProperty,
        )

class NewpanelST(bpy.types.Panel):
    bl_label = "STOOL"
    bl_idname = "OBJECT_PT_STOOL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        layout.operator("object.parent_to_empty_visn")
        layout.operator("object.clear_parent_visn")
        layout.operator("object.release_all_children_visn")
        layout.operator("object.pickup_new_parent_visn")
        layout.operator("object.fast_set_parent_visn") 

def register():
    bpy.utils.register_class(NewpanelST)
    bpy.utils.register_class(P2E)
    bpy.utils.register_class(ClearParent)
    bpy.utils.register_class(RAQ)
    bpy.utils.register_class(PickupNewParent)
    bpy.utils.register_class(fastSetParent)
    
def unregister():
    bpy.utils.unregister_class(NewpanelST)
    bpy.utils.unregister_class(P2E)
    bpy.utils.unregister_class(ClearParent)
    bpy.utils.unregister_class(RAQ)
    bpy.utils.unregister_class(PickupNewParent)
    bpy.utils.unregister_class(fastSetParent)
    
def centro(sel):
    x = sum([obj.location[0] for obj in sel]) / len(sel)
    y = sum([obj.location[1] for obj in sel]) / len(sel)
    z = sum([obj.location[2] for obj in sel]) / len(sel)
    return (x, y, z)

def getChildren(myObject): 
    children = [] 
    for ob in bpy.data.objects: 
        if ob.parent == myObject: 
            children.append(ob) 
    return children 

class PickupNewParent(Operator):
    bl_idname = "object.pickup_new_parent_visn"
    bl_label = "Pickup to New Parent"
    bl_description = "pickup anywhere selected objects to new parent"
    bl_options = {"REGISTER", "UNDO"}

    nombre: StringProperty(
                    name="",
                    default='OBJECTS',
                    description='Give the empty / group a name'
                    )
    grupo: BoolProperty(
                    name="Create Group",
                    default=False,
                    description="Also add objects to a group"
                    )
    locat: EnumProperty(
                    name='',
                    items=[('CURSOR', 'Cursor', 'Cursor'), ('ACTIVE', 'Active', 'Active'),
                           ('CENTER', 'Center', 'Selection Center')],
                    description='Empty location',
                    default='CENTER'
                   )

    def execute(self, context):
        objs = context.selected_objects
        act = context.object
        sce = context.scene
        try:
            bpy.ops.object.mode_set()
        except:
            pass
        for obj in objs:
            obj.select_set(True)
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            obj.select_set(False)
            
        if self.locat == 'CURSOR':
            loc = sce.cursor.location
        elif self.locat == 'ACTIVE':
            loc = act.location
        else:
            loc = centro(objs)
   
        bpy.ops.object.add(type='EMPTY', location=loc)
        context.object.name = self.nombre
        context.object.show_name = True
        context.object.show_in_front = True
            
        if self.grupo:
            bpy.ops.collection.create(name=self.nombre)
            bpy.ops.collection.objects_add_active()

        for o in objs:
            o.select_set(True)
            if not o.parent:
                bpy.ops.object.parent_no_inverse_set(keep_transform=True)
            if self.grupo:
                bpy.ops.collection.objects_add_active()
            o.select_set(False)
            
        return {'FINISHED'}
        return {'FINISHED'}

class fastSetParent(Operator):
    bl_idname = "object.fast_set_parent_visn"
    bl_label = "Fast Parent"
    bl_description = "one click to parent"
    bl_options = {"REGISTER", "UNDO"}
    def execute(self, context):
        try:
            bpy.ops.object.mode_set()
        except:
            pass
        bpy.ops.object.parent_no_inverse_set(keep_transform=True)
        return {'FINISHED'}
    

class ClearParent(Operator):
    bl_idname = "object.clear_parent_visn"
    bl_label = "Clear Parent"
    bl_description = "clear the parent of object"
    bl_options = {"REGISTER", "UNDO"}
    def execute(self, context):
        objs = context.selected_objects
        act = context.object
        sce = context.scene

        try:
            bpy.ops.object.mode_set()
        except:
            pass

        for obj in objs:
            obj.select_set(True)
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            obj.select_set(False)
        return {'FINISHED'}

class RAQ(Operator):    
    bl_idname = "object.release_all_children_visn"
    bl_label = "Release children"
    bl_description = "clear all the children of selected objects"
    bl_options = {"REGISTER", "UNDO"}
    def execute(self, context):
        objs = context.selected_objects
        act = context.object
        sce = context.scene

        try:
            bpy.ops.object.mode_set()
        except:
            pass

        for obj in objs:
            for children in getChildren(obj):
                children.select_set(True)
                bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                children.select_set(False)
        return {'FINISHED'}
    

class P2E(Operator):
    bl_idname = "object.parent_to_empty_visn"
    bl_label = "Parent to Empty"
    bl_description = "Parent selected objects to a new Empty"
    bl_options = {"REGISTER", "UNDO"}

    nombre: StringProperty(
                    name="",
                    default='OBJECTS',
                    description='Give the empty / group a name'
                    )
    grupo: BoolProperty(
                    name="Create Group",
                    default=False,
                    description="Also add objects to a group"
                    )
    locat: EnumProperty(
                    name='',
                    items=[('CURSOR', 'Cursor', 'Cursor'), ('ACTIVE', 'Active', 'Active'),
                           ('CENTER', 'Center', 'Selection Center')],
                    description='Empty location',
                    default='CENTER'
                   )

    @classmethod
    def poll(cls, context):
        objs = context.selected_objects
        return (len(objs) > 0)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "nombre")
        column = layout.column(align=True)
        column.prop(self, "locat")
        column.prop(self, "grupo")

    def execute(self, context):
        objs = context.selected_objects
        act = context.object
        sce = context.scene

        try:
            bpy.ops.object.mode_set()
        except:
            pass

        if self.locat == 'CURSOR':
            loc = sce.cursor.location
        elif self.locat == 'ACTIVE':
            loc = act.location
        else:
            loc = centro(objs)

        sameParent = True
        for o in objs:
            if not o.parent:
                sameParent = False
                break
            sameParent = o.parent == objs[0].parent
            
              
        bpy.ops.object.add(type='EMPTY', location=loc)
        context.object.name = self.nombre
        context.object.show_name = True
        context.object.show_in_front = True
        if sameParent:
            context.object.parent = objs[0].parent
            
        if self.grupo:
            bpy.ops.collection.create(name=self.nombre)
            bpy.ops.collection.objects_add_active()

        for o in objs:
            o.select_set(True)
            if not o.parent:
                bpy.ops.object.parent_no_inverse_set(keep_transform=True)
            if sameParent:
                bpy.ops.object.parent_no_inverse_set(keep_transform=True)
            if self.grupo:
                bpy.ops.collection.objects_add_active()
            o.select_set(False)
            
        return {'FINISHED'}
