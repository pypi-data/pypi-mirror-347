# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import numpy as np
#------------------------------------------------------------------------------
from PyQt5 import uic
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter, QPen
#------------------------------------------------------------------------------
from Graph import new_graph
from utils_qt import ResizableGrid, question_box
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Page_Config :

    #==========================================================================
    def get_configs() :
        #----------------------------------------------------------------------
        configs = []
        #----------------------------------------------------------------------
        configs.append(Page_Config([[1]]))
        #----------------------------------------------------------------------
        configs.append(Page_Config([[1,2]]))
        configs.append(Page_Config([[1],[2]]))
        #----------------------------------------------------------------------
        configs.append(Page_Config([[1,2,3]]))
        configs.append(Page_Config([[1],[2],[3]]))
        configs.append(Page_Config([[1,1],[2,3]]))
        configs.append(Page_Config([[1,2],[1,3]]))
        #----------------------------------------------------------------------
        configs.append(Page_Config([[1,2],[3,4]]))
        configs.append(Page_Config([[1,2,3,4]]))
        configs.append(Page_Config([[1],[2],[3],[4]]))
        configs.append(Page_Config([[1,1,1],[2,3,4]]))
        configs.append(Page_Config([[1,2],[1,3],[1,4]]))
        #----------------------------------------------------------------------
        configs.append(Page_Config([[1,2,3,4,5]]))
        configs.append(Page_Config([[1],[2],[3],[4],[5]]))
        configs.append(Page_Config([[1,1,1,1],[2,3,4,5]]))
        configs.append(Page_Config([[1,2],[1,3],[1,4],[1,5]]))
        configs.append(Page_Config([[1,1,1,2,2,2],[3,3,4,4,5,5]]))
        configs.append(Page_Config([[1,3],[1,3],[1,4],[2,4],[2,5],[2,5]]))
        #----------------------------------------------------------------------
        configs.append(Page_Config([[1,1,2],[1,1,3],[4,5,6]]))
        configs.append(Page_Config([[1,4],[2,5],[3,6]]))
        configs.append(Page_Config([[1,2,3],[4,5,6]]))

        #----------------------------------------------------------------------
        for c1,config1 in enumerate(configs) :
            _to_rename = None
            for c2,config2 in enumerate(configs[c1+1:], start=c1+1) :
                if config2.N == config1.N and config2.name == config1.name :
                    if _to_rename is None : _to_rename = [c1]
                    _to_rename.append(c2)
            if _to_rename is not None :
                for c,_c in enumerate(_to_rename) :
                    suffix = chr(ord('a')+c)
                    configs[_c].name += suffix

        #----------------------------------------------------------------------
        return configs

    #==========================================================================
    def __init__(self, A) :
        #----------------------------------------------------------------------
        self.A  = np.array(A)
        self.update_parameters()
        
    #==========================================================================
    def copy(self) :
        #----------------------------------------------------------------------
        return Page_Config(np.array(self.A, copy=True))
    
    #==========================================================================
    def update_parameters(self) :
        #----------------------------------------------------------------------
        self.N  = len(np.unique(self.A))
        self.NR = self.A.shape[0]
        self.NC = self.A.shape[1]
        #----------------------------------------------------------------------
        self.name = "{}x{}".format(self.NR,self.NC)
        self.icon = self.get_config_icon()
        #----------------------------------------------------------------------
        self.grid_indices = []
        for g in np.unique(self.A) :
            I = np.where(self.A==g)
            self.grid_indices.append((np.min(I[0]), np.min(I[1]), np.max(I[0]), np.max(I[1])))
            
    #==========================================================================
    def insert(self, g, side) :
        #----------------------------------------------------------------------
        r0,c0,r1,c1 = self.grid_indices[g]
        r1 += 1
        c1 += 1
        dc = c1-c0
        dr = r1-r0
        G = self.A[r0,c0]
        _G = self.N+1
        
        #----------------------------------------------------------------------
        if side in ['right','left'] :
            P1 = self.A[:,0:c0].reshape(self.NR,c0)
            P3 = self.A[:,c1:].reshape(self.NR,self.NC-c1)
            if dc == 1 :
                P2 = self.A[:,c0:c1].reshape(self.NR,c1-c0)
                P4 = np.array(P2)
            else :
                if dc%2 == 0 : cm = c0 + int(dc/2)
                else         : cm = c0 + int(dc/2)+1
                P2 = self.A[:,c0:cm].reshape(self.NR,cm-c0)
                P4 = self.A[:,cm:c1].reshape(self.NR,c1-cm)
            P4[np.where(P4==G)] = _G
            if   side == 'right' : subs = (P1,P2,P4,P3)
            elif side == 'left'  : subs = (P1,P4,P2,P3)
            self.A = np.hstack(subs)
            
        #----------------------------------------------------------------------
        elif side in ['top','bottom'] :
            P1 = self.A[0:r0,:].reshape(r0, self.NC)
            P3 = self.A[r1:,:].reshape(self.NR-r1, self.NC)
            if dr == 1 :
                P2 = self.A[r0:r1,:].reshape(r1-r0, self.NC)
                P4 = np.array(P2)
            else :
                if dr%2 == 0 : rm = r0 + int(dr/2)
                else         : rm = r0 + int(dr/2)+1
                P2 = self.A[r0:rm,:].reshape(rm-r0, self.NC)
                P4 = self.A[rm:r1,:].reshape(r1-rm, self.NC)
            P4[np.where(P4==G)] = _G
            if   side == 'bottom' : subs = (P1,P2,P4,P3)
            elif side == 'top'    : subs = (P1,P4,P2,P3)
            self.A = np.vstack(subs)
                
        #----------------------------------------------------------------------
        self.update_parameters()
        
    #==========================================================================
    def remove(self, g, side) :
        #----------------------------------------------------------------------
        r0,c0,r1,c1 = self.grid_indices[g]
        r1 += 1
        c1 += 1
        G = self.A[r0,c0]
        
        #----------------------------------------------------------------------
        if side in ['right','left'] :
            P1 = self.A[:,0:c0].reshape(self.NR,c0)
            P2 = self.A[:,c0:c1].reshape(self.NR,c1-c0)
            P3 = self.A[:,c1:].reshape(self.NR,self.NC-c1)
            
            for i in range(P2.shape[0]) :
                if   side == 'right' : _G = self.A[i,c0-1]
                elif side == 'left'  : _G = self.A[i,c1]
                for j in range(P2.shape[1]) :
                    if P2[i,j] == G : P2[i,j] = _G
            self.A = np.hstack((P1,P2,P3))
            
        #----------------------------------------------------------------------
        elif side in ['top','bottom'] :
            P1 = self.A[0:r0,:].reshape(r0, self.NC)
            P2 = self.A[r0:r1,:].reshape(r1-r0, self.NC)
            P3 = self.A[r1:,:].reshape(self.NR-r1, self.NC)
            
            for j in range(P2.shape[1]) :
                if   side == 'bottom' : _G = self.A[r0-1,j]
                elif side == 'top'    : _G = self.A[r1,j]
                for i in range(P2.shape[0]) :
                    if P2[i,j] == G : P2[i,j] = _G
            self.A = np.vstack((P1,P2,P3))
                
        #----------------------------------------------------------------------
        I = np.where(self.A >= G)
        self.A[I] -= 1
        
        self.update_parameters()
        
    #==========================================================================
    def get_config_icon(self) :
        #----------------------------------------------------------------------
        b = 1
        S = 3*4*5
        X = [int(b+i*(S-2*b)/self.A.shape[1]) for i in range(self.A.shape[1]+1)]
        Y = [int(b+i*(S-2*b)/self.A.shape[0]) for i in range(self.A.shape[0]+1)]
        #----------------------------------------------------------------------
        pixmap = QPixmap(S,S)
        pixmap.fill(QColor('black'))
        painter = QPainter(pixmap)
        painter.setBrush(QColor('white'))
        pen = QPen(QColor("black"))
        pen.setWidth(b)
        painter.setPen(pen)
        #----------------------------------------------------------------------
        for g in np.unique(self.A) :
            I = np.where(self.A==g)
            x0,x1 = X[np.min(I[1])], X[np.max(I[1])+1]
            y0,y1 = Y[np.min(I[0])], Y[np.max(I[0])+1]
            painter.drawRect(x0, y0, x1-x0, y1-y0)
        painter.end()
        #----------------------------------------------------------------------
        return QIcon(pixmap)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Page(QWidget) :

    #==========================================================================
    INDEX = 1

    #==========================================================================
    def __init__(self, pm, name, page_config, graph_configs) :
        #----------------------------------------------------------------------
        self.index = Page.INDEX
        Page.INDEX += 1

        #----------------------------------------------------------------------
        self.pm = pm
        self.mw = self.pm.mw
        
        #----------------------------------------------------------------------
        QWidget.__init__(self)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        #----------------------------------------------------------------------
        self.default_name = "Page_{}".format(self.index)
        if name is None : self.name = "Page_{}".format(self.index)
        else : self.name = name
        
        self.page_config = page_config.copy()
        self.graph_configs = graph_configs
        self.tool_bar_height = 24
        
        #----------------------------------------------------------------------
        self.resizable_grid = None
        self.graphs = None
        
        #----------------------------------------------------------------------
        self.load_ui()
        
    #==========================================================================
    def set_name(self, new_name) :
        #----------------------------------------------------------------------
        self.name = new_name

        #----------------------------------------------------------------------
        index = self.pm.get_index(self)
        self.pm.tab_widget.setTabText(index, self.name)
        
    #==========================================================================
    def load_ui(self) :
        #----------------------------------------------------------------------
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), "UI", "Page.ui"), self)
        
    #==========================================================================
    def can_remove(self, graph, side) :
        #----------------------------------------------------------------------
        g = self.graphs.index(graph)
        r0,c0,r1,c1 = self.page_config.grid_indices[g]
        for e,(_r0,_c0,_r1,_c1) in enumerate(self.page_config.grid_indices) :
            if e == g : continue
            if side == 'right'  and c0 == _c1+1 and r0 == _r0 and r1 == _r1 : return True
            if side == 'left'   and c1+1 == _c0 and r0 == _r0 and r1 == _r1 : return True
            if side == 'bottom' and c0 == _c0 and c1 == _c1 and r0 == _r1+1 : return True
            if side == 'top'    and c0 == _c0 and c1 == _c1 and r1+1 == _r0 : return True
        #----------------------------------------------------------------------
        return False
    
    #==========================================================================
    def place_graphs(self) :
        #----------------------------------------------------------------------
        self.graphs = []
        for e,(r0,c0,r1,c1) in enumerate(self.page_config.grid_indices) :
            graph = new_graph(self, self.graph_configs[e])
            self.graphs.append(graph)
            
        #----------------------------------------------------------------------
        self.resizable_grid = ResizableGrid()
        for e,(r0,c0,r1,c1) in enumerate(self.page_config.grid_indices) :
            self.resizable_grid.add_widget(self.graphs[e], r0,c0,r1,c1)
            
        #----------------------------------------------------------------------
        self.resizable_grid.add_to_layout(self.main_layout)
        
    #==========================================================================
    def insert_graph(self, on_graph, side, gc) :
        #----------------------------------------------------------------------
        g = self.graphs.index(on_graph)
        self.page_config.insert(g, side)
        
        #----------------------------------------------------------------------
        _graph = new_graph(self, gc)
        self.graphs.append(_graph)
        
        #----------------------------------------------------------------------
        self.on_graph_changed()
        
        _graph.update_graph()
        
    #==========================================================================
    def remove_graph(self, graph, side) :
        #----------------------------------------------------------------------
        g = self.graphs.index(graph)
        self.page_config.remove(g, side)
        
        #----------------------------------------------------------------------
        graph.remove_graph()
        self.graphs.remove(graph)
        
        self.update_parameters()
        #----------------------------------------------------------------------
        self.on_graph_changed()
        
    #==========================================================================
    def on_graph_changed(self) :
        #----------------------------------------------------------------------
        self.resizable_grid.reset()
        
        #----------------------------------------------------------------------
        for e,(r0,c0,r1,c1) in enumerate(self.page_config.grid_indices) :
            self.resizable_grid.add_widget(self.graphs[e], r0,c0,r1,c1)
            
        #----------------------------------------------------------------------
        self.resizable_grid.add_to_layout(self.main_layout)
        self.resizable_grid.reset_sizes()
        
        QApplication.processEvents()
    
    #==========================================================================
    def update_page_config(self, name, page_config, graph_configs) :
        #----------------------------------------------------------------------
        if name != self.name :
            self.set_name(name)
        
        #----------------------------------------------------------------------
        for e,gc in enumerate(graph_configs) :
            self.convert_graph(gc, index=e)
    
    #==========================================================================
    def get_graph_index(self, graph) :
        #----------------------------------------------------------------------
        for e,g in enumerate(self.graphs) :
            if g == graph :
                return e
        return None
    
    #==========================================================================
    def convert_graph(self, gc, graph=None, index=None) :
        #----------------------------------------------------------------------
        if graph is None : graph = self.graphs[index]
        if index is None : index = self.get_graph_index(graph)
        
        #----------------------------------------------------------------------
        if graph.graph_config.name == gc.name :
            return
        
        #----------------------------------------------------------------------
        _graph = new_graph(self, gc, index=graph.index)
        self.graphs[index] = _graph
        self.resizable_grid.replace_widget(graph, _graph)
        
        #----------------------------------------------------------------------
        for ge in graph.graph_elements :
            _graph.add_element(graph_element=ge, update=False)
        
        #----------------------------------------------------------------------
        graph.remove_graph()
        
        #----------------------------------------------------------------------
        skip = [k for k in graph.style.items.keys() if k.split(".")[0] in ['xaxis','yaxis','zaxis']]
        skip.append('title.style')
        _graph.style.update_from(graph.style, skip=skip)
        _graph.autoscale = True
        _graph.update_graph()
        _graph.update_style()
        
    #==========================================================================
    def update_parameters(self) :
        #----------------------------------------------------------------------
        self.mw.parameters_manager.update_items(self)
        
    #==========================================================================
    def redraw(self) :
        #----------------------------------------------------------------------
        self.mw.set_busy(1)
        for graph in self.graphs : graph.redraw()
        self.mw.set_busy(-1)
        
    #==========================================================================
    def save_image(self, filepath=None) :
        #----------------------------------------------------------------------
        print("> Sauvegarde de la page '{}' ... ".format(self.name), end="", flush=True)
        
        #----------------------------------------------------------------------
        if filepath is None :
            defaultname = "{}.png".format(self.name)
            if len(self.mw.files_manager.files) == 1 : defaultname = os.path.join(os.path.dirname(self.mw.files_manager.files[0].nc_path), defaultname)
            filepath,_ = QFileDialog.getSaveFileName(self, "Enregistrer sous", defaultname, "Tous les fichiers (*);;Images PNG (*.png)", "Images PNG (*.png)")
        
        #----------------------------------------------------------------------
        if filepath == '' :
            print("annulé")
            return
        
        self.mw.set_busy(1)
        
        #----------------------------------------------------------------------
        H0 = min([graph.mapTo(self, QPoint(0, 0)).y() for graph in self.graphs])
        W = self.width()
        H = self.height() - H0
        
        #----------------------------------------------------------------------
        pixmap = QPixmap(W, H)
        pixmap.fill(Qt.transparent)
        
        #----------------------------------------------------------------------
        painter = QPainter(pixmap)
        for g,graph in enumerate(self.graphs) :
            temp_path = filepath.replace(".png", "_{}.png".format(g+1))
            graph.save_image(temp_path, multi=True)
            _pixmap = QPixmap(temp_path)
            pos = graph.mapTo(self, QPoint(0, 0))
            painter.drawPixmap(pos.x(), pos.y()-H0, _pixmap)
            os.remove(temp_path)
        painter.end()
        
        #----------------------------------------------------------------------
        pixmap.save(filepath, "PNG")
        print("OK")
        self.mw.set_busy(-1)
        
        #----------------------------------------------------------------------
        rep = question_box('question', "Sauvegarde terminée", "La sauvegarde de l'image est terminée !", buttons=[('Yes','OK','check'), ('No','Ouvrir','image')])
        if rep == 'No' : os.startfile(filepath)
        
    #==========================================================================
    def save_data(self, filepath=None) :
        #----------------------------------------------------------------------
        self.pm.save_data(filepath=filepath, page=self)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




