# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------
from Style import Style
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** GRAPHS ***
#==============================================================================
class Graph_Style(Style) :
    
    #==========================================================================
    def get_options(k, graph=None) :
        #----------------------------------------------------------------------
        if k == 'ticks.format' : return ['Auto','Normal','Scientifique']
        elif k == 'legend.pos' : 
            values = []
            values.append('Auto')
            values.append('Droite')
            values.append('Haut Droite')
            values.append('Haut')
            values.append('Haut Gauche')
            values.append('Gauche')
            values.append('Bas Gauche')
            values.append('Bas')
            values.append('Bas Droite')
            values.append('Droite (Ext.)')
            values.append('Gauche (Ext.)')
            return values
        #----------------------------------------------------------------------
        return None
        
    #==========================================================================
    def __init__(self, graph) :
        #----------------------------------------------------------------------
        self.graph = graph
        
        #----------------------------------------------------------------------
        Style.__init__(self)
    
    #==========================================================================
    def init_defaults(self) :
        #----------------------------------------------------------------------
        self.set('title.is_active'   , True)
        self.set('title.text'        , self.graph.name)
        self.set('title.default_text', self.graph.name)
        
        #----------------------------------------------------------------------
        self.set('legend.is_active', True)
        self.set('legend.pos'      , 'Auto')
        
        self.set('axes.is_active',True)
        
        #----------------------------------------------------------------------
        self._init_defaults()
    
    #==========================================================================
    def _init_defaults(self) :
        pass
    
    #==========================================================================
    def _update(self, redraw=False) :
        #----------------------------------------------------------------------
        self.graph.update_style(redraw=redraw)
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_MPL_Style(Graph_Style) :
        
    #==========================================================================
    def _init_defaults(self) :
        #----------------------------------------------------------------------
        self.set('title.style'       , {'font_name':'Arial', 'font_size':12, 'font_color':'black', 'font_bold':True, 'font_italic':False}) # font_style
        
        #---- axis ------------------------------------------------------------
        for axis in ['xaxis','yaxis'] :
            self.set(axis+'.is_active', True)
            self.set(axis+'.name', {'xaxis':'Abcisses', 'yaxis':'Ordonnées'}[axis])
            
            if   axis == 'xaxis' : title = self.graph.graph_config.dimensions[0]
            elif axis == 'yaxis' and len(self.graph.graph_config.dimensions) > 1 : title = self.graph.graph_config.dimensions[1]
            else : title = 'Valeurs'
            
            self.set(axis+'.title.is_active', True)
            self.set(axis+'.title.text'        , title)
            self.set(axis+'.title.default_text', title)
            self.set(axis+'.title.style', {'font_name':'Arial', 'font_size':10, 'font_color':'black', 'font_bold':True, 'font_italic':False})
            
            self.set(axis+'.ticks.is_active', True)
            self.set(axis+'.ticks.format', Graph_Style.get_options('ticks.format')[0])
            self.set(axis+'.ticks.decimals', 3)
            self.set(axis+'.ticks.style', {'font_name':'Arial', 'font_size':10, 'font_color':'black', 'font_bold':False, 'font_italic':False})
            
            self.set(axis+'.line.is_active', True)
            self.set(axis+'.line.style', {'line_width':1, 'line_color':'black', 'line_alpha':1}) # line_style inchangeable
            
            #------------------------------------------------------------------
            self.set(axis+'.min.is_active', False)
            self.set(axis+'.max.is_active', False)
            self.set(axis+'.min.text', '')
            self.set(axis+'.max.text', '')
        
        #---- grid ------------------------------------------------------------
        self.set('grid.is_active', True)
        self.set('grid.style', {'line_width':0.5, 'line_style':'--', 'line_color':'gray', 'line_alpha':0.5})
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_VTK_Style(Graph_Style) :
    
    #==========================================================================
    def _init_defaults(self) :
        #----------------------------------------------------------------------
        self.set('title.style'       , {'font_name':'Arial', 'font_size':12, 'font_color':'white', 'font_bold':True, 'font_italic':False}) # font_style
        
        #---- axis ------------------------------------------------------------
        for axis in ['xaxis','yaxis','zaxis'] :
            name = {'xaxis':'X', 'yaxis':'Y', 'zaxis':'Z'}[axis]
            
            self.set(axis+'.is_active', True)
            self.set(axis+'.name', name)
            
            color = 'white'
            self.set(axis+'.title.is_active', True)
            self.set(axis+'.title.text'        , name)
            self.set(axis+'.title.default_text', name)
            self.set(axis+'.title.style', {'font_name':'Arial', 'font_size':10, 'font_color':color, 'font_bold':True, 'font_italic':False})
            
            self.set(axis+'.ticks.is_active', False)
            self.set(axis+'.ticks.format', Graph_Style.get_options('ticks.format')[0])
            self.set(axis+'.ticks.decimals', 3)
            self.set(axis+'.ticks.style', {'font_name':'Arial', 'font_size':10, 'font_color':color, 'font_bold':False, 'font_italic':False})
            
            self.set(axis+'.line.is_active', True)
            self.set(axis+'.line.style', {'line_width':2, 'line_color':color, 'line_alpha':1}) # line_style inchangeable
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
