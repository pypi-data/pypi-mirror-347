# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
#------------------------------------------------------------------------------
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
from matplotlib.transforms import blended_transform_factory
#------------------------------------------------------------------------------
import vtk
#------------------------------------------------------------------------------
from Graph_Element import VTK_Actor, Graph_Element_Style, Graph_Element
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** CONSTANT ***
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Element_Style_Constant(Graph_Element_Style) :
    
    #==========================================================================
    def _init_defaults(self) :
        #----------------------------------------------------------------------
        self.set('line.is_active', True)
        self.set('line.style', {'line_style':'-',
                                'line_width':1,
                                'line_color':'auto',
                                'line_alpha':1,
                                })
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Element_Constant(Graph_Element) :
        
    #==========================================================================
    def _create_plotted(self) :
        #----------------------------------------------------------------------
        segs = [[[0,self.element.value],[1,self.element.value]]]
        transform = blended_transform_factory(self.graph.ax.transAxes, self.graph.ax.transData)
        _plotted = self.graph.ax.add_collection(LineCollection(segs, transform=transform))
        self.plotted.configure(plotted=_plotted, ymin=self.element.value, ymax=self.element.value)
        
    #==========================================================================
    def _get_pointed_data(self, pointed_x, pointed_y) :
        #----------------------------------------------------------------------
        return {'y':self.element.value, 'text':"{}={:.8G}".format(self.label, self.element.value)}
        
    #==========================================================================
    def _update_style(self) :
        #----------------------------------------------------------------------
        gs = self.style
        
        #----------------------------------------------------------------------
        restyle = len([k for k in ['line.is_active','line.style'] if k in gs.changed]) > 0
        if not restyle : return
        
        #----------------------------------------------------------------------
        autocolor = self.graph.get_autocolor(self)
        
        #----------------------------------------------------------------------
        P = self.plotted.plotted
        P.set_visible(gs.get('line.is_active'))
        if gs.get('line.is_active') :
            S = gs.get('line.style')
            P.set_linestyle(S['line_style'])
            P.set_linewidth(S['line_width'])
            P.set_alpha(S['line_alpha'])
            P.set_color(S['line_color'] if S['line_color'] != 'auto' else autocolor)
        
        #----------------------------------------------------------------------
        self.graph.update_legend()
        
    #==========================================================================
    def _get_legend(self) :
        #----------------------------------------------------------------------
        return {'handle':self.plotted.plotted, 'label':self.style.get('legend.text')}
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** VECTOR ***
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Element_Style_Vector(Graph_Element_Style) :
    
    #==========================================================================
    def _init_defaults(self) :
        #----------------------------------------------------------------------
        self.set('line.is_active', True)
        self.set('line.style', {'line_style':'-',
                                'line_width':1,
                                'line_color':'gray',
                                'line_alpha':0.5,
                                })
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Element_Vector(Graph_Element) :
        
    #==========================================================================
    def _create_plotted(self) :
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
        
        #---- Graph_MPL_1D ----------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            segs = [[[value,0],[value,1]] for value in self.element.values]
            transform = blended_transform_factory(self.graph.ax.transData, self.graph.ax.transAxes)
            _plotted = self.graph.ax.add_collection(LineCollection(segs, transform=transform, color=self.element.get_style('line_color'), linewidth=self.element.get_style('line_width'), label=self.label))
            self.plotted.configure(plotted=_plotted, xmin=np.nanmin(self.element.values), xmax=np.nanmax(self.element.values))
        
        #---- Graph_MPL_2D/Vector ---------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            xdim = self.graph.graph_config.dimensions[0]
            ydim = self.graph.graph_config.dimensions[1]
            
            #------------------------------------------------------------------
            if self.element.dimension == xdim :
                ymin,ymax = self.element.get_lims(ydim)
                if None in (ymin,ymax) :
                    segs = [[[value,0],[value,1]] for value in self.element.values]
                    transform = blended_transform_factory(self.graph.ax.transData, self.graph.ax.transAxes)
                else :
                    segs = [[[value,ymin],[value,ymax]] for value in self.element.values]
                    transform = blended_transform_factory(self.graph.ax.transData, self.graph.ax.transData)
                    self.plotted.configure(ymin=ymin, ymax=ymax)
                self.plotted.configure(xmin=np.nanmin(self.element.values), xmax=np.nanmax(self.element.values))
                
            #------------------------------------------------------------------
            elif self.element.dimension == ydim :
                xmin,xmax = self.element.get_lims(xdim)
                if None in (xmin,xmax) :
                    segs = [[[0,value],[1,value]] for value in self.element.values]
                    transform = blended_transform_factory(self.graph.ax.transAxes, self.graph.ax.transData)
                else :
                    segs = [[[xmin,value],[xmax,value]] for value in self.element.values]
                    transform = blended_transform_factory(self.graph.ax.transData, self.graph.ax.transData)
                    self.plotted.configure(xmin=xmin, xmax=xmax)
                self.plotted.configure(ymin=np.nanmin(self.element.values), ymax=np.nanmax(self.element.values))
                
            #------------------------------------------------------------------
            _plotted = self.graph.ax.add_collection(LineCollection(segs, transform=transform, color=self.element.get_style('line_color'), linewidth=self.element.get_style('line_width'), label=self.label))
            self.plotted.configure(plotted=_plotted)
        
    #==========================================================================
    def _get_pointed_data(self, pointed_x, pointed_y) :
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
        
        #---- Graph_MPL_1D ----------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            X = self.element.values
            idx = self.element.coord_to_index(pointed_x, allow_out=True)
            if idx is None : return None
            return {'x':X[idx], 'text':"{}={:.8G}".format(self.label, X[idx])}
        
        #---- Graph_MPL_2D ----------------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            xdim = self.graph.graph_config.dimensions[0]
            ydim = self.graph.graph_config.dimensions[1]
            
            X = self.element.values
            if   self.element.dimension == xdim : coord,idx = 'x',np.argmin(np.abs(X-pointed_x))
            elif self.element.dimension == ydim : coord,idx = 'y',np.argmin(np.abs(X-pointed_y))
            return {coord:X[idx], 'text':"{}={:.8G}".format(self.label, X[idx])}
            
    #==========================================================================
    def _update_style(self) :
        #----------------------------------------------------------------------
        gs = self.style
        
        #----------------------------------------------------------------------
        restyle = len([k for k in ['line.is_active','line.style'] if k in gs.changed]) > 0
        if not restyle : return
        
        #----------------------------------------------------------------------
        autocolor = 'gray'
        
        #----------------------------------------------------------------------
        P = self.plotted.plotted
        P.set_visible(gs.get('line.is_active'))
        if gs.get('line.is_active') :
            S = gs.get('line.style')
            P.set_linestyle(S['line_style'])
            P.set_linewidth(S['line_width'])
            P.set_alpha(S['line_alpha'])
            P.set_color(S['line_color'] if S['line_color'] != 'auto' else autocolor)
        
        #----------------------------------------------------------------------
        self.graph.update_legend()
        
    #==========================================================================
    def _get_legend(self) :
        #----------------------------------------------------------------------
        gs = self.style
        if not gs.get('line.is_active') : return None
        
        #----------------------------------------------------------------------
        S = gs.get('line.style')
        
        opts = {}
        opts['color'] = S['line_color'] if S['line_color'] != 'auto' else 'gray'
        opts['ls'] = S['line_style']
        opts['lw'] = S['line_width']
        opts['alpha'] = S['line_alpha']
        
        handle = Line2D([],[], **opts)
        
        #----------------------------------------------------------------------
        return {'handle':handle, 'label':self.style.get('legend.text')}
                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** MESH ***
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Element_Style_Mesh(Graph_Element_Style) :
    
    #==========================================================================
    def _init_defaults(self) :
        #----------------------------------------------------------------------
        self.set('line.is_active', True)
        self.set('line.style', {'line_style':'-',
                                'line_width':1,
                                'line_color':'gray',
                                'line_alpha':0.5,
                                })
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Element_Mesh(Graph_Element) :
        
    #==========================================================================
    def _create_plotted(self) :
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
        
        
        #---- Graph_MPL_1D ----------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            segs = [[[edge,0],[edge,1]] for edge in self.element.edges]
            transform = blended_transform_factory(self.graph.ax.transData, self.graph.ax.transAxes)
            _plotted = self.graph.ax.add_collection(LineCollection(segs, transform=transform, color=self.element.get_style('line_color'), linewidth=self.element.get_style('line_width'), label=self.label))
            self.plotted.configure(plotted=_plotted, xmin=self.element.edges[0], xmax=self.element.edges[-1])
        
        
        #---- Graph_MPL_2D ----------------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            xdim = self.graph.graph_config.dimensions[0]
            ydim = self.graph.graph_config.dimensions[1]
            
            #------------------------------------------------------------------
            if self.element.dimension == xdim :
                ymin,ymax = self.element.get_lims(ydim)
                if None in (ymin,ymax) :
                    segs = [[[edge,0],[edge,1]] for edge in self.element.edges]
                    transform = blended_transform_factory(self.graph.ax.transData, self.graph.ax.transAxes)
                else :
                    segs = [[[edge,ymin],[edge,ymax]] for edge in self.element.edges]
                    transform = blended_transform_factory(self.graph.ax.transData, self.graph.ax.transData)
                    self.plotted.configure(ymin=ymin, ymax=ymax)
                self.plotted.configure(xmin=self.element.edges[0], xmax=self.element.edges[-1])
            #------------------------------------------------------------------
            elif self.element.dimension == ydim :
                xmin,xmax = self.element.get_lims(xdim)
                if None in (xmin,xmax) :
                    segs = [[[0,edge],[1,edge]] for edge in self.element.edges]
                    transform = blended_transform_factory(self.graph.ax.transAxes, self.graph.ax.transData)
                else :
                    segs = [[[xmin,edge],[xmax,edge]] for edge in self.element.edges]
                    transform = blended_transform_factory(self.graph.ax.transData, self.graph.ax.transData)
                    self.plotted.configure(xmin=xmin, xmax=xmax)
                self.plotted.configure(ymin=self.element.edges[0], ymax=self.element.edges[-1])
            #--------------------------------------------------------------
            _plotted = self.graph.ax.add_collection(LineCollection(segs, transform=transform, color=self.element.get_style('line_color'), linewidth=self.element.get_style('line_width'), label=self.label))
            self.plotted.configure(plotted=_plotted)
            
            
        #---- Graph_VTK -------------------------------------------------------
        elif gclass == 'Graph_VTK' :
            values = {}
            for dim in 'XYZ' :
                if self.element.dimension == dim : values[dim] = self.element.edges
                else : values[dim] = self.element.get_lims(dim)
            
            A = {}
            for dim in 'XYZ' :
                A[dim] = vtk.vtkDoubleArray()
                for v in values[dim] : A[dim].InsertNextValue(v)
            edge_grid = vtk.vtkRectilinearGrid()
            edge_grid.SetDimensions(A['X'].GetNumberOfTuples(), A['Y'].GetNumberOfTuples(), A['Z'].GetNumberOfTuples())
            edge_grid.SetXCoordinates(A['X'])
            edge_grid.SetYCoordinates(A['Y'])
            edge_grid.SetZCoordinates(A['Z'])
            edge_mapper = vtk.vtkDataSetMapper()
            edge_mapper.SetInputData(edge_grid)
            edge_actor = VTK_Actor(renderer=self.graph.renderer, mapper=edge_mapper, color='gray', alpha=0.5, line_width=0.5)
            edge_actor.GetProperty().SetRepresentationToWireframe()
            self.plotted.configure(edge_actor=edge_actor)
            
        # self._update_style()
        
    #==========================================================================
    def _get_pointed_data(self, pointed_x, pointed_y) :
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
        
        
        #---- Graph_MPL_1D ----------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            X = self.element.edges
            idx = self.element.coord_to_index(pointed_x)
            if idx is None : return None
            return {'x0':X[idx], 'x1':X[idx+1], 'text':"{}={:.8G};{:.8G}".format(self.label, X[idx],X[idx+1])}
        
        
        #---- Graph_MPL_2D ----------------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            xdim = self.graph.graph_config.dimensions[0]
            ydim = self.graph.graph_config.dimensions[1]
            
            X = self.element.edges
            if self.element.dimension == xdim :
                ymin,ymax = self.element.get_lims(ydim)
                if ymin is not None and pointed_y < ymin : return None
                if ymax is not None and pointed_y > ymax : return None
                idx = self.element.coord_to_index(pointed_x)
                if idx is None : return
                return {'x0':X[idx], 'x1':X[idx+1],'y':pointed_y, 'text':"{}={:.8G};{:.8G}".format(self.label, X[idx],X[idx+1])}
                
            elif self.element.dimension == ydim :
                xmin,xmax = self.element.get_lims(xdim)
                if xmin is not None and pointed_x < xmin : return None
                if xmax is not None and pointed_x > xmax : return None
                idx = self.element.coord_to_index(pointed_y)
                if idx is None : return
                return {'y0':X[idx], 'y1':X[idx+1],'x':pointed_x, 'text':"{}={:.8G};{:.8G}".format(self.label, X[idx],X[idx+1])}
            
    #==========================================================================
    def _update_style(self) :
        #----------------------------------------------------------------------
        gs = self.style
        
        #----------------------------------------------------------------------
        autocolor = 'gray'
        
        #----------------------------------------------------------------------
        if self.graph.engine == 'MPL' :
            P = self.plotted.plotted
            P.set_visible(gs.get('line.is_active'))
            if gs.get('line.is_active') :
                S = gs.get('line.style')
                P.set_linestyle(S['line_style'])
                P.set_linewidth(S['line_width'])
                P.set_alpha(S['line_alpha'])
                P.set_color(S['line_color'] if S['line_color'] != 'auto' else autocolor)
        
        #----------------------------------------------------------------------
        elif self.graph.engine == 'VTK' :
            self.plotted.edge_actor.SetVisibility(gs.get('line.is_active'))
            if gs.get('line.is_active') :
                self.plotted.edge_actor.set_props(**gs.get('line.style'))
            
        #----------------------------------------------------------------------
        self.graph.update_legend()
        
    #==========================================================================
    def _get_legend(self) :
        #----------------------------------------------------------------------
        gs = self.style
        if not gs.get('line.is_active') : return None
        
        #----------------------------------------------------------------------
        S = gs.get('line.style')
        
        opts = {}
        opts['color'] = S['line_color'] if S['line_color'] != 'auto' else 'gray'
        opts['ls'] = S['line_style']
        opts['lw'] = S['line_width']
        opts['alpha'] = S['line_alpha']
        
        handle = Line2D([],[], **opts)
        
        #----------------------------------------------------------------------
        return {'handle':handle, 'label':self.style.get('legend.text')}
                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


