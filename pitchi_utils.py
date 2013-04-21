# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

#
#  Author            : Tamir Lousky [ tlousky@gmail.com, tamir@pitchipoy.tv ]
#
#  Homepage(Wiki)    : http://bioblog3d.wordpress.com/
#  Studio (sponsor)  : Pitchipoy Animation Productions (www.pitchipoy.tv)
# 
#  Start of project              : 2013-04-04 by Tamir Lousky
#  Last modified                 : 2013-04-04
#
#  Acknowledgements 
#  ================
#   

bl_info = {    
    "name"       : "Pitchipoy Utilities",
    "author"     : "Tamir Lousky",
    "version"    : (0, 0, 1),
    "blender"    : (2, 66, 0),
    "category"   : "Object",
    "location"   : "3D View >> Tools",
    "wiki_url"   : "https://github.com/pitchipoy/pitchipoy_utilities/wiki",
    "tracker_url": "https://github.com/pitchipoy/pitchipoy_utilities/blob/master/pitchi_utils.py",
    "description": "Various utilities used for production"
}

import bpy
import re

class random_mat_panel(bpy.types.Panel):
    bl_idname      = "PitchiUtilsPanel"
    bl_label       = "Pitchipoy Utilities"
    bl_space_type  = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw( self, context) :
        layout = self.layout
        
        rename_props = context.scene.rename_props
        
        layout.operator( 'object.apply_modifiers' )
        layout.operator( 'object.delete_vgroups'  )

        box = layout.box()
        box.prop( rename_props, "base_name" )
        box.operator( 'object.batch_rename' )
        
class apply_all_modifiers( bpy.types.Operator ):
    """ Applies all the modifiers in the object's stack in order """
    bl_idname      = "object.apply_modifiers"
    bl_label       = "Apply all modifiers"
    bl_description = "Apply all the modifiers in the object's stack in order"
    bl_options     = {'REGISTER', 'UNDO' }

    @classmethod
    def poll( self, context ):
        modifiable_objects = [ 'MESH', 'CURVE', 'SURFACE', 'FONT', 'LATTICE' ]
        
        # If the object is of the correct type, enable this operator
        return context.object.type in modifiable_objects

    def execute( self, context):
        modifiable_objects = [ 'MESH', 'CURVE', 'SURFACE', 'FONT', 'LATTICE' ]
        
        selected_objects = [ obj.name for obj in context.selected_objects ]
        
        # Iterate over all selected objects
        for name in selected_objects:
            # Reference object
            obj = context.scene.objects[name]

            # If the current object is of the right type
            if obj.type in modifiable_objects:
                # Deselect all objects
                bpy.ops.object.select_all(action='TOGGLE')
                
                # Select and activate current object
                obj.select                   = True
                context.scene.objects.active = obj

                # Iterate over the object's modifiers and apply them one at a time
                for m in obj.modifiers:
                    bpy.ops.object.modifier_apply(modifier = m.name )
        
        return {'FINISHED'}

class delete_all_vertex_groups( bpy.types.Operator ):
    """ Deletes all the mesh object's vertex groups """
    bl_idname      = "object.delete_vgroups"
    bl_label       = "Delete all Vertex Groups"
    bl_description = "Delete all the mesh object's vertex groups"
    bl_options     = {'REGISTER', 'UNDO' }

    @classmethod
    def poll( self, context ):
        # If the object is of the correct type 
        if context.object.type == 'MESH':
            # and it has at least 1 vgroup 
            if context.object.vertex_groups:
                # then enable this operator
                return True
        return False

    def execute( self, context):
        bpy.ops.object.vertex_group_remove(all=True)
        
        return {'FINISHED'}

class batch_rename( bpy.types.Operator ):
    """ Renames all selected objects based on the specified base name """
    bl_idname      = "object.batch_rename"
    bl_label       = "Rename selected objects"
    bl_description = "Rename selected objects based on the specified base name"
    bl_options     = {'REGISTER', 'UNDO' }

    @classmethod
    def poll( self, context ):
        return True

    def execute( self, context):
        i = 0
        base = context.scene.rename_props.base_name
        for obj in context.selected_objects:
            if   i == 0:
                name = base
            elif i > 999:
                name = base + '_' + str(i)
            else:
                # Add zeros before the number
                div_by_1k  = str( float( i / 1000 ) )
                pattern    = r'\d\.(\d+)'
                match      = re.search( pattern, div_by_1k )
                num_suffix = match.groups(0)[0]

                name = base + '_' + num_suffix

            # Set the name of the object and the object's data (mesh)
            obj.name      = name
            obj.data.name = name
            
            i += 1
                
        return {'FINISHED'}

class rename_props( bpy.types.PropertyGroup ):
    base_name = bpy.props.StringProperty(name="base_name", default="object")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.rename_props = bpy.props.PointerProperty( 
        type = rename_props )
    
def unregister():
    bpy.utils.unregister_module(__name__)

# Registers the class and panel when you run the script from the text editor
# bpy.utils.register_module(__name__)
