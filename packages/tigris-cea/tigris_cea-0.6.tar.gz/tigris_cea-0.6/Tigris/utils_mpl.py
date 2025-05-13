# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
#------------------------------------------------------------------------------
from matplotlib.widgets import RectangleSelector
#------------------------------------------------------------------------------
from PyQt5.QtCore import QObject, pyqtSignal
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class RectSelector(RectangleSelector, QObject) :
    
    #==========================================================================
    zoneSelected = pyqtSignal(float,float,float,float) # x0,x1,y0,y1 = self.extents
    
    #==========================================================================
    def __init__(self, ax, buttons, color, linewidth=1, alpha=0.1, fill_x=False, fill_y=False) :
        """kwargs : color, linewidth, alpha"""
        #----------------------------------------------------------------------
        QObject.__init__(self)
        #----------------------------------------------------------------------
        self.ax = ax
        self.buttons = buttons
        #----------------------------------------------------------------------
        self.fill_x = fill_x
        self.fill_y = fill_y
        #----------------------------------------------------------------------
        RectangleSelector.__init__(self, ax, self.on_select, button=buttons, useblit=True, ignore_event_outside=False)
        #----------------------------------------------------------------------
        self.set_active(False)
        #----------------------------------------------------------------------
        rect = self.artists[0]
        rect.set_color(color)
        rect.set_edgecolor('black')
        rect.set_linewidth(linewidth)
        rect.set_alpha(alpha)
        
    #==========================================================================
    def _onmove(self, event) :
        pass
        
    #==========================================================================
    def set_active(self, state) :
        #----------------------------------------------------------------------
        self.is_active = state
        self.set_visible(state)
        if not state :
            self.update() # pour masquer
            self.infos = None
        
    #==========================================================================
    def on_move(self, event, fill_x=False, fill_y=False) :
        #----------------------------------------------------------------------
        if not self.is_active :
            return
    
        #----------------------------------------------------------------------
        if self.infos is None :
            X0,Y0,X1,Y1 = self.ax.bbox.extents # pixels
            (x0,x1),(y0,y1) = self.ax.get_xlim(), self.ax.get_ylim() # data
            self.infos = (X0,Y0,X1,Y1,x0,x1,y0,y1)
        else :
            X0,Y0,X1,Y1,x0,x1,y0,y1 = self.infos
            
        #----------------------------------------------------------------------
        _x0,_y0 = self._eventpress.xdata,self._eventpress.ydata
        _x1,_y1 = event.xdata,event.ydata
        
        if None in (_x1,_y1) :
            x,y = self.ax.transData.inverted().transform((event.x, event.y))
            
            if event.x < X0 : _x1 = x0 # left
            elif event.x > X1 : _x1= x1 # right
            else : _x1 = x # inside
            
            if event.y < Y0 : _y1 = y0 # left
            elif event.y > Y1 : _y1= y1 # right
            else : _y1 = y # inside
            
        if fill_x or self.fill_x : _x0,_x1 = x0,x1
        if fill_y or self.fill_y : _y0,_y1 = y0,y1
        
        #----------------------------------------------------------------------
        self.extents = _x0,_x1,_y0,_y1
        
    #==========================================================================
    def on_select(self, c_event, r_event) :
        #----------------------------------------------------------------------
        if not self.is_active : return False
        if (r_event.x-c_event.x)**2 + (r_event.y-c_event.y)**2 < 10**2 : return False
        #----------------------------------------------------------------------
        x0,x1,y0,y1 = self.extents
        self.zoneSelected.emit(x0,x1,y0,y1)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_mpl_plotted_range(e, axis) :
    #--------------------------------------------------------------------------
    if e is None : return None,None
    
    #--------------------------------------------------------------------------
    etype = type(e).__name__
    if not e.get_visible() : return None,None
    
    #--------------------------------------------------------------------------
    values = None
    #--------------------------------------------------------------------------
    tr = e.get_transform()
    if type(tr).__name__ == 'BlendedGenericTransform' :
        if   axis == 'X' and type(tr._x).__name__ == 'BboxTransformTo' : return None,None
        elif axis == 'Y' and type(tr._y).__name__ == 'BboxTransformTo' : return None,None
        
    #--------------------------------------------------------------------------
    if etype == 'Line2D' :
        if   axis == 'X' : values = e.get_xdata()
        elif axis == 'Y' : values = e.get_ydata()
    #--------------------------------------------------------------------------
    elif etype == 'LineCollection' :
        if   axis == 'X' : values = np.array([seg[:,0] for seg in e.get_segments()])
        elif axis == 'Y' : values = np.array([seg[:,1] for seg in e.get_segments()])
    #--------------------------------------------------------------------------
    elif etype == 'PolyCollection' :
        values = []
        for p in e.get_paths() :
            if   axis == 'X' : values += [v[0] for v in p.vertices]
            elif axis == 'Y' : values += [v[1] for v in p.vertices]
    #--------------------------------------------------------------------------
    elif etype == 'QuadMesh' :
        coords = e.get_coordinates()
        if   axis == 'X' : values = coords[0,:,0]
        elif axis == 'Y' : values = coords[:,0,1]
    #--------------------------------------------------------------------------
    elif etype == 'Polygon' :
        if   axis == 'X' : values = e.get_xy()[:,0]
        elif axis == 'Y' : values = e.get_xy()[:,1]
    #--------------------------------------------------------------------------
    elif etype == 'Rectangle' :
        if   axis == 'X' : values = [e.get_x(), e.get_x() + e.get_width()]
        elif axis == 'Y' : values = [e.get_y(), e.get_y() + e.get_height()]
        
    #--------------------------------------------------------------------------
    if values is None :
        raise Exception("type '{}' not implemented".format(etype))
        
    #--------------------------------------------------------------------------
    if len(values) == 0 :
        return None,None
    
    #--------------------------------------------------------------------------
    vmin,vmax = np.nanmin(values), np.nanmax(values)
    if np.isnan(vmin) or np.isnan(vmax) : return None,None
    
    #--------------------------------------------------------------------------
    return vmin,vmax

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
