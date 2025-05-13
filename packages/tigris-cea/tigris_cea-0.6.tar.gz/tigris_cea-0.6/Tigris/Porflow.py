# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import random
import numpy as np
import datetime
from itertools import product
#------------------------------------------------------------------------------
import platform
if platform.system() == 'Windows' :
    import win32com.client
#------------------------------------------------------------------------------
import matplotlib as mpl
#------------------------------------------------------------------------------
from Element import Element
from Element_Constants import Constant, Vector, Mesh
from Element_Matrix import Matrix
from Element_Cuboids import Cuboid, PolyCuboid
from Calcul import Calcul, Calcul_Convertor
from utils import to_float, get_temp_path, get_now
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Porflow(Calcul) :
    
    #==========================================================================
    CODE      = 'porflow'
    UNITS     = ['T','L','Q']
    #--------------------------------------------------------------------------
    ATTR_INPUTPATH   = 'INPUT_PATH'
    ATTR_UNIT_PREFIX = "UNIT_"
    #--------------------------------------------------------------------------
    PRIMARY_NAME    = "Primaire"
    SECONDARY_NAME  = "Secondaire"
    FINAL_ZONE_NAME = "Finale"
    #--------------------------------------------------------------------------
    HIST_NAME       = "HIST"
    FLUX_NAME       = "FLUX"
    SAVE_NAME       = "SAVE"
    #--------------------------------------------------------------------------
    FLUX_OUTPUTS    = [None        , None          , "StorageNow"   , "TotalDecay",
                       "InConv"    , "InDiff"      , "InSource"     ,
                       "OutConv"   , "OutDiff"     , "OutSource"    ,
                       "InDiver"   , "ConvInBlock" , "DiffLossBlock", "TotDiscr",
                       "InstInConv", "InstInDiff"  , "InstInSource"]
    
    #==========================================================================
    def __init__(self) :
        #----------------------------------------------------------------------
        Calcul.__init__(self, Porflow.CODE)
        
        #----------------------------------------------------------------------
        self.zones  = None
        self.props  = None
        self.hists  = None
        self.fluxs  = None
        self.saves  = None
        
    #==========================================================================
    def _details(self, **kwargs) :
        #----------------------------------------------------------------------
        nb_p = len([z for z in self.zones.values() if z.get_attribute('zone_type') == 'primary'])
        nb_s = len([z for z in self.zones.values() if z.get_attribute('zone_type') == 'secondary'])
        print("   - zones".ljust(Calcul.DETAILS_ALIGN,' ')+": {} matériaux ({} primaires et {} secondaires)".format(nb_p+nb_s, nb_p, nb_s))
        
        #----------------------------------------------------------------------
        prop_names,prop_zones = [],[]
        for prop_name,prop_zone in self.props.keys() :
            if prop_name not in prop_names : prop_names.append(prop_name)
            if prop_zone not in prop_zones : prop_zones.append(prop_zone)
        print("   - propriétés".ljust(Calcul.DETAILS_ALIGN,' ')+": {} définition(s), sur {} zone(s)".format(len(prop_names), len(prop_zones)))

        #----------------------------------------------------------------------
        print("   - résultats".ljust(Calcul.DETAILS_ALIGN,' ')+": {} HIST, {} FLUX, {} SAVES".format(len(self.hists),len(self.fluxs),len(self.saves)))
        
    #==========================================================================
    def _load(self) :
        #----------------------------------------------------------------------
        self.zones  = {}
        self.props  = {}
        self.hists  = []
        self.fluxs  = []
        self.saves  = []
        
        #----------------------------------------------------------------------
        for e in self.elements :
            if   e.path[0] == Calcul.ZONES_NAME  : self.zones[e.label] = e
            elif e.path[0] == Calcul.PROPS_NAME  : self.props[(e.get_attribute('prop_name'),e.get_attribute('zone_name'))] = e
            elif e.path[0] == Calcul.RESULTS_NAME :
                if   e.path[1] == Porflow.HIST_NAME : self.hists.append(e)
                elif e.path[1] == Porflow.FLUX_NAME : self.fluxs.append(e)
                elif e.path[1] == Porflow.SAVE_NAME : self.saves.append(e)
        
        #----------------------------------------------------------------------
        zone_by_index = {zone.get_attribute('zone_index'):zone for zlabel,zone in self.zones.items() if zone.get_attribute('zone_type') != 'final'}
        for zlabel,zone in self.zones.items() :
            zone.configure(value=zone.get_attribute('zone_index'))
            if zone.get_attribute('zone_type') == 'secondary' : zone.configure(sub_elements=[self.get_element(path=sub_path) for sub_path in zone.sub_paths])
            if zone.get_attribute('zone_type') == 'final'     : zone.configure(linked_elements=zone_by_index)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Porflow_Convertor(Calcul_Convertor) :
    
    #==========================================================================
    def __init__(self, **opts) :
        #----------------------------------------------------------------------
        Calcul_Convertor.__init__(self, **opts)
        
        #----------------------------------------------------------------------
        self.zones  = None
        self.props  = None
        self.hists  = None
        self.fluxs  = None
        self.saves  = None
        
        #----------------------------------------------------------------------
        self.cells_by_zone = {}
        
        #----------------------------------------------------------------------
        self.convert(**opts)
        
    #==========================================================================
    def _convert(self, **opts) :
        """
        obligatoires : input_path, name
        optionnels : unit_T, unit_L, unit_Q, check_zones, nc_path
        """
        #----------------------------------------------------------------------
        print("> Conversion d'un calcul {} :".format(Calcul.CODE_NAMES[Porflow.CODE]))
        
        #----------------------------------------------------------------------
        if 'input_path' not in opts.keys() :
            raise Exception("paramètre 'input_path' manquant")
        
        #----------------------------------------------------------------------
        self.input_path = opts.get('input_path')
        self.name = opts.get('name', os.path.basename(".".join(self.input_path.split(".")[:-1])))
        self.dirpath = os.path.dirname(self.input_path)
        #----------------------------------------------------------------------
        kwargs = {}
        kwargs[Calcul.ATTR_CODE]     = Porflow.CODE
        kwargs[Calcul.ATTR_CALCUL]   = self.name
        kwargs[Calcul.ATTR_POSTDATE] = get_now(fmt='%d/%m/%Y %H:%M')
        kwargs[Calcul.ATTR_DIRPATH]  = self.dirpath
        #----------------------------------------------------------------------
        kwargs[Porflow.ATTR_INPUTPATH] = self.input_path
        for unit in Porflow.UNITS : kwargs[Porflow.ATTR_UNIT_PREFIX+unit] = opts.get('unit_'+unit,'-')
        
        #----------------------------------------------------------------------
        self.config = Element(path=[Calcul.CONFIG_NAME], label='config', **kwargs)
        
        #----------------------------------------------------------------------
        self.read_inputs()
        self.configure_grid()
        self.configure_zones()
        self.configure_props()
        self.configure_final_zones()
        if opts.get('check_zones',False) : self.check_final_zones()
        self.configure_hist()
        self.configure_flux()
        self.configure_save()
        self.configure_times()
        
    #==========================================================================
    def read_inputs(self) :
        #----------------------------------------------------------------------
        print("   - lecture des fichiers d'entrée ... ", end="", flush=True)
        
        #----------------------------------------------------------------------
        self.input_lines = None
        
        #----------------------------------------------------------------------
        if not os.path.exists(self.input_path) :
            raise Exception("fichier '{}' introuvable".format(os.path.basename(self.input_path)))
            
        #----------------------------------------------------------------------
        self.input_lines = {}
        self.input_lines['raw'] = [] # lignes brutes
        self.input_lines['origin'] = [] # fichier et ligne
        self.input_lines['key_word'] = [] # mot clé
        
        #----------------------------------------------------------------------
        self.read_inputfile(self.input_path)
        
        #----------------------------------------------------------------------
        print('OK ({} lignes)'.format(len(self.input_lines['raw'])))
        
    #==========================================================================
    def read_inputfile(self, inpath, h=0) :
        #----------------------------------------------------------------------
        inname = os.path.basename(inpath)
        dirpath = os.path.dirname(inpath)
        
        #----------------------------------------------------------------------
        if not os.path.exists(dirpath) :
            raise Exception("Le dossier '{}' est introuvable".format(dirpath))
            
        #----------------------------------------------------------------------
        if not os.path.exists(inpath) :
            raise Exception("Le fichier '{}' est introuvable dans le dossier '{}'".format(inname, dirpath))
            
        #----------------------------------------------------------------------
        key_words = ["GRID","COOR","LOCA","READ","HIST","FLUX","SAVE","PORO","HYDR","TRAN","COND"]
        key_word = None
        
        #----------------------------------------------------------------------
        file = open(inpath, 'r')
        for l,line in enumerate(file) :
            if line.startswith('INCLUDE') :
                _inname = line.replace('"',"'").split("'")[1]
                self.read_inputfile(os.path.join(os.path.dirname(inpath), _inname), h+1)
            else :
                line = line.strip()
                rp = [
                    ('"',"'"),
                    ('='," "),
                    ('\t'," "),
                    ]
                for rp1,rp2 in rp : line = line.replace(rp1,rp2)
                
                #--------------------------------------------------------------
                if line == "" :
                    key_word = None
                    continue
                
                #--------------------------------------------------------------
                if line[0] == "/" : continue
                
                #------------------------------------------------------------------
                if len(line) > 4 and line[0:4] in key_words : key_word = line[0:4]
                if key_word is None : continue
            
                if key_word in ['PORO','HYDR','TRAN','COND'] and line[0:4] != key_word :
                    self.input_lines['raw'][-1] += ' '+line.strip()
                    continue
                
                self.input_lines['raw'].append(line.strip())
                self.input_lines['origin'].append((inname, l+1))
                self.input_lines['key_word'].append(key_word)
                
        #----------------------------------------------------------------------
        file.close()
        if h > 0 : return

    #==========================================================================
    def configure_grid(self) :
        #----------------------------------------------------------------------
        print("   - préparation du maillage ... ", end="", flush=True)
        
        #----------------------------------------------------------------------
        keywords = ['COOR']
        input_llines = [(l,line) for l,line in enumerate(self.input_lines['raw']) if self.input_lines['key_word'][l] in keywords]
        
        #----------------------------------------------------------------------
        X = []
        Y = []
        Z = []
        subWord = None
        #----------------------------------------------------------------------
        for l,line in input_llines :
            fields = line.split()
            #------------------------------------------------------------------
            if line.startswith('COOR') :
                if 'NODE' in fields :
                    raise Exception("fichier {}, ligne {} : le mode de maillage 'Node' n'est pas implémenté".format(*self.input_lines['origin'][l]))
                    
                if 'MINI' in fields or 'MAXI' in fields :
                    raise Exception("fichier {}, ligne {} : le mode de maillage 'MinMax' n'est pas implémenté".format(*self.input_lines['origin'][l]))
                
                subWord = fields[1]
                continue
            
            elif subWord is not None :
                if   subWord == 'X' : X += [round(float(v),5) for v in fields]
                elif subWord == 'Y' : Y += [round(float(v),5) for v in fields]
                elif subWord == 'Z' : Z += [round(float(v),5) for v in fields]
                
        #----------------------------------------------------------------------
        if len(X) == 0 : X = [0.0,1.0]
        if len(Y) == 0 : Y = [0.0,1.0]
        if len(Z) == 0 : Z = [0.0,1.0]
        
        #----------------------------------------------------------------------
        for dim,V in [('X',X), ('Y',Y), ('Z',Z)] :
           self.meshs[dim] = Mesh(path=[Calcul.COORD_NAME, dim],
                                  dimension=dim,
                                  edges=V)
        
        #----------------------------------------------------------------------
        Ns = [self.meshs[dim].N for dim in ['X','Y','Z']]
        print('OK ({} x {} x {} = {} mailles)'.format(*Ns, np.prod(Ns)))
        
    #==========================================================================
    def configure_zones(self) :
        #----------------------------------------------------------------------
        print("   - préparation des matériaux ... ", end="", flush=True)
        self.zones = {}
        
        #----------------------------------------------------------------------
        keywords = ['LOCA']
        input_llines = [(l,line) for l,line in enumerate(self.input_lines['raw']) if self.input_lines['key_word'][l] in keywords]
        
        #----------------------------------------------------------------------
        NX,NY,NZ = [self.meshs[dim].N for dim in ['X','Y','Z']]
        names = []
        
        #----------------------------------------------------------------------
        nb_p = 0
        nb_s = 0
        
        axes_paths = {dim:self.meshs[dim].path for dim in ['X','Y','Z']}
                             
        #----------------------------------------------------------------------
        for zi,(l,line) in enumerate(input_llines) :
            fields = []
            for field in line.split() :
                field = field.strip()
                if field == '' : continue
                if field.upper() == 'ID' : field = 'ID'
                fields.append(field)
            
            #------------------------------------------------------------------
            if 'ID' not in [field.upper() for field in fields] :
                raise Exception("fichier {}, ligne {} : champ 'ID' manquant".format(*self.input_lines['origin'][l]))
            
            #------------------------------------------------------------------
            name = fields[[f for f,field in enumerate(fields) if field=='ID'][-1]+1]
            if name in names :
                raise Exception("fichier {}, ligne {} : zone '{}' déjà définie".format(*self.input_lines['origin'][l], name))
            names.append(name)
            
            #------------------------------------------------------------------
            if line.count("(") == 2 and line.count(")") == 2 : # zone primaire
                coords = (line.split("(")[1].split(")")[0] + ' ' + line.split("(")[2].split(")")[0]).split()
                if len(coords) != 6 :
                    raise Exception("fichier {}, ligne {} : la zone doit être définie par 6 coordonnées, {} trouvées".format(*self.input_lines['origin'][l], len(coords)))
                
                #--------------------------------------------------------------
                if 'COOR' in fields : # mode "coordonnées"
                    x0,y0,z0,x1,y1,z1 = [round(float(coord),10) for coord in coords]
                    i0 = self.meshs['X'].coord_to_index(x0, 'left')
                    i1 = self.meshs['X'].coord_to_index(x1, 'right')
                    j0 = self.meshs['Y'].coord_to_index(y0, 'left')
                    j1 = self.meshs['Y'].coord_to_index(y1, 'right')
                    k0 = self.meshs['Z'].coord_to_index(z0, 'left')
                    k1 = self.meshs['Z'].coord_to_index(z1, 'right')
                    
                    si = [name for name,i in [('i0',i0),('j0',j0),('k0',k0),('i1',i1),('j1',j1),('k1',k1)] if i is None]
                    if len(si) > 0 :
                        raise Exception("fichier {}, ligne {} : coordonnée{plu} {li} invalide{plu}".format(*self.input_lines['origin'][l], plu='s' if len(si) > 1 else '', li=','.join(si)))
                    
                #--------------------------------------------------------------
                else : # mode "indices"
                    i0,j0,k0,i1,j1,k1 = [int(coord) for coord in coords]
                    x0 = self.meshs['X'].edges[i0]
                    x1 = self.meshs['X'].edges[i1+1]
                    y0 = self.meshs['Y'].edges[j0]
                    y1 = self.meshs['Y'].edges[j1+1]
                    z0 = self.meshs['Z'].edges[k0]
                    z1 = self.meshs['Z'].edges[k1+1]
                    si  = [name for name,i in [('i0',i0),('j0',j0),('k0',k0)] if i < 1]
                    si += [name for name,i,m in [('i1',i1,NX),('j1',j1,NY),('k1',k1,NZ)] if i > m]
                    if len(si) > 0 :
                        raise Exception("fichier {}, ligne {} : indice{plu} {li} invalide{plu}".format(*self.input_lines['origin'][l], plu='s' if len(si) > 1 else '', li=','.join(si)))
                
                #--------------------------------------------------------------
                self.zones[name] = Cuboid(path        = [Calcul.ZONES_NAME,Porflow.PRIMARY_NAME,name],
                                          zone_type   = 'primary',
                                          dimensions  = ['X','Y','Z'],
                                          coordinates = (x0,x1,y0,y1,z0,z1),
                                          indices     = (i0,i1,j0,j1,k0,k1),
                                          axes_paths  = axes_paths,
                                          zone_index  = zi+1,
                                          final_zone  = False)
                nb_p += 1
                
            #------------------------------------------------------------------
            else : # zone secondaire
                sub_zones_names = []
                invert = inter = union = False
                #--------------------------------------------------------------
                for f,field in enumerate(fields) :
                    if field.upper() == "ID" :
                        _name = fields[f+1]
                        if _name == name : continue
                        if _name not in names :
                            raise Exception("fichier {}, ligne {} : zone '{}' inconnue".format(*self.input_lines['origin'][l], _name))
                        sub_zones_names.append(_name)

                    elif field.upper()      == "NOT"  : invert = True
                    elif field.upper()[0:4] == "INTE" : inter  = True
                    elif field.upper()[0:4] == "UNIO" : union  = True
                
                #--------------------------------------------------------------
                if   inter and invert     : operation = "NOT_INTER"
                elif inter and not invert : operation = "INTER"
                elif union                : operation = "UNION"
                
                #--------------------------------------------------------------
                sub_zones = ["/".join(self.zones[sub_name].path) for sub_name in sub_zones_names]
                self.zones[name] = PolyCuboid(path         = [Calcul.ZONES_NAME,Porflow.SECONDARY_NAME,name],
                                              zone_type    = 'secondary',
                                              sub_paths    = sub_zones,
                                              operation    = operation,
                                              axes_paths   = axes_paths,
                                              zone_index   = zi+1,
                                              final_zone   = False)
                
                nb_s += 1
            
        #----------------------------------------------------------------------
        self.zones_by_path = {"/".join(zone.path):zone for zone in self.zones.values()}
        
        #----------------------------------------------------------------------
        cmap = mpl.colormaps['gist_rainbow']
        norm = mpl.colors.Normalize(vmin=0, vmax=len(self.zones.keys())-1)
        colors = [mpl.colors.rgb2hex(cmap(norm(zone.get_attribute('zone_index')-1))) for zone in self.zones.values()]
        random.seed(25072020)
        #----------------------------------------------------------------------
        for zone in self.zones.values() :
            zone.set_style(color=colors[zone.get_attribute('zone_index')-1])
            
        #----------------------------------------------------------------------
        print('OK ({} matériaux, {} primaires, {} secondaires)'.format(nb_p+nb_s, nb_p, nb_s))
        
    #==========================================================================
    def configure_props(self) :
        #----------------------------------------------------------------------
        print("   - préparation des propriétés ... ", end="", flush=True)
        self.props = {}
        
        #----------------------------------------------------------------------
        keywords = ['PORO','HYDR','TRAN','COND']
        #----------------------------------------------------------------------
        p_names_by_kw = {}
        p_names_by_kw['PORO'] = ['Poro']
        p_names_by_kw['HYDR'] = ['Comp','Kx','Ky','Kz']
        p_names_by_kw['TRAN'] = ['Delay','Dm','Disp_L','Disp_T']
        
        #----------------------------------------------------------------------
        for kw in keywords :
            input_llines = [(l,line) for l,line in enumerate(self.input_lines['raw']) if self.input_lines['key_word'][l] == kw]
            
            for l,line in input_llines :
                fields = [field for field in line.strip().split() if field not in ['=']]
                fields4 = [field[:4].upper() for field in fields]
                
                zone_name = fields[fields.index('ID')+1]
                if zone_name not in self.zones.keys() :
                    raise Exception("fichier {}, ligne {} : zone '{}' inconnue".format(*self.input_lines['origin'][l], zone_name))
                
                self.zones[zone_name].set_attributes(final_zone=True)
                
                num_fields = [to_float(field) for field in fields if to_float(field) is not None]
                
                #--------------------------------------------------------------
                if 'TABL' in fields4 :
                    func = fields4[fields4.index('TABL')+1]
                    if func not in ['LINE','STEP'] :
                        raise Exception("fichier {}, ligne {} : la fonction '{}' n'est pas implémentée".format(*self.input_lines['origin'][l]), func)
                    
                    times = []
                    values = []
                    N = int(num_fields.pop(0))
                    for n in range(N) :
                        time = num_fields.pop(0)
                        value = num_fields.pop(0)
                        if func == 'STEP' and len(times) > 0 and n < N-1 :
                            times.append(time)
                            values.append(values[-1])
                        times.append(time)
                        values.append(value)
                    
                    if times[0] != 0.0 :
                        raise Exception("fichier {}, ligne {} : les temps ne commencent pas à 0 -> vérifier le comportement !".format(*self.input_lines['origin'][l]))
                    
                    if   kw == 'PORO'                      : p_names = [p_names_by_kw['PORO'][0]]
                    elif kw == 'COND' and fields[1] == 'P' : p_names = p_names_by_kw['HYDR'][1:4]
                    elif kw == 'COND' and fields[1] == 'C' : p_names = [p_names_by_kw['TRAN'][1]]
                    
                    for p_name in p_names :
                        self.props[(p_name, zone_name)] = Matrix(path        = [Calcul.PROPS_NAME,p_name,zone_name],
                                                                 dimensions  = ['T'],
                                                                 axes        = {'T':times},
                                                                 sizes       = {'T':len(times)},
                                                                 variable    = p_name,
                                                                 M           = values)
                    
                #--------------------------------------------------------------
                else :
                    if kw == 'COND' :
                        raise Exception("fichier {}, ligne {} : propriété 'COND' non implémentée".format(*self.input_lines['origin'][l]))
                        
                    for v,prop_name in enumerate(p_names_by_kw[kw]) :
                        self.props[(prop_name, zone_name)] = Constant(path=[Calcul.PROPS_NAME,prop_name,zone_name],
                                                                      value=num_fields[v],
                                                                      zone_name=zone_name,
                                                                      prop_name=prop_name)
                
        #----------------------------------------------------------------------
        _zones,_props = [],[]
        for prop_name, zone_name in self.props.keys() :
            if prop_name not in _props : _props.append(prop_name)
            if zone_name not in _zones : _zones.append(zone_name)
        print('OK (propriétés {} définies pour {} zones)'.format(','.join(_props), len(_zones)))
        
    #==========================================================================
    def get_cells(self, zone, h=1) :
        #----------------------------------------------------------------------
        cells = self.cells_by_zone.get(zone.label,None)
        if cells is not None : return cells
        
        #----------------------------------------------------------------------
        zone_type = zone.get_attribute('zone_type')
        
        #----------------------------------------------------------------------
        if zone_type == 'primary' :
            i0,i1,j0,j1,k0,k1 = zone.indices
            cells = np.array(list(product(range(i0,i1+1),range(j0, j1+1),range(k0, k1+1))))
        
        #----------------------------------------------------------------------
        elif zone_type == 'secondary' :
            sub_zones = [self.zones_by_path[path] for path in zone.sub_paths]
            operation = zone.operation
            
            concat = [self.get_cells(_zone, h+1) for _zone in sub_zones]
            _cells,_counts = np.unique(np.concatenate(concat), axis=0, return_counts=True)
            if   operation == 'UNION'     : cells = _cells
            elif operation == 'NOT_INTER' : cells = _cells[np.where(_counts==1)[0]]
            elif operation == 'INTER'     : cells = _cells[np.where(_counts>1)[0]]
            
        #----------------------------------------------------------------------
        self.cells_by_zone[zone.label] = cells
        return cells
        
    #==========================================================================
    def configure_final_zones(self) :
        #----------------------------------------------------------------------
        print("   - configuration des matériaux finaux ... ", end="", flush=True)
        
        #----------------------------------------------------------------------
        nb_zones = len(self.zones.keys())
        if   nb_zones <= 255 : dtype = 'uint8'
        elif nb_zones <= 65535 : dtype = 'uint16'
        else : dtype = 'uint32'
        
        #----------------------------------------------------------------------
        axes_paths = {dim:self.meshs[dim].path for dim in ['X','Y','Z']}
        sizes      = {dim:self.meshs[dim].N for dim in ['X','Y','Z']}
        #----------------------------------------------------------------------
        final_zone = Matrix(path       = [Calcul.ZONES_NAME,Porflow.FINAL_ZONE_NAME],
                            dimensions = ['X','Y','Z'],
                            axes_paths = axes_paths,
                            sizes      = sizes,
                            dtype      = dtype,
                            null_value = 0,
                            zone_type  = 'final',
                            vmin       = 1,
                            vmax       = nb_zones,
                            zone_index = nb_zones+1,
                            )
        #----------------------------------------------------------------------
        final_zone.create(array_path=get_temp_path(self.dirpath, element=final_zone))
        
        #----------------------------------------------------------------------
        sorted_zones = [zone for zone in sorted(self.zones.values(), key=lambda e:e.get_attribute('zone_index'))]
        n = 0
        for zone in sorted_zones :
            if zone.get_attribute('zone_type') == 'final' : continue # ne devrait pas arriver
            if not zone.get_attribute('final_zone') : continue
            
            zone_type = zone.get_attribute('zone_type')
            zone_index = zone.get_attribute('zone_index')
            
            if zone_type == 'primary' :
                i0,i1,j0,j1,k0,k1 = zone.indices
                final_zone.M[i0:i1+1,j0:j1+1,k0:k1+1] = zone_index
                
            elif zone.get_attribute('zone_type') == 'secondary' :
                for i,j,k in self.get_cells(zone) :
                    final_zone.M[i,j,k] = zone_index
            
            n += 1
        #----------------------------------------------------------------------
        self.zones[Porflow.FINAL_ZONE_NAME] = final_zone
        
        #----------------------------------------------------------------------
        print("OK ({} matériaux finaux)".format(n))
        
    #==========================================================================
    def check_final_zones(self) :
        #----------------------------------------------------------------------
        print("> Vérification des matériaux")
        
        #----------------------------------------------------------------------
        bad_zones = []
        cells_by_zone = {}
        final_zones = [zone for zone in sorted(self.zones.values(), key=lambda e:e.get_attribute('zone_index')) if zone.get_attribute('zone_type') != 'final']
        
        #----------------------------------------------------------------------
        print("   - test des {} zones finales ... ".format(len(final_zones)), end="", flush=True)
        #----------------------------------------------------------------------
        for z,z1 in enumerate(final_zones) :
            zone1_type = z1.get_attribute('zone_type')
            if   zone1_type == 'primary' : i0,i1,j0,j1,k0,k1 = z1.indices
            elif zone1_type == 'secondary' and z1.label not in cells_by_zone.keys() : cells_by_zone[z1.label] = self.get_cells(z1)

            for z,z2 in enumerate(final_zones[z+1:], start=z+1) :
                zone2_type = z2.get_attribute('zone_type')
                if   zone2_type == 'primary' : _i0,_i1,_j0,_j1,_k0,_k1 = z2.indices
                elif zone2_type == 'secondary' and z2.label not in cells_by_zone.keys() : cells_by_zone[z2.label] = self.get_cells(z2)
                
                common_props = []
                for (prop_name,zone_name),prop in self.props.items() :
                    if zone_name == z1.label and (prop_name,z2.label) in self.props.keys() :
                        if prop_name not in common_props :
                            common_props.append(prop_name)
                if len(common_props) == 0 : continue
                
                if zone1_type == 'primary' :
                    if zone2_type == 'primary' :
                        if (_i1 < i0 or _i0 > i1) or (_j1 < j0 or _j0 > j1) or (_k1 < k0 or _k0 > k1) : continue # disjoint
                        else : bad_zones.append((z1.label,z2.label,common_props))
                    elif zone2_type == 'secondary' :
                        for _i,_j,_k in cells_by_zone[z2.label] :
                            if (_i < i0 or _i > i1) or (_j < j0 or _j > j1) or (_k < k0 or _k > k1) : continue # disjoint
                            else : bad_zones.append((z1.label,z2.label,common_props)) ; break
                elif zone1_type == 'secondary' :
                    if zone2_type == 'primary' :
                        for i,j,k in cells_by_zone[z1.label] :
                            if (i < _i0 or i > _i1) or (j < _j0 or j > _j1) or (k < _k0 or k > _k1) : continue # disjoint
                            else : bad_zones.append((z1.label,z2.label,common_props)) ; break
                    elif zone2_type == 'secondary' :
                        for key in cells_by_zone[z1.label] :
                            if key in cells_by_zone[z2.label] : bad_zones.append((z1.label,z2.label,common_props)) ; break
                        
        #----------------------------------------------------------------------
        print("OK")
        
        #----------------------------------------------------------------------
        print("   - conflits de propriété ... ", end="", flush=True)
        if len(bad_zones) == 0 : print("aucun conflit détecté :)")
        else : print("{} conflit(s) détecté(s) :".format(len(bad_zones)))
        for z1,z2,common_props in bad_zones[:10] :
            print("      - zones {} et {} : {}".format(z1,z2,", ".join(common_props)))
        if len(bad_zones) > 10 :
            print("      - ...")
        
        #----------------------------------------------------------------------
        print("   - mailles sans propriétés ... ", end="", flush=True)
        final_zone = None
        for zone in self.zones.values() :
            if zone.get_attribute('zone_type') == 'final' :
                final_zone = zone
                break
        #----------------------------------------------------------------------
        if final_zone is None : print("zone finale non calculée")
        #----------------------------------------------------------------------
        else :
            I = np.where(final_zone.M == 0)
            ni = len(I[0])
            
            if ni == 0 : print("aucune maille détectée :)")
            else :
                print("{} maille(s) détectée(s) :".format(ni))
                for i,j,k in zip(I[0][:10],I[1][:10],I[2][:10]) :
                    
                    mzones = []
                    for zone in self.zones.values() :
                        if (i,j,k) in self.get_cells(zone) :
                            mzones.append(zone.label)
                            
                    msg  = "      - ({},{},{}) => ".format(i,j,k)
                    msg += ",".join(["{}({:.2e},{:.2e})".format(dim.lower(),self.meshs[dim].edges[i],self.meshs[dim].edges[i+1]) for dim in ['X','Y','Z']])
                    msg += " : "+', '.join(mzones)
                    print(msg)
                    
                if ni > 10 :
                    print("      - ...")
                
        #----------------------------------------------------------------------
        print("> Vérification terminée !")
        
    #==========================================================================
    def configure_hist(self) :
        #----------------------------------------------------------------------
        print("   - préparation des sorties HIST :")
        self.hists = []
        
        #----------------------------------------------------------------------
        input_llines = [(l,line) for l,line in enumerate(self.input_lines['raw']) if self.input_lines['key_word'][l] == 'HIST']
        filepaths = []
        for l,line in input_llines :
            if line.count("'") < 2 : continue
            filename = line.split("'")[1]
            filepath = os.path.join(self.dirpath, filename)
            if filepath in filepaths : continue
            filepaths.append(filepath)
    
        #----------------------------------------------------------------------
        data = {}
        points = []
        #----------------------------------------------------------------------
        for filepath in filepaths :
            filename = os.path.basename(filepath)
            print("      - {} ... ".format(filename), end="", flush=True)
            
            #------------------------------------------------------------------
            if not os.path.exists(filepath) :
                print('Echec (fichier introuvable)')
                continue
            
            #------------------------------------------------------------------
            renamed = {}
            T = np.genfromtxt(filepath, delimiter=None, skip_header=12, dtype=None, encoding='utf-8')
            #------------------------------------------------------------------
            keys = []
            for line in T :
                var = line[1]
                point = (line[2],line[3],line[4])
                key = (var,point)
                if key in keys : continue
                keys.append(key)
                if point not in points : points.append(point)
                
            #------------------------------------------------------------------
            for var,point in keys :
                if (var,point) in data.keys() :
                    suffix = 2
                    while (var+str(suffix),point) in data.keys() : suffix += 1
                    renamed[(var,point)] = var+str(suffix)
                    var = var+str(suffix)
                data[(var,point)] = {'times':[], 'values':[], 'filename':filename}
                
            #------------------------------------------------------------------
            for line in T :
                _var = line[1]
                point = (line[2],line[3],line[4])
                var = renamed.get((_var,point),_var)
                data[(var,point)]['times'].append(line[5])
                data[(var,point)]['values'].append(line[6])
                
            #------------------------------------------------------------------
            print("OK ({} valeurs)".format(len(T)))
            
            #------------------------------------------------------------------
            for (var,point),newvar in renamed.items() :
                print("         -> renommage Point{}({}) : {} -> {}".format(points.index(point)+1, point, var, newvar))
            
        #----------------------------------------------------------------------
        for var,point in data.keys() :
            times = data[(var,point)]['times']
            values = data[(var,point)]['values']
            
            path = [Calcul.RESULTS_NAME, Porflow.HIST_NAME, var, "Point{}".format(points.index(point)+1)]
            label = "{}_{}({:.2g},{:.2g},{:.2g})".format(Porflow.HIST_NAME, var, *point)
            
            matrix = Matrix(path        = path,
                            label       = label,
                            dimensions  = ['T'],
                            axes        = {'T':times},
                            sizes       = {'T':len(times)},
                            filename    = data[(var,point)]['filename'],
                            variable    = var,
                            point       = point,
                            # fields      = ['values'],
                            )
            matrix.create(array_path=get_temp_path(self.dirpath, element=matrix))
            matrix.M[:] = values[:]
            self.hists.append(matrix)
            
    #==========================================================================
    def configure_flux(self) :
        #----------------------------------------------------------------------
        print("   - préparation des sorties FLUX :")
        self.fluxs = []
        
        #----------------------------------------------------------------------
        input_llines = [(l,line) for l,line in enumerate(self.input_lines['raw']) if self.input_lines['key_word'][l] == 'FLUX']
        filepaths = []
        for l,line in input_llines :
            if line.count("'") < 2 : continue
            filename = line.split("'")[1]
            filepath = os.path.join(self.dirpath, filename)
            if filepath in filepaths : continue
            filepaths.append(filepath)
        
        #----------------------------------------------------------------------
        data = {}
        #----------------------------------------------------------------------
        for filepath in filepaths :
            filename = os.path.basename(filepath)
            print("      - {} ... ".format(filename), end="", flush=True)

            if not os.path.exists(filepath) :
                print('Echec (fichier introuvable)')
                continue
            
            #------------------------------------------------------------------
            file = open(filepath, 'r')
            key_by_id = {}
            skiprows = None
            renamed = {}
            #------------------------------------------------------------------
            for l,line in enumerate(file) :
                line = line.strip()
                if l == 0 : continue
                if line == '' :
                    skiprows = l+5
                    break
                #--------------------------------------------------------------
                fields = line.split()
                data_id = int(fields[0])
                var = fields[1]
                face = fields[5]+"_"+fields[4]
                #--------------------------------------------------------------
                if (var,face) in data.keys() :
                    suffix = 2
                    while (var+str(suffix),face) in data.keys() : suffix += 1
                    renamed[(var,face)] = var+str(suffix)
                    var = var+str(suffix)
                #--------------------------------------------------------------
                key_by_id[data_id] = (var,face)
                data[(var,face)] = {'filename':filename}
                
            #------------------------------------------------------------------
            file.close()
            print("OK")
            
            #------------------------------------------------------------------
            for (var,face),newvar in renamed.items() :
                print("         -> renommage {} : {} -> {}".format(face, var, newvar))
                
            #------------------------------------------------------------------
            T = np.loadtxt(filepath, delimiter=None, skiprows=skiprows)
            #------------------------------------------------------------------
            if   len(T) <= 255 : dtype = np.uint8
            elif len(T) <= 65535 : dtype = np.uint16
            else : dtype = np.uint32
            data_ids = np.array(T[:,0], dtype=dtype)
            #------------------------------------------------------------------
            C = [c for c,output in enumerate(Porflow.FLUX_OUTPUTS) if output is not None]
            H = [output for output in Porflow.FLUX_OUTPUTS if output is not None]
            #------------------------------------------------------------------
            for data_id,(var,face) in key_by_id.items() :
                I = np.where(data_ids==data_id)[0]
                path = [Calcul.RESULTS_NAME, Porflow.FLUX_NAME, var, face]
                label = "{}_{}_{}".format(Porflow.FLUX_NAME, var, face)
                matrix = Matrix(path       = path,
                                label      = label,
                                dimensions = ['T',Matrix.FIELDS_NAME],
                                axes       = {'T':T[I,1]},
                                sizes      = {'T':len(I), Matrix.FIELDS_NAME:len(C)},
                                filename   = data[(var,face)]['filename'],
                                variable   = var,
                                face       = face,
                                fields     = H,
                                )
                matrix.create(array_path=get_temp_path(self.dirpath, element=matrix))
                for _c,c in enumerate(C) : matrix.M[:,_c] = T[I,c]
                self.fluxs.append(matrix)
            
    #==========================================================================
    def configure_save(self) :
        #----------------------------------------------------------------------
        print("   - préparation des sorties SAVE :")
        self.saves = []
        
        #----------------------------------------------------------------------
        input_llines = [(l,line) for l,line in enumerate(self.input_lines['raw']) if self.input_lines['key_word'][l] in ['READ','SAVE']]
        
        #----------------------------------------------------------------------
        links = {}
        if platform.system() == 'Windows' :
            shell = win32com.client.Dispatch("WScript.Shell")
            for f in os.scandir(self.dirpath) :
                if not f.name.endswith('.lnk') : continue
                shortcut = shell.CreateShortcut(f.path)
                target_path = shortcut.TargetPath
                links[os.path.basename(target_path).lower()] = target_path
        
        #----------------------------------------------------------------------
        filenames = []
        for l,line in input_llines :
            if line.count("'") < 2 : continue
            filename = line.split("'")[1]
            if filename in filenames : continue
            filenames.append(filename)
            
        #----------------------------------------------------------------------
        for filename in filenames :
            filepath = os.path.join(self.dirpath, filename)
            link_relpath = None
            
            #------------------------------------------------------------------
            if not os.path.exists(filepath) and filename.lower() in links.keys() :
                filepath = links[filename.lower()]
                link_relpath = os.path.relpath(os.path.dirname(filepath), self.dirpath)+"/."
            
            #------------------------------------------------------------------
            print("      - {}{} : ".format(filename, " (link)" if link_relpath is not None else ''), end="", flush=True)
            
            #------------------------------------------------------------------
            if not os.path.exists(filepath) :
                print('Echec (fichier introuvable)')
                continue
            
            #------------------------------------------------------------------
            first_add = True
            variable = None
            Emax = 1 # nombre d'edges
            Mmax = 1 # nombre de mailles, avec 2 boundaries
            
            times_by_record = {} # [record] = time
            data = {} # [variable][step]
            
            prev_record = None
            file = open(filepath, 'r')
            for line in file :
                line = line.strip()
                
                #--------------------------------------------------------------
                if 'DIRECTION NODES' in line :
                    fields = line.split()
                    dim = fields[1]
                    N = int(fields[0])-2
                    
                    if self.meshs[dim] is not None : _N = self.meshs[dim].N
                    if _N != N :
                        print("Echec : dimension '{}' incohérente ({}, {})".format(dim, N, _N))
                        break
                    
                    if   dim == 'X' : NX = N
                    elif dim == 'Y' : NY = N
                    elif dim == 'Z' : NZ = N
                    
                    Emax *= (N+1)
                    Mmax *= (N+2)
                    continue
                
                #--------------------------------------------------------------
                if 'RECORD' in line :
                    fields = line.split(",")
                    record = int(fields[0].replace("%RECORD% # =",""))
                    step = int(fields[1].replace("STEP # =",""))
                    time = float(fields[2].replace("TIME =",""))
                    line2 = file.readline().strip()
                    fields2 = line2.split()
                    variable = fields2[0].replace("-","")
                    
                    if record != prev_record :
                        first_add = True
                        print("")
                        print("         - record {} : ".format(record), end="", flush=True)
                    prev_record = record
                    
                    if record not in times_by_record.keys() :
                        times_by_record[record] = time
                        
                    if variable == 'MTYP' :
                        variable = None
                        continue
                    
                    if record == 0 and variable not in ['MTYP','X','Y','Z','XC','YC','ZC'] :
                        variable = None
                        continue
                    
                    if variable in ['XC','YC','ZC'] : Nmax = Emax
                    else : Nmax = Mmax
                    
                    N = int(line2.split("VALUES")[-2].split()[-1])
                    if N != Nmax :
                        variable = None
                        continue
                    
                    values = []
                    continue
                
                #--------------------------------------------------------------
                if variable is None : continue
                
                #--------------------------------------------------------------
                values += [float(field) for field in line.split()]
                if len(values) == Nmax :
                    if not first_add : print(",", end="", flush=True)
                    # print("{}[{}]".format(variable, record), end="", flush=True)
                    print(variable, end="", flush=True)
                    first_add = False
                    
                    #----------------------------------------------------------
                    values = np.array(values, dtype='float')
                    
                    #----------------------------------------------------------
                    if variable in ['X','Y','Z'] : # centres + 2 bordures
                        M = np.reshape(values, (NZ+2, NY+2, NX+2))
                        X = np.unique(M[1:-1,1:-1,1:-1]) # suppression des mailles de bordure
                        
                        _X = None
                        if   variable == 'X' and self.meshs['X'] is not None : _X = self.meshs['X'].centers
                        elif variable == 'Y' and self.meshs['Y'] is not None : _X = self.meshs['Y'].centers
                        elif variable == 'Z' and self.meshs['Z'] is not None : _X = self.meshs['Z'].centers
                        
                        if _X is not None and not np.array_equal(X, _X) :
                            print("Echec : centres des mailles incohérents suivant '{}'".format(variable))
                            break
                        
                    #----------------------------------------------------------
                    elif variable in ['XC','YC','ZC'] : # edges (C pour Corner)
                        M = np.reshape(values, (NZ+1, NY+1, NX+1))
                        X = np.unique(M)
                        
                        _X = None
                        if   variable == 'XC' and self.meshs['X'] is not None : _X = self.meshs['X'].edges
                        elif variable == 'YC' and self.meshs['Y'] is not None : _X = self.meshs['Y'].edges
                        elif variable == 'ZC' and self.meshs['Z'] is not None : _X = self.meshs['Z'].edges
                        
                        if _X is not None and not np.array_equal(X, _X) :
                            print("Echec : bordures de mailles incohérents suivant '{}'".format(variable[0]))
                            break
                        
                    #----------------------------------------------------------
                    else :
                        M = np.reshape(values, (NZ+2, NY+2, NX+2)) # centres + 2 bordures
                        array_path = get_temp_path(self.dirpath, name="{}_{}_{}".format(variable,record,step))
                        _M = np.memmap(array_path, dtype=np.float32, mode='w+', shape=(NX,NY,NZ))
                        _M[:] = M[1:-1,1:-1,1:-1].T
                        if variable not in data.keys() : data[variable] = {}
                        if step in data[variable] : raise Exception("le step {} est déjà renseigné pour la variable '{}'".format(step, variable))
                        data[variable][record] = _M
                        
            #------------------------------------------------------------------
            file.close()
            
            #------------------------------------------------------------------
            print("")
            print("         - création des matrices ... ", end="", flush=True)
            for variable in data :
                records = sorted(data[variable].keys())
                
                path = [Calcul.RESULTS_NAME, Porflow.SAVE_NAME, filename, variable]
                axes_paths = {dim:self.meshs[dim].path for dim in ['X','Y','Z']}
                #--------------------------------------------------------------
                if len(records) == 1 and records[0] == 0 : # conditions stables
                    element = Matrix(path       = path,
                                     label      = variable,
                                     dimensions = ['X','Y','Z'],
                                     axes_paths = axes_paths,
                                     sizes      = {'X':NX, 'Y':NY, 'Z':NZ},
                                     filename   = filename,
                                     variable   = variable,
                                     )
                    element.create(array_path=get_temp_path(self.dirpath, element=element))
                    element.M = data[variable][records[0]]
                    
                #--------------------------------------------------------------
                else :
                    times = [times_by_record[record] for record in records]
                    element = Matrix(path       = path,
                                     label      = variable,
                                     dimensions = ['X','Y','Z','T'],
                                     axes       = {'T':times},
                                     axes_paths = axes_paths,
                                     sizes      = {'X':NX, 'Y':NY, 'Z':NZ, 'T':len(times)},
                                     filename   = filename,
                                     variable   = variable,
                                     )
                    element.create(array_path=get_temp_path(self.dirpath, element=element))
                    for t,record in enumerate(records) :
                        element.M[:,:,:,t] = data[variable][record][:]
                    
                #--------------------------------------------------------------
                vmin,vmax = np.nanmin(element.M), np.nanmax(element.M)
                if vmin == vmax : element = Constant(path=path, label=variable, value=vmin)
                
                #--------------------------------------------------------------
                self.saves.append(element)
                
            #------------------------------------------------------------------
            print("OK")
            
    #==========================================================================
    def configure_times(self) :
        #----------------------------------------------------------------------
        print("   - préparation des temps ... ", end="", flush=True)
        #----------------------------------------------------------------------
        times = []
        for hist in self.hists : times += list(hist.axes['T'])
        for flux in self.fluxs : times += list(flux.axes['T'])
        for save in self.saves : times += list(save.axes['T'])
        times = np.unique(times)
        
        #----------------------------------------------------------------------
        self.vects['T'] = Vector(path=[Calcul.COORD_NAME,'T'],
                                 dimension='T',
                                 values=times)
        
        #----------------------------------------------------------------------
        print("OK")
        
    #==========================================================================
    
    
    #==========================================================================
    #---- *** SAVE TO NC ***
    #==========================================================================
    def _save(self, ds) :
        #----------------------------------------------------------------------
        if self.zones is not None :
            print("   - matériaux ... ", end="", flush=True)
            for zone in self.zones.values() : zone.save(ds)
            print("OK")
        
        #----------------------------------------------------------------------
        if self.props is not None :
            print("   - propriétés ... ", end="", flush=True)
            for prop in self.props.values() : prop.save(ds)
            print("OK")
        
        #----------------------------------------------------------------------
        if self.hists is not None :
            print("   - fichiers HIST ... ", end="", flush=True)
            for hist in self.hists : hist.save(ds)
            print("OK")
        
        #----------------------------------------------------------------------
        if self.fluxs is not None :
            print("   - fichiers FLUX ... ", end="", flush=True)
            for flux in self.fluxs : flux.save(ds)
            print("OK")
        
        #----------------------------------------------------------------------
        if self.saves is not None :
            print("   - fichiers SAVE ... ", end="", flush=True)
            for save in self.saves : save.save(ds)
            print("OK")
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** PROGRAM ***
#------------------------------------------------------------------------------
if __name__ == '__main__' :
    # input_path = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/Porflow/Porflow_Simple/ITER_CSA_OG_AlvExp_Ref3.inp"
    input_path = r"C:/Users/jt250258/Documents/Python/TIGRIS/Calculs/ITER_FAVL_SCRMixte_MC_Hydrau/ITER_FAVL_SCRMixte_MC_Hydrau.inp"
    # input_path = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/Porflow/Porflow_dComplexe/Tc99_Forage_49970colis_S1_Kd_NonLabile_Mole.inp"
    conv = Porflow_Convertor(input_path=input_path, check_zones=False)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
