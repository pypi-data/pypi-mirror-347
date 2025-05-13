# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
#------------------------------------------------------------------------------
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------
from matplotlib.patches import Polygon, Patch
#------------------------------------------------------------------------------
import vtk
#------------------------------------------------------------------------------
import shapely
#------------------------------------------------------------------------------
from Graph_Element import VTK_Actor, Graph_Element_Style, Graph_Element
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def add_edge(edges, x0,x1,y0,y1,z0,z1) :
    #--------------------------------------------------------------------------
    A,B,C,D,E,F,G,H = (x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)
    keys = []
    keys += [('X',A,D),('X',D,H),('X',H,E),('X',E,A)]
    keys += [('X',B,C),('X',C,G),('X',G,F),('X',F,B)]
    keys += [('Y',A,B),('Y',B,F),('Y',F,E),('Y',E,A)]
    keys += [('Y',C,D),('Y',D,H),('Y',H,G),('Y',G,C)]
    keys += [('Z',A,B),('Z',B,C),('Z',C,D),('Z',A,D)]
    keys += [('Z',E,F),('Z',F,G),('Z',G,H),('Z',H,E)]
    for key in keys :
        _key = tuple([key[0]] + sorted(key[1:3]))
        edges[_key] = edges.get(_key,0) + 1
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def add_face(faces, x0,x1,y0,y1,z0,z1) :
    #--------------------------------------------------------------------------
    keys = []
    keys += [('X',x0,x0,y0,y1,z0,z1)]
    keys += [('X',x1,x1,y0,y1,z0,z1)]
    keys += [('Y',x0,x1,y0,y0,z0,z1)]
    keys += [('Y',x0,x1,y1,y1,z0,z1)]
    keys += [('Z',x0,x1,y0,y1,z0,z0)]
    keys += [('Z',x0,x1,y0,y1,z1,z1)]
    for key in keys : faces[key] = faces.get(key,0) + 1
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** CUBOID ***
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Element_Style_Cuboid(Graph_Element_Style) :
    
    #==========================================================================
    def _init_defaults(self) :
        #----------------------------------------------------------------------
        gclass = type(self.graph_element.graph).__name__
        
        #----------------------------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            self.set('line.is_active', True)
            self.set('line.style', {'line_style':'-',
                                    'line_width':1,
                                    'line_color':'auto',
                                    'line_alpha':1,
                                    })
            
        #----------------------------------------------------------------------
        else :
            self.set('fill.is_active', True)
            self.set('fill.style', {'fill_color':'auto',
                                    'fill_alpha':0.5,
                                    })

            self.set('border.is_active', True)
            self.set('border.style', {'line_style':'-',
                                      'line_width':1,
                                      'line_color':'auto',
                                      'line_alpha':1,
                                      })
        
        #----------------------------------------------------------------------
        if gclass == 'Graph_VTK' :
            self.set('highlight.is_active', False)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Element_Cuboid(Graph_Element) :
        
    #==========================================================================
    def _create_plotted(self) :
        #----------------------------------------------------------------------
        self.element.load_axes()
        
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
        
        
        #---- Graph_MPL_1D ----------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            _plotted = self.graph.ax.plot([], [], label=self.label)[0]
            self.plotted.configure(plotted=_plotted)
        
        
        #---- Graph_MPL_2D ----------------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            _plotted = Polygon([(np.nan,np.nan)], closed=True, label=self.label)
            self.graph.ax.add_patch(_plotted)
            self.plotted.configure(plotted=_plotted)
            
            
        #---- Graph_VTK -------------------------------------------------------
        elif gclass == 'Graph_VTK' :
            #--------------------------------------------------------------
            faces_counts = {}
            edges_counts = {}
            x0,x1,y0,y1,z0,z1 = self.element.coordinates
            add_face(faces_counts, x0,x1,y0,y1,z0,z1)
            add_edge(edges_counts, x0,x1,y0,y1,z0,z1)
            #--------------------------------------------------------------
            surf_points = vtk.vtkPoints()
            surf_polygons = vtk.vtkCellArray()
            for key,N in faces_counts.items() :
                if N != 1 : continue
                d,x0,x1,y0,y1,z0,z1 = key
                if   d == 'X' : A,B,C,D = (x0,y0,z0),(x0,y1,z0),(x0,y1,z1),(x0,y0,z1)
                elif d == 'Y' : A,B,C,D = (x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)
                elif d == 'Z' : A,B,C,D = (x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)
                ptA_id = surf_points.InsertNextPoint(A)
                ptB_id = surf_points.InsertNextPoint(B)
                ptC_id = surf_points.InsertNextPoint(C)
                ptD_id = surf_points.InsertNextPoint(D)
                surf_polygons.InsertNextCell(4, [ptA_id,ptB_id,ptC_id,ptD_id])
            surf_data = vtk.vtkPolyData()
            surf_data.SetPoints(surf_points)
            surf_data.SetPolys(surf_polygons)
            surf_mapper = vtk.vtkPolyDataMapper()
            surf_mapper.SetInputData(surf_data)
            surf_actor = VTK_Actor(renderer=self.graph.renderer, mapper=surf_mapper, alpha=0.5)
            #--------------------------------------------------------------
            prev_edges = []
            edge_points = vtk.vtkPoints()
            edge_lines = vtk.vtkCellArray()
            for key,N in edges_counts.items() :
                if N in [2,4] : continue
                K = (key[1],key[2])
                if K in prev_edges : continue
                prev_edges.append(K)
                pt1_id = edge_points.InsertNextPoint(key[1])
                pt2_id = edge_points.InsertNextPoint(key[2])
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, pt1_id)
                line.GetPointIds().SetId(1, pt2_id)
                edge_lines.InsertNextCell(line)
            edge_polydata = vtk.vtkPolyData()
            edge_polydata.SetPoints(edge_points)
            edge_polydata.SetLines(edge_lines)
            edge_mapper = vtk.vtkPolyDataMapper()
            edge_mapper.SetInputData(edge_polydata)
            edge_actor = VTK_Actor(mapper=edge_mapper)
            self.plotted.configure(surf_actor=surf_actor, edge_actor=edge_actor)
        
    #==========================================================================
    def _update_plotted(self) :
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
        
        #----------------------------------------------------------------------
        positions = self.get_positions()
        
        #---- Graph_MPL_1D ----------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            P = self.plotted.plotted
            xdim = self.graph.graph_config.dimensions[0]
            
            x = self.element.axes[xdim]
            i,j,k = [positions[dim]['pos'] for dim in ['X','Y','Z']]
            i0,i1,j0,j1,k0,k1 = self.element.indices
            ivalid = i >= i0 and i <= i1
            jvalid = j >= j0 and j <= j1
            kvalid = k >= k0 and k <= k1
            X = []
            if   xdim == 'X' and jvalid and kvalid : X += [x[i0], x[i1+1]]
            elif xdim == 'Y' and ivalid and kvalid : X += [x[j0], x[j1+1]]
            elif xdim == 'Z' and jvalid and kvalid : X += [x[k0], x[k1+1]]
            Y = [self.element.value for v in X]
            P.set_data(X,Y)
            
            if len(X) == 0 : self.plotted.configure(xmin=None, xmax=None, ymin=None, ymax=None, empty=True)
            else : self.plotted.configure(xmin=np.nanmin(X), xmax=np.nanmax(X), ymin=np.nanmin(Y), ymax=np.nanmax(Y), empty=False)
                
        #---- Graph_MPL_2D ----------------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            P = self.plotted.plotted
            xdim = self.graph.graph_config.dimensions[0]
            ydim = self.graph.graph_config.dimensions[1]
            
            x = self.element.axes[xdim]
            y = self.element.axes[ydim]
            i,j,k = [positions[dim]['pos'] for dim in ['X','Y','Z']]
            i0,i1,j0,j1,k0,k1 = self.element.indices
            ivalid = i >= i0 and i <= i1
            jvalid = j >= j0 and j <= j1
            kvalid = k >= k0 and k <= k1
            x0 = None
            if   xdim == 'X' and ydim == 'Y' and kvalid : x0,x1,y0,y1 = x[i0],x[i1+1], y[j0],y[j1+1]
            elif xdim == 'X' and ydim == 'Z' and jvalid : x0,x1,y0,y1 = x[i0],x[i1+1], y[k0],y[k1+1]
            elif xdim == 'Y' and ydim == 'Z' and ivalid : x0,x1,y0,y1 = x[j0],x[j1+1], y[k0],y[k1+1]
            if x0 is not None :
                P.set_xy([(x0,y0),(x1,y0),(x1,y1),(x0,y1),(x0,y0)])
                self.plotted.configure(xmin=x0, xmax=x1, ymin=y0, ymax=y1, empty=False)
            else :
                P.set_xy([(np.nan,np.nan)])
                self.plotted.configure(xmin=None, xmax=None, ymin=None, ymax=None, empty=True)
                
    #==========================================================================
    def _get_pointed_data(self, pointed_x, pointed_y) :
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
        positions = self.get_positions()
        
        #---- Graph_MPL_1D ----------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            xdim = self.graph.graph_config.dimensions[0]
            indices = []
            for dim in ['X','Y','Z'] :
                if   dim == xdim : i = idx = self.element.coord_to_index(dim, pointed_x)
                else             : i = positions[dim]['pos']
                if i is None : return None
                indices.append(i)
            if not self.element.contains(*indices) : return None
            X = self.element.axes[xdim]
            return {'x0':X[idx],
                    'x1':X[idx+1],
                    'y':self.element.value,
                    'text':self.element.label,
                    }
        
        #---- Graph_MPL_2D ----------------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            xdim = self.graph.graph_config.dimensions[0]
            ydim = self.graph.graph_config.dimensions[1]
            
            indices = []
            for dim in ['X','Y','Z'] :
                if   dim == xdim : i = idx = self.element.coord_to_index(dim, pointed_x)
                elif dim == ydim : i = idy = self.element.coord_to_index(dim, pointed_y)
                else             : i = positions[dim]['pos']
                if i is None : return None
                indices.append(i)
                
            if not self.element.contains(*indices) : return None
            X = self.element.axes[xdim]
            Y = self.element.axes[ydim]
            return {'x0':X[idx],
                    'x1':X[idx+1],
                    'y0':Y[idy],
                    'y1':Y[idy+1],
                    'text':self.element.label,
                    }
        
    #==========================================================================
    def _update_style(self) :
        #----------------------------------------------------------------------
        gs = self.style
        gclass = type(self.graph).__name__
        
        #----------------------------------------------------------------------
        resync = 'sync.is_active' in gs.changed
        if resync :
            self.update_plotted()
            
        #----------------------------------------------------------------------
        if self.graph.engine == 'MPL' :
            P = self.plotted.plotted
            g_index = self.graph.graph_elements.index(self)
            P.set_zorder(g_index+1)
        
        #----------------------------------------------------------------------
        autocolor = self.element.get_style('color')
        
        #----------------------------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            P = self.plotted.plotted
            P.set_visible(gs.get('line.is_active'))
            if gs.get('line.is_active') :
                S = gs.get('line.style')
                P.set_color(S['line_color'] if S['line_color'] != 'auto' else autocolor)
                P.set_linestyle(S['line_style'])
                P.set_linewidth(S['line_width'])
                P.set_alpha(S['line_alpha'])
                
        #----------------------------------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            P = self.plotted.plotted
            alpha = None
            
            if gs.get('fill.is_active') :
                S = gs.get('fill.style')
                P.set_facecolor(S['fill_color'] if S['fill_color'] != 'auto' else autocolor)
                P.set_alpha(S['fill_alpha'])
                alpha = S['fill_alpha']
            else :
                P.set_facecolor('none')
                
            if gs.get('border.is_active') :
                S = gs.get('border.style')
                P.set_edgecolor(S['line_color'] if S['line_color'] != 'auto' else 'black')
                P.set_linewidth(S['line_width'])
                P.set_linestyle(S['line_style'])
                if alpha is None : P.set_alpha(S['line_alpha'])
            else :
                P.set_linestyle('none')
            
        #----------------------------------------------------------------------
        elif self.graph.engine == 'VTK' :
            self.plotted.edge_actor.SetVisibility(gs.get('border.is_active') or gs.get('highlight.is_active'))
            if gs.get('highlight.is_active') : self.plotted.edge_actor.set_renderer(self.graph.renderer2)
            else                             : self.plotted.edge_actor.set_renderer(self.graph.renderer)
            LS = gs.get('border.style').copy()
            if LS['line_color'] == 'auto' : LS['line_color'] = 'white'
            self.plotted.edge_actor.set_props(**LS)
            
            self.plotted.surf_actor.SetVisibility(gs.get('fill.is_active'))
            FS = gs.get('fill.style').copy()
            if FS['fill_color'] == 'auto' : FS['fill_color'] = autocolor
            self.plotted.surf_actor.set_props(**FS)
            
        #----------------------------------------------------------------------
        self.graph.update_legend()
        
    #==========================================================================
    def _get_legend(self) :
        #----------------------------------------------------------------------
        gs = self.style
        
        gclass = type(self.graph).__name__
        
        label = gs.get('legend.text')
        if self.plotted.empty : label = '$'+label.replace("_","\\_")+'$'
        
        autocolor = self.element.get_style('color')
        
        #----------------------------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            handle = self.plotted.plotted
            
        #----------------------------------------------------------------------
        else :
            opts = {}
            if gs.get('fill.is_active') :
                S = gs.get('fill.style')
                opts['facecolor'] = S['fill_color'] if S['fill_color'] != 'auto' else autocolor
                opts['alpha']     = S['fill_alpha']
            else :
                opts['facecolor'] = 'none'
            
            if gs.get('border.is_active') :
                S = gs.get('border.style')
                opts['edgecolor'] = S['line_color'] if S['line_color'] != 'auto' else 'black'
                opts['linewidth'] = S['line_width']
                opts['linestyle'] = S['line_style']
                if 'alpha' not in opts.keys() : opts['alpha'] = S['line_alpha']
            
            handle = Patch(**opts)
            
        #----------------------------------------------------------------------
        return {'handle':handle, 'label':label}
                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** POLYCUBOID ***
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Element_Style_PolyCuboid(Graph_Element_Style_Cuboid) :
    pass
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Element_PolyCuboid(Graph_Element_Cuboid) :
        
    #==========================================================================
    def _create_plotted(self) :
        #----------------------------------------------------------------------
        self.element.compute_cuboids()
        
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
        
        
        #---- Graph_MPL_1D ----------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            _plotted = self.graph.ax.plot([], [], label=self.label)[0]
            self.plotted.configure(plotted=_plotted)
        
        
        #---- Graph_MPL_2D ----------------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            _plotted = Polygon([(np.nan,np.nan)], closed=True, label=self.label)
            self.graph.ax.add_patch(_plotted)
            self.plotted.configure(plotted=_plotted)
            
            
        #---- Graph_VTK -------------------------------------------------------
        elif gclass == 'Graph_VTK' :
            #--------------------------------------------------------------
            faces_counts = {}
            edges_counts = {}
            for x0,x1,y0,y1,z0,z1 in self.element.coordinates :
                add_face(faces_counts, x0,x1,y0,y1,z0,z1)
                add_edge(edges_counts, x0,x1,y0,y1,z0,z1)
            #--------------------------------------------------------------
            surf_points = vtk.vtkPoints()
            surf_polygons = vtk.vtkCellArray()
            for key,N in faces_counts.items() :
                if N != 1 : continue
                d,x0,x1,y0,y1,z0,z1 = key
                if   d == 'X' : A,B,C,D = (x0,y0,z0),(x0,y1,z0),(x0,y1,z1),(x0,y0,z1)
                elif d == 'Y' : A,B,C,D = (x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)
                elif d == 'Z' : A,B,C,D = (x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)
                ptA_id = surf_points.InsertNextPoint(A)
                ptB_id = surf_points.InsertNextPoint(B)
                ptC_id = surf_points.InsertNextPoint(C)
                ptD_id = surf_points.InsertNextPoint(D)
                surf_polygons.InsertNextCell(4, [ptA_id,ptB_id,ptC_id,ptD_id])
            surf_data = vtk.vtkPolyData()
            surf_data.SetPoints(surf_points)
            surf_data.SetPolys(surf_polygons)
            surf_mapper = vtk.vtkPolyDataMapper()
            surf_mapper.SetInputData(surf_data)
            surf_actor = VTK_Actor(renderer=self.graph.renderer, mapper=surf_mapper, alpha=0.5)
            #--------------------------------------------------------------
            prev_edges = []
            edge_points = vtk.vtkPoints()
            edge_lines = vtk.vtkCellArray()
            for key,N in edges_counts.items() :
                if N in [2,4] : continue
                K = (key[1],key[2])
                if K in prev_edges : continue
                prev_edges.append(K)
                pt1_id = edge_points.InsertNextPoint(key[1])
                pt2_id = edge_points.InsertNextPoint(key[2])
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, pt1_id)
                line.GetPointIds().SetId(1, pt2_id)
                edge_lines.InsertNextCell(line)
            edge_polydata = vtk.vtkPolyData()
            edge_polydata.SetPoints(edge_points)
            edge_polydata.SetLines(edge_lines)
            edge_mapper = vtk.vtkPolyDataMapper()
            edge_mapper.SetInputData(edge_polydata)
            edge_actor = VTK_Actor(mapper=edge_mapper)
            self.plotted.configure(surf_actor=surf_actor, edge_actor=edge_actor)
        
    #==========================================================================
    def _update_plotted(self) :
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
        
        #----------------------------------------------------------------------
        positions = self.get_positions()
        
        #---- Graph_MPL_1D ----------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            P = self.plotted.plotted
            xdim = self.graph.graph_config.dimensions[0]
            
            x = self.element.axes[xdim]
            i,j,k = [positions[dim]['pos'] for dim in ['X','Y','Z']]
            X,Y = [],[]
            for i0,i1,j0,j1,k0,k1 in self.element.cuboids :
                ivalid = i >= i0 and i <= i1
                jvalid = j >= j0 and j <= j1
                kvalid = k >= k0 and k <= k1
                if   xdim == 'X' and jvalid and kvalid : X += [x[i0], x[i1+1], np.nan]
                elif xdim == 'Y' and ivalid and kvalid : X += [x[j0], x[j1+1], np.nan]
                elif xdim == 'Z' and jvalid and kvalid : X += [x[k0], x[k1+1], np.nan]
                Y = [self.element.value if ~np.isnan(v) else np.nan for v in X]
            P.set_data(X,Y)
            if len(X) == 0 : self.plotted.configure(xmin=None, xmax=None, ymin=None, ymax=None, empty=True)
            else : self.plotted.configure(xmin=np.nanmin(X), xmax=np.nanmax(X), ymin=np.nanmin(Y), ymax=np.nanmax(Y), empty=False)
                
        #---- Graph_MPL_2D ----------------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            P = self.plotted.plotted
            xdim = self.graph.graph_config.dimensions[0]
            ydim = self.graph.graph_config.dimensions[1]
            
            x = self.element.axes[xdim]
            y = self.element.axes[ydim]
            i,j,k = [positions[dim]['pos'] for dim in ['X','Y','Z']]
            
            polygons = []
            _x,_y = [],[]
            for i0,i1,j0,j1,k0,k1 in self.element.cuboids :
                ivalid = i >= i0 and i <= i1
                jvalid = j >= j0 and j <= j1
                kvalid = k >= k0 and k <= k1
                if   xdim == 'X' and ydim == 'Y' and kvalid : x0,x1,y0,y1 = x[i0],x[i1+1], y[j0],y[j1+1]
                elif xdim == 'X' and ydim == 'Z' and jvalid : x0,x1,y0,y1 = x[i0],x[i1+1], y[k0],y[k1+1]
                elif xdim == 'Y' and ydim == 'Z' and ivalid : x0,x1,y0,y1 = x[j0],x[j1+1], y[k0],y[k1+1]
                else : continue
                polygons.append(shapely.geometry.Polygon([(x0,y0),(x1,y0),(x1,y1),(x0,y1)]))
                _x += [x0,x1]
                _y += [y0,y1]
            
            if len(polygons) == 0 :
                P.set_xy([(np.nan,np.nan)])
                self.plotted.configure(xmin=None, xmax=None, ymin=None, ymax=None, empty=True)
            else :
                merged_polygon = shapely.unary_union(polygons)
                if   merged_polygon.geom_type == 'Polygon' : vertices = list(merged_polygon.exterior.coords)
                elif merged_polygon.geom_type == 'MultiPolygon' :
                    vertices = []
                    for p in merged_polygon.geoms :
                        vertices += list(p.exterior.coords)
                        vertices.append((np.nan,np.nan)) # cut entre les polygons non joints
                else :
                    raise Exception("merged_polygon de type '{}'".format(type(merged_polygon)))
                P.set_xy(vertices)
                self.plotted.configure(xmin=np.nanmin(_x), xmax=np.nanmax(_x), ymin=np.nanmin(_y), ymax=np.nanmax(_y), empty=False)
                
    #==========================================================================
    def _get_pointed_data(self, pointed_x, pointed_y) :
        #----------------------------------------------------------------------
        gclass = type(self.graph).__name__
        positions = self.get_positions()
        
        #---- Graph_MPL_1D ----------------------------------------------------
        if gclass == 'Graph_MPL_1D' :
            xdim = self.graph.graph_config.dimensions[0]
            indices = []
            for dim in ['X','Y','Z'] :
                if   dim == xdim : i = idx = self.element.coord_to_index(dim, pointed_x)
                else             : i = positions[dim]['pos']
                if i is None : return None
                indices.append(i)
            if not self.element.contains(*indices) : return None
            X = self.element.axes[xdim]
            return {'x0':X[idx],
                    'x1':X[idx+1],
                    'y':self.element.value,
                    'text':self.element.label,
                    }
        
        #---- Graph_MPL_2D ----------------------------------------------------
        elif gclass == 'Graph_MPL_2D' :
            xdim = self.graph.graph_config.dimensions[0]
            ydim = self.graph.graph_config.dimensions[1]
            
            indices = []
            for dim in ['X','Y','Z'] :
                if   dim == xdim : i = idx = self.element.coord_to_index(dim, pointed_x)
                elif dim == ydim : i = idy = self.element.coord_to_index(dim, pointed_y)
                else             : i = positions[dim]['pos']
                if i is None : return None
                indices.append(i)
                
            if not self.element.contains(*indices) : return None
            X = self.element.axes[xdim]
            Y = self.element.axes[ydim]
            return {'x0':X[idx],
                    'x1':X[idx+1],
                    'y0':Y[idy],
                    'y1':Y[idy+1],
                    'text':self.element.label,
                    }
                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


