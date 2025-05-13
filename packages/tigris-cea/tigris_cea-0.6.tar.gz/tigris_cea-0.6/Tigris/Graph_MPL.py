# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
#------------------------------------------------------------------------------
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QCursor
#------------------------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import font_manager as fm
import matplotlib.ticker as mticker
#------------------------------------------------------------------------------
from utils_mpl import RectSelector, get_mpl_plotted_range
from Graph import Graph
from Graph_Style import Graph_Style,Graph_MPL_Style
from utils import to_float
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def new_graph(page, graph_config, **kwargs) :
    #--------------------------------------------------------------------------
    if   graph_config.gtype == '1D' : return Graph_MPL_1D(page, graph_config, **kwargs)
    elif graph_config.gtype == '2D' : return Graph_MPL_2D(page, graph_config, **kwargs)
    #--------------------------------------------------------------------------
    return Graph(page, graph_config, **kwargs)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_MPL(Graph) :
    
    #==========================================================================
    def __init__(self, page, graph_config, **kwargs) :
        #----------------------------------------------------------------------
        self.fig    = None
        self.canvas = None
        self.ax     = None
        
        #----------------------------------------------------------------------
        self.f_lims = {}
        self.invert = {'X':False, 'Y':False}
        self.margin = {'X':0.05 , 'Y':0.05}
        self.selectors = {}
        
        #----------------------------------------------------------------------
        self.redraw_timer = QTimer()
        self.redraw_timer.setSingleShot(True)
        self.redraw_timer.timeout.connect(self._redraw)
        
        #----------------------------------------------------------------------
        Graph.__init__(self, page, graph_config, **kwargs)
        
        #----------------------------------------------------------------------
        self.engine = 'MPL'
            
    #==========================================================================
    def __repr__(self) :
        #----------------------------------------------------------------------
        return "Graph_MPL {}".format(self.name)
    
    #==========================================================================
    def _create_graph(self) :
        #----------------------------------------------------------------------
        self.fig = Figure(figsize=(5, 4), dpi=100, constrained_layout=False, facecolor='none', tight_layout=True)
        self.canvas = FigureCanvas(self.fig)
        #----------------------------------------------------------------------
        self.canvas.mpl_connect('button_press_event'  , self.on_mouse_press)
        self.canvas.mpl_connect("button_release_event", self.on_mouse_release)
        self.canvas.mpl_connect('motion_notify_event' , self.on_mouse_motion)
        self.canvas.mpl_connect('scroll_event'        , self.on_mouse_scroll)
        self.canvas.mpl_connect('axes_enter_event'  , self.on_enter_plot)
        self.canvas.mpl_connect('axes_leave_event'  , self.on_leave_plot)
        #----------------------------------------------------------------------
        self.lc_event = None
        self.mc_event = None
        self.rc_event = None
        self.mv_event = None
        self.ax_limits = None
        self.modifiers = {Qt.Key_Control:False, Qt.Key_Shift:False, Qt.Key_Alt:False}
        #----------------------------------------------------------------------
        self.ax = self.fig.add_subplot(1, 1, 1, facecolor=self.background_color)
        self.ax.set_axisbelow(False) # grid toujours au dessus
        #----------------------------------------------------------------------
        self.selectors['zoom'] = s = RectSelector(self.ax, buttons=[1], color='red', linewidth=1, alpha=0.1, fill_x=False, fill_y=False)
        s.zoneSelected.connect(self.on_zoom_changed)
        
        #----------------------------------------------------------------------
        self.style = Graph_MPL_Style(self)
        
        #----------------------------------------------------------------------
        return self.canvas
    
    #==========================================================================
    def _remove_graph(self) :
        #----------------------------------------------------------------------
        if self.fig is not None : self.fig.clear()
        if self.canvas is not None : self.canvas.deleteLater()
        
    #==========================================================================
    def keyPressEvent(self, event) :
        #----------------------------------------------------------------------
        if event.key() in self.modifiers.keys() :
            self.modifiers[event.key()] = True
            self.on_mouse_motion(self.mv_event)
            
        #----------------------------------------------------------------------
        else :
            super().keyPressEvent(event)
        
    #==========================================================================
    def keyReleaseEvent(self, event) :
        #----------------------------------------------------------------------
        if event.key() in self.modifiers.keys() :
            self.modifiers[event.key()] = False
            self.on_mouse_motion(self.mv_event)
            
    #==========================================================================
    def on_enter_plot(self, event) :
        #----------------------------------------------------------------------
        for ge in self.graph_elements :
            ge.set_pointed_visible(True)
            
    #==========================================================================
    def on_leave_plot(self, event) :
        #----------------------------------------------------------------------
        for ge in self.graph_elements :
            ge.set_pointed_visible(False)
        
    #==========================================================================
    def on_mouse_press(self, event) :
        #----------------------------------------------------------------------
        self.lc_event = None
        self.mc_event = None
        self.rc_event = None
        self.ax_limits = None
        
        #----------------------------------------------------------------------
        self.mv_event = None
        for rs in self.selectors.values() :
            rs.set_active(False)
            
        #----------------------------------------------------------------------
        if event.button == 1 and event.dblclick :
            self.rescale(redraw=True)
            return
        
        #----------------------------------------------------------------------
        if   event.button == 1 : self.lc_event = event
        elif event.button == 2 : self.mc_event = event
        elif event.button == 3 : self.rc_event = event
        
        #----------------------------------------------------------------------
        for ge in self.graph_elements :
            ge.set_pointed_visible(False)
        
        #----------------------------------------------------------------------
        if event.inaxes is not None and self.lc_event is not None :
            self.selectors['zoom'].set_active(True)
            
        #----------------------------------------------------------------------
        if event.button == 2 :
            if event.inaxes is not None :
                ax = event.inaxes
                self.canvas.setCursor(QCursor(Qt.ClosedHandCursor))
                self.ax_limits = ax.get_xlim(),ax.get_ylim()
                    
    #==========================================================================
    def on_mouse_release(self, event) :
        #----------------------------------------------------------------------
        if event.button == 3 and self.rc_event is not None : # Right-click
            self.open_menu()
            
        #----------------------------------------------------------------------
        self.lc_event = None
        self.mc_event = None
        self.rc_event = None
        self.ax_limits = None
        
        #----------------------------------------------------------------------
        self.canvas.setCursor(QCursor(Qt.ArrowCursor))
        
    #==========================================================================
    def on_mouse_motion(self, event) :
        #----------------------------------------------------------------------
        if event is None :
            self.mw.statusbar.showMessage("")
            return
        
        #----------------------------------------------------------------------
        redraw_needed = False
        
        #----------------------------------------------------------------------
        if self.lc_event is None and self.mc_event is None :
            self.update_pointed(event)
            
        #----------------------------------------------------------------------
        self.mv_event = event
        
        #----------------------------------------------------------------------
        if self.lc_event is not None and self.lc_event.inaxes == self.ax :
            fill_x = self.modifiers[Qt.Key_Control]
            fill_y = self.modifiers[Qt.Key_Shift]
            self.selectors['zoom'].on_move(event, fill_x=fill_x, fill_y=fill_y)
            
        #----------------------------------------------------------------------
        if event.button == 2 :
            if self.mc_event is not None :
                ax = self.mc_event.inaxes
                
                if ax is not None :
                    px,py = ax.transData.inverted().transform((self.mc_event.x, self.mc_event.y))
                    nx,ny = ax.transData.inverted().transform((event.x, event.y))
                    (x0,x1),(y0,y1) = self.ax_limits
                    
                    #----------------------------------------------------------
                    if not self.modifiers[Qt.Key_Control] :
                        if ax.xaxis.get_scale() == 'linear' :
                            dx = nx - px
                            x0 -= dx
                            x1 -= dx
                        elif ax.xaxis.get_scale() == 'log' :
                            _dx = np.log10(nx) - np.log10(px)
                            x0 = 10**(np.log10(x0)-_dx)
                            x1 = 10**(np.log10(x1)-_dx)
                        
                        ax.set_xlim([x0, x1])
                        redraw_needed = True
                        
                    #----------------------------------------------------------
                    if not self.modifiers[Qt.Key_Shift] :
                        if ax.yaxis.get_scale() == 'linear' :
                            dy = ny - py
                            y0 -= dy
                            y1 -= dy
                        elif ax.yaxis.get_scale() == 'log' :
                            _dy = np.log10(ny) - np.log10(py)
                            y0 = 10**(np.log10(y0)-_dy)
                            y1 = 10**(np.log10(y1)-_dy)
                        
                        ax.set_ylim([y0, y1])
                        redraw_needed = True
                        
            #------------------------------------------------------------------
            if redraw_needed :
                self._redraw()
            self.autoscale = False
            
    #==========================================================================
    def on_mouse_scroll(self, event) :
        #----------------------------------------------------------------------
        ax = event.inaxes
        if ax is None : return
        
        #----------------------------------------------------------------------
        f = 1.2
        F = 1/f if event.button == "up" else f
        
        aspect = ax.get_aspect()
        
        #----------------------------------------------------------------------
        if aspect == 1.0 or not self.modifiers[Qt.Key_Control] :
            x = event.xdata
            x0,x1 = ax.get_xlim()
            
            if ax.xaxis.get_scale() == 'linear' :
                x0 = x-(x-x0)*F
                x1 = x+(x1-x)*F
            elif ax.xaxis.get_scale() == 'log' :
                _x  = np.log10(x)
                x0 = 10**(_x-(_x-np.log10(x0))*F)
                x1 = 10**(_x+(np.log10(x1)-_x)*F)
                
            ax.set_xlim(x0,x1)
        
        #----------------------------------------------------------------------
        if aspect == 1.0 or not self.modifiers[Qt.Key_Shift] :
            y = event.ydata
            y0,y1 = ax.get_ylim()
            
            if ax.yaxis.get_scale() == 'linear' :
                y0 = y-(y-y0)*F
                y1 = y+(y1-y)*F
            elif ax.yaxis.get_scale() == 'log' :
                _y  = np.log10(y)
                y0 = 10**(_y-(_y-np.log10(y0))*F)
                y1 = 10**(_y+(np.log10(y1)-_y)*F)
                
            ax.set_ylim(y0, y1)
        
        #----------------------------------------------------------------------
        self.update_pointed(event)
        
        #----------------------------------------------------------------------
        self.canvas.draw()
        self.autoscale = False
        
    #==========================================================================
    def on_zoom_changed(self, x0,x1,y0,y1) :
       #----------------------------------------------------------------------
        self.ax.set_xlim([x0,x1])
        self.ax.set_ylim([y0,y1])
        self.autoscale = False
        self._redraw()
        
    #==========================================================================
    def set_forced_lim(self, axis, lims, update=False) :
        #----------------------------------------------------------------------
        self.f_lims[axis] = lims
        if update :
            if   axis == 'X' : self.ax.set_xlim(lims)
            elif axis == 'Y' : self.ax.set_ylim(lims)
            
    #==========================================================================
    def get_lims(self, axis) :
        #----------------------------------------------------------------------
        if   axis == 'X' : log = self.ax.xaxis.get_scale() == 'log'
        elif axis == 'Y' : log = self.ax.yaxis.get_scale() == 'log'
        
        #----------------------------------------------------------------------
        vmin,vmax = None,None
        #----------------------------------------------------------------------
        for ge in self.graph_elements :
            if ge.plotted is None : continue
            _vmin,_vmax = get_mpl_plotted_range(ge.plotted, axis)
            if vmin is None or (_vmin is not None and _vmin < vmin) : vmin = _vmin
            if vmax is None or (_vmax is not None and _vmax > vmax) : vmax = _vmax
        
        #----------------------------------------------------------------------
        if log and vmin <= 0 : vmin = 1e-5
        if log and vmax <= 0 : vmax = 1e5
            
        #----------------------------------------------------------------------
        return vmin,vmax
            
    #==========================================================================
    def set_lims(self, axis, lims) :
        #----------------------------------------------------------------------
        if axis == 'X' :
            log  = self.ax.xaxis.get_scale() == 'log'
            clim = self.ax.get_xlim()
            
        #----------------------------------------------------------------------
        elif axis == 'Y' :
            log  = self.ax.yaxis.get_scale() == 'log'
            clim = self.ax.get_ylim()
        
        #----------------------------------------------------------------------
        invert = self.invert[axis]
        margin = self.margin[axis]
        
        #----------------------------------------------------------------------
        d0,d1 = lims[:]
        if d0 is None : d0 = clim[0]
        if d1 is None : d1 = clim[1]
        if d0 > d1 : d0,d1 = d1,d0
        
        #----------------------------------------------------------------------
        if log :
            if np.isnan(d1) or np.isinf(d1) or d1 <= 0 : d1 = 1.0
            if np.isnan(d0) or np.isinf(d0) or d0 <= 0 : d0 = d1*1e-4
            dd = np.log10(d1) - np.log10(d0)
            d0 = 10**(np.log10(d0) - margin*dd)
            d1 = 10**(np.log10(d1) + margin*dd)
            
        #----------------------------------------------------------------------
        else :
            dd = d1 - d0
            d0 = d0 - margin*dd
            d1 = d1 + margin*dd
            
        #----------------------------------------------------------------------
        if invert : d0,d1 = d1,d0
        if clim == [d0,d1] : return False
        
        #----------------------------------------------------------------------
        if   axis == 'X' : self.ax.set_xlim([d0,d1])
        elif axis == 'Y' : self.ax.set_ylim([d0,d1])
        
        #----------------------------------------------------------------------
        return True
    
    #==========================================================================
    def update_pointed(self, event=None) :
        #----------------------------------------------------------------------
        if event is None : event = self.mv_event
        if event is None : return
        
        #----------------------------------------------------------------------
        str_xaxis = self.graph_config.dimensions[0]
        str_yaxis = 'Valeurs' if len(self.graph_config.dimensions) == 1 else self.graph_config.dimensions[1]
        
        #----------------------------------------------------------------------
        str_x = "{:.5G}".format(event.xdata) if event.xdata is not None else "-"
        str_y = "{:.5G}".format(event.ydata) if event.ydata is not None else "-"
        msg = "Position : {}={}, {}={}".format(str_xaxis, str_x, str_yaxis, str_y)
        
        #----------------------------------------------------------------------
        pointeds = []
        for ge in self.graph_elements :
            text = ge.update_pointed(event, pointeds=pointeds)
            if text is not None : msg += ", {}={}".format(ge.label,text)
            
            if ge.pointed is not None and ge.pointed.get_visible() :
                pointeds.append(ge.pointed)
                
        #----------------------------------------------------------------------
        self.mw.statusbar.showMessage(msg)
                
    #==========================================================================
    def _update_style(self) :
        #----------------------------------------------------------------------
        gs = self.style
        
        #---- title -----------------------------------------------------------
        if gs.get('title.is_active') : 
            S = gs.get('title.style')
            self.ax.set_title(gs.get('title.text'),
                              fontfamily=S['font_name'],
                              fontsize=S['font_size'], 
                              color=S['font_color'],
                              fontweight='bold' if S['font_bold'] else 'normal',
                              style='italic' if S['font_italic'] else 'normal',
                              )
        else : self.ax.set_title(None)
        
        
        #---- axis ------------------------------------------------------------
        for axis in ['xaxis','yaxis'] :
            if   axis == 'xaxis' : fct = self.ax.set_xlabel
            elif axis == 'yaxis' : fct = self.ax.set_ylabel
            
            if gs.get('axes.is_active') and gs.get(axis+'.is_active') and gs.get(axis+'.title.is_active') :
                S = gs.get(axis+'.title.style')
                fct(gs.get(axis+'.title.text'),
                    fontfamily=S['font_name'],
                    fontsize=S['font_size'],
                    color=S['font_color'],
                    fontweight='bold' if S['font_bold'] else 'normal',
                    style='italic' if S['font_italic'] else 'normal',
                    )
            else : fct(None)
            
            #---- axis ticks --------------------------------------------------
            tick_params = {'axis':axis[0]}
            if gs.get('axes.is_active') and gs.get(axis+'.is_active') and gs.get(axis+'.ticks.is_active') :
                S = gs.get(axis+'.ticks.style')
                N = gs.get(axis+'.ticks.decimals')
                fmt = "{"+"x:."+ str(N) + ['G','f','E'][Graph_Style.get_options('ticks.format').index(gs.get(axis+'.ticks.format'))] + "}"
                tick_params['length'] = 3
                tick_params['labelcolor'] = S['font_color']
                tick_params['color'] = S['font_color']
                font_prop = fm.FontProperties(family=S['font_name'],
                                              size=S['font_size'],
                                              style='italic' if S['font_italic'] else 'normal',
                                              weight='bold' if S['font_bold'] else 'normal',
                                              )
                
                if axis == 'xaxis' :
                    self.ax.xaxis.set_major_formatter(mticker.StrMethodFormatter(fmt))
                    tick_params['labelbottom'] = True
                    labels = self.ax.get_xticklabels()
                elif axis == 'yaxis' :
                    self.ax.yaxis.set_major_formatter(mticker.StrMethodFormatter(fmt))
                    tick_params['labelleft'] = True
                    labels = self.ax.get_yticklabels()
                    
                for label in labels : label.set_fontproperties(font_prop)
                
            else :
                tick_params['length'] = 0
                if   axis == 'xaxis' : tick_params['labelbottom'] = False
                elif axis == 'yaxis' : tick_params['labelleft']   = False
                
            self.ax.tick_params(**tick_params)
            
            
        #---- grid ------------------------------------------------------------
        if gs.get('grid.is_active') :
            S = gs.get('grid.style')
            self.ax.tick_params(axis='both', gridOn=True, grid_linewidth=S['line_width'], grid_linestyle=S['line_style'], grid_color=S['line_color'], grid_alpha=S['line_alpha'])
        else :
            self.ax.tick_params(axis='both', gridOn=False)
            
        #---- range -----------------------------------------------------------
        rescale = len([k for k in ['element.is_active',
                                   'xaxis.min.is_active','xaxis.min.text','xaxis.max.is_active','xaxis.max.text',
                                   'yaxis.min.is_active','yaxis.min.text','yaxis.max.is_active','yaxis.max.text']
                       if k in gs.changed]) > 0
        if rescale :
            self.rescale(ignore_autoscale=False)
            
    #==========================================================================
    def rescale(self, ignore_autoscale=True, redraw=False) :
        #----------------------------------------------------------------------
        if not self.autoscale and not ignore_autoscale :
            return
        
        #----------------------------------------------------------------------
        X,Y = [],[]
        for ge in self.graph_elements :
            if ge.plotted is None : continue
            if not ge.plotted.get_visible() : continue
            X += [ge.plotted.xmin,ge.plotted.xmax]
            Y += [ge.plotted.ymin,ge.plotted.ymax]
            
        #----------------------------------------------------------------------
        _X = [x for x in X if x is not None and ~np.isnan(x)]
        _Y = [y for y in Y if y is not None and ~np.isnan(y)]
        xmin,xmax,ymin,ymax = None,None,None,None
        
        #----------------------------------------------------------------------
        gs = self.style
        if gs.get('xaxis.min.is_active') : xmin = to_float(gs.get('xaxis.min.text'), None)
        if gs.get('xaxis.max.is_active') : xmax = to_float(gs.get('xaxis.max.text'), None)
        if gs.get('yaxis.min.is_active') : ymin = to_float(gs.get('yaxis.min.text'), None)
        if gs.get('yaxis.max.is_active') : ymax = to_float(gs.get('yaxis.max.text'), None)
        
        #----------------------------------------------------------------------
        add_margin = []
        if len(_X) > 0 :
            if xmin is None : xmin = np.nanmin(_X) ; add_margin.append('xmin')
            if xmax is None : xmax = np.nanmax(_X) ; add_margin.append('xmax')
        if len(_Y) > 0 :
            if ymin is None : ymin = np.nanmin(_Y) ; add_margin.append('ymin')
            if ymax is None : ymax = np.nanmax(_Y) ; add_margin.append('ymax')
        
        #----------------------------------------------------------------------
        if xmin is not None :
            delta = (xmax-xmin)*0.05
            if 'xmin' in add_margin : xmin = xmin-delta
            if 'xmax' in add_margin : xmax = xmax+delta
        else :
            xmin,xmax = 0.0,1.0
            
        #----------------------------------------------------------------------
        if ymin is not None :
            delta = (ymax-ymin)*0.05
            if 'ymin' in add_margin : ymin -= delta
            if 'ymax' in add_margin : ymax += delta
        else :
            ymin,ymax = 0.0,1.0
            
        #----------------------------------------------------------------------
        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)
        self.autoscale = True
        
        #----------------------------------------------------------------------
        if redraw :
            self._redraw()
            
    #==========================================================================
    def redraw(self, event=None, delay=200) :
        #----------------------------------------------------------------------
        self.redraw_timer.stop()
        self.redraw_timer.start(delay)
        
    #==========================================================================
    def _redraw(self, event=None) :
        #----------------------------------------------------------------------
        self.mw.set_busy(1)
        
        #----------------------------------------------------------------------
        cbars = []
        for ge in self.graph_elements :
            if ge.cbar is None : continue
            self.legend.update_cbar(ge)
            cbars.append(ge.cbar)
            
        #----------------------------------------------------------------------
        for cbar in cbars :
            try : cbar.fig.tight_layout(rect=(0,0.2,1,0.9))
            except : pass
        
        #----------------------------------------------------------------------
        self.canvas.draw()
        for cbar in cbars : cbar.ax.get_figure().canvas.draw()
        
        #----------------------------------------------------------------------
        if self.legend is not None :
            self.legend.redraw()
        
        #----------------------------------------------------------------------
        self.redraw_timer.stop()
        self.mw.set_busy(-1)
        
    #==========================================================================
    def _save_image(self, filepath) :
        #----------------------------------------------------------------------
        self.fig.savefig(filepath, transparent=False)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_MPL_1D(Graph_MPL) :
    
    #==========================================================================
    def __init__(self, page, graph_config, **kwargs) :
        #----------------------------------------------------------------------
        self.background_color = 'white'
        Graph_MPL.__init__(self, page, graph_config, **kwargs)
    
    #==========================================================================
    def __repr__(self) :
        #----------------------------------------------------------------------
        return "Graph_1D(id={},{})".format(self.index, self.graph_config.dimensions[0])
        
    #==========================================================================
    def _create_graph(self) :
        #----------------------------------------------------------------------
        widget = Graph_MPL._create_graph(self)
        
        #----------------------------------------------------------------------
        self.ax.set_xlabel(self.graph_config.dimensions[0])
        self.ax.set_ylabel('Valeurs')
            
        #----------------------------------------------------------------------
        return widget
    
    #==========================================================================
    def get_autocolor(self, ge) :
        #----------------------------------------------------------------------
        c_index = [_ge for _ge in ge.graph.graph_elements if type(_ge.element).__name__ in ['Constant','Matrix']].index(ge)
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        autocolor = colors[c_index%len(colors)]
            
        return autocolor
        
    #==========================================================================
    def _get_save_data(self) :
        #----------------------------------------------------------------------
        blocks = []
        
        for ge in self.graph_elements :
            data = ge.get_save_data()
            if data is None : continue
            
            #------------------------------------------------------------------
            axes = data['axes']
            
            #------------------------------------------------------------------
            found = False
            for block in blocks :
                if len(axes) != len(block['axes']) : continue
                if block['axes'] != axes : continue
                same_axes = True
                for ax in axes :
                    if len(block['values'][ax]) != len(data[ax]) or not (block['values'][ax] == data[ax]).all() :
                        same_axes = False
                        break
                if not same_axes : continue
                
                #--------------------------------------------------------------
                name = data['name']
                if name in block['variables'] :
                    i = 2
                    while "{}({})".format(name,i) in block['variables'] : i += 1
                    name = "{}({})".format(name,i)
                #--------------------------------------------------------------
                block['variables'].append(name)
                block['values'][name] = np.array(data['values'])
                block['infos'].append(data['infos'])
                found = True
                
            #------------------------------------------------------------------
            if not found :
                name = data['name']
                block = {}
                block['axes']      = axes
                block['dims']      = self.graph_config.dimensions
                block['variables'] = [name]
                block['values']    = {k:np.array(data[k]) for k in axes}
                block['values'][name] = np.array(data['values'])
                block['infos'] = [data['infos']]
                blocks.append(block)
                
        #----------------------------------------------------------------------
        sheet_name = 'P{}G{}'.format(self.page.index, self.index)
        return {sheet_name:blocks}
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_MPL_2D(Graph_MPL) :
    
    #==========================================================================
    def __init__(self, page, graph_config, **kwargs) :
        #----------------------------------------------------------------------
        self.background_color = 'lightgray'
        Graph_MPL.__init__(self, page, graph_config, **kwargs)
        
    #==========================================================================
    def __repr__(self) :
        #----------------------------------------------------------------------
        return "Graph_2D(id={},{}{})".format(self.index, self.graph_config.dimensions[0], self.graph_config.dimensions[1])
    
    #==========================================================================
    def _create_graph(self) :
        #----------------------------------------------------------------------
        widget = Graph_MPL._create_graph(self)
        
        #----------------------------------------------------------------------
        self.ax.set_xlabel(self.graph_config.dimensions[0])
        self.ax.set_ylabel(self.graph_config.dimensions[1])
            
        #----------------------------------------------------------------------
        return widget
    
    #==========================================================================
    def _get_save_data(self) :
        #----------------------------------------------------------------------
        all_blocks = {}
        
        #----------------------------------------------------------------------
        for ge in self.graph_elements :
            data = ge.get_save_data()
            if data is None : continue
            
            #------------------------------------------------------------------
            axes = [k for k in data.keys() if k not in ['values','name']]
            
            #------------------------------------------------------------------
            name = data['name']
            block = {}
            block['dims']      = self.graph_config.dimensions
            block['axes']      = axes
            block['variable']  = name
            block['values']    = {k:np.array(data[k]) for k in axes}
            block['values'][name] = np.array(data['values'])
            block['infos'] = [data['infos']]
            
            sheet_name = 'P{}G{}_{}'.format(self.page.index, self.index, data['infos']['beacon'])
            for c in ["'"] : sheet_name = sheet_name.replace(c,'')
            
            all_blocks[sheet_name] = [block]
            
        #----------------------------------------------------------------------
        return all_blocks
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


