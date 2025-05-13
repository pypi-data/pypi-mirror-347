# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------
from PyQt5.QtWidgets import QWidget, QHBoxLayout
#------------------------------------------------------------------------------
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mticker
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Legend(QWidget) :
    
    #==========================================================================
    def __init__(self, graph) :
        #----------------------------------------------------------------------
        self.graph = graph
        
        #----------------------------------------------------------------------
        QWidget.__init__(self)
        
        #----------------------------------------------------------------------
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        #----------------------------------------------------------------------
        self.fig = Figure(facecolor='none', tight_layout=(0,0,1,1))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.axis('off')
        self.layout.addWidget(self.canvas)
        self.legend = None
        
        #----------------------------------------------------------------------
        self.cbars = {} # [ge.index] = cbar
        
        #----------------------------------------------------------------------
        self.update_main_size()
        
    #==========================================================================
    def get_figs(self) :
        #----------------------------------------------------------------------
        figs = []
        
        if self.legend is not None : figs.append(self.fig)
        for i,cbar in sorted(self.cbars.items()) : figs.append(cbar.ax.get_figure())
        
        return figs
        
    #==========================================================================
    def update(self) :
        #----------------------------------------------------------------------
        state = self.graph.style.get('legend.is_active')
        self.setVisible(state)
        if self.legend is not None : 
            self.legend.set_visible(state)
        
        #----------------------------------------------------------------------
        self.update_plotteds()
            
    #==========================================================================
    def update_plotteds(self) :
        #----------------------------------------------------------------------
        ge_ids = []
        handles = []
        labels = []
        
        #----------------------------------------------------------------------
        if self.legend is not None : 
            self.legend.remove()
        
        #----------------------------------------------------------------------
        for ge in self.graph.graph_elements :
            ge_id = (ge.element.index,ge.opts.get('field'))
            _leg = ge.get_legend()
            if _leg is not None :
                ge_ids.append(ge_id)
                handles.append(_leg['handle'])
                labels.append(_leg['label'])
                
        for ge in self.graph.graph_elements :
            _lleg = ge.get_linked_legend()
            if _lleg is not None :
                for index,(handle,label) in _lleg.items() :
                    if index in ge_ids : continue
                    ge_ids.append(index)
                    handles.append(handle)
                    labels.append(label)
    
        #----------------------------------------------------------------------
        if len(handles) > 0 :
            pos = self.graph.style.get('legend.pos')
            
            if self.graph.engine == 'VTK' and '(Ext.)' not in pos :
                pos = 'Gauche (Ext.)' if 'Gauche' in pos else 'Droite (Ext.)'
                
            if '(Ext.)' in pos :
                self.legend = self.ax.legend(handles=handles, labels=labels, loc='center', bbox_to_anchor=(0.5,0.5))
                self.canvas.setVisible(True)
                
            else :
                loc = {'Auto':'best',
                       'Droite':'center right',
                       'Haut Droite':'upper right',
                       'Haut':'upper center',
                       'Haut Gauche':'upper left',
                       'Gauche':'center left',
                       'Bas Gauche':'lower left',
                       'Bas':'lower center',
                       'Bas Droite':'lower right'}[pos]
                
                self.legend = self.graph.ax.legend(handles=handles, labels=labels, loc=loc)
                self.canvas.setVisible(False)
                
        else :
            self.canvas.setVisible(False)
            self.legend = None
            
        #----------------------------------------------------------------------
        self.update_main_size()
        
    #==========================================================================
    def update_main_size(self) :
        #----------------------------------------------------------------------
        pos = self.graph.style.get('legend.pos')
        if '(Ext.)' in pos :
        
            W = 0
            if self.legend is not None : W = int(self.legend.get_window_extent(renderer=self.fig.canvas.get_renderer()).width)+10
            self.canvas.setMinimumWidth(W)
            self.canvas.setMaximumWidth(W)
            # self.canvas.setMinimumHeight(0)
            # self.canvas.setMaximumHeight(self.graph.height())
        else :
            self.canvas.setMinimumWidth(0)
            self.canvas.setMaximumWidth(0)
        
        #----------------------------------------------------------------------
        self.redraw()
        
    #==========================================================================
    def set_main_visible(self, state) :
        #----------------------------------------------------------------------
        # if state == self.isVisible() : return
        self.setVisible(state)
        if self.legend is not None :
            self.legend.setVisible(state)
        
    #==========================================================================
    def remove(self) :
        #----------------------------------------------------------------------
        if self.legend is not None : 
            self.legend.remove()
            
        #----------------------------------------------------------------------
        self.canvas.deleteLater()
        self.deleteLater()
        
    #==========================================================================
    def redraw(self) :
        self.canvas.draw()
        
    #==========================================================================
    def add_cbar(self, ge) :
        #----------------------------------------------------------------------
        fig = Figure(facecolor='none', tight_layout=(0,0.2,0,0.7))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(1, 1, 1)
        
        #----------------------------------------------------------------------
        # cbar = None
        if self.graph.engine == "MPL" :
            mappable = ge.plotted.plotted
            
        else :
            cmap = plt.get_cmap('gist_rainbow')
            norm = mpl.colors.Normalize(vmin=ge.element.vmin, vmax=ge.element.vmax)
            mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
            
            # ge.plotted.configure(mappable=mappable)
        
        cbar = fig.colorbar(mappable, cax=ax, orientation='vertical')
        cbar.set_label(ge.label, loc='center', rotation=-90, labelpad=15)
        cbar.formatter = mticker.StrMethodFormatter('{x:.5G}')
        #----------------------------------------------------------------------
        self.layout.addWidget(canvas)
        
        #----------------------------------------------------------------------
        self.cbars[ge.index] = cbar
        return cbar
        
    #==========================================================================
    def update_cbar(self, ge) :
        #----------------------------------------------------------------------
        cbar = self.cbars.get(ge.index)
        if cbar is None : return
        
        #----------------------------------------------------------------------
        ggs = self.graph.style
        gs = ge.style
        
        #----------------------------------------------------------------------
        canvas = cbar.ax.get_figure().canvas
        visible = ggs.get('legend.is_active') and gs.get('element.is_active') and gs.get('legend.is_active')
        cbar.set_label(gs.get('legend.text'))
        cbar.formatter = mticker.StrMethodFormatter('{x:.5G}')
        
        #----------------------------------------------------------------------
        W = int(max([t.get_window_extent(renderer=canvas.get_renderer()).width for t in cbar.ax.get_yticklabels()]) + 85)
        canvas.setMinimumWidth(W)
        canvas.setMaximumWidth(W)
        canvas.setVisible(visible)
        
        canvas.draw()
        
    #==========================================================================
    def remove_cbar(self, ge) :
        #----------------------------------------------------------------------
        canvas = self.cbars[ge.index].ax.get_figure().canvas
        canvas.setVisible(False)
        canvas.deleteLater()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


