# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
#------------------------------------------------------------------------------
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QFileDialog, QCheckBox
#------------------------------------------------------------------------------
from Calcul import Calcul
from Porflow import Porflow_Convertor
from Min3p import Min3p_Convertor
from Hytec import Hytec_Convertor
from Crunch import Crunch_Convertor
from utils_qt import LogsWidget, QComboBox
from utils_qt import get_line, get_icon, question_box
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_convert_dialog(mw, code) :
    if   code == 'porflow' : dialog = Porflow_Convertor_Dialog(mw)
    elif code == 'min3p'   : dialog = Min3p_Convertor_Dialog(mw)
    elif code == 'hytec'   : dialog = Hytec_Convertor_Dialog(mw)
    elif code == 'crunch'  : dialog = Crunch_Convertor_Dialog(mw)
    return dialog
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Calcul_Convertor_Dialog(QDialog) :
    
    #==========================================================================
    def __init__(self, mw, code) :
        #----------------------------------------------------------------------
        self.mw = mw
        self.code = code
        
        #----------------------------------------------------------------------
        QDialog.__init__(self, parent=self.mw)
        
        #----------------------------------------------------------------------
        self.load_ui()
        
    #==========================================================================
    def load_ui(self) :
        #----------------------------------------------------------------------
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), "UI", "Convertor_Dialog.ui"), self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Conversion d'un calcul {}".format(Calcul.CODE_NAMES[self.code]))
        self.setWindowIcon(get_icon(self.code))
        
        #----------------------------------------------------------------------
        self.te_logs = LogsWidget(self)
        self.logs_layout.addWidget(self.te_logs)
        
        #----------------------------------------------------------------------
        self.but_input.clicked.connect(self.get_input)
        self.but_convert.clicked.connect(self.convert)
        self.but_close.clicked.connect(self.close)
        
        #----------------------------------------------------------------------
        # self.gp_options.setVisible(False)
        self._load_ui()
    
    #==========================================================================
    def _load_ui(self) :
        pass
    
    #==========================================================================
    def set_default_name(self, default_name) :
        #----------------------------------------------------------------------
        self.le_name.setPlaceholderText(default_name)
        if self.le_name.text() == '' : self.le_name.setText(default_name)
        
    #==========================================================================
    def convert(self) :
        #----------------------------------------------------------------------
        opts = self._convert_opts()
        
        #----------------------------------------------------------------------
        print("> Conversion d'un calcul {} ... ".format(self.code), end="", flush=True)
        
        #----------------------------------------------------------------------
        if os.path.exists(opts['nc_path']) :
            rep = question_box('warning', "Fichier existant", "Le fichier '{}' existe déjà !".format(os.path.basename(opts['nc_path'])), buttons=[('Yes','Remplacer'), ('Cancel','Annuler')])
            if rep != 'Yes' : 
                print("annulé")
                return
                
        #----------------------------------------------------------------------
        self.mw.set_busy(1)
        
        #----------------------------------------------------------------------
        self.te_logs.redirect()
        self.te_logs.clear()
        
        #----------------------------------------------------------------------
        if   self.code == 'porflow' : convertor = Porflow_Convertor(**opts)
        elif self.code == 'min3p'   : convertor = Min3p_Convertor(**opts)
        elif self.code == 'hytec'   : convertor = Hytec_Convertor(**opts)
        elif self.code == 'crunch'  : convertor = Crunch_Convertor(**opts)
        
        #----------------------------------------------------------------------
        self.mw.te_logs.redirect()
        print("OK")
        self.mw.set_busy(-1)
        
        #----------------------------------------------------------------------
        rep = question_box('question', 'Conversion terminée', "La conversion du calcul {} est terminée".format(self.code), buttons=[('Yes','OK','check'), ('No','Charger','open')])
        if rep == 'No' :
            self.mw.files_manager.load_file(nc_path=convertor.nc_path)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Porflow_Convertor_Dialog(Calcul_Convertor_Dialog) :
    
    #==========================================================================
    def __init__(self, mw) :
        #----------------------------------------------------------------------
        Calcul_Convertor_Dialog.__init__(self, mw, code='porflow')
        
    #==========================================================================
    def _load_ui(self) :
        #----------------------------------------------------------------------
        self.cb_check_zones = QCheckBox("Vérifier les matériaux")
        self.layout_options.addRow(self.cb_check_zones)
        
        #----------------------------------------------------------------------
        self.layout_options.addRow(get_line(Qt.Horizontal))
        
        #----------------------------------------------------------------------
        self.combo_T = QComboBox()
        self.combo_T.addItems(['années','secondes'])
        self.layout_options.addRow('Temps', self.combo_T)
        #----------------------------------------------------------------------
        self.combo_L = QComboBox()
        self.combo_L.addItems(['mètres'])
        self.layout_options.addRow('Longueurs', self.combo_L)
        #----------------------------------------------------------------------
        self.combo_Q = QComboBox()
        self.combo_Q.addItems(['mol'])
        self.layout_options.addRow('Quantités', self.combo_Q)
        
        
    #==========================================================================
    def get_input(self) :
        #----------------------------------------------------------------------
        input_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier d'entrée Porflow", "", "Tous (*);;Input (*.inp)", "Input (*.inp)")
        if input_path == '' : return
        
        #----------------------------------------------------------------------
        self.le_input.setText(input_path)
        self.set_default_name(".".join(os.path.basename(input_path).split(".")[:-1]))
        
    #==========================================================================
    def _convert_opts(self) :
        #----------------------------------------------------------------------
        opts = {}
        opts['input_path']  = self.le_input.text()
        opts['name']        = self.le_name.text()
        opts['unit_T']      = self.combo_T.currentText()
        opts['unit_L']      = self.combo_L.currentText()
        opts['unit_Q']      = self.combo_Q.currentText()
        opts['check_zones'] = self.cb_check_zones.isChecked()
        opts['nc_path'] = os.path.join(os.path.dirname(opts['input_path']), opts['name']+".nc")
        #----------------------------------------------------------------------
        return opts
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Min3p_Convertor_Dialog(Calcul_Convertor_Dialog) :
    
    #==========================================================================
    def __init__(self, mw) :
        #----------------------------------------------------------------------
        Calcul_Convertor_Dialog.__init__(self, mw, code='min3p')
        
    #==========================================================================
    def get_input(self) :
        #----------------------------------------------------------------------
        input_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier d'entrée Min3P", "", "Tous (*);;Input (*.dat)", "Input (*.dat)")
        if input_path == '' : return
        
        #----------------------------------------------------------------------
        self.le_input.setText(input_path)
        self.set_default_name(".".join(os.path.basename(input_path).split(".")[:-1]))
        
    #==========================================================================
    def _convert_opts(self) :
        #----------------------------------------------------------------------
        opts = {}
        opts['input_path']  = self.le_input.text()
        opts['name']        = self.le_name.text()
        opts['nc_path'] = os.path.join(os.path.dirname(opts['input_path']), opts['name']+".nc")
        #----------------------------------------------------------------------
        return opts
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Hytec_Convertor_Dialog(Calcul_Convertor_Dialog) :
    
    #==========================================================================
    def __init__(self, mw) :
        #----------------------------------------------------------------------
        Calcul_Convertor_Dialog.__init__(self, mw, code='hytec')
        
    #==========================================================================
    def get_input(self) :
        #----------------------------------------------------------------------
        input_path = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier de calcul Hytec", "", QFileDialog.ShowDirsOnly)
        if input_path == '' : return
        
        #----------------------------------------------------------------------
        self.le_input.setText(input_path)
        self.set_default_name(os.path.basename(input_path))
        
    #==========================================================================
    def _convert_opts(self) :
        #----------------------------------------------------------------------
        opts = {}
        opts['input_path'] = self.le_input.text()
        opts['name']       = self.le_name.text()
        opts['nc_path']    = os.path.join(opts['input_path'], opts['name']+".nc")
        #----------------------------------------------------------------------
        return opts
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Crunch_Convertor_Dialog(Calcul_Convertor_Dialog) :
    
    #==========================================================================
    def __init__(self, mw) :
        #----------------------------------------------------------------------
        Calcul_Convertor_Dialog.__init__(self, mw, code='crunch')
        
    #==========================================================================
    def get_input(self) :
        #----------------------------------------------------------------------
        input_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier d'entrée Crunch", "", "Tous (*);;Input (*.in)", "Input (*.in)")
        if input_path == '' : return
        
        #----------------------------------------------------------------------
        self.le_input.setText(input_path)
        self.set_default_name(".".join(os.path.basename(input_path).split(".")[:-1]))
        
    #==========================================================================
    def _convert_opts(self) :
        #----------------------------------------------------------------------
        opts = {}
        opts['input_path']  = self.le_input.text()
        opts['name']        = self.le_name.text()
        opts['nc_path'] = os.path.join(os.path.dirname(opts['input_path']), opts['name']+".nc")
        #----------------------------------------------------------------------
        return opts
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

