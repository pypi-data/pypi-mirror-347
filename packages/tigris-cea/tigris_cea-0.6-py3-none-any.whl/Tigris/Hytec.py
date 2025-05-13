# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import random
import numpy as np
from itertools import product
#------------------------------------------------------------------------------
import matplotlib as mpl
#------------------------------------------------------------------------------
from Element import Element
from Element_Constants import Vector, Mesh
from Element_Matrix import Matrix
from Element_Cuboids import Cuboid
from Calcul import Calcul, Calcul_Convertor
from utils import get_temp_path, get_now
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Hytec(Calcul) :
    
    #==========================================================================
    CODE      = 'hytec'
    RES_NAME  = 'Results'
    
    #==========================================================================
    def __init__(self) :
        #----------------------------------------------------------------------
        Calcul.__init__(self, Hytec.CODE)
        
        #----------------------------------------------------------------------
        self.zones = None
        self.result = None
        
    #==========================================================================
    def _details(self, **kwargs) :
        #----------------------------------------------------------------------
        print("   - zones".ljust(Element.DETAILS_ALIGN,' ')+": {} matériaux".format(len(self.zones.keys())))
        print("   - résultats".ljust(Element.DETAILS_ALIGN,' ')+": {} variables".format(len(self.result.get_fields())))
        
    #==========================================================================
    def _load(self) :
        #----------------------------------------------------------------------
        self.zones  = {}
        self.result = None
        
        #----------------------------------------------------------------------
        for e in self.elements :
            if   e.path[0] == Calcul.ZONES_NAME   : self.zones[e.label] = e
            elif e.path[0] == Calcul.RESULTS_NAME : self.result = e
        
        #----------------------------------------------------------------------
        for zone in self.zones.values() :
            zone.configure(value=zone.get_attribute('zone_index'))
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Hytec_Convertor(Calcul_Convertor) :
    
    #==========================================================================
    def __init__(self, **opts) :
        #----------------------------------------------------------------------
        Calcul_Convertor.__init__(self, **opts)
        
        #----------------------------------------------------------------------
        self.zones = None
        self.result = None
        
        #----------------------------------------------------------------------
        self.convert(**opts)
        
    #==========================================================================
    def _convert(self, **opts) :
        """
        dirpath, name
        [nc_path]
        """
        #----------------------------------------------------------------------
        print("> Conversion d'un calcul {} :".format(Calcul.CODE_NAMES[Hytec.CODE]))
        
        #----------------------------------------------------------------------
        if 'input_path' not in opts.keys() :
            raise Exception("paramètre 'input_path' manquant")
        
        #----------------------------------------------------------------------
        self.dirpath = opts.get('input_path')
        self.name = opts.get('name', os.path.basename(self.dirpath))
        #----------------------------------------------------------------------
        kwargs = {}
        kwargs[Calcul.ATTR_CODE]     = Hytec.CODE
        kwargs[Calcul.ATTR_CALCUL]   = self.name
        kwargs[Calcul.ATTR_POSTDATE] = get_now(fmt='%d/%m/%Y %H:%M')
        kwargs[Calcul.ATTR_DIRPATH]  = self.dirpath
        #----------------------------------------------------------------------
        self.config = Element(path=[Calcul.CONFIG_NAME], label='config', **kwargs)
        
        #----------------------------------------------------------------------
        self.configure_grid()
        self.configure_zones()
        self.configure_results()
        
    #==========================================================================
    def configure_grid(self) :
        #----------------------------------------------------------------------
        print("   - préparation du maillage ... ", end="", flush=True)
        
        #----------------------------------------------------------------------
        if not os.path.exists(self.dirpath) :
            raise Exception("dossier '{}' introuvable".format(os.path.basename(self.dirpath)))
            
        #----------------------------------------------------------------------
        domain_path = os.path.join(self.dirpath, 'HYTEC_grid', 'domain.dat')
        grid_path   = os.path.join(self.dirpath, 'HYTEC_grid', 'Hgrid.dat')
        #----------------------------------------------------------------------
        for filepath in [domain_path,grid_path] :
            if not os.path.exists(filepath) :
                rpath = os.path.relpath(filepath, self.dirpath).replace("\\","/")
                raise Exception("fichier '.../{}' introuvable".format(rpath))
        
        #----------------------------------------------------------------------
        _centers = {}
        T = np.loadtxt(grid_path, delimiter=None, skiprows=1, usecols=(0,1,2))
        _centers['X'] = np.round(T[:,0],8)
        _centers['Y'] = np.round(T[:,1],8)
        _centers['Z'] = np.full(_centers['X'].shape, 0.5)
        _zone_indices = np.array(T[:,2], dtype=np.int8) # commence à 0
        
        #----------------------------------------------------------------------
        file = open(domain_path, 'r')
        coords = []
        for l,line in enumerate(file) :
            line = line.strip()
            if line == "" : continue
            fields = line.split()
            if l == 0 :
                if fields[1] != 'R2D2' : raise Exception("grille '{}' non gérées".format(fields[1]))
                continue
            coords.append([float(fields[0]),float(fields[1])])
        #----------------------------------------------------------------------
        file.close()
        #----------------------------------------------------------------------
        domain = {}
        if len(coords) > 0  :
            C = np.array(coords)
            NC = C.shape[1]
            for c,dim in enumerate(['X','Y','Z']) :
                if c < NC : domain[dim] = np.nanmin(C[:,c]),np.nanmax(C[:,c])
                else : domain[dim] = 0.0,1.0
        #----------------------------------------------------------------------
        else :
            NC = 0
            for c,dim in enumerate(['X','Y','Z']) :
                domain[dim] = 0.0, _centers[dim][-1] + (_centers[dim][-1]-_centers[dim][-2])/2
        
        #----------------------------------------------------------------------
        edges = {}
        centers = {}
        for dim in ['X','Y','Z'] :
            centers[dim] = np.unique(_centers[dim])
            edges[dim] = [domain[dim][0]]
            for c,center in enumerate(centers[dim]) : edges[dim].append(round(center+center-edges[dim][-1],8))
            edges[dim][-1] = domain[dim][1]
            edges[dim] = np.round(edges[dim],5)
            
            self.meshs[dim] = Mesh(path=[Calcul.COORD_NAME,dim],
                                   dimension=dim,
                                   edges=edges[dim],
                                   centers=centers[dim])
            
        #----------------------------------------------------------------------
        Ns = [self.meshs[dim].N for dim in ['X','Y','Z']]
        print('OK ({} x {} x {} = {} mailles)'.format(*Ns, np.prod(Ns)))
        
        self._temp = {}
        self._temp['centers'] = centers
        self._temp['_centers'] = _centers
        self._temp['_centers'] = _centers
        self._temp['_zone_indices'] = _zone_indices
        
    #==========================================================================
    def configure_zones(self) :
        #----------------------------------------------------------------------
        print("   - préparation des matériaux ... ", end="", flush=True)
        self.zones = {}
        
        #----------------------------------------------------------------------
        zones_path  = os.path.join(self.dirpath, 'HYTEC_grid', 'Hzone.dat')
        if not os.path.exists(zones_path) :
            rpath = os.path.relpath(zones_path, self.dirpath).replace("\\","/")
            raise Exception("fichier '.../{}' introuvable".format(rpath))
        
        #----------------------------------------------------------------------
        axes_paths = {dim:self.meshs[dim].path for dim in ['X','Y','Z']}
        
        #----------------------------------------------------------------------
        file = open(zones_path, 'r')
        zi = -1
        for l,line in enumerate(file) :
            line = line.strip()
            if line == "" : continue
            fields = line.split()
            name = fields[0]
            
            zi += 1
            _I = np.where(self._temp['_zone_indices']==zi)[0]
            
            I = {}
            all_continu = True
            for dim in ['X','Y','Z'] :
                I[dim] = np.unique(np.searchsorted(self._temp['centers'][dim], self._temp['_centers'][dim][_I]))
                
                if list(I[dim]) != list(range(I[dim][0],I[dim][-1]+1)) :
                    all_continu = False
                    raise Exception("la zone '{}' n'est pas continue suivant {}".format(name, dim))
                    
            if all_continu :
                i0,i1 = I['X'][0], I['X'][-1]
                j0,j1 = I['Y'][0], I['Y'][-1]
                k0,k1 = I['Z'][0], I['Z'][-1]
                
                
                x0 = self.meshs['X'].edges[i0]
                x1 = self.meshs['X'].edges[i1+1]
                y0 = self.meshs['Y'].edges[j0]
                y1 = self.meshs['Y'].edges[j1+1]
                z0 = self.meshs['Z'].edges[k0]
                z1 = self.meshs['Z'].edges[k1+1]
                
                self.zones[name] = Cuboid(path        = [Calcul.ZONES_NAME,name],
                                          dimensions  = ['X','Y','Z'],
                                          coordinates = (x0,x1,y0,y1,z0,z1),
                                          indices     = (i0,i1,j0,j1,k0,k1),
                                          axes_paths  = axes_paths,
                                          zone_index  = zi+1, # commence à 1
                                          )
            else :
                raise Exception("la zone '{}' n'est pas continue".format(name))
        #----------------------------------------------------------------------
        file.close()
        
        #----------------------------------------------------------------------
        cmap = mpl.colormaps['gist_rainbow']
        norm = mpl.colors.Normalize(vmin=0, vmax=len(self.zones.keys())-1)
        colors = [mpl.colors.rgb2hex(cmap(norm(zone.get_attribute('zone_index')-1))) for zone in self.zones.values()]
        random.seed(25072020)
        #----------------------------------------------------------------------
        for zone in self.zones.values() :
            zone.set_style(color=colors[zone.get_attribute('zone_index')-1])
            
        #----------------------------------------------------------------------
        print('OK ({} matériaux)'.format(len(self.zones)))
        
    #==========================================================================
    def configure_results(self) :
        #----------------------------------------------------------------------
        print("   - préparation des résultats ... ", end="", flush=True)
        self.result = None
        
        #----------------------------------------------------------------------
        res_path  = os.path.join(self.dirpath, 'HYTEC.res')
        if not os.path.exists(res_path) :
            raise Exception("fichier 'HYTEC.res' introuvable")
        
        #----------------------------------------------------------------------
        times = []
        variables = []
        units = []
        
        #----------------------------------------------------------------------
        file = open(res_path, 'r')
        for l,line in enumerate(file) :
            line = line.strip()
            if not line.startswith('#') : continue
            if 'column' in line :
                fields = line.split()
                variables.append(fields[3])
                units.append(fields[4][1:-1])
            elif 'time' in line :
                times.append(float(line.split()[3]))
        #----------------------------------------------------------------------
        file.close()
        
        #----------------------------------------------------------------------
        if len(variables) == 0 :
            print("Echec (fichier vide)")
            return
        
        #----------------------------------------------------------------------
        NX = self.meshs['X'].N
        NY = self.meshs['Y'].N
        NZ = self.meshs['Z'].N
        NT = len(times)
        
        #----------------------------------------------------------------------
        self.vects['T'] = Vector(path=[Calcul.COORD_NAME,'T'],
                                 dimension='T',
                                 values=times)
        
        #----------------------------------------------------------------------
        path = [Calcul.RESULTS_NAME]
        axes_paths = {dim:self.meshs[dim].path for dim in ['X','Y','Z']}
        axes_paths['T'] = self.vects['T'].path
        self.result = Matrix(path       = path,
                             label      = Calcul.RESULTS_NAME,
                             dimensions = ['X','Y','Z','T','FIELDS'],
                             sizes      = {'X':NX, 'Y':NY, 'Z':NZ, 'T':NT, 'FIELDS':len(variables)},
                             axes_paths = axes_paths,
                             fields     = variables,
                             units      = units,
                             )
        #----------------------------------------------------------------------
        self.result.create(array_path=get_temp_path(self.dirpath, element=self.result))
        #----------------------------------------------------------------------
        I = np.array(list(product(range(NT),range(NZ),range(NY),range(NX))))
        # TODO : vérifier l'ordre d'écriture des coordonnées (x->y->z ou z->y->x)
        
        IX,IY,IZ,IT = I[:,3], I[:,2], I[:,1], I[:,0]
        file = open(res_path, 'r')
        l = -1
        for line in file :
            line = line.strip()
            if line.startswith('#') : continue
            if line == "" : continue
            l += 1
            i,j,k,t = IX[l],IY[l],IZ[l],IT[l]
            self.result.M[i,j,k,t,:] = np.fromstring(line, sep=" ")[:]
        file.close()
        
        #----------------------------------------------------------------------
        Ntot = NX*NY*NZ*NT
        if l+1 != Ntot :
            raise Exception("la longueur du fichier 'HYTEC.res' ({} lignes) est incorrecte ({} lignes attendues)".format(l+1, Ntot))
        
        #----------------------------------------------------------------------
        print("OK ({} instants, {} variables)".format(NT, len(variables)))
        
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
        if self.result is not None :
            print("   - résultats ... ", end="", flush=True)
            self.result.save(ds)
            print("OK")
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#---- *** PROGRAM ***
#------------------------------------------------------------------------------
if __name__ == '__main__' :
    dirpath = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/Hytec/Carb_bench_cas2_473mag5FVaqueous_SA_TM_6"
    # dirpath = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/Hytec/Eurad3Dversion13"
    # dirpath = r"C:/Users/jt250258/Documents/Developpement/Python/TIGRIS/_Calculs/Hytec/HR_73_bagueV3_10mm"
    conv = Hytec_Convertor(dirpath=dirpath, name='test')
    
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
