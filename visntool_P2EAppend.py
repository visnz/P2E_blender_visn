bl_info = {
    "name": "STOOL",
    "author": "ST",
    "version": (0, 2, 2),
    "blender": (4, 0, 0),
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
        layout.operator("object.fast_set_parent_visn") 
        layout.operator("object.clear_parent_visn")
        layout.operator("object.select_parent_visn")
        layout.operator("object.select_children_visn")
        layout.operator("object.release_all_children_to_world_visn")
        layout.operator("object.release_all_children_to_subparent_visn")
        layout.operator("object.solo_pick_visn")
        layout.operator("object.pickup_new_parent_visn")
        layout.operator("object.fast_camera_visn")

def register():
    bpy.utils.register_class(NewpanelST)
    bpy.utils.register_class(P2E)
    bpy.utils.register_class(ClearParent)
    bpy.utils.register_class(RAQ)
    bpy.utils.register_class(RAQtoSubparent)
    bpy.utils.register_class(PickupNewParent)
    bpy.utils.register_class(fastSetParent)
    bpy.utils.register_class(selectChildren)
    bpy.utils.register_class(selectParent)
    bpy.utils.register_class(soloPick)
    bpy.utils.register_class(fastCentreCamera)
   
def unregister():
    bpy.utils.unregister_class(NewpanelST)
    bpy.utils.unregister_class(P2E)
    bpy.utils.unregister_class(ClearParent)
    bpy.utils.unregister_class(RAQ)
    bpy.utils.unregister_class(RAQtoSubparent)
    bpy.utils.unregister_class(PickupNewParent)
    bpy.utils.unregister_class(fastSetParent)
    bpy.utils.unregister_class(selectChildren)
    bpy.utils.unregister_class(selectParent)
    bpy.utils.unregister_class(soloPick)
    bpy.utils.unregister_class(fastCentreCamera)
    
def centro(sel):
    x = sum([obj.location[0] for obj in sel]) / len(sel)
    y = sum([obj.location[1] for obj in sel]) / len(sel)
    z = sum([obj.location[2] for obj in sel]) / len(sel)
    return (x, y, z)

def centroGlobal(sel):
    x = sum([obj.matrix_world.translation[0] for obj in sel]) / len(sel)
    y = sum([obj.matrix_world.translation[1] for obj in sel]) / len(sel)
    z = sum([obj.matrix_world.translation[2] for obj in sel]) / len(sel)
    return (x, y, z)

def getChildren(myObject): 
    children = [] 
    for ob in bpy.data.objects: 
        if ob.parent == myObject: 
            children.append(ob) 
    return children 

class fastCentreCamera(Operator):
    bl_idname = "object.fast_camera_visn"
    bl_label = "Fast Camera"
    bl_description = "Create camera stare at the selections"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        '''获取创建点'''
        objs = context.selected_objects
        if len(objs)==0:
            loc = (0,0,0)
        else:
            loc = centroGlobal(objs)
        '''创建摄像机'''
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.active_object.name = 'NewCamera'
        cams = context.selected_objects
        bpy.context.space_data.camera = cams[0]
        bpy.ops.view3d.camera_to_view()
        bpy.ops.object.add(type='EMPTY', location=cams[0].location, rotation=cams[0].rotation_euler)
        bpy.context.active_object.name = 'CameraProtection'
        bpy.ops.object.constraint_add(type='DAMPED_TRACK')
        camP = context.selected_objects
        cams[0].select_set(True)
        bpy.ops.object.parent_no_inverse_set(keep_transform=True)
        cams[0].lock_location[0]=True
        cams[0].lock_location[1]=True
        cams[0].lock_location[2]=True
        cams[0].lock_rotation[0]=True
        cams[0].lock_rotation[1]=True
        cams[0].lock_rotation[2]=True
        '''创建原点的空物体'''
        bpy.ops.object.add(type='EMPTY', location=loc)
        bpy.context.active_object.name = 'CameraCentre'
        camC = context.selected_objects
        camP[0].select_set(True)
        bpy.ops.object.parent_no_inverse_set(keep_transform=True)
        camP[0].select_set(False)
        cams[0].select_set(False)
        camP[0].constraints["Damped Track"].target = bpy.data.objects[camC[0].name]
        camP[0].constraints["Damped Track"].track_axis = 'TRACK_NEGATIVE_Z'

        return {'FINISHED'}

class soloPick(Operator):
    '''断开所选物体的所有父子级关系，捡出来放在世界层级，子级归更上一层父级管。'''
    bl_idname = "object.solo_pick_visn"
    bl_label = "Pickup Solo"
    bl_description = "Break all of the selections"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = context.selected_objects
        try:
            bpy.ops.object.mode_set()
        except:
            pass
        NOParent = False
        '''检测所有选中对象，取消选择'''
        for obj in objs:
            obj.select_set(False)
        for obj in objs:
            if not obj.parent:
                NOParent = True
                '''如果是世界内对象，则释放子级'''
                for children in getChildren(obj):
                    children.select_set(True)
                    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                    children.select_set(False)
                continue
            else:
                '''如果是父子级之间对象，则将子级释放到更上一层的父级'''
                for children in getChildren(obj):
                    children.select_set(True)
                    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                    bpy.context.view_layer.objects.active = obj.parent
                    bpy.ops.object.parent_no_inverse_set(keep_transform=True)
                    children.select_set(False)
        for obj in objs:
            '''清除所有选中对象的父级，完成取出。'''
            obj.select_set(True)
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            obj.select_set(False)
        for obj in objs:
            ''''''
            obj.select_set(True)
        return {'FINISHED'}
        
class selectParent(Operator):
    bl_idname = "object.select_parent_visn"
    bl_label = "Select Parent"
    bl_description = "Select Parent"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = context.selected_objects
        try:
            bpy.ops.object.mode_set()
        except:
            pass
        for obj in objs:
            obj.select_set(False)
        for obj in objs:
            if not obj.parent:
                continue
            obj.parent.select_set(True)
        return {'FINISHED'}    

class selectChildren(Operator):
    bl_idname = "object.select_children_visn"
    bl_label = "Select Children"
    bl_description = "Select All Children"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = context.selected_objects
        try:
            bpy.ops.object.mode_set()
        except:
            pass
        for obj in objs:
            '''取消本体选择'''
            obj.select_set(False)
        for obj in objs:
            '''获取子级选择'''
            for children in getChildren(obj):
                children.select_set(True)
        return {'FINISHED'}    

class PickupNewParent(Operator):
    '''把选定对象，捡出来放在世界层级，保留子级关系'''
    bl_idname = "object.pickup_new_parent_visn"
    bl_label = "Pickup to New Parent"
    bl_description = "pickup anywhere selected objects to new parent"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = context.selected_objects
        try:
            bpy.ops.object.mode_set()
        except:
            pass
        for obj in objs:
            '''清除选定对象的父级'''
            obj.select_set(True)
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            obj.select_set(False)
            
        loc = centro(objs)
        bpy.ops.object.add(type='EMPTY', location=loc)
        for o in objs:
            o.select_set(True)
            if not o.parent:
                bpy.ops.object.parent_no_inverse_set(keep_transform=True)
            o.select_set(False)
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
    bl_idname = "object.release_all_children_to_world_visn"
    bl_label = "Release to World"
    bl_description = "release all the children of selected objects to world"
    bl_options = {"REGISTER", "UNDO"}
    def execute(self, context):
        objs = context.selected_objects
        try:
            bpy.ops.object.mode_set()
        except:
            pass
        for obj in objs:
            obj.select_set(False)
        for obj in objs:
            for children in getChildren(obj):
                children.select_set(True)
                bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                children.select_set(False)
        return {'FINISHED'}
    
class RAQtoSubparent(Operator):    
    bl_idname = "object.release_all_children_to_subparent_visn"
    bl_label = "Release to Sub-parent"
    bl_description = "release all the children of selected objects to subparent"
    bl_options = {"REGISTER", "UNDO"}
    def execute(self, context):
        objs = context.selected_objects
        try:
            bpy.ops.object.mode_set()
        except:
            pass
        NOParent = False
        for obj in objs:
            obj.select_set(False)
        for obj in objs:
            if not obj.parent:
                NOParent = True
                for children in getChildren(obj):
                    children.select_set(True)
                    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                    children.select_set(False)
            else:
                for children in getChildren(obj):
                    children.select_set(True)
                    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                    bpy.context.view_layer.objects.active = obj.parent
                    bpy.ops.object.parent_no_inverse_set(keep_transform=True)
                    children.select_set(False)
        if not NOParent:
            '''如果是父子级之间对象，选择区域再返回更上层父级'''
            for obj in objs:
                bpy.context.view_layer.objects.active = obj.parent
                obj.parent.select_set(True)
        return {'FINISHED'}

class P2E(Operator):
    bl_idname = "object.parent_to_empty_visn"
    bl_label = "Parent to Empty"
    bl_description = "Parent selected objects to a new Empty"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = context.selected_objects
        try:
            bpy.ops.object.mode_set()
        except:
            pass
        
        loc = centro(objs)
        sameParent = True
        for o in objs:
            if not o.parent:
                sameParent = False
                break
            sameParent = o.parent == objs[0].parent
        if len(objs)==1:
            bpy.ops.object.add(type='EMPTY', location=loc,rotation=objs[0].rotation_euler)
        else: 
            bpy.ops.object.add(type='EMPTY', location=loc)   
        if sameParent:
            context.object.parent = objs[0].parent

        for o in objs:
            o.select_set(True)
            if not o.parent:
                bpy.ops.object.parent_no_inverse_set(keep_transform=True)
            if sameParent:
                bpy.ops.object.parent_no_inverse_set(keep_transform=True)
            o.select_set(False)
            
        return {'FINISHED'}
