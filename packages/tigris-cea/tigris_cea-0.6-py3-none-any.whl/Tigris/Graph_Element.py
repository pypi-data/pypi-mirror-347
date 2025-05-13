# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
#------------------------------------------------------------------------------
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QBrush
#------------------------------------------------------------------------------
import matplotlib.pyplot as plt
#------------------------------------------------------------------------------
import vtk
#------------------------------------------------------------------------------
from Style import Style
from utils_vtk import get_vtk_color
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def new_graph_element(graph, element, **opts) :
    eclass = type(element).__name__
    
    from Graph_Element_Constants import Graph_Element_Constant, Graph_Element_Vector, Graph_Element_Mesh
    from Graph_Element_Matrix    import Graph_Element_Matrix
    from Graph_Element_Cuboids   import Graph_Element_Cuboid, Graph_Element_PolyCuboid

    if   eclass == 'Constant'   : return Graph_Element_Constant(graph, element, **opts)
    elif eclass == 'Vector'     : return Graph_Element_Vector(graph, element, **opts)
    elif eclass == 'Mesh'       : return Graph_Element_Mesh(graph, element, **opts)
    elif eclass == 'Matrix'     : return Graph_Element_Matrix(graph, element, **opts)
    elif eclass == 'Cuboid'     : return Graph_Element_Cuboid(graph, element, **opts)
    elif eclass == 'PolyCuboid' : return Graph_Element_PolyCuboid(graph, element, **opts)
    else : raise Exception("Pas de classe de style pour les éléments {}".format(eclass))

