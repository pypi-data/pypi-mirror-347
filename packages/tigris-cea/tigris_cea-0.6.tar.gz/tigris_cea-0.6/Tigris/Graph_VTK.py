# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import datetime
#------------------------------------------------------------------------------
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------
from PyQt5.QtWidgets import QMenu
#------------------------------------------------------------------------------
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkRenderingCore import vtkCamera
#------------------------------------------------------------------------------
from Style import Style
from Graph import Graph
from Graph_Style import Graph_Style,Graph_VTK_Style
from utils_vtk import get_vtk_color
from utils_qt import get_icon
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** GRAPH FUNCTIONS ***
#==============================================================================
def new_graph(page, graph_config, **kwargs) :
    #--------------------------------------------------------------------------
    if graph_config.gtype == '3D' : return Graph_VTK(page, graph_config, **kwargs)
    
    #--------------------------------------------------------------------------
    return Graph(page, graph_config, **kwargs)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class VTK_Axes :
    
    #==========================================================================
    def __init__(self, graph) :
        #----------------------------------------------------------------------
        self.graph = graph
        self.renderer = self.graph.renderer
        
        #----------------------------------------------------------------------
        self.create_actors()
        self.set_bounds(0,1,0,1,0,1)
        
    #==========================================================================
    def create_actors(self) :
        #----------------------------------------------------------------------
        self.lines = []
        self.titles = []
        self.L_labels = []
        self.R_labels = []
        
        #----------------------------------------------------------------------
        for a,axis in enumerate(['xaxis','yaxis','zaxis']) :
            self.lines.append(vtk.vtkActor())
            self.titles.append(vtk.vtkTextActor())
            self.L_labels.append(vtk.vtkTextActor())
            self.R_labels.append(vtk.vtkTextActor())
        
        #----------------------------------------------------------------------
        self.actors = self.lines + self.titles + self.L_labels + self.R_labels
        for actor in self.actors : self.renderer.AddActor(actor)
    
    #==========================================================================
    def update_bound(self) :
        #----------------------------------------------------------------------
        all_actors = [a for a in self.renderer.GetActors() if a not in self.actors]
        
        #----------------------------------------------------------------------
        if len(all_actors) > 0 :
            xmin = min([0] + [actor.GetBounds()[0] for actor in all_actors])
            ymin = min([0] + [actor.GetBounds()[2] for actor in all_actors])
            zmin = min([0] + [actor.GetBounds()[4] for actor in all_actors])
            
            xmax = max([actor.GetBounds()[1] for actor in all_actors])
            ymax = max([actor.GetBounds()[3] for actor in all_actors])
            zmax = max([actor.GetBounds()[5] for actor in all_actors])
            
        #----------------------------------------------------------------------
        else :
            xmin,xmax,ymin,ymax,zmin,zmax = 0, 1, 0, 1, 0, 1
        
        #----------------------------------------------------------------------
        self.set_bounds(xmin,xmax,ymin,ymax,zmin,zmax)
        
    #==========================================================================
    def set_bounds(self, x0,x1,y0,y1,z0,z1) :
        #----------------------------------------------------------------------
        # print("set_bounds", x0,x1,y0,y1,z0,z1)
        self.coordinates = (x0,x1,y0,y1,z0,z1)
        
        #----------------------------------------------------------------------
        O,X,Y,Z = (x0,y0,z0),(x1,y0,z0),(x0,y1,z0),(x0,y0,z1)
        points = vtk.vtkPoints()
        for P in [O,X,Y,Z] : points.InsertNextPoint(P)
        
        #----------------------------------------------------------------------
        for a,axis in enumerate(['xaxis','yaxis','zaxis']) :
            lines = vtk.vtkCellArray()
            lines.InsertNextCell(2, [0,1+a])
            polydata = vtk.vtkPolyData()
            polydata.SetPoints(points)
            polydata.SetLines(lines)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(polydata)
            self.lines[a].SetMapper(mapper)
            
        #----------------------------------------------------------------------
        for actor in self.lines + self.titles + self.L_labels + self.R_labels :
            self.renderer.AddActor(actor)
        
        #----------------------------------------------------------------------
        self.on_view_changed()
        
    #==========================================================================
    def on_view_changed(self, caller=None, event=None) :
        #----------------------------------------------------------------------
        x0,x1,y0,y1,z0,z1 = self.coordinates
        
        #----------------------------------------------------------------------
        def convert(x,y,z) :
            P = vtk.vtkCoordinate()
            P.SetCoordinateSystemToWorld()
            P.SetValue((x,y,z))
            return P.GetComputedDisplayValue(self.renderer)
        
        #----------------------------------------------------------------------
        offset = 0.03
        dx,dy,dz = (x1-x0)*offset,(y1-y0)*offset,(z1-z0)*offset
        xc,yc,zc = (x0+x1)/2, (y0+y1)/2, (z0+z1)/2
        
        #----------------------------------------------------------------------
        self.titles[0].SetPosition(convert(xc,y0-dy,z0-dz))
        self.titles[1].SetPosition(convert(x0-dx,yc,z0-dz))
        self.titles[2].SetPosition(convert(x0-dx,y0-dy,zc))
        
        #----------------------------------------------------------------------
        self.L_labels[0].SetPosition(convert(x0+dx,y0-dy,z0-dz))
        self.R_labels[0].SetPosition(convert(x1-dx,y0-dy,z0-dz))
        self.L_labels[1].SetPosition(convert(x0-dx,y0+dy,z0-dz))
        self.R_labels[1].SetPosition(convert(x0-dx,y1-dy,z0-dz))
        self.L_labels[2].SetPosition(convert(x0-dx,y0-dy,z0+dz))
        self.R_labels[2].SetPosition(convert(x0-dx,y0-dy,z1-dz))
    
        #----------------------------------------------------------------------
        self.on_style_changed()
        
    #==========================================================================
    def on_style_changed(self) :
        #----------------------------------------------------------------------
        x0,x1,y0,y1,z0,z1 = self.coordinates
        gs = self.graph.style
        
        #----------------------------------------------------------------------
        for a,axis in enumerate(['xaxis','yaxis','zaxis']) :
            
            #------------------------------------------------------------------
            if gs.get('axes.is_active') and gs.get(axis+'.is_active') and gs.get(axis+'.title.is_active') :
                self.titles[a].VisibilityOn()
                self.titles[a].SetInput(gs.get(axis+'.title.text'))
                
                S = gs.get(axis+'.title.style').copy()
                props = self.titles[a].GetTextProperty()
                props.SetJustificationToCentered()
                props.SetVerticalJustificationToCentered()
                props.SetColor(get_vtk_color(S['font_color']))
                props.SetFontFamilyAsString(S['font_name'])
                props.SetFontSize(int(S['font_size']*Style.FONT_SIZE_FACTOR))
                props.SetBold(S['font_bold'])
                props.SetItalic(S['font_italic'])
            else :
                self.titles[a].VisibilityOff()
            
            #------------------------------------------------------------------
            if gs.get('axes.is_active') and gs.get(axis+'.is_active') and gs.get(axis+'.ticks.is_active') :
                self.L_labels[a].VisibilityOn()
                self.R_labels[a].VisibilityOn()
                if   axis == 'xaxis' :  v0,v1 = x0,x1
                elif axis == 'yaxis' :  v0,v1 = y0,y1
                elif axis == 'zaxis' :  v0,v1 = z0,z1
                fmt = "{"+":."+ str(gs.get(axis+'.ticks.decimals')) + ['G','f','E'][Graph_Style.get_options('ticks.format').index(gs.get(axis+'.ticks.format'))] + "}"
                self.L_labels[a].SetInput(fmt.format(v0))
                self.R_labels[a].SetInput(fmt.format(v1))
                S = gs.get(axis+'.ticks.style').copy()
                for actor in [self.L_labels[a],self.R_labels[a]] :
                    props = actor.GetTextProperty()
                    props.SetJustificationToCentered()
                    props.SetVerticalJustificationToCentered()
                    props.SetColor(get_vtk_color(S['font_color']))
                    props.SetFontFamilyAsString(S['font_name'])
                    props.SetFontSize(int(S['font_size']*Style.FONT_SIZE_FACTOR))
                    props.SetBold(S['font_bold'])
                    props.SetItalic(S['font_italic'])
            else :
                self.L_labels[a].VisibilityOff()
                self.R_labels[a].VisibilityOff()
                
            #------------------------------------------------------------------
            if gs.get('axes.is_active') and gs.get(axis+'.is_active') and gs.get(axis+'.line.is_active') :
                self.lines[a].VisibilityOn()
                S = gs.get(axis+'.line.style').copy()
                props = self.lines[a].GetProperty()
                props.SetColor(get_vtk_color(S['line_color']))
                props.SetLineWidth(S['line_width'])
                props.SetOpacity(S['line_alpha'])
            else :
                self.lines[a].VisibilityOff()
                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_VTK(Graph) :
    
    #==========================================================================
    def __init__(self, page, graph_config, **kwargs) :
        #----------------------------------------------------------------------
        Graph.__init__(self, page, graph_config, **kwargs)
        
        #----------------------------------------------------------------------
        self.engine = 'VTK'
        
    #==========================================================================
    def __repr__(self) :
        #----------------------------------------------------------------------
        return "Graph_3D(id={})".format(self.index)
    
    #==========================================================================
    def _open_menu(self, menu) :
        #----------------------------------------------------------------------
        menu_orient = QMenu("Orienter", self.mw)
        menu_orient.setIcon(get_icon("orient"))
        
        #----------------------------------------------------------------------
        str_side = {'top':'Dessus','bottom':'Dessous','left':'Gauche','right':'Droite','front':'Devant','back':'Derrière'}
        for side in ['top','bottom','left','right','front','back'] :
            menu_orient.addAction(get_icon('side_'+side), str_side[side]).triggered.connect(lambda e,side=side : self.set_view(side))
            
        #----------------------------------------------------------------------
        menu.addMenu(menu_orient)
        menu.addSeparator()
            
    #==========================================================================
    def _create_graph(self) :
        #----------------------------------------------------------------------
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.vtk_widget.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        
        #----------------------------------------------------------------------
        self.render_window = self.vtk_widget.GetRenderWindow()
        self.renderer = vtk.vtkRenderer()
        self.render_window.AddRenderer(self.renderer)
        #----------------------------------------------------------------------
        self.camera = vtkCamera()
        self.renderer.SetActiveCamera(self.camera)
        self.renderer.SetBackground(0.1, 0.2, 0.4)
        #----------------------------------------------------------------------
        self.renderer2 = vtk.vtkRenderer()
        self.renderer2.SetActiveCamera(self.camera)
        self.renderer2.SetLayer(1)
        self.renderer2.SetInteractive(0)
        self.renderer2.SetBackground(0, 0, 0)
        self.render_window.AddRenderer(self.renderer2)
        self.render_window.SetNumberOfLayers(2)
        
        #----------------------------------------------------------------------
        self.style = Graph_VTK_Style(self)
        
        #----------------------------------------------------------------------
        self.axes = VTK_Axes(self)
        self.camera.AddObserver("ModifiedEvent", self.on_view_changed)
        
        #----------------------------------------------------------------------
        self.title_actor = vtk.vtkTextActor()
        self.renderer.AddActor(self.title_actor)
        
        #----------------------------------------------------------------------
        self.lc_event = None
        self.lc_time_tag = None
        self.mc_event = None
        self.rc_event = None
        
        #----------------------------------------------------------------------
        self.vtk_widget.AddObserver("LeftButtonPressEvent", lambda o,e,button=1 : self.on_mouse_press(e,button))
        self.vtk_widget.AddObserver("RightButtonPressEvent", lambda o,e,button=2 : self.on_mouse_press(e,button))
        self.vtk_widget.AddObserver("MiddleButtonPressEvent", lambda o,e,button=3 : self.on_mouse_press(e,button))
        self.vtk_widget.AddObserver("EndInteractionEvent", lambda o,e:self.on_mouse_release())
        self.vtk_widget.AddObserver("KeyPressEvent", lambda o,e:self.on_key_press())
        
        #----------------------------------------------------------------------
        self.vtk_widget.Initialize()
        return self.vtk_widget
    
    #==========================================================================
    def on_key_press(self) :
        #----------------------------------------------------------------------
        key = self.vtk_widget.GetKeySym()      
        
        #----------------------------------------------------------------------
        if key == 'Escape' :
            self.mw.close()
    
    #==========================================================================
    def on_mouse_press(self, event=None, button=None) :
        #----------------------------------------------------------------------
        if button == 1 :
            last = self.lc_time_tag
            self.lc_time_tag = datetime.datetime.now()
            
            if last is not None :
                dd = (self.lc_time_tag-last).total_seconds()
                if dd < 0.2 :
                    self.on_mouse_dblclick(event, 1)
                    return
            
        #----------------------------------------------------------------------
        self.lc_event = None
        self.mc_event = None
        self.rc_event = None
        
        #----------------------------------------------------------------------
        if   button == 1 : self.lc_event = event
        elif button == 2 : self.rc_event = event
        elif button == 3 : self.mc_event = event

    #==========================================================================
    def on_mouse_dblclick(self, event=None, button=None) :
        #----------------------------------------------------------------------
        self.lc_time_tag = None
        if button == 1 : self.rescale()
        
    #==========================================================================
    def on_mouse_release(self) :
        #----------------------------------------------------------------------
        if self.rc_event is not None :
            self.open_menu()
    
    #==========================================================================
    def resizeEvent(self, event=None) :
        #----------------------------------------------------------------------
        self.update_title_position()
        self.on_view_changed(redraw=True)
        
    #==========================================================================
    def set_view(self, side) :
        #----------------------------------------------------------------------
        if side not in ['top','bottom','left','right','front','back'] :
            return
        
        #----------------------------------------------------------------------
        f = self.camera.GetFocalPoint()
        D = self.camera.GetDistance()
        
        #----------------------------------------------------------------------
        self.camera.SetRoll(0)
        
        #----------------------------------------------------------------------
        if   side == 'top'    : self.camera.SetViewUp(0,1,0)
        elif side == 'bottom' : self.camera.SetViewUp(0,-1,0)
        else                  : self.camera.SetViewUp(0,0,1)
        
        #----------------------------------------------------------------------
        if   side == 'top'    : self.camera.SetPosition(f[0]  , f[1]  , f[2]+D)
        elif side == 'bottom' : self.camera.SetPosition(f[0]  , f[1]  , f[2]-D)
        elif side == 'front'  : self.camera.SetPosition(f[0]  , f[1]-D, f[2]  )
        elif side == 'back'   : self.camera.SetPosition(f[0]  , f[1]+D, f[2]  )
        elif side == 'right'  : self.camera.SetPosition(f[0]+D, f[1]  , f[2]  )
        elif side == 'left'   : self.camera.SetPosition(f[0]-D, f[1]  , f[2]  )
        
        #----------------------------------------------------------------------
        self.camera.SetParallelProjection(True)
        
        #----------------------------------------------------------------------
        self.rescale()
    
    #==========================================================================
    def on_view_changed(self, call=None, event=None, redraw=False) :
        #----------------------------------------------------------------------
        self.camera.SetParallelProjection(len([v for v in self.camera.GetViewUp() if v == 0.0]) == 2)
        self.axes.on_view_changed()
        
        #----------------------------------------------------------------------
        if len(self.graph_elements) > 0 :
            self.autoscale = False
        
        #----------------------------------------------------------------------
        if redraw :
            self.redraw()
        
    #==========================================================================
    def remove_actor(self, actor) :
        #----------------------------------------------------------------------
        for renderer in self.render_window.GetRenderers() :
            renderer.RemoveActor(actor)
        
    #==========================================================================
    def update_title_position(self) :
        #----------------------------------------------------------------------
        width, height = self.render_window.GetSize()
        self.title_actor.SetPosition(width/2, height-5)
        
    #==========================================================================
    def _update_graph(self) :
        #----------------------------------------------------------------------
        self.axes.on_view_changed()
    
    #==========================================================================
    def _update_style(self) :
        #----------------------------------------------------------------------
        gs = self.style
        
        #---- title -----------------------------------------------------------
        if gs.get('title.is_active') :
            self.title_actor.VisibilityOn()
            self.title_actor.SetInput(gs.get('title.text'))
            S = gs.get('title.style')
            props = self.title_actor.GetTextProperty()
            props.SetColor(get_vtk_color(S['font_color']))
            props.SetJustificationToCentered()
            props.SetVerticalJustificationToTop()
            props.SetFontFamilyAsString(S['font_name'])
            props.SetBold(S['font_bold'])
            props.SetItalic(S['font_italic'])
            props.SetFontSize(int(S['font_size']*Style.FONT_SIZE_FACTOR))
        else :
            self.title_actor.VisibilityOff()
            
        #---- axis ------------------------------------------------------------
        self.axes.on_view_changed()
        
    #==========================================================================
    def rescale(self, ignore_autoscale=True, redraw=False) :
        #----------------------------------------------------------------------
        self.update_title_position()
        self.axes.update_bound()
        
        #----------------------------------------------------------------------
        if not self.autoscale and not ignore_autoscale : return
        
        #----------------------------------------------------------------------
        self.renderer.ResetCamera()
        self.autoscale = True
        
        #----------------------------------------------------------------------
        if redraw :
            self.redraw()
        
    #==========================================================================
    def redraw(self) :
        #----------------------------------------------------------------------
        self.render_window.Render()
        
    #==========================================================================
    def _save_image(self, filepath) :
        #----------------------------------------------------------------------
        windowToImageFilter = vtk.vtkWindowToImageFilter()
        windowToImageFilter.SetInput(self.render_window)
        windowToImageFilter.Update()
        
        #----------------------------------------------------------------------
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(filepath)
        writer.SetInputConnection(windowToImageFilter.GetOutputPort())
        writer.Write()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
