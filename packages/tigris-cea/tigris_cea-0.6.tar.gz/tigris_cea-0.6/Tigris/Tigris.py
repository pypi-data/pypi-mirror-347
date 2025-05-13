# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import sys
#------------------------------------------------------------------------------
try : from ctypes import windll ; windll.shell32.SetCurrentProcessExplicitAppUserModelID('CEA.TIGRIS.VIEWER')
except ImportError : pass
#------------------------------------------------------------------------------
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QCursor
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolButton, QMenu
#------------------------------------------------------------------------------
import matplotlib
matplotlib.use('Qt5Agg')
#------------------------------------------------------------------------------
try : import vtk
except : os.system('pip install vtk')
#------------------------------------------------------------------------------
try : import openpyxl
except : os.system('pip install openpyxl')
#------------------------------------------------------------------------------
try : import netCDF4
except : os.system('pip install netCDF4')
#------------------------------------------------------------------------------
try : import shapely
except : os.system('pip install shapely')
#------------------------------------------------------------------------------
from Pages_Manager import Pages_Manager
from IHM_Files import Files_Manager
from Combiner import Combiner
from IHM_Parameters import Parameters_Manager
from utils_qt import LogsWidget, get_icon
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Tigris(QMainWindow) :
    
    #==========================================================================
    __version__ = "0.6"
    click = pyqtSignal(QMouseEvent)

    #==========================================================================
    def __init__(self, mode='prod') :
        #----------------------------------------------------------------------
        QMainWindow.__init__(self)
        
        #----------------------------------------------------------------------
        self.pages_manager = None
        self.files_manager = None
        self.parameters_manager = None
        
        #----------------------------------------------------------------------
        self.load_ui(mode)
        self.busy_state = 0
        
        #----------------------------------------------------------------------
        self.pages = []
        
    #==========================================================================
    def load_ui(self, mode) :
        #----------------------------------------------------------------------
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), "UI", "Tigris.ui"), self)
        
        #----------------------------------------------------------------------
        self.te_logs = LogsWidget(self)
        self.layout_logs.addWidget(self.te_logs)
        if mode == 'prod' : self.te_logs.redirect()
        Tigris.splash()
        
        #----------------------------------------------------------------------
        self.files_manager = Files_Manager(self, self.layout_files)
        
        #----------------------------------------------------------------------
        self.pages_manager = Pages_Manager(self)
        self.stackedWidget.addWidget(self.pages_manager.tab_widget)
        
        #----------------------------------------------------------------------
        self.combiner = Combiner(self)
        self.stackedWidget.addWidget(self.combiner)
        
        #----------------------------------------------------------------------
        self.parameters_manager = Parameters_Manager(self)
        
        #----------------------------------------------------------------------
        self.action_exit.triggered.connect(self.close)
        #----------------------------------------------------------------------
        self.action_convert = QToolButton()
        self.action_convert.setToolTip('Convertir un calcul')
        self.action_convert.setIcon(get_icon('convert'))
        self.action_convert.setPopupMode(QToolButton.InstantPopup)
        menu = QMenu(self)
        for code in ['porflow','min3p','hytec','crunch'] :
            a = getattr(self, 'action_convert_'+code)
            a.triggered.connect(lambda e,code=code : self.files_manager.convert_calcul(code))
            menu.addAction(a)
        self.action_convert.setMenu(menu)
        self.toolBar.insertWidget(self.action_load_file, self.action_convert)
        #----------------------------------------------------------------------
        self.action_load_file.triggered.connect(lambda e : self.files_manager.load_file())
        self.action_combiner.toggled.connect(self.combiner.set_activated)
        #----------------------------------------------------------------------
        self.action_new_page.triggered.connect(self.pages_manager.open_new_page_dialog)
        self.action_save_image.triggered.connect(self.pages_manager.save_image)
        self.action_save_data.triggered.connect(lambda e:self.pages_manager.save_data())
        self.action_inspector.triggered.connect(self.pages_manager.inspector_toggled)
        
        #----------------------------------------------------------------------
        self.tabifyDockWidget(self.dock_graphs, self.dock_elements)
        # self.dock_graphs.setVisible(True)
        # self.dock_elements.setVisible(True)
        
    #==========================================================================
    def splash() :
        # https://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=POSTGR
        print("""#================================================#
|                                                |
|  ████████╗██╗ ██████╗ ██████╗ ██╗███████╗      |
|  ╚══██╔══╝██║██╔════╝ ██╔══██╗██║██╔════╝      |
|     ██║   ██║██║  ███╗██████╔╝██║███████╗      |
|     ██║   ██║██║   ██║██╔══██╗██║╚════██║      |
|     ██║   ██║╚██████╔╝██║  ██║██║███████║      |
|     ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝ {}  |
#================================================#""".format(Tigris.__version__))
    
    #==========================================================================
    def keyPressEvent(self, event) :
        #----------------------------------------------------------------------
        if event.key() == Qt.Key_Escape :
            self.close()
            event.accept()
            
        #----------------------------------------------------------------------
        elif event.key() == Qt.Key_I :
            self.action_inspector.setChecked(not self.action_inspector.isChecked())
            self.pages_manager.inspector_toggled()
            
        #----------------------------------------------------------------------
        for page in self.pages_manager.pages :
            if page.graphs is None : continue
            for graph in page.graphs :
                graph.keyPressEvent(event)
                
        #----------------------------------------------------------------------
        else :
            super().keyPressEvent(event)
            
    #==========================================================================
    def keyReleaseEvent(self, event) :
        #----------------------------------------------------------------------
        for page in self.pages_manager.pages :
            if page.graphs is None : continue
            for graph in page.graphs :
                graph.keyReleaseEvent(event)
            
    #==========================================================================
    def mousePressEvent(self, event) :
        #----------------------------------------------------------------------
        self.click.emit(event)
        
    #==========================================================================
    def set_busy(self, d) :
        #----------------------------------------------------------------------
        self.busy_state += d
        if self.busy_state < 0 : self.busy_state = 0
        self.setCursor(QCursor(Qt.ArrowCursor if self.busy_state == 0 else Qt.WaitCursor))
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def command(argv) :
    #--------------------------------------------------------------------------
    sep = '-------------------------------------------------------------------------------'
    print(sep)
    
    #--------------------------------------------------------------------------
    if argv[0] == '--help' :
        # print(sep)
        print("""> Usage de Tigris :
   - lancement de l'interface : Tigris
   - affichage de l'aide      : Tigris --help
   - conversion d'un calcul   : Tigris --convert <code> <input> [<name>]""")
        print(sep)
        
    #--------------------------------------------------------------------------
    elif argv[0] == '--convert' :
        h = ['']
        h.append("> Usage : Tigris --convert <code> <path> [<name>]")
        h.append("   - code : parmis 'Porflow','Min3P', 'HYTEC','Crunch' (casse ignorée)")
        h.append("   - path : chemin vers le fichier d'entrée ou le dossier de calcul (absolu ou relatif)")
        h.append("   - <name> : optionnel, permet d'indiquer le nom du fichier NetCDF de sortie")
        
        #----------------------------------------------------------------------
        if len(argv) < 3 : 
            print("\n".join([sep, "Erreur : nombre d'arguments invalide"] + h))
            return
        
        #----------------------------------------------------------------------
        code = argv[1].lower()
        if code not in ['porflow','min3p','hytec','crunch'] : 
            print("\n".join([sep, "Erreur : code '{}' invalide".format(code)] + h))
            return
        
        #----------------------------------------------------------------------
        path = os.path.abspath(argv[2])
        if not os.path.exists(path) :
            print("Erreur : fichier '{}' introuvable".format(path))
            return
        
        #----------------------------------------------------------------------
        opts = {}
        if len(argv) >= 4 : opts['name'] = argv[3]
        
        #----------------------------------------------------------------------
        if   code == 'porflow' : from Porflow import Porflow_Convertor as Convertor
        elif code == 'min3p'   : from Min3p   import Min3p_Convertor   as Convertor
        elif code == 'hytec'   : from Hytec   import Hytec_Convertor   as Convertor
        elif code == 'crunch'  : from Crunch  import Crunch_Convertor  as Convertor
        
        #----------------------------------------------------------------------
        convertor = Convertor(input_path=path, **opts)
        print(sep)
        print("-> Fichier de calcul :", convertor.nc_path)
        
    #--------------------------------------------------------------------------
    else :
        # print(sep)
        print("Commande invalide :")
        print(">> "+" ".join(['Tigris'] + argv))
        command(['--help'])
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- PROGRAMME
#==============================================================================
if __name__ == '__main__' :
    #--------------------------------------------------------------------------
    if len(sys.argv) > 1 :
        command(sys.argv[1:])
        
    #--------------------------------------------------------------------------
    else :
        app = QApplication(sys.argv)
        prog = Tigris()
        prog.show()
        app.exec_()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



