# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
#------------------------------------------------------------------------------
import warnings
warnings.filterwarnings("ignore")
#------------------------------------------------------------------------------
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QCursor
from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy, QFileDialog, QMenu
#------------------------------------------------------------------------------
from Element_Constants import Constant, Vector, Mesh
from Element_Matrix import Matrix
from Element_Cuboids import Cuboid, PolyCuboid
from Graph_Element import new_graph_element
from Graph_Legend import Graph_Legend
from utils_qt import get_icon, question_box
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** GRAPH FUNCTIONS ***
#==============================================================================
def new_graph(page, graph_config, **kwargs) :
    #--------------------------------------------------------------------------
    if graph_config.gtype in ['1D','2D'] :
        from Graph_MPL import new_graph as new_graph_MPL
        return new_graph_MPL(page, graph_config, **kwargs)
    #--------------------------------------------------------------------------
    elif graph_config.gtype in ['3D'] :
        from Graph_VTK import new_graph as new_graph_VTK
        return new_graph_VTK(page, graph_config, **kwargs)
    #--------------------------------------------------------------------------
    return Graph(page, graph_config, **kwargs)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph_Config :
    
    #==========================================================================
    def get_configs() :
        #----------------------------------------------------------------------
        configs = []
        #----------------------------------------------------------------------
        configs.append(Graph_Config('1D', ['X']))
        configs.append(Graph_Config('1D', ['Y']))
        configs.append(Graph_Config('1D', ['Z']))
        configs.append(Graph_Config('1D', ['T']))
        #----------------------------------------------------------------------
        configs.append(Graph_Config('2D', ['X','Y']))
        configs.append(Graph_Config('2D', ['X','Z']))
        configs.append(Graph_Config('2D', ['X','T']))
        configs.append(Graph_Config('2D', ['Y','X']))
        configs.append(Graph_Config('2D', ['Y','Z']))
        configs.append(Graph_Config('2D', ['Y','T']))
        configs.append(Graph_Config('2D', ['Z','X']))
        configs.append(Graph_Config('2D', ['Z','Y']))
        configs.append(Graph_Config('2D', ['Z','T']))
        configs.append(Graph_Config('2D', ['T','X']))
        configs.append(Graph_Config('2D', ['T','Y']))
        configs.append(Graph_Config('2D', ['T','Z']))
        #----------------------------------------------------------------------
        configs.append(Graph_Config('3D', ['X','Y','Z']))
        #----------------------------------------------------------------------
        return configs
        
    #==========================================================================
    def add_to_menu(menu, pm=None, graph=None, mode=None, side=None) :
        #----------------------------------------------------------------------
        gcs = {}
        for i,gc in enumerate(Graph_Config.get_configs()) :
            if gc.gtype not in gcs.keys() : gcs[gc.gtype] = []
            gcs[gc.gtype].append(gc)
        
        #----------------------------------------------------------------------
        if   graph is not None : mw = graph.mw
        elif pm is not None : mw = pm.mw
        
        #----------------------------------------------------------------------
        for gtype in sorted(gcs.keys()) :
            menu_gtype = QMenu("{}".format(gtype), mw)
            menu_gtype.setIcon(get_icon(gtype))
            
            for g,gc in enumerate(gcs[gtype]) :
                if g > 0 and len(gc.dimensions) > 1 and gcs[gtype][g-1].dimensions[0] != gc.dimensions[0] : menu_gtype.addSeparator()
                
                text = gc.name
                if graph is not None and mode == 'convert' :
                    n = len([ge for ge in graph.graph_elements if gc.can_plot(ge.element)])
                    if n == 0 : n = "-"
                    text = "{} ({})".format(gc.name, n)
                    
                action = menu_gtype.addAction(gc.get_icon(), text)
                
                if graph is not None :
                    if mode == 'convert' :
                        action.setEnabled(graph.graph_config != gc)
                        action.triggered.connect(lambda e,gc=gc,page=graph.page,graph=graph : page.convert_graph(gc, graph=graph))
                    
                    elif mode == 'add' :
                        action.triggered.connect(lambda e,page=graph.page,graph=graph,side=side,gc=gc : page.insert_graph(graph, side, gc))
                        
                elif pm is not None :
                    action.triggered.connect(lambda e,pm=pm,gc=gc : pm.add_page(gc=gc))
                    
            menu.addMenu(menu_gtype)
            
    #==========================================================================
    def __init__(self, gtype, dimensions) :
        #----------------------------------------------------------------------
        self.name = "{}_{}".format(gtype, "".join(dimensions))
        self.gtype = gtype
        self.dimensions  = dimensions
        
    #==========================================================================
    def __repr__(self) :
        #----------------------------------------------------------------------
        return "Graph_Config({})".format(self.name)
    
    #==========================================================================
    def __eq__(self, other) :
        #----------------------------------------------------------------------
        return self.name == other.name
    
    #==========================================================================
    def copy(self) :
        #----------------------------------------------------------------------
        return Graph_Config(self.gtype, self.dimensions.copy())
    
    #==========================================================================
    def get_icon(self) :
        #----------------------------------------------------------------------
        if self.gtype == '1D' : return get_icon(self.dimensions[0])
        else                  : return get_icon(self.gtype)
    
    #==========================================================================
    def can_plot(self, element) :
        #----------------------------------------------------------------------
        if isinstance(element, Constant) :
            return len(self.dimensions) == 1
        
        #----------------------------------------------------------------------
        elif isinstance(element, Mesh) :
            return element.dimension in self.dimensions
        
        #----------------------------------------------------------------------
        elif isinstance(element, Vector) :
            return element.dimension in self.dimensions
        
        #----------------------------------------------------------------------
        elif isinstance(element, Matrix) :
            if len(self.dimensions) == 1 : return True
            
            for axe in self.dimensions :
                if axe not in element.dimensions :
                    return False
            return True
        
        #----------------------------------------------------------------------
        elif isinstance(element, Cuboid) or isinstance(element, PolyCuboid) :
            for axe in self.dimensions :
                if axe not in ['X','Y','Z'] : return False
            return True
        
        #----------------------------------------------------------------------
        raise Exception("fonction 'can_plot' non configuré pour un élément de type {}".format(type(element).__name__))
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Graph(QWidget) :
    
    #==========================================================================
    INDEX = 1
    
    #==========================================================================
    def __init__(self, page, graph_config, **kwargs) :
        #----------------------------------------------------------------------
        if 'index' in kwargs.keys() :
            self.index = kwargs.pop('index')
        else :
            self.index = Graph.INDEX
            Graph.INDEX += 1
        
        #----------------------------------------------------------------------
        self.name = "Graphique {}".format(self.index)
        
        #----------------------------------------------------------------------
        self.page = page
        self.pm = self.page.pm
        self.mw = self.page.mw
        
        #----------------------------------------------------------------------
        self.graph_config = None
        self.style = None
        self.central_widget = None
        self.legend = None
        self.autoscale = True
        self.engine = None
        
        self.graph_elements = []
        
        #----------------------------------------------------------------------
        QWidget.__init__(self)
        self.setAcceptDrops(True)
        
        #----------------------------------------------------------------------
        self.load_ui()
        self.configure(graph_config)
        
    #==========================================================================
    def __repr__(self) :
        #----------------------------------------------------------------------
        return "Graph {}".format(self.name)
        
    #==========================================================================
    def load_ui(self) :
        #----------------------------------------------------------------------
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), "UI", "Graph.ui"), self)
        
        #----------------------------------------------------------------------
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    #==========================================================================
    def open_menu(self) :
        #----------------------------------------------------------------------
        menu = QMenu(self.mw)
        
        self._open_menu(menu)
        
        #----------------------------------------------------------------------
        menu_convert = QMenu("Convertir le graphe", self.mw)
        menu_convert.setIcon(get_icon('convert'))
        Graph_Config.add_to_menu(menu_convert, graph=self, mode='convert')
        menu.addMenu(menu_convert)
        
        #----------------------------------------------------------------------
        menu_add = QMenu("Ajouter un graphe", self.mw)
        menu_add.setIcon(get_icon('add_graph'))
        side_str = {'right':'A droite', 'left':'A gauche', 'top':'En haut', 'bottom':'En bas'}
        for side in ['right','bottom','left','top'] :
            menu_side = QMenu(side_str[side], self.mw)
            menu_side.setIcon(get_icon("add_{}".format(side)))
            Graph_Config.add_to_menu(menu_side, graph=self, mode='add', side=side)
            menu_add.addMenu(menu_side)
        menu.addMenu(menu_add)
        
        #----------------------------------------------------------------------
        sides = [side for side in ['right','bottom','left','top'] if self.page.can_remove(self,side)]
        side_str = {'right':'A droite', 'left':'A gauche', 'top':'En haut', 'bottom':'En bas'}
        if len(sides) > 1 :
            menu_remove = QMenu("Fermer le graphe", self.mw)
            menu_remove.setIcon(get_icon('empty'))
            for side in sides :
                action = menu_remove.addAction(get_icon("fill_"+side), side_str[side])
                action.triggered.connect(lambda e,page=self.page,graph=self,side=side : page.remove_graph(graph,side))
            menu.addMenu(menu_remove)
        else :
            action = menu.addAction("Fermer le graphe")
            if len(sides) == 1 :
                action.setIcon(get_icon("fill_"+sides[0]))
                action.triggered.connect(lambda e,page=self.page,graph=self,side=sides[0] : page.remove_graph(graph,side))
            else :
                action.setIcon(get_icon('empty'))
                action.triggered.connect(lambda e,pm=self.pm,index=self.page.index : pm.remove_page(index))
            
        #----------------------------------------------------------------------
        menu.addSeparator()
        #----------------------------------------------------------------------
        menu_show = QMenu("Afficher un élément", self.mw)
        menu_show.setIcon(get_icon("visible"))
        active_show = False
        #----------------------------------------------------------------------
        menu_hide = QMenu("Masquer un élément", self.mw)
        menu_hide.setIcon(get_icon("hidden"))
        active_hide = False
        #----------------------------------------------------------------------
        menu_rm = QMenu("Supprimer un élément", self.mw)
        menu_rm.setIcon(get_icon("close"))
        active_rm   = False
        #----------------------------------------------------------------------
        for ge in self.graph_elements :
            gs = ge.style
            action = menu_rm.addAction(ge.label)
            action.setIcon(get_icon(ge.get_icon()))
            action.triggered.connect(lambda e,graph=self,ge=ge : graph.remove_element(ge))
            active_rm = True
            if gs.get('element.is_active') :
                action = menu_hide.addAction(ge.label)
                action.setIcon(get_icon(ge.get_icon()))
                action.triggered.connect(lambda e,gs=gs,k='element.is_active',v=False : gs.set(k,v))
                active_hide = True
            else :
                action = menu_show.addAction(ge.label)
                action.setIcon(get_icon(ge.get_icon()))
                action.triggered.connect(lambda e,gs=gs,k='element.is_active',v=True : gs.set(k,v))
                active_show = True
        #----------------------------------------------------------------------
        if active_rm   : menu.addMenu(menu_rm)
        if active_show : menu.addMenu(menu_show)
        if active_hide : menu.addMenu(menu_hide)
        
        #----------------------------------------------------------------------
        menu.addSeparator()
        
        #----------------------------------------------------------------------
        menu_sf = QMenu("Sauvegarder les graphiques", self.mw)
        menu_sf.setIcon(get_icon("image"))
        menu_sf.addAction(get_icon('image'), "Graphe").triggered.connect(lambda e:self.save_image())
        menu_sf.addAction(get_icon('image'), "Page").triggered.connect(lambda e,page=self.page:page.save_image())
        menu.addMenu(menu_sf)
        
        #----------------------------------------------------------------------
        if self.engine == 'MPL' :
            menu_sd = QMenu("Sauvegarder les données", self.mw)
            menu_sd.setIcon(get_icon("excel"))
            menu_sd.addAction(get_icon('excel'), "Graphe").triggered.connect(lambda e:self.save_data())
            menu_sd.addAction(get_icon('excel'), "Page").triggered.connect(lambda e,page=self.page:page.save_data())
            menu_sd.addAction(get_icon('excel'), "Tout").triggered.connect(lambda e,pm=self.pm:pm.save_data())
            menu.addMenu(menu_sd)
        
        #----------------------------------------------------------------------
        menu.exec_(QCursor.pos())
        
    #==========================================================================
    def _open_menu(self, menu) :
        pass
        
    #==========================================================================
    def configure(self, graph_config) :
        #----------------------------------------------------------------------
        if self.graph_config is not None and self.graph_config.name == graph_config.name :
            return
        
        #----------------------------------------------------------------------
        self.graph_config = graph_config
        
        #----------------------------------------------------------------------
        self.create_graph()
        
    #==========================================================================
    def create_graph(self) :
        #----------------------------------------------------------------------
        self.main_widget = self._create_graph()
        self.main_layout.addWidget(self.main_widget, 0, 1)
        
        #----------------------------------------------------------------------
        self.legend = Graph_Legend(self)
        self.style.add_change('legend.pos')
        
        #----------------------------------------------------------------------
        self.main_layout.setColumnStretch(1,1)
        
        #----------------------------------------------------------------------
        self.update_style(redraw=False)
        
    #==========================================================================
    def _create_graph(self) :
        #----------------------------------------------------------------------
        widget = QLabel(self.name)
        widget.setStyleSheet('background-color:red')
        self.main_layout.addWidget(widget)
        return widget
        
    #==========================================================================
    def remove_graph(self) :
        #----------------------------------------------------------------------
        self._remove_graph()
        
        #----------------------------------------------------------------------
        for ge in self.graph_elements : 
            ge.reset()
            ge = None
            del ge
            
        if self.legend is not None :
            self.legend.remove()
                
        #----------------------------------------------------------------------
        self.graph_elements = []
        self.deleteLater()
        
    #==========================================================================
    def _remove_graph(self) :
        #----------------------------------------------------------------------
        pass
            
    #==========================================================================
    def add_element(self, update=True, after=None, **kwargs) :
        #----------------------------------------------------------------------
        self.mw.set_busy(1)
        
        #----------------------------------------------------------------------
        if 'element' in kwargs.keys() :
            element = kwargs.pop('element')
        #----------------------------------------------------------------------
        elif 'path' in kwargs.keys() :
            file    = kwargs.pop('file')
            path    = kwargs.pop('path')
            element = file.get_element(path=path)
        #----------------------------------------------------------------------
        elif 'graph_element' in kwargs.keys() :
            ge = kwargs.pop('graph_element')
            element = ge.element
            kwargs['style'] = ge.style
            kwargs['index'] = ge.index
            for k,v in ge.opts.items() : kwargs[k] = v
            
        #----------------------------------------------------------------------
        graph_element = new_graph_element(self, element, **kwargs)
        self.graph_elements.append(graph_element)
        
        #----------------------------------------------------------------------
        self.plot(graph_element)
        
        #----------------------------------------------------------------------
        if update :
            self.update_graph()
        
        #----------------------------------------------------------------------
        self.mw.set_busy(-1)
        return graph_element
        
    #==========================================================================
    def remove_element(self, ge, update=True) :
        #----------------------------------------------------------------------
        ge.reset()
        self.graph_elements.pop(self.graph_elements.index(ge))
        
        #----------------------------------------------------------------------
        for ge in self.graph_elements :
            ge.update_style(redraw=False)
            
        #----------------------------------------------------------------------
        if len(self.graph_elements) == 0 :
            self.autoscale = True
        
        #----------------------------------------------------------------------
        if update :
            self.update_graph()
        
    #==========================================================================
    def move_element(self, ge, direction) :
        #----------------------------------------------------------------------
        index = self.graph_elements.index(ge)
        if   direction == 'up'   : self.graph_elements.insert(index-1, self.graph_elements.pop(index))
        elif direction == 'down' : self.graph_elements.insert(index+1, self.graph_elements.pop(index))
        
        #----------------------------------------------------------------------
        for ge in self.graph_elements :
            if self.engine == 'VTK' :
                ge.reset()
                self.plot(ge)
            ge.update_style(redraw=False)

        #----------------------------------------------------------------------
        self.update_legend()
        self.update_parameters()
        self.redraw()
        
    #==========================================================================
    def dragEnterEvent(self, event) :
        #----------------------------------------------------------------------
        stype = type(event.source()).__name__
        
        #----------------------------------------------------------------------
        if stype == 'Files_Tree' :
            objs = event.source().get_selected_objects()
            if len(objs) > 0 :
                event.accept()
                
    #==========================================================================
    def dropEvent(self, event) :
        #----------------------------------------------------------------------
        stype = type(event.source()).__name__
        
        #----------------------------------------------------------------------
        if stype == 'Files_Tree' :
            objs = event.source().get_selected_objects()
            
            for obj in objs :
                self.add_element(update=False, **obj)
                
            if len(objs) > 0 :
                self.update_graph()
                event.accept()
    
    #==========================================================================
    def plot(self, graph_element) :
        #----------------------------------------------------------------------
        if not self.graph_config.can_plot(graph_element.element) :
            return
        
        #----------------------------------------------------------------------
        graph_element.create_plotted()
        graph_element.update_plotted()
        graph_element.update_style()
        
    #==========================================================================
    def update_graph(self, **kwargs) :
        #----------------------------------------------------------------------
        relegend     = kwargs.pop('relegend', True)
        reparameters = kwargs.pop('reparameters', True)
        rescale      = kwargs.pop('rescale', True) and self.autoscale
        redraw       = kwargs.pop('redraw', True)
        
        #----------------------------------------------------------------------
        self._update_graph()
        
        #----------------------------------------------------------------------
        if relegend     : self.update_legend()
        if reparameters : self.update_parameters()
        if rescale      : self.rescale(redraw=False)
        if redraw       : self.redraw()
    
    #==========================================================================
    def _update_graph(self) :
        pass
    
    #==========================================================================
    def update_style(self, redraw=False) :
        #----------------------------------------------------------------------
        self._update_style()
        if redraw : self.redraw()
        
        #----------------------------------------------------------------------
        self.update_legend()

    #==========================================================================
    def _update_style(self) :
        pass
        
    #==========================================================================
    def update_legend(self) :
        #----------------------------------------------------------------------
        if self.legend is None : return
        
        c = 0 if 'Gauche' in self.style.get('legend.pos') else 2
        self.main_layout.addWidget(self.legend, 0,c)
        
        #----------------------------------------------------------------------
        self.legend.update()
        
        #----------------------------------------------------------------------
        for ge in self.graph_elements :
            self.legend.update_cbar(ge)
    
    #==========================================================================
    def update_pointed(self, event=None) :
        pass
    
    #==========================================================================
    def update_parameters(self) :
        #----------------------------------------------------------------------
        self.mw.parameters_manager.update_items(self.page)
        
    #==========================================================================
    def rescale(self, ignore_autoscale=True, redraw=False) :
        #----------------------------------------------------------------------
        print("fonction 'rescale' non implémentée pour la classe {}".format(type(self).__name__))
        
    #==========================================================================
    def redraw(self) :
        #----------------------------------------------------------------------
        print("fonction 'redraw' non implémentée pour la classe {}".format(type(self).__name__))
        
    #==========================================================================
    def save_image(self, filepath=None, multi=False) :
        #----------------------------------------------------------------------
        if filepath is None :
            defaultname = '{}_graph_{}.png'.format(self.page.name, self.index)
            if len(self.mw.files_manager.files) == 1 : defaultname = os.path.join(os.path.dirname(self.mw.files_manager.files[0].nc_path), defaultname)
            filepath,_ = QFileDialog.getSaveFileName(self, "Enregistrer sous", defaultname, "Tous les fichiers (*);;Images PNG (*.png)", "Images PNG (*.png)")
        
        #----------------------------------------------------------------------
        if filepath == '' :
            return
        
        #----------------------------------------------------------------------
        self._save_image(filepath)
        
        #----------------------------------------------------------------------
        W = self.geometry().width()
        H = self.geometry().height()
        gpos = self.mapToGlobal(self.rect().topLeft())
        
        #----------------------------------------------------------------------
        pixmap = QPixmap(W, H)
        pixmap.fill(Qt.transparent)
        
        #----------------------------------------------------------------------
        painter = QPainter(pixmap)
        
        #----------------------------------------------------------------------
        temp_path = filepath.replace(".png", "_0.png")
        self._save_image(temp_path)
        _pixmap = QPixmap(temp_path)
        rpos = self.main_widget.mapToGlobal(self.main_widget.rect().topLeft()) - gpos
        painter.drawPixmap(rpos.x(), rpos.y(), _pixmap)
        os.remove(temp_path)
        
        #----------------------------------------------------------------------
        if self.legend is not None :
            for f,fig in enumerate(self.legend.get_figs()) :
                temp_path = filepath.replace(".png", "_{}.png".format(f+1))
                fig.savefig(temp_path, transparent=False)
                _pixmap = QPixmap(temp_path)
                rpos = fig.canvas.mapToGlobal(fig.canvas.rect().topLeft()) - gpos
                painter.drawPixmap(rpos.x(), rpos.y(), _pixmap)
                os.remove(temp_path)
                
        #----------------------------------------------------------------------
        painter.end()
        pixmap.save(filepath, "PNG")
        
        #----------------------------------------------------------------------
        if not multi :
            rep = question_box('question', "Sauvegarde terminée", "La sauvegarde de l'image est terminée !", buttons=[('Yes','OK','check'), ('No','Ouvrir','image')])
            if rep == 'No' : os.startfile(filepath)
        
    #==========================================================================
    def _save_image(self, filepath) :
        #----------------------------------------------------------------------
        raise Exception("fonction '_save_image' non implémentée pour la classe {}".format(type(self).__name__))
        
    #==========================================================================
    def save_data(self, filepath=None) :
        #----------------------------------------------------------------------
        self.pm.save_data(filepath=filepath, page=self.page, graph=self)
        
    #==========================================================================
    def _get_save_data(self) :
        #----------------------------------------------------------------------
        return {}
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

