# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
#------------------------------------------------------------------------------
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------
import matplotlib as mpl
from matplotlib.patches import Patch
from matplotlib.collections import LineCollection
from matplotlib.transforms import blended_transform_factory
#------------------------------------------------------------------------------
import vtk
#------------------------------------------------------------------------------
from Graph_Element import VTK_Actor, Graph_Element_Style, Graph_Element
from Element_Matrix import Matrix
from utils import to_float
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Element_Style_Matrix(Graph_Element_Style) :
    
    #==========================================================================
    def _init_defaults(self) :
        #----------------------------------------------------------------------
        engine = self.graph_element.graph.engine
        gclass = type(self.graph_element.graph).__name__
        element = self.graph_element.element
        
        #----------------------------------------------------------------------
        if element.linked_elements is None :
            self.set('range.min.is_active', False)
            self.set('range.max.is_active', False)
            self.set('range.min.text', '')
            self.set('range.max.text', '')
            self.set('range.min.hide', True)
            self.set('range.max.hide', True)
            
            self.add_change('range.min.is_active')
        
        #----------------------------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            self.set('line.is_active', True)
            self.set('line.style', {'line_style':'-',
                                    'line_width':2,
                                    'line_color':'auto',
                                    'line_alpha':1,
                                    })
            
            self.set('mark.is_active', False)
            self.set('mark.style', {'mark_shape':'o',
                                    'mark_size':5,
                                    'mark_edge_width':1,
                                    'mark_edge_color':'auto',
                                    'mark_face_color':'auto',
                                    'mark_alpha':1,
                                    })
        
        #----------------------------------------------------------------------
        if gclass in ['Graph_MPL_2D','Graph_VTK'] :
            self.set('fill.is_active', True)
            self.set('fill.style', {'fill_palette':'gist_rainbow',
                                    'fill_alpha':0.5,
                                    })
        
        #----------------------------------------------------------------------
        if engine == 'VTK' :
            self.set('border.is_active', True)
            self.set('border.style', {'line_style':'-',
                                      'line_width':1,
                                      'line_color':'white',
                                      'line_alpha':1
                                      })
            
        #----------------------------------------------------------------------
        if engine == 'VTK' :
            self.set('slice.is_active', False)
            self.set('slice.plan', 'XY')
            self.set('slice.position', 0)
            
            self.set('highlight.is_active', False)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Element_Matrix(Graph_Element) :
    
    #==========================================================================
    def __init__(self, graph, element, **opts) :
        #----------------------------------------------------------------------
        if isinstance(element, Matrix) and 'field' in opts.keys() :
            # self.label = element.label + "_" + opts['field']
            self.label = opts['field']
            self.icon  = element.get_field_icon(opts['field'])
        
        #----------------------------------------------------------------------
        Graph_Element.__init__(self, graph, element, **opts)
        
    #==========================================================================
    def get_icon(self) :
        #----------------------------------------------------------------------
        if self.style.get('slice.is_active') == True : return 'slice'
        return self.icon
        
    #==========================================================================
    def is_linked(self) :
        #----------------------------------------------------------------------
        return self.element.linked_elements is not None
        
    #==========================================================================
    def add_slice(self, plan) :
        #----------------------------------------------------------------------
        ge = Graph_Element_Matrix(self.graph, self.element, **self.opts)
        ge.style.update_from(self.style)
        
        #----------------------------------------------------------------------
        ge.label = self.label + " ({})".format(plan)
        self.graph.graph_elements.append(ge)
        
        #----------------------------------------------------------------------
        dim = {'XY':'Z', 'XZ':'Y', 'YZ':'X'}[plan]
        N = self.element.get_dim_size(dim)
        ge.style.set('slice.is_active', True, redraw=False)
        ge.style.set('slice.plan', plan, redraw=False)
        ge.style.set('slice.position', int(N/2), redraw=False)
        ge.style.add_change('slice.is_active')
        
        #----------------------------------------------------------------------
        self.style.set('element.is_active', False, redraw=False) # déactivation du graph_element de base
        
        #----------------------------------------------------------------------
        self.graph.plot(ge)
        self.graph.update_graph()
        
    #==========================================================================
    def _create_plotted(self) :
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
        
        #----------------------------------------------------------------------
        self.element.load_data()
        
        #----------------------------------------------------------------------
        if gclass in ['Graph_MPL_2D','Graph_VTK'] :
            if self.element.linked_elements is not None :
                colors = [link.get_style('color') for i,link in sorted(self.element.linked_elements.items(), key=lambda e:e[0])]
                cmap = mpl.colors.ListedColormap(colors)
                norm = mpl.colors.BoundaryNorm(boundaries=np.arange(self.element.vmin, self.element.vmax+2), ncolors=len(colors))
            else :
                cmap = 'gist_rainbow'
                norm =  mpl.colors.Normalize(vmin=self.element.vmin, vmax=self.element.vmax)

        
        #---- Graph_MPL_1D ----------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            xdim = self.graph.graph_config.dimensions[0]
            if xdim in self.element.axes.keys() :
                _plotted = self.graph.ax.plot([], [], label=self.label)[0]
            else :
                transform = blended_transform_factory(self.graph.ax.transAxes, self.graph.ax.transData)
                _plotted = self.graph.ax.add_collection(LineCollection([], transform=transform, label=self.label))
            
            xmin,xmax = self.element.get_lims(xdim)
            self.plotted.configure(plotted=_plotted, xmin=xmin, xmax=xmax)
            
        #---- Graph_MPL_2D ----------------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            xdim = self.graph.graph_config.dimensions[0]
            ydim = self.graph.graph_config.dimensions[1]
            
            x = self.element.axes[xdim]
            y = self.element.axes[ydim]
            dup_x = self.element.is_dim_edge(xdim) and not self.element.is_dim_nodes(xdim)
            dup_y = self.element.is_dim_edge(ydim) and not self.element.is_dim_nodes(ydim)
            
            if dup_x and dup_y :
                X,Y = np.meshgrid(x,y)
                Z = np.full((len(x)-1, len(y)-1), np.nan).T
                _plotted = self.graph.ax.imshow(X, Y, Z, zorder=1, cmap=cmap, norm=norm, shading='flat', label=self.label)

            else :
                _x,_y = x,y
                if   dup_x : _x = np.vstack((x,x)).T.ravel()[1:-1]
                elif dup_y : _y = np.vstack((y,y)).T.ravel()[1:-1]
                X,Y = np.meshgrid(_x,_y)
                Z = np.full((len(_x), len(_y)), np.nan).T
                _plotted = self.graph.ax.pcolormesh(X, Y, Z, zorder=1, edgecolors='none', cmap=cmap, norm=norm, shading='gouraud', label=self.label)
                
            xmin,xmax = self.element.get_lims(xdim)
            ymin,ymax = self.element.get_lims(ydim)
            self.plotted.configure(Z=Z, plotted=_plotted, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
            
            if self.element.linked_elements is None :
                self.cbar = self.graph.legend.add_cbar(self)
        
        #---- Graph_VTK -------------------------------------------------------
        elif gclass == 'Graph_VTK' :
            
            arrays = {}
            for dim in 'XYZ' :
                arrays[dim] = vtk.vtkDoubleArray()
                for v in self.element.axes[dim] :
                    arrays[dim].InsertNextValue(v)
            grid = vtk.vtkRectilinearGrid()
            grid.SetDimensions(arrays['X'].GetNumberOfTuples(), arrays['Y'].GetNumberOfTuples(), arrays['Z'].GetNumberOfTuples())
            grid.SetXCoordinates(arrays['X'])
            grid.SetYCoordinates(arrays['Y'])
            grid.SetZCoordinates(arrays['Z'])
            
            indices = self.element.get_indices(self.get_positions(), graph_dimensions=self.graph.graph_config.dimensions, field=self.opts.get('field'))
            Z = self.element.get_matrix_data(indices).T
            
            scalars = vtk.vtkFloatArray()
            for value in Z.ravel() : scalars.InsertNextValue(value)
            xnode,ynode,znode = self.element.is_dim_nodes('X'), self.element.is_dim_nodes('Y'), self.element.is_dim_nodes('Z')
            if True not in [xnode,ynode,znode] :
                grid.GetCellData().SetScalars(scalars)
            else :
                if not xnode : Z = np.repeat(Z, 2, axis=0)
                if not ynode : Z = np.repeat(Z, 2, axis=1)
                if not znode : Z = np.repeat(Z, 2, axis=2)
                grid.GetPointData().SetScalars(scalars)
                
            volu_mapper = vtk.vtkDataSetMapper()
            volu_mapper.SetInputData(grid)
            volu_mapper.SetScalarRange(scalars.GetRange())
            volu_actor = VTK_Actor(renderer=self.graph.renderer, mapper=volu_mapper)
            
            #------------------------------------------------------------------
            edge_points = vtk.vtkPoints()
            edge_lines = vtk.vtkCellArray()
            x0,x1,y0,y1,z0,z1 = self.element.axes['X'][0],self.element.axes['X'][-1], self.element.axes['Y'][0],self.element.axes['Y'][-1], self.element.axes['Z'][0],self.element.axes['Z'][-1]
            ptA_id = edge_points.InsertNextPoint((x0,y0,z0))
            ptB_id = edge_points.InsertNextPoint((x1,y0,z0))
            ptC_id = edge_points.InsertNextPoint((x1,y1,z0))
            ptD_id = edge_points.InsertNextPoint((x0,y1,z0))
            ptE_id = edge_points.InsertNextPoint((x0,y0,z1))
            ptF_id = edge_points.InsertNextPoint((x1,y0,z1))
            ptG_id = edge_points.InsertNextPoint((x1,y1,z1))
            ptH_id = edge_points.InsertNextPoint((x0,y1,z1))
            faces = [(ptA_id,ptB_id,ptC_id,ptD_id), (ptE_id,ptF_id,ptG_id,ptH_id), (ptA_id,ptB_id,ptF_id,ptE_id), (ptC_id,ptD_id,ptH_id,ptG_id), (ptA_id,ptD_id,ptH_id,ptE_id), (ptB_id,ptC_id,ptG_id,ptF_id)]
            for a,b,c,d in faces :
                edge_lines.InsertNextCell(2, (a,b))
                edge_lines.InsertNextCell(2, (b,c))
                edge_lines.InsertNextCell(2, (c,d))
                edge_lines.InsertNextCell(2, (d,a))
            edge_polydata = vtk.vtkPolyData()
            edge_polydata.SetPoints(edge_points)
            edge_polydata.SetLines(edge_lines)
            edge_mapper = vtk.vtkPolyDataMapper()
            edge_mapper.SetInputData(edge_polydata)
            edge_actor = VTK_Actor(mapper=edge_mapper)
            
            #------------------------------------------------------------------
            self.plotted.configure(Z=Z, volu_grid=grid, volu_scalars=scalars, volu_actor=volu_actor, edge_actor=edge_actor)
            
            #------------------------------------------------------------------
            if self.element.linked_elements is None :
                self.cbar = self.graph.legend.add_cbar(self)
                
    #==========================================================================
    def _update_plotted(self) :
        #----------------------------------------------------------------------
        self.element.load_data()
        positions = self.get_positions()
    
        #----------------------------------------------------------------------
        gs = self.style
        gclass = type(self.graph).__name__
        
        
        #---- Graph_MPL_1D ----------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            P = self.plotted.plotted
            xdim = self.graph.graph_config.dimensions[0]
            
            indices = self.element.get_indices(positions, graph_dimensions=self.graph.graph_config.dimensions, field=self.opts.get('field'))
            y = self.element.get_matrix_data(indices)
            if xdim in self.element.axes.keys() :
                x = self.element.axes[xdim]
                xnode = self.element.is_dim_nodes(xdim)
                X,Y = x,y
                if not xnode : X,Y = np.vstack((x[:-1],x[1:])).T.ravel(),np.vstack((y,y)).T.ravel() # créneaux
                else : X,Y = x,y
                P.set_data(X, Y)
                self.plotted.configure(ymin=np.nanmin(Y), ymax=np.nanmax(Y))
            else :
                segs = [[[0,y],[1,y]]]
                P.set_segments(segs)
                self.plotted.configure(ymin=y, ymax=y)
                
        #---- Graph_MPL_2D ----------------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            P = self.plotted.plotted
            xdim = self.graph.graph_config.dimensions[0]
            ydim = self.graph.graph_config.dimensions[1]
            
            indices = self.element.get_indices(positions, graph_dimensions=self.graph.graph_config.dimensions, field=self.opts.get('field'))
            Z = self.element.get_matrix_data(indices)
            if self.element.dimensions.index(xdim) < self.element.dimensions.index(ydim) : Z = Z.T
            if self.plotted.plotted._shading != 'flat' :
                nx = len(self.element.axes[xdim])
                ny = len(self.element.axes[ydim])
                if Z.shape[0] != ny : Z = np.repeat(Z, 2, axis=0)
                if Z.shape[1] != nx : Z = np.repeat(Z, 2, axis=1)
            self.plotted.configure(Z=Z)
            P.set_array(Z)
            
            cmin,cmax = self.element.get_range(self.opts.get('field'))
            self.plotted.set_clim(cmin,cmax)
            
        #---- Graph_VTK -------------------------------------------------------
        elif gclass == 'Graph_VTK' :
            self.plotted.volu_actor.SetVisibility(not gs.get('slice.is_active'))
            if self.plotted.slice_actor is not None : self.plotted.slice_actor.SetVisibility(gs.get('slice.is_active'))
            
            #------------------------------------------------------------------
            cmin,cmax = self.element.get_range(self.opts.get('field'))
            self.plotted.set_clim(cmin,cmax)
            
            #------------------------------------------------------------------
            if gs.get('slice.is_active') :
                if self.plotted.slice_actor is not None : self.graph.remove_actor(self.plotted.slice_actor)
                
                plan = gs.get('slice.plan')
                plane = vtk.vtkPlane()
                if plan == 'XY' : plane.SetNormal(0, 0, 1)
                if plan == 'XZ' : plane.SetNormal(0, 1, 0)
                if plan == 'YZ' : plane.SetNormal(1, 0, 0)
                pos = []
                indices = {dim:slice(0, self.element.sizes[dim]) for dim in self.element.dimensions}
                for dim in 'XYZ' :
                    if dim in plan :
                        c = (self.element.axes[dim][0]+self.element.axes[dim][-1])/2.0
                    else :
                        i = gs.get('slice.position')
                        indices[dim] = i
                        c = (self.element.axes[dim][i]+self.element.axes[dim][i+1])/2.0
                    pos.append(c)
                plane.SetOrigin(*pos)
                cutter = vtk.vtkCutter()
                cutter.SetCutFunction(plane)
                cutter.SetInputData(self.plotted.volu_grid)
                slice_mapper = vtk.vtkDataSetMapper()
                slice_mapper.SetInputConnection(cutter.GetOutputPort())
                slice_mapper.SetScalarRange(self.plotted.volu_scalars.GetRange())
                slice_actor = VTK_Actor(renderer=self.graph.renderer, mapper=slice_mapper)
                Z = self.element.get_matrix_data([indices[d] for d in self.element.dimensions])
                self.plotted.configure(slice_cutter=cutter, slice_actor=slice_actor, Z=Z)
                
    #==========================================================================
    def _get_pointed_data(self, pointed_x, pointed_y) :
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
        positions = self.get_positions()
                
        #---- Graph_MPL_1D ----------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            xdim = self.graph.graph_config.dimensions[0]
            indices = self.element.get_indices(positions, searches={xdim:pointed_x}, field=self.opts.get('field'))
            if None in indices : return None
            
            _y = self.element.get_matrix_data(indices)
            text = '{}={:.8G}'.format(self.label, _y)
            if self.element.linked_elements is not None : text = self.element.linked_elements[_y].label
            dims = self.element.dimensions
            
            if xdim in dims :
                idx = indices[dims.index(xdim)]
                X = self.element.axes[xdim]
                if xdim in self.element.edge_axes : return {'x0':X[idx], 'x1':X[idx+1], 'y':_y, 'text':text}
                else                              : return {'x':X[idx], 'y':_y, 'text':text}
            else : return {'y':_y, 'text':text}
            
        #---- Graph_MPL_2D ----------------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            xdim = self.graph.graph_config.dimensions[0]
            ydim = self.graph.graph_config.dimensions[1]
            
            indices = self.element.get_indices(positions, searches={xdim:pointed_x, ydim:pointed_y}, field=self.opts.get('field'))
            if None in indices : return None
            _y = self.element.get_matrix_data(indices)
            
            if self.element.linked_elements is not None : text = "{}={}".format(self.label, self.element.linked_elements[_y].label)
            else : text = '{}={:.8G}'.format(self.label, _y)
            rep = {'text':text}
                
            dims = self.element.dimensions
            
            if xdim in dims :
                idx = indices[dims.index(xdim)]
                X = self.element.axes[xdim]
                if self.element.is_dim_edge(xdim) : rep['x0'],rep['x1'] = X[idx],X[idx+1]
                else : rep['x'] = X[idx]
                
            if ydim in dims :
                idy = indices[dims.index(ydim)]
                Y = self.element.axes[ydim]
                if self.element.is_dim_edge(ydim) : rep['y0'],rep['y1'] = Y[idy],Y[idy+1]
                else : rep['y'] = Y[idy]
                
            return rep
            
        #----------------------------------------------------------------------
        return None
        
    #==========================================================================
    def _update_style(self) :
        #----------------------------------------------------------------------
        gs = self.style
        
        #----------------------------------------------------------------------
        resync = 'sync.is_active' in gs.changed
        reslice = 'element.is_active' in gs.changed and gs.get('element.is_active') and gs.get('slice.is_active')
        reslice = reslice or len([k for k in ['slice.is_active','slice.plan','slice.position'] if k in gs.changed]) > 0
        rerange = resync or reslice or len([k for k in ['range.min.is_active','range.min.text','range.min.hide', 'range.max.is_active','range.max.text','range.max.hide'] if k in gs.changed]) > 0
        
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
            
        #----------------------------------------------------------------------
        if resync or reslice :
            self.update_plotted()
            self.update_pointed(None)
        
        #----------------------------------------------------------------------
        if self.graph.engine == 'VTK' :
            self.plotted.edge_actor.SetVisibility(gs.get('border.is_active') or gs.get('highlight.is_active'))
            if gs.get('highlight.is_active') : self.plotted.edge_actor.set_renderer(self.graph.renderer2)
            else                             : self.plotted.edge_actor.set_renderer(self.graph.renderer)
            LS = gs.get('border.style').copy()
            if LS['line_color'] == 'auto' : LS['line_color'] = 'white'
            self.plotted.edge_actor.set_props(**LS)
            
        #----------------------------------------------------------------------
        if self.graph.engine == 'MPL' :
            P = self.plotted.plotted
            g_index = self.graph.graph_elements.index(self)
            P.set_zorder(g_index+1)
                
        #----------------------------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            P = self.plotted.plotted
            pclass = type(P).__name__
            
            autocolor = self.graph.get_autocolor(self)
            alpha = None
            
            if gs.has('line.is_active') :
                if pclass == 'LineCollection' : # pas de marker, et style invalide
                    P.set_visible(gs.get('line.is_active'))
                    
                if gs.get('line.is_active') :
                    S = gs.get('line.style')
                    P.set_linestyle(S['line_style'])
                    P.set_linewidth(S['line_width'])
                    P.set_alpha(S['line_alpha'])
                    P.set_color(S['line_color'] if S['line_color'] != 'auto' else autocolor)
                    alpha = S['line_alpha']
                    
                elif pclass != 'LineCollection' :
                    P.set_linestyle('none')
            
            if gs.has('mark.is_active') and pclass != 'LineCollection' :
                autocolor = 'black'
                if gs.get('mark.is_active') :
                    S = gs.get('mark.style')
                    P.set_marker(S['mark_shape'])
                    P.set_markersize(S['mark_size'])
                    P.set_markeredgewidth(S['mark_edge_width'])
                    P.set_markeredgecolor(S['mark_edge_color'] if S['mark_edge_width'] != 'auto' else autocolor)
                    P.set_markerfacecolor(S['mark_face_color'] if S['mark_face_color'] != 'auto' else autocolor)
                    if alpha is None : P.set_alpha(S['mark_alpha']) # que si pas de ligne
                else :
                    P.set_marker('none')
        
        #----------------------------------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            if rerange :
                P = self.plotted.plotted
                Z = np.array(self.plotted.Z)
                cmin,cmax = icmin,icmax = self.element.get_range(self.opts.get('field'))
                if gs.get('range.min.is_active') :
                    cmin = to_float(gs.get('range.min.text'),cmin)
                    if gs.get('range.min.hide') :
                        Z[(Z < cmin)] = np.nan
                if gs.get('range.max.is_active') :
                    cmax = to_float(gs.get('range.max.text'),cmax)
                    if gs.get('range.max.hide') :
                        Z[(Z > cmax)] = np.nan
                P.set_array(Z)
                self.plotted.set_clim(cmin,cmax)
            
            S = gs.get('fill.style')
            alpha = S['fill_alpha'] if gs.get('fill.is_active') else 0.0
            P.set_alpha(alpha)
            self.plotted.set_cmap(S['fill_palette'])
            
        #----------------------------------------------------------------------
        elif gclass == 'Graph_VTK' :
            if rerange :
                cmin,cmax = icmin,icmax = self.element.get_range(self.opts.get('field'))
                if gs.get('range.min.is_active') : cmin = to_float(gs.get('range.min.text'),cmin)
                if gs.get('range.max.is_active') : cmax = to_float(gs.get('range.max.text'),cmax)
                
                if gs.get('slice.is_active') :
                    cutter = self.plotted.slice_cutter
                    mapper = self.plotted.slice_actor.GetMapper()
                    if cmin != icmin or cmax != icmax :
                        threshold = vtk.vtkThreshold()
                        threshold.SetInputConnection(cutter.GetOutputPort())
                        threshold.SetLowerThreshold(cmin)
                        threshold.SetUpperThreshold(cmax)
                        threshold.Update()
                        mapper.SetInputConnection(threshold.GetOutputPort())
                    else :
                        cutter.SetInputData(self.plotted.volu_grid)
                        mapper.SetInputConnection(cutter.GetOutputPort())
                else :
                    mapper = self.plotted.volu_actor.GetMapper()
                    if cmin != icmin or cmax != icmax :
                        xnode,ynode,znode = self.element.is_dim_nodes('X'), self.element.is_dim_nodes('Y'), self.element.is_dim_nodes('Z')
                        threshold = vtk.vtkThreshold()
                        threshold.SetInputData(self.plotted.volu_grid)
                        threshold.SetLowerThreshold(cmin)
                        threshold.SetUpperThreshold(cmax)
                        if True not in [xnode,ynode,znode] : threshold.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_CELLS, vtk.vtkDataSetAttributes.SCALARS)
                        else                               : threshold.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, vtk.vtkDataSetAttributes.SCALARS)
                        threshold.Update()
                        mapper.SetInputData(threshold.GetOutput())
                    else :
                        mapper.SetInputData(self.plotted.volu_grid)
                    mapper.SetScalarRange(cmin, cmax)
                self.plotted.set_clim(cmin,cmax)
        
            S = gs.get('fill.style')
            alpha = S['fill_alpha'] if gs.get('fill.is_active') else 0.0
            if gs.get('slice.is_active') : self.plotted.slice_actor.set_props(fill_alpha=alpha)
            else                         : self.plotted.volu_actor.set_props(fill_alpha=alpha)
            self.plotted.set_cmap(S['fill_palette'])
            
            
            
    #==========================================================================
    def _get_legend(self) :
        #----------------------------------------------------------------------
        gs = self.style
        
        #----------------------------------------------------------------------
        if self.graph.engine == 'MPL' :
            handle = self.plotted.plotted
        
        #----------------------------------------------------------------------
        elif self.graph.engine == 'VTK' :
            # TODO : patch avec dégradé si cbar
            return None
            
        #----------------------------------------------------------------------
        return {'handle':handle, 'label':gs.get('legend.text')}
        
    #==========================================================================
    def _get_linked_legend(self) :
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
        if gclass not in ['Graph_MPL_2D','Graph_VTK'] : return None
        
        #----------------------------------------------------------------------
        linked = {}
        indices = np.unique(self.plotted.Z)
        for i in indices :
            if i is None : continue
            linked_element = self.element.linked_elements[i]
            handle = Patch(facecolor=linked_element.get_style('color'),
                           edgecolor='black',
                           linewidth=0.5,
                           linestyle='-'
                           )
            index = (linked_element.index,self.opts.get('field'))
            linked[index] = (handle,linked_element.label)
            
        #----------------------------------------------------------------------
        return linked
    
    #==========================================================================
    def get_save_data(self) :
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
        positions = self.get_positions()
        
        #----------------------------------------------------------------------
        data = {}
        data['axes'] = []
        
        #----------------------------------------------------------------------
        xdim = self.graph.graph_config.dimensions[0]
        if xdim not in self.element.dimensions : return None
        x = self.element.axes[xdim]
        if xdim in self.element.edge_axes :
            data[xdim+'0'] = x[:-1]
            data[xdim+'1'] = x[1:]
            data['axes'] += [xdim+'0',xdim+'1']
        else :
            data[xdim] = x
            data['axes'] += [xdim]
        
        #----------------------------------------------------------------------
        if gclass == 'Graph_MPL_2D' :
            ydim = self.graph.graph_config.dimensions[1]
            if ydim not in self.element.dimensions : return None
            y = self.element.axes[ydim]
            if ydim in self.element.edge_axes :
                data[ydim+'0'] = y[:-1]
                data[ydim+'1'] = y[1:]
                data['axes'] += [ydim+'0',ydim+'1']
            else :
                data[ydim] = y
                data['axes'] += [ydim]
        
        #----------------------------------------------------------------------
        indices = self.element.get_indices(positions, graph_dimensions=self.graph.graph_config.dimensions, field=self.opts.get('field'))
        if gclass == 'Graph_MPL_1D' :
            data['values'] = self.element.get_matrix_data(indices, round_fmt='{:.6G}')
            
        #----------------------------------------------------------------------
        elif gclass == 'Graph_MPL_2D'  :
            Z = self.element.get_matrix_data(indices, round_fmt='{:.6G}')
            if self.element.dimensions.index(xdim) < self.element.dimensions.index(ydim) : Z = Z.T
            data['values'] = Z
            
        #----------------------------------------------------------------------
        path = self.element.path.copy()
        dims = []
        str_indices = []
        coords = {}
        for i,indice in enumerate(indices) :
            dim = self.element.dimensions[i]
            
            if self.element.dimensions[i] == Matrix.FIELDS_NAME :
                path.append(self.element.get_fields()[indice])
                continue
            
            dims.append(dim)
            
            if type(indice) == int :
                str_indices.append(str(indice+1))
                C = self.element.get_dim_value(dim, indice)
                if type(C) == tuple : coord = '{:.8G} ; {:.8G}'.format(C[0],C[1])
                else : coord = '{:.8G}'.format(C)
            else :
                str_indices.append("-")
                C = self.element.get_lims(dim)
                coord = '{:.8G} -> {:.8G} ({})'.format(C[0],C[1],self.element.get_dim_size(dim))
                
            coords[dim] = coord
            
        #----------------------------------------------------------------------
        beacon = self.get_beacon()
        data['name'] = "{}_({})".format(beacon, ','.join(str_indices))
        data['infos'] = {'beacon':beacon, 'element':self.element, 'path':path, 'dimensions':dims, 'indices':str_indices, 'coordinates':coords}
        
        #----------------------------------------------------------------------
        return data
                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


