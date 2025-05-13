# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import vtk
from vtkmodules.vtkCommonColor import vtkNamedColors
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_vtk_color(color, default=(1.0,1.0,1.0)) :
    #--------------------------------------------------------------------------
    if type(color) == str :
        if color.startswith('#') :
            if len(color) != 7 : return default
            try : return tuple(float(int(color[i+1:i+3], 16)/255) for i in (0, 2, 4))
            except : return default
        
        else :
            rgb = tuple(vtkNamedColors().GetColor3d(color))
            if rgb == (0.0,0.0,0.0) and color not in ['black'] : return default
            return rgb
    
    #--------------------------------------------------------------------------
    return color

#==============================================================================
def world_to_screen(renderer, x,y,z) :
    P = vtk.vtkCoordinate()
    P.SetCoordinateSystemToWorld()
    P.SetValue((x,y,z))
    return P.GetComputedDisplayValue(renderer)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