#------------------------------------------------------------------------------
def new_graph_element_style(graph_element) :
    eclass = type(graph_element.element).__name__
    
    from Graph_Element_Constants import Graph_Element_Style_Constant, Graph_Element_Style_Vector, Graph_Element_Style_Mesh
    from Graph_Element_Matrix    import Graph_Element_Style_Matrix
    from Graph_Element_Cuboids   import Graph_Element_Style_Cuboid, Graph_Element_Style_PolyCuboid

    if   eclass == 'Constant'   : return Graph_Element_Style_Constant(graph_element)
    elif eclass == 'Vector'     : return Graph_Element_Style_Vector(graph_element)
    elif eclass == 'Mesh'       : return Graph_Element_Style_Mesh(graph_element)
    elif eclass == 'Matrix'     : return Graph_Element_Style_Matrix(graph_element)
    elif eclass == 'Cuboid'     : return Graph_Element_Style_Cuboid(graph_element)
    elif eclass == 'PolyCuboid' : return Graph_Element_Style_PolyCuboid(graph_element)
    else : raise Exception("Pas de classe de style pour les éléments {}".format(eclass))
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Plotted :
    
    #==========================================================================
    def __init__(self, graph_element) :
        #----------------------------------------------------------------------
        self.graph_element = graph_element
        self.graph = self.graph_element.graph
        
        #----------------------------------------------------------------------
        self.plotted = None
        
        #----------------------------------------------------------------------
        self.edge_actor   = None
        self.surf_actor   = None
        self.slice_actor  = None
        self.volu_actor   = None
        self.volu_grid    = None
        self.volu_scalars = None
        
        #----------------------------------------------------------------------
        self.xmin = None
        self.xmax = None
        self.ymin = None
        self.ymax = None
        
        #----------------------------------------------------------------------
        self.visible = True
        self.empty   = False
        self.Z       = None
        self.colors  = None
        self.mappable = None
        
    #==========================================================================
    def configure(self, **kwargs) :
        #----------------------------------------------------------------------
        for k,v in kwargs.items() :
            setattr(self, k, v)
    
    #==========================================================================
    def remove(self) :
        #----------------------------------------------------------------------
        if self.graph.engine == 'MPL' :
            self.plotted.remove()
            
        #----------------------------------------------------------------------
        elif self.graph.engine == 'VTK' :
            for actor in self.get_actors() :
                self.graph.remove_actor(actor)
                    
    #==========================================================================
    def get_actors(self) :
        #----------------------------------------------------------------------
        actors = []
        for obj_name in dir(self) :
            obj = getattr(self, obj_name)
            if isinstance(obj, vtk.vtkActor) :
                actors.append(obj)
                
        #----------------------------------------------------------------------
        return actors
        
    #==========================================================================
    def set_visible(self, state) :
        #----------------------------------------------------------------------
        self.visible = state
        
        #----------------------------------------------------------------------
        if self.graph.engine == 'MPL' :
            self.plotted.set_visible(state)
        
        #----------------------------------------------------------------------
        elif self.graph.engine == 'VTK' :
            for actor in self.get_actors() :
                actor.SetVisibility(state)
                    
    #==========================================================================
    def get_visible(self) :
        #----------------------------------------------------------------------
        return self.visible
        
    #==========================================================================
    def set_clim(self, cmin, cmax) :
        #----------------------------------------------------------------------
        if self.graph_element.cbar is None :
            return
        
        #----------------------------------------------------------------------
        self.graph_element.cbar.mappable.set_clim(cmin, cmax)
        
        #----------------------------------------------------------------------
        if self.graph.engine == 'VTK' :
            if self.volu_actor  is not None : self.volu_actor.mapper.SetScalarRange(cmin, cmax)
            if self.slice_actor is not None : self.slice_actor.mapper.SetScalarRange(cmin, cmax)

        #----------------------------------------------------------------------
        self.graph.legend.update_cbar(self.graph_element)
        
    #==========================================================================
    def set_cmap(self, cmap_name) :
        #----------------------------------------------------------------------
        element = self.graph_element.element
        
        #----------------------------------------------------------------------
        self.colors = vtk.vtkLookupTable()
        if element.linked_elements is not None and len(element.linked_elements) > 0 :
            N = max(sorted(list(element.linked_elements.keys())))
            self.colors.SetNumberOfTableValues(N)
            self.colors.Build()
            for i in range(N) :
                if i+1 in element.linked_elements.keys() : r,g,b = get_vtk_color(element.linked_elements[i+1].get_style('color'))
                else : r,g,b = 0,0,0
                self.colors.SetTableValue(i,r,g,b,1)
        else :
            N = 256
            self.colors.SetNumberOfTableValues(N)
            cmap = plt.get_cmap(cmap_name)
            _colors = cmap(np.linspace(0, 1, N))
            for i in range(N) : self.colors.SetTableValue(i, _colors[i][0], _colors[i][1], _colors[i][2], 1)
        
        #----------------------------------------------------------------------
        if self.volu_actor is not None : self.volu_actor.GetMapper().SetLookupTable(self.colors)
        if self.slice_actor is not None : self.slice_actor.GetMapper().SetLookupTable(self.colors)
        
        #----------------------------------------------------------------------
        if self.graph_element.cbar is not None :
            self.graph_element.cbar.mappable.set_cmap(cmap_name)
            self.graph.legend.update_cbar(self.graph_element)
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Pointed(QWidget) :
    
    #==========================================================================
    def __init__(self, graph_element) :
        #----------------------------------------------------------------------
        self.graph_element = graph_element
        self.graph = self.graph_element.graph
        
        #----------------------------------------------------------------------
        QWidget.__init__(self, parent=self.graph)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        #----------------------------------------------------------------------
        self.label = QLabel('', parent=self.graph)
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.font_height = 10
        self.label.setFont(QFont("Arial", self.font_height))
        # self.label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.label.setAlignment(Qt.AlignTop| Qt.AlignHCenter)
        
        #----------------------------------------------------------------------
        self.lw = 2
        self.ms = 4
        self.text = None
        self.set_visible(False)
        
    #==========================================================================
    def set_visible(self, state) :
        #----------------------------------------------------------------------
        self.setVisible(state)
        self.label.setVisible(state)
        
    #==========================================================================
    def get_visible(self) :
        #----------------------------------------------------------------------
        return self.isVisible()
    
    #==========================================================================
    def remove(self) :
        #----------------------------------------------------------------------
        self.set_visible(False)
        self.label.deleteLater()
        self.deleteLater()
        
    #==========================================================================
    def configure(self, text, x0, y0, x1, y1, pointeds) :
        #----------------------------------------------------------------------
        GH = self.graph.height()
        y0 = GH-y0
        y1 = GH-y1
        
        #----------------------------------------------------------------------
        if x0 > x1 : x0,x1 = x1,x0
        if y0 > y1 : y0,y1 = y1,y0
        
        #----------------------------------------------------------------------
        if   x0 == x1 and y0 == y1 : self.shape = 'point'
        elif y0 == y1 : self.shape = 'hline'
        elif x0 == x1 : self.shape = 'vline'
        else : self.shape = 'rect'
        
        #----------------------------------------------------------------------
        x = x0
        y = y0
        self.W = x1-x0+1
        self.H = y1-y0+1
        #----------------------------------------------------------------------
        if self.shape == 'hline' :
            y -= self.lw
            self.H += 2*self.lw
        #----------------------------------------------------------------------
        elif self.shape == 'vline' :
            x -= self.lw
            self.W += 2*self.lw
        #----------------------------------------------------------------------
        elif self.shape == 'point' :
            x -= self.ms
            self.W += 2*self.ms
            y -= self.ms
            self.H += 2*self.ms
        
        #----------------------------------------------------------------------
        self.text = text
        self.label.setText(text)
        self.label.resize(self.label.sizeHint())
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setOffset(0,0)
        shadow.setColor(Qt.white)
        self.label.setGraphicsEffect(shadow)
        
        lx = int(x + self.W/2 - self.label.sizeHint().width()/2)
        if self.shape == 'rect' : ly = int(y0 - self.font_height - 10)
        else : ly = int(y - self.font_height - 10)
        
        while True :
            self.label.move(lx, ly)
            found = False
            for pointed in pointeds :
                if pointed.label.geometry().intersects(self.label.geometry()) :
                    ly -= pointed.label.height()
                    found = True
                    break
            if not found : break
        
        #----------------------------------------------------------------------
        self.W = int(self.W)
        self.H = int(self.H)
        self.setGeometry(int(x), int(y), self.W, self.H)
        
    #==========================================================================
    def paintEvent(self, event) :
        #----------------------------------------------------------------------
        if self.text is None : return
        
        #----------------------------------------------------------------------
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        #----------------------------------------------------------------------
        color = QColor('black')
        if self.shape == 'rect' :
            painter.setPen(QPen(color, 1))
            painter.drawRect(0,0,self.W,self.H)
        
        elif self.shape == 'hline' :
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRect(0,0,self.W,2*self.lw)
        
        elif self.shape == 'vline' :
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRect(0,0, 2*self.lw, self.H)
            
        elif self.shape == 'point' :
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(0, 0, self.W, self.H)
        
        #----------------------------------------------------------------------
        painter.end()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class VTK_Actor(vtk.vtkActor) :
    
    #==========================================================================
    def __init__(self, renderer=None, mapper=None, color=None, alpha=None, line_width=None) :
        #----------------------------------------------------------------------
        vtk.vtkActor.__init__(self)
        
        #----------------------------------------------------------------------
        self.renderer = None
        self.set_renderer(renderer)
        
        #----------------------------------------------------------------------
        self.mapper = mapper
        if mapper is not None : self.SetMapper(mapper)
        
        #----------------------------------------------------------------------
        props = self.GetProperty()
        if color is not None      : props.SetColor(get_vtk_color(color))
        if alpha is not None      : props.SetOpacity(alpha)
        if line_width is not None : props.SetLineWidth(line_width)
    
    #==========================================================================
    def set_props(self, **kwargs) :
        #----------------------------------------------------------------------
        props = self.GetProperty()
        
        #----------------------------------------------------------------------
        for k,v in kwargs.items() :
            if k == 'line_color' : props.SetColor(get_vtk_color(v))
            if k == 'line_alpha' : props.SetOpacity(v)
            if k == 'line_width' : props.SetLineWidth(v)
        
            if k == 'fill_color' : props.SetColor(get_vtk_color(v))
            if k == 'fill_alpha' : props.SetOpacity(v)
            
    #==========================================================================
    def set_renderer(self, renderer) :
        #----------------------------------------------------------------------
        if renderer == self.renderer : return False
        
        #----------------------------------------------------------------------
        if self.renderer is not None : self.renderer.RemoveActor(self)
        self.renderer = renderer
        self.renderer.AddActor(self)
        
        #----------------------------------------------------------------------
        return True
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Element_Style(Style) :
    
    #==========================================================================
    INDEX = 1
    
    #==========================================================================
    def __init__(self, graph_element) :
        #----------------------------------------------------------------------
        self.index = Graph_Element_Style.INDEX
        Graph_Element_Style.INDEX += 1
        
        #----------------------------------------------------------------------
        self.graph_element = graph_element
        
        #----------------------------------------------------------------------
        Style.__init__(self)
        
    #==========================================================================
    def init_defaults(self) :
        #----------------------------------------------------------------------
        engine = self.graph_element.graph.engine
    
        #----------------------------------------------------------------------
        self.set('element.is_active'  , True)
        #----------------------------------------------------------------------
        self.set('sync.is_active', True)
        #----------------------------------------------------------------------
        self.set('legend.is_active'   , True)
        self.set('legend.text'        , self.graph_element.label)
        self.set('legend.default_text', self.graph_element.label)
        
        #----------------------------------------------------------------------
        if engine == 'MPL' :
            self.set('inspector.is_active', True)
            
        #----------------------------------------------------------------------
        self._init_defaults()
        
    #==========================================================================
    def _update(self, redraw=False) :
        #----------------------------------------------------------------------
        self.graph_element.update_style(redraw=redraw)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Element :
    
    #==========================================================================
    INDEX = 1
    
    #==========================================================================
    def __init__(self, graph, element, **opts) :
        #----------------------------------------------------------------------
        if 'index' in opts.keys() :
            self.index = opts.pop('index')
        else :
            self.index = Graph_Element.INDEX
            Graph_Element.INDEX += 1
        
        #----------------------------------------------------------------------
        self.graph = graph
        self.mw = self.graph.mw
        self.page = self.graph.page
        self.element = element
        
        if not hasattr(self, 'label') : self.label = self.element.label
        if not hasattr(self, 'icon')  : self.icon  = self.element.icon
            
        #----------------------------------------------------------------------
        self.style = new_graph_element_style(self)
        for k,v in self.element.style.items() :
            self.style.set(k,v)
        
        #----------------------------------------------------------------------
        if 'style' in opts.keys() :
            self.style.update_from(opts.pop('style'))
        
        #----------------------------------------------------------------------
        opts_keys = ['field']
        self.opts = {k:v for k,v in opts.items() if k in opts_keys}
        
        #----------------------------------------------------------------------
        self.plotted = None
        self.pointed = None
        self.cbar = None
        self.range = {'xmin':None, 'xmax':None, 'ymin':None, 'ymax':None}
        
        #----------------------------------------------------------------------
        self.reset()
    
    #==========================================================================
    def get_icon(self) :
        #----------------------------------------------------------------------
        return self.icon
        
    #==========================================================================
    def reset(self) :
        #----------------------------------------------------------------------
        if self.plotted is not None : self.plotted.remove()
        if self.pointed is not None : self.pointed.remove()
        if self.cbar    is not None : self.graph.legend.remove_cbar(self)        
        
        #----------------------------------------------------------------------
        self.plotted = None
        self.pointed = None
        self.cbar    = None
    
    #==========================================================================
    def is_linked(self) :
        #----------------------------------------------------------------------
        return None
        
    #==========================================================================
    def get_positions(self) :
        #----------------------------------------------------------------------
        ftree = self.mw.parameters_manager.ftrees[self.page.index]
        etree = self.mw.parameters_manager.etrees[self.page.index]
        
        #----------------------------------------------------------------------
        positions = {}
        
        for dim in self.element.get_dimensions() :
            e_pos = etree.positions.get((self.index,dim),0)
            f_pos = ftree.positions.get((self.element.file.index,dim),None)
            
            if self.style.get('sync.is_active') and f_pos is not None : positions[dim] = {'pos':f_pos, 'origin':'file'}
            else                                                      : positions[dim] = {'pos':e_pos, 'origin':'element'}
            
        #----------------------------------------------------------------------
        return positions
    
    #==========================================================================
    def get_beacon(self) :
        #----------------------------------------------------------------------
        return self.element.get_beacon(field=self.opts.get('field',None))
        
    #==========================================================================
    def create_plotted(self) :
        #----------------------------------------------------------------------
        self.plotted = Plotted(self)
        self.pointed = Pointed(self)
        
        #----------------------------------------------------------------------
        self._create_plotted()
        
    #==========================================================================
    def _create_plotted(self) :
        #----------------------------------------------------------------------
        pass
    
    #==========================================================================
    def update_plotted(self) :
        #----------------------------------------------------------------------
        if not self.graph.graph_config.can_plot(self.element) :
            return
            
        if not self.style.get('element.is_active') :
            return
        
        #----------------------------------------------------------------------
        if self.plotted is None :
            self.create_plotted()
        
        #----------------------------------------------------------------------
        self._update_plotted()
        self.graph.rescale(ignore_autoscale=False)
        
    #==========================================================================
    def _update_plotted(self) :
        #----------------------------------------------------------------------
        pass
    
    #==========================================================================
    def get_pointed_data(self, pointed_x, pointed_y) :
        #----------------------------------------------------------------------
        if None in (pointed_x, pointed_y) : return None
        if self.plotted is None : return None
        if not self.plotted.get_visible() : return None
        
        return self._get_pointed_data(pointed_x, pointed_y)
        
    #==========================================================================
    def update_pointed(self, event, pointeds=[]) :
        #----------------------------------------------------------------------
        if self.plotted is None : return None
        if self.pointed is None : return None
        
        #----------------------------------------------------------------------
        if event is None or event.inaxes != self.graph.ax :
            self.set_pointed_visible(False)
            return None
        
        #----------------------------------------------------------------------
        inspector_activated = True
        if   not self.mw.action_inspector.isChecked() : inspector_activated = False
        elif not self.style.get('inspector.is_active') : inspector_activated = False
        elif not self.style.get('element.is_active') : inspector_activated = False
        
        #----------------------------------------------------------------------
        if not inspector_activated :
            self.set_pointed_visible(False)
            return None
        
        #----------------------------------------------------------------------
        pos = self.get_pointed_data(event.xdata, event.ydata)
        if pos is None :
            self.set_pointed_visible(False)
            return None
        
        #----------------------------------------------------------------------
        x0,x1,y0,y1 = None,None,None,None
        #----------------------------------------------------------------------
        if   'x' in pos.keys() : x0 = x1 = pos['x']
        elif 'x0' in pos.keys() : x0,x1 = pos['x0'],pos['x1']
        else : x0 = x1 = event.xdata
        #----------------------------------------------------------------------
        if   'y' in pos.keys() : y0 = y1 = pos['y']
        elif 'y0' in pos.keys() : y0,y1 = pos['y0'],pos['y1']
        else : y0 = y1 = event.ydata
        
        #----------------------------------------------------------------------
        (X0,X1),(Y0,Y1) = self.graph.ax.get_xlim(),self.graph.ax.get_ylim()
        visible = x0 <= X1 and x1 >= X0 and y0 <= Y1 and y1 >= Y0
        if not visible :
            self.set_pointed_visible(False)
            return None
        
        #----------------------------------------------------------------------
        self.set_pointed_visible(True)
        
        #----------------------------------------------------------------------
        data_to_pixels = self.graph.ax.transData
        x0,x1,y0,y1 = max(X0,x0), min(X1,x1), max(Y0,y0), min(Y1,y1)
        px0,py0 = data_to_pixels.transform((x0,y0))
        px1,py1 = data_to_pixels.transform((x1,y1))
        self.pointed.configure(pos['text'], px0, py0, px1, py1, pointeds=pointeds)
        
        #----------------------------------------------------------------------
        return pos['text']
    
    #==========================================================================
    def set_pointed_visible(self, state) :
        #----------------------------------------------------------------------
        if self.pointed is None : return False
        
        #----------------------------------------------------------------------
        changed = state != self.pointed.get_visible()
        
        #----------------------------------------------------------------------
        self.pointed.set_visible(state)
        self.pointed.update()
        
        #----------------------------------------------------------------------
        return changed
        
    #==========================================================================
    def update_style(self, redraw=False) :
        #----------------------------------------------------------------------
        if self.plotted is None :
            return
        
        #----------------------------------------------------------------------
        gs = self.style
        
        #----------------------------------------------------------------------
        if 'element.is_active' in gs.changed :
            self.plotted.set_visible(gs.get('element.is_active'))
            
        #----------------------------------------------------------------------
        self._update_style()
        
        self.graph.update_legend()
        
        #----------------------------------------------------------------------
        if redraw :
            self.graph.redraw()
        
    #==========================================================================
    def _update_style(self) :
        pass
        
    #==========================================================================
    def get_legend(self) :
        #----------------------------------------------------------------------
        gs = self.style
        
        #----------------------------------------------------------------------
        if not gs.get('element.is_active') : return None
        if not gs.get('legend.is_active') : return None
        if self.plotted is None : return None
        if self.cbar is not None : return None
        
        #----------------------------------------------------------------------
        return self._get_legend()

    #==========================================================================
    def _get_legend(self) :
        return None
        
    #==========================================================================
    def get_linked_legend(self) :
        #----------------------------------------------------------------------
        gs = self.style
        gclass = type(self.graph).__name__
        
        #----------------------------------------------------------------------
        if not gs.get('element.is_active') : return None
        if not gs.get('legend.is_active') : return None
        if self.plotted is None : return None
        if gclass not in ['Graph_MPL_2D','Graph_VTK'] : return None
        if not hasattr(self.element, 'linked_elements') : return None
        if self.element.linked_elements is None : return
        
        #----------------------------------------------------------------------
        return self._get_linked_legend()
    
    #==========================================================================
    def _get_linked_legend(self) :
        return None
        
    #==========================================================================
    def get_save_data(self) :
        #----------------------------------------------------------------------
        return None
                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


