from __future__ import division, absolute_import, print_function
import sys
import os
import math
import numpy as np
import argparse
from collections import OrderedDict
import logging
#logging.basicConfig(level=logging.INFO)

atnumas = {'LP': ('0', '0'), 'H': ('1', '1'), 'D': ('1', '2'), 'T': ('1', '3'), 'He': ('2', '4'), 'Li': ('3', '7'), 'Be': ('4', '9'), 'B': ('5', '11'), 
'C': ('6', '14'), 'N': ('7', '15'), 'O': ('8', '18'), 'F': ('9', '19'), 'Ne': ('10', '22'), 'Na': ('11', '23'), 'Mg': ('12', '26'), 'Al': ('13', '27'),
'Si': ('14', '30'), 'P': ('15', '31'), 'S': ('16', '36'), 'Cl': ('17', '37'), 'Ar': ('18', '40'), 'K': ('19', '41'), 'Ca': ('20', '48'), 'Sc': ('21', '45'),
'Ti': ('22', '50'), 'V': ('23', '51'), 'Cr': ('24', '54'), 'Mn': ('25', '55'), 'Fe': ('26', '58'), 'Co': ('27', '59'), 'Ni': ('28', '64'), 'Cu': ('29', '65'), 
'Zn': ('30', '70'), 'Ga': ('31', '71'), 'Ge': ('32', '76'), 'As': ('33', '75'), 'Se': ('34', '82'), 'Br': ('35', '81'), 'Kr': ('36', '86'), 'Rb': ('37', '87'), 
'Sr': ('38', '88'), 'Y': ('39', '89'), 'Zr': ('40', '96'), 'Nb': ('41', '93'), 'Mo': ('42', '100'), 'Tc': ('43', '99'), 'Ru': ('44', '104'), 'Rh': ('45', '103'), 
'Pd': ('46', '110'), 'Ag': ('47', '109'), 'Cd': ('48', '116'), 'In': ('49', '115'), 'Sn': ('50', '124'), 'Sb': ('51', '123'), 'Te': ('52', '130'), 'I': ('53', '127'),
'Xe': ('54', '136'), 'Cs': ('55', '133'), 'Ba': ('56', '138'), 'La': ('57', '139'), 'Ce': ('58', '142'), 'Pr': ('59', '141'), 'Nd': ('60', '150'), 'Pm': ('61', '147'), 
'Sm': ('62', '154'), 'Eu': ('63', '153'), 'Gd': ('64', '160'), 'Tb': ('65', '159'), 'Dy': ('66', '164'), 'Ho': ('67', '165'), 'Er': ('68', '170'), 'Tm': ('69', '169'), 
'Yb': ('70', '176'), 'Lu': ('71', '176'), 'Hf': ('72', '180'), 'Ta': ('73', '181'), 'W': ('74', '186'), 'Re': ('75', '187'), 'Os': ('76', '192'), 'Ir': ('77', '193'), 
'Pt': ('78', '198'), 'Au': ('79', '197'), 'Hg': ('80', '204'), 'Tl': ('81', '205'), 'Pb': ('82', '208'), 'Bi': ('83', '209'), 'Po': ('84', '210'), 'At': ('85', '211'), 
'Rn': ('86', '222'), 'Fr': ('87', '223'), 'Ra': ('88', '228'), 'Ac': ('89', '227'), 'Th': ('90', '232'), 'Pa': ('91', '231'), 'U': ('92', '238'), 'Np': ('93', '237'), 
'Pu': ('94', '244'), 'Am': ('95', '243'), 'Cm': ('96', '248'), 'Bk': ('97', '249'), 'Cf': ('98', '252'), 'Es': ('99', '252'), 'Fm': ('100', '257'), 'Md': ('101', '260'), 
'No': ('102', '259'), 'Lr': ('103', '262'), 'Rf': ('104', '267'), 'Db': ('105', '268'), 'Sg': ('106', '271'), 'Bh': ('107', '272'), 'Hs': ('108', '270'), 'Mt': ('109', '276'),
'Ds': ('110', '281'), 'Rg': ('111', '280'), 'Cn': ('112', '285'), 'Nh': ('113', '284'), 'Fl': ('114', '289'), 'Mc': ('115', '288'), 'Lv': ('116', '293'), 'Ts': ('117', '292'),'Og': ('118', '294')}


class Psi4input(): 
    def __init__(self,mol2name,**kwargs): 
        # Option reading ###################
        chrg=None
        mult=None
        outdir=None
        mem="1000Mb"
        cpu=4
        olot=rlot=plot="mp2"
        obasis="6-31+g*"
        rbasis=pbasis="Sadlej"
        qqm = True
        qopt = qpol = qlp = True
        quiet = False
        qwxyz = False
        qwpdb = False
        nobad = True
        symm = False
        reorient = False
        recenter = False
        for kwa,vwa in kwargs.items():
            if kwa.lower() == "chrg":     chrg     = vwa 
            if kwa.lower() == "mult":     mult     = vwa 
            if kwa.lower() == "outdir":   outdir   = vwa 
            if kwa.lower() == "mem":      mem      = vwa 
            if kwa.lower() == "cpu":      cpu      = vwa 
            if kwa.lower() == "olot":     olot     = vwa 
            if kwa.lower() == "obasis":   obasis   = vwa 
            if kwa.lower() == "rlot":     rlot     = vwa 
            if kwa.lower() == "rbasis":   rbasis   = vwa 
            if kwa.lower() == "plot":     plot     = vwa 
            if kwa.lower() == "pbasis":   pbasis   = vwa 
            if kwa.lower() == "noqm":     qqm      = not vwa 
            if kwa.lower() == "noopt":    qopt     = not vwa 
            if kwa.lower() == "nopol":    qpol     = not vwa 
            if kwa.lower() == "nolp":     qlp      = not vwa 
            if kwa.lower() == "noresp":   qresp    = not vwa 
            if kwa.lower() == "nobad":    qwbad    = not vwa 
            if kwa.lower() == "quiet":    quiet    = vwa 
            if kwa.lower() == "qwxyz":    qwxyz    = vwa 
            if kwa.lower() == "qwpdb":    qwpdb    = vwa 
            if kwa.lower() == "symm":     symm     = vwa 
            if kwa.lower() == "reorient": reorient = vwa 
            if kwa.lower() == "recenter": recenter = vwa 
        if not qqm:
           qopt = qpol = qresp = False
        # All options reading done ###################

        self.molinfo = self.readmol2(mol2name)
        _,self.molinfo["bondnums"] = self.findbonds(self.molinfo["atomnames"],self.molinfo["bonds"])
        _,self.molinfo["anglnums"] = self.findangles(self.molinfo["atomnames"],self.molinfo["bonds"])
        _,self.molinfo["dihenums"] = self.finddihedrals(self.molinfo["atomnames"],self.molinfo["bonds"])
        self.molinfo["atomposiang"] = self.molinfo["atomposi"]
        self.molinfo["atomposiau"] = OrderedDict()
        for key,val in self.molinfo["atomposiang"].items():
            valau = val[3]*1.889725989
            self.molinfo["atomposiau"].update({key:[val[0],val[1],val[2],valau]})

        self.molinfo["lpposi"] = OrderedDict() 
        if qlp and not qqm:
            lonepinfo = self.createlonepair(self.molinfo["atomposiang"],self.molinfo["atomnames"],self.molinfo["bonds"])
            self.molinfo["nlps"] = lonepinfo["nlps"]
            self.molinfo["lpnames"] = lonepinfo["lpnames"]
            self.molinfo["lpposi"] = lonepinfo["lpposi"]
            self.molinfo["lpbonds"] = lonepinfo["lpbonds"] 
            self.molinfo["allnames"] = OrderedDict(**(self.molinfo["atomnames"]),**(self.molinfo["lpnames"]))
            self.molinfo["allposi"] = OrderedDict(**(self.molinfo["atomposiang"]),**(self.molinfo["lpposi"]))
            self.molinfo["allbonds"] = self.molinfo["bonds"]  
            for key, value in self.molinfo["lpbonds"].items():
                for v in value:
                    self.molinfo["allbonds"].update({v:[key]})
                    self.molinfo["allbonds"][key].append(v)  
            _,self.molinfo["allbondnums"] = self.findbonds(self.molinfo["allnames"],self.molinfo["allbonds"])
            _,self.molinfo["allanglnums"] = self.findangles(self.molinfo["allnames"],self.molinfo["allbonds"])
            _,self.molinfo["alldihenums"] = self.finddihedrals(self.molinfo["allnames"],self.molinfo["allbonds"])
        
        if outdir is None: outdir = "."

        if qqm:
            if chrg is None:
                chrg = self.molinfo["rescharge"]
            if mult is None:
                ele = []
                for key,val in self.molinfo["atomposi"].items(): 
                    ele.append(val[1]) 
                mult = self.calc_multip(ele,chrg) 

            psi4out = str(os.path.basename(mol2name)).split(".")[0] + ".out"
            self.runPsi4(outdir,psi4out,rescharge=chrg,multiplicity=mult,atomposi=self.molinfo["atomposiang"],mem=mem,cpu=cpu,olot=olot,obasis=obasis,rlot=rlot,rbasis=rbasis,plot=plot,pbasis=pbasis,quiet=quiet,qopt=qopt,qpol=qpol,qlp=qlp,qresp=qresp,symm=symm,reorient=reorient,recenter=recenter)

        if qwbad: 
            badout = str(os.path.basename(mol2name)).split(".")[0] + "_nolp.txt"
            self._printbad(outdir,badout)
            if qlp: 
               lpbadout = str(os.path.basename(mol2name)).split(".")[0] + "_atlp.txt"
               self._printbadlp(outdir,lpbadout)

        if qqm and qlp: 
            crpout = str(os.path.basename(mol2name)).split(".")[0] + "._crp.txt"
            self._printcrp(outdir,crpout,"allposi")
        elif qqm and not qlp: 
            crpout = str(os.path.basename(mol2name)).split(".")[0] + "._crp.txt"
            self._printcrp(outdir,crpout,"atomposiang")

        if qwxyz and qlp: 
            xyzout = str(os.path.basename(mol2name)).split(".")[0] + ".xyz"
            self._printxyz(outdir,xyzout,self.molinfo["allposi"])

        if qwpdb and qlp: 
            pdbout = str(os.path.basename(mol2name)).split(".")[0] + ".pdb"
            self._printpdb(outdir,pdbout,self.molinfo["allposi"])
          
    def readmol2(self,mol2name,resname="resi"):
        """ Read atomnames, element, position, charges, and bonds"""
        foundatm=False
        foundbnd=False
        
        with open(mol2name,"r") as filein:
            ind = 0
            chrg = 0.0
            for line in filein:
                field = line.split()  
                if "@<TRIPOS>" in field[0].strip() and field[0].strip("@<TRIPOS>") not in ["MOLECULE","ATOM","BOND"]: break 
                if len(field) != 0 and not foundatm:
                    if field[0] == "@<TRIPOS>ATOM":
                        foundatm=True
                        foundbnd=False
                        totchrg=None
                        atminfo = OrderedDict()
                        posinfo = OrderedDict()
                        inam = {}
                        continue
                elif len(field) != 0 and not foundbnd:
                    if field[0] == "@<TRIPOS>BOND":
                        foundbnd = True
                        foundatm = False
                        bndlist = OrderedDict()
                        continue
                if foundatm and len(field) >= 4:
                    try:
                        ind += 1
                        ele = field[5].split(".")[0]
                        atnam = ele.upper()+str(ind)
                        atminfo[atnam] = ind
                        inam[ind] = atnam
                        pos = np.array(list(map(lambda x:float(x),field[2:5])))
                        posinfo[ind] = [atnam,ele,"XXXXX",pos]
                        chrg = chrg + float(field[-1]) 
                    except (IndexError,ValueError):
                        foundatm = False
                    continue

                if foundbnd and len(field) == 4:
                    try:
                        bndlist[inam[int(field[1])]].append(inam[int(field[2])])
                    except KeyError:
                        bndlist[inam[int(field[1])]]=[inam[int(field[2])]]
                    try:
                        bndlist[inam[int(field[2])]].append(inam[int(field[1])])
                    except KeyError:
                        bndlist[inam[int(field[2])]]=[inam[int(field[1])]]
                    continue    
        totchrg = int(round(chrg))
        filein.close()
        return ({"atomnames":atminfo,"atomposi":posinfo,"bonds":bndlist,"rescharge":totchrg})   

    def findbonds(self,atomlist,listofbonds):
        """Make a list of list of bond pairs with atomnames and atomindices"""
        bonds = []
        bondnum = []
        for key,value in list(listofbonds.items()):
            for val in value:
                if [val,key] not in bonds:
                    bonds.append([key,val])
                    bondnum.append([atomlist[key],atomlist[val]])
        return(bonds,bondnum)

    def findangles(self,atomlist,listofbonds):
        """Make a list of list of angle triplets with atomnames and atomindices"""
        angles = []
        anglenum = []
        for k0,v0 in list(listofbonds.items()):
            if len(v0) > 1:
               for i in range(0,(len(v0)-1)):
                   ang2 = k0
                   ang1 = v0[i]
                   for j in range(i+1,len(v0)):
                       ang3 = v0[j]
                       angles.append([ang1,ang2,ang3])
                       anglenum.append([atomlist[ang1],atomlist[ang2],atomlist[ang3]])
        return(angles,anglenum)

    def finddihedrals(self,atomlist,listofbonds):
        """Make a list of list of dihedral quads with atomnames and atomindices"""
        dihedrals = []
        dihedralnum = []
        for k0,v0 in list(listofbonds.items()):
            dih0 = k0
            for k1 in v0:
                if len(listofbonds[k1]) != 1:
                   dih1 = k1
                   for k2 in listofbonds[k1]:
                         if len(listofbonds[k2]) != 1 and k2 != dih0:
                             dih2 = k2
                             for k3 in listofbonds[k2]:
                                 if k3 != dih1 and k3 != dih0:
                                    dih3 = k3
                                    if [dih3,dih2,dih1,dih0] not in dihedrals:
                                       dihedrals.append([dih0,dih1,dih2,dih3])
                                       dihedralnum.append([atomlist[dih0],atomlist[dih1],atomlist[dih2],atomlist[dih3]])
        return(dihedrals,dihedralnum)
    
    def calc_multip(self,ele,charge):
        mult=None
        electrons=0
        totelec = 0
        for e in ele:
            totelec = totelec + int(atnumas[e][0])
        if (totelec-charge)%2==0:
            mult=1
        else:
            mult=2
        return mult

    def createlonepair(self,atomposi,ind,bndlst):
        def colinear(ar,scale,hcoor=[]):
            pos = [] 
            if len(hcoor) != 2:
               return
            r_a = list(map(float,hcoor[0][0:3]))
            r_b = list(map(float,hcoor[1][0:3]))
            slope = [r_ai - r_bi for r_ai, r_bi in zip(r_a, r_b)] 
            slope = slope / np.linalg.norm(slope)
            new_x = r_a[0] + ar*scale*slope[0]
            new_y = r_a[1] + ar*scale*slope[1]
            new_z = r_a[2] + ar*scale*slope[2]
            pos = [new_x,new_y,new_z] 
            return pos   

        def relative(ar,ang,dih,hcoor=[]):
            pos = [] 
            if len(hcoor) != 3:
               return
            r_i = list(map(float,hcoor[0][0:3]))
            a_i = list(map(float,hcoor[1][0:3]))
            d_i = list(map(float,hcoor[2][0:3]))

            ar = ar
            ang = ang * np.pi / 180.0
            dih = dih * np.pi / 180.0
            
            sinTheta = np.sin(ang)
            cosTheta = np.cos(ang)
            sinPhi = np.sin(dih)
            cosPhi = np.cos(dih)

            ax = ar * cosTheta
            ay = ar * cosPhi * sinTheta
            az = ar * sinPhi * sinTheta
            
            ad = [a_ii - d_ii for a_ii, d_ii in zip(a_i, d_i)] 
            ra = [r_ii - a_ii for r_ii, a_ii in zip(r_i, a_i)] 
            ra = ra / np.linalg.norm(ra)
            nv = np.cross(ad, ra)
            nv = nv / np.linalg.norm(nv)
            ncra = np.cross(nv, ra)
            
            new_x = r_i[0] - ra[0] * ax + ncra[0] * ay + nv[0] * az
            new_y = r_i[1] - ra[1] * ax + ncra[1] * ay + nv[1] * az
            new_z = r_i[2] - ra[2] * ax + ncra[2] * ay + nv[2] * az
            pos = [new_x,new_y,new_z] 
            return pos   

        def pyramidal(ar,hcoor=[]):
            v1 = []
            v1.append(hcoor[1][0]-hcoor[2][0])
            v1.append(hcoor[1][1]-hcoor[2][1])
            v1.append(hcoor[1][2]-hcoor[2][2])
            v1 = np.array(v1)
            v2 = []
            v2.append(hcoor[1][0]-hcoor[3][0])
            v2.append(hcoor[1][1]-hcoor[3][1])
            v2.append(hcoor[1][2]-hcoor[3][2])
            v2=np.array(v2)
            vc = np.cross(v1,v2)
            length = np.linalg.norm(vc)
            vc = vc/length
            v3 = np.array(hcoor[0])
            vp = np.dot(vc,v3)
            if vp != 0.0:
               projc = v3 - vp*vc
            else:
               projc = vc
            slope = [v3i - projci for v3i, projci in zip(v3, projc)] 
            if np.linalg.norm(slope) == 0.0:
               new_x = v3[0] + ar
               new_y = v3[1] + ar
               new_z = v3[2] + ar
            else:
               slope = slope / np.linalg.norm(slope)
               new_x = v3[0] + ar*slope[0]
               new_y = v3[1] + ar*slope[1]
               new_z = v3[2] + ar*slope[2]
            pos = [new_x,new_y,new_z] 
            return pos   

        #initializing variables
        curntid = len(atomposi.items())
        lpinfo = OrderedDict() 
        lpposi  = OrderedDict() 
        lpbndlst = OrderedDict() 

        for key,val in atomposi.items(): 
            anam = val[0]
            
            # lonepair relative
            if anam[0:1] == "O" and len(bndlst.get(anam)) == 1 or anam[0:1] == "S" and len(bndlst.get(anam)) == 1:
                  hsta = anam
                  hstb = bndlst.get(hsta)[0]
                  hstc = ""
                  if len(bndlst.get(hstb)) == 1:
                      hstc = bndlst.get(hstb)[0]
                  if len(bndlst.get(hstb)) > 1:
                      for atms in bndlst.get(hstb):
                          if atms[0:1] == "H":
                              hstc = bndlst.get(hstb)[bndlst.get(hstb).index(atms)]
                          if atms[0:1] != "H" and atms != hsta:
                              hstc = bndlst.get(hstb)[bndlst.get(hstb).index(atms)]
                              break
                  hcoor = [atomposi[ind[hsta]][3],atomposi[ind[hstb]][3],atomposi[ind[hstc]][3]]
                  curntid += 1
                  lpnam1 = "LP"+str(hsta)+"1"
                  lpinfo[lpnam1] = curntid
                  if hsta[0:1] == "O": lpposi[curntid] = [lpnam1,"LP","LPDO1",relative(0.35,110.0,0.0,hcoor)] 
                  if hsta[0:1] == "S": lpposi[curntid] = [lpnam1,"LP","LPDO1",relative(0.75,95.0,0.0,hcoor)] 
                  try:
                      lpbndlst[hsta].append(lpnam1)
                  except KeyError:
                      lpbndlst[hsta]=[lpnam1]
                  curntid += 1
                  lpnam2 = "LP"+str(hsta)+"2"
                  lpinfo[lpnam2] = curntid
                  if hsta[0:1] == "O": lpposi[curntid] = [lpnam2,"LP","LPDO1",relative(0.35,110.0,180.0,hcoor)] 
                  if hsta[0:1] == "S": lpposi[curntid] = [lpnam2,"LP","LPDO1",relative(0.75,95.0,180.0,hcoor)] 
                  try:
                      lpbndlst[hsta].append(lpnam2)
                  except KeyError:
                      lpbndlst[hsta]=[lpnam2]
                  continue

            # lonepair colinear
            if anam[0:1] == "N" and len(bndlst.get(anam)) == 1 or anam[0:1] == "P" and len(bndlst.get(anam)) == 1:
                  hsta = anam
                  hstb = bndlst.get(anam)[0]
                  hcoor = [atomposi[ind[hsta]][3],atomposi[ind[hstb]][3]]
                  curntid += 1
                  lpnam1 = "LP"+str(hsta)+"1"
                  lpinfo[lpnam1] = curntid
                  lpposi[curntid] = [lpnam1,"LP","LPDN1",colinear(0.35,1.0,hcoor)] 
                  try:
                      lpbndlst[hsta].append(lpnam1)
                  except KeyError:
                      lpbndlst[hsta]=[lpnam1]
                  continue
                  
            # lonepair bisector
            if anam[0:1] == "O" and len(bndlst.get(anam)) == 2 or anam[0:1] == "S" and len(bndlst.get(anam)) == 2: 
                  hsta = anam
                  hstb = bndlst.get(hsta)[0]
                  hstc = bndlst.get(hsta)[1]
                  medcor = [(ca-cb)/2.0 for ca,cb in zip(atomposi[ind[hstb]][3],atomposi[ind[hstc]][3])]
                  medcor = [ca+cb for ca,cb in zip(atomposi[ind[hstc]][3],medcor)]
                  hcoor = [atomposi[ind[hsta]][3],medcor,atomposi[ind[hstc]][3]]
                  curntid += 1
                  lpnam1 = "LP"+str(hsta)+"1"
                  lpinfo[lpnam1] = curntid
                  if hsta[0:1] == "O": lpposi[curntid] = [lpnam1,"LP","LPDO1",relative(0.35,110.0,90.0,hcoor)] 
                  if hsta[0:1] == "S": lpposi[curntid] = [lpnam1,"LP","LPDO1",relative(0.70,95.0,100.0,hcoor)] 
                  try:
                      lpbndlst[hsta].append(lpnam1)
                  except KeyError:
                      lpbndlst[hsta]=[lpnam1]
                  curntid += 1
                  lpnam2 = "LP"+str(hsta)+"2"
                  lpinfo[lpnam2] = curntid
                  if hsta[0:1] == "O": lpposi[curntid] = [lpnam2,"LP","LPDO1",relative(0.35,110.0,270.0,hcoor)] 
                  if hsta[0:1] == "S": 
                      hcoor = [atomposi[ind[hsta]][3],atomposi[ind[hstc]][3],medcor]
                      lpposi[curntid] = [lpnam2,"LP","LPDO1",relative(0.70,95.0,100.0,hcoor)] 
                  try:
                      lpbndlst[hsta].append(lpnam2)
                  except KeyError:
                      lpbndlst[hsta]=[lpnam2]
                  continue
        
            # lonepair bisector
            if anam[0:1] == "N" and len(bndlst.get(anam)) == 2 or anam[0:1] == "P" and len(bndlst.get(anam)) == 2:
                  hsta = anam
                  hstb = bndlst.get(hsta)[0]
                  hstc = bndlst.get(hsta)[1]
                  medcor = [(ca-cb)/2.0 for ca,cb in zip(atomposi[ind[hstb]][3],atomposi[ind[hstc]][3])]
                  medcor = [ca+cb for ca,cb in zip(atomposi[ind[hstc]][3],medcor)]
                  hcoor = [atomposi[ind[hsta]][3],medcor,atomposi[ind[hstc]][3]]
                  curntid += 1
                  lpnam1 = "LP"+str(hsta)+"1"
                  lpinfo[lpnam1] = curntid
                  if hsta[0:1] == "N": lpposi[curntid] = [lpnam1,"LP","LPDO1",relative(0.30,180.0,180.0,hcoor)] 
                  if hsta[0:1] == "P": lpposi[curntid] = [lpnam1,"LP","LPDO1",relative(0.70,180.0,180.0,hcoor)] 
                  try:
                      lpbndlst[hsta].append(lpnam1)
                  except KeyError:
                      lpbndlst[hsta]=[lpnam1]
                  continue

            # lonepair pyramidal
            if anam[0:1] == "N" and len(bndlst.get(anam)) == 3 or anam[0:1] == "P" and len(bndlst.get(anam)) == 3:
                  hsta = anam
                  hstb = bndlst.get(hsta)[0]
                  hstc = bndlst.get(hsta)[1]
                  hstd = bndlst.get(hsta)[2]
                  hcoor = [atomposi[ind[hsta]][3],atomposi[ind[hstb]][3],atomposi[ind[hstc]][3],atomposi[ind[hstd]][3]]
                  curntid += 1
                  lpnam1 = "LP"+str(hsta)+"1"
                  lpinfo[lpnam1] = curntid
                  if hsta[0:1] == "N": lpposi[curntid] = [lpnam1,"LP","LPDO1",pyramidal(0.30,hcoor)] 
                  if hsta[0:1] == "P": lpposi[curntid] = [lpnam1,"LP","LPDO1",pyramidal(0.70,hcoor)] 
                  try:
                      lpbndlst[hsta].append(lpnam1)
                  except KeyError:
                      lpbndlst[hsta]=[lpnam1]
                  continue

        nlps = curntid - (len(atomposi.items()))
        return ({"nlps":nlps,"lpnames":lpinfo,"lpposi":lpposi,"lpbonds":lpbndlst}) 

    def runPsi4(self,outdir,prefname,rescharge=0,multiplicity=1,atomposi=None,mem="1000Mb",cpu=4,olot="mp2",obasis="6-31+g*",rlot="mp2",rbasis="Sadlej",plot="mp2",pbasis="Sadlej",quiet=False,qopt=True,qpol=True,qlp=True,qresp=True,symm=False,reorient=False,recenter=False):
        import pytest
        import sys
        import psi4
        #import psi4.driver.p4util.exceptions
        from localresp import resp
        import numpy as np
        from collections import OrderedDict
        from multiprocessing import Process, current_process, Manager
        
        def opt(theory,basis,mol): 
            options={'scf_type':'df','g_convergence':'gau','freeze_core':'true','mp2_type':'df','df_basis_scf':'def2-tzvpp-jkfit','df_basis_mp2':'def2-tzvppd-ri'}
            psi4.set_options(options)
        #    try:
            psi4.optimize(theory+'/'+basis,molecule=mol)
        #    except SCFConvergenceError:
        #       print ("Problem detected")
            mol.update_geometry() 
            return(mol) 

        def pol(theory,basis): 
            dmadict = {} 
            flag = {0:["x",[0.0008, 0, 0]],1:["mx",[-0.0008, 0, 0]],2:["y",[0, 0.0008, 0]],3:["my",[0, -0.0008, 0]],4:["z",[0, 0 , 0.0008]],5:["mz",[0, 0 , -0.0008]]}
            wfn = [None]*6
            for i in range(6):
                options={'scf_type':'df','g_convergence':'gau','freeze_core':'true','mp2_type':'df','df_basis_scf':'def2-tzvpp-jkfit','df_basis_mp2':'def2-tzvppd-ri','perturb_h':'true','perturb_with':'dipole','perturb_dipole':flag[i][1]}
                psi4.set_options(options)
                grad,wfn[i]=psi4.gradient(theory+"/"+basis,return_wfn=True) 
                psi4.fchk(wfn[i],str(flag[i][0])+'.fchk')
                fdma = open(str(flag[i][0])+"control.dma","w")
                fdma.write(self.createdma(str(flag[i][0])+'.fchk',dentype,1))
                fdma.close()
            parallel = False
            if parallel: 
                processes = []
                for i in range(6):
                    d[i] = Manager().Value('i',0)
                    process = Process(target=psi4.gdma,args=(wfn[i],str(flag[i][0])+"control.dma"))
                    processes.append(process)
                    process.start()
                for process in processes:
                    process.join()
            else:
                for i in range(6):
                    psi4.gdma(wfn[i],datafile=str(flag[i][0])+"control.dma") 
                    dma_results = psi4.variable('DMA DISTRIBUTED MULTIPOLES')
                    dma_results = list(map(lambda x:x[0:4],dma_results.np))
                    dmadict[i] = np.array(dma_results)
                   # print (dmadict)
                   # print (flag[i],"dma done")
            #os.remove(str(flag[i][0])+'.fchk') 
            #os.remove(str(flag[i][0])+'control.dma') 
            #del wfn
            return(dmadict)
 
        def calcresp(theory,basis,mol,mollp=None,mollpbnd=None):
            options = {'N_VDW_LAYERS'       : 4,
                       'VDW_SCALE_FACTOR'   : 1.4,
                       'VDW_INCREMENT'      : 0.2,
                       'VDW_POINT_DENSITY'  : 1.0,
                       'resp_a'             : 0.0005,
                       'RESP_B'             : 0.1,
                       'METHOD_ESP'         : theory,
                       'BASIS_ESP'          : basis,
                       'g_convergence'      : 'gau',
                       'RADIUS'             : {'BR':1.97,'I':2.19},
                       'psi4_options'       : {'scf_type':'df','mp2_type':'df','freeze_core':'true','df_basis_scf':'def2-tzvpp-jkfit','df_basis_mp2':'def2-tzvppd-ri','maxiter':250}
                       }
            
            if qlp:
                geoline = ""
                for key,val in mollp.items():
                    geoline = geoline + val[0] + "  " + str(val[3][0]) + "  " + str(val[3][1]) + "  " + str(val[3][2]) + " \n"
                lp="""
                %s
                """%(geoline)
                options['LPCOOR'] = lp

            mol.set_name('stage1')
            charges1 = resp.resp([mol], [options])
            if qlp:
               allatoms = mol.natom() + len(mollp)
            else:
               allatoms = mol.natom()
        
            respchar = OrderedDict()
            for i in range(allatoms):
                respchar[i+1]  = charges1[0][1][i]
            
            #print("RESP Stage 1 Fitting") 
            #for key,value in respchar.items():
            #    print("%s  %7.3f \n"%(key, value))
            if qlp:
                for key,val in self.molinfo["lpbonds"].items():  
                    dbute = respchar[self.molinfo["atomnames"][key]]/len(val) 
                    respchar[self.molinfo["atomnames"][key]] = 0.0
                    for v in val: 
                        respchar[self.molinfo["lpnames"][v]] += dbute
        
            #print("Reshuffling Charges") 
            #for key,value in respchar.items():
            #    print("%s  %7.3f \n"%(key, value))
            stage2=resp.stage2_helper()
            stage2.set_stage2_constraint(mol,list(respchar.values()),options,cutoff=1.2)
            options['resp_a'] = 0.001
            options['grid'] = '1_%s_grid.dat' %mol.name()
            options['esp'] = '1_%s_grid_esp.dat' %mol.name()
            fout = open(outdir+"/"+"resp.dat","w")
            
            charges2 = resp.resp([mol], [options])
        
            for i in range(allatoms):
                respchar[i+1]  = charges2[0][1][i]
            #print("RESP Stage 2 Fitting")
            #for key,value in respchar.items():
            #    print("%s  %7.3f \n"%(key, value)) 
            #os.remove('1_%s_grid.dat' %mol.name()) 
            #os.remove('1_%s_grid_esp.dat' %mol.name()) 
            return (respchar)
 
        #def esppol(theory,basis): 
        #    flag = {0:["x",[0.0008, 0, 0]],1:["y",[0, 0.0008, 0]],2:["z",[0, 0 , 0.0008]]}
        #    px = []; py= []; pz=[]
        #    for i in range(mol.natom()):
        #        px.append(mol.x(i))
        #        py.append(mol.y(i))
        #        pz.append(mol.z(i))
        #    xmax=max(px); ymax=max(py); zmax=max(pz)
        #    xmin=min(px); ymin=min(py); zmin=min(pz)
        #    xboxe = xmax + 2.0
        #    yboxe = xmax + 2.0
        #    zboxe = xmax + 2.0
        #    xboxs = xmax - 2.0
        #    yboxs = xmax - 2.0
        #    zboxs = xmax - 2.0
        #    boxx = np.arange(xboxs,xboxe,0.2)
        #    boxy = np.arange(yboxs,yboxe,0.2)
        #    boxz = np.arange(zboxs,zboxe,0.2)
        #    x, y, z = np.meshgrid(boxx, boxy, boxz, indexing='ij')
        #    xyz = np.vstack((x.ravel(), y.ravel(), z.ravel())).T
        #    np.savetxt('grid.dat', xyz)

        #    wfn = [None]*3
        #    for i in range(3):
        #        options={'scf_type':'df','g_convergence':'gau','freeze_core':'true','mp2_type':'df','df_basis_scf':'def2-tzvpp-jkfit','df_basis_mp2':'def2-tzvppd-ri','perturb_h':'true','perturb_with':'dipole','perturb_dipole':flag[i][1],'basis':basis}
        #        psi4.set_options(options)
        #        E,wfn=psi4.prop(theory,properties=['GRID_ESP'],return_wfn=True) 
        #        Vvals = wfn.oeprop.Vvals()
        #    #    options['esp_values'] = np.loadtxt('grid_esp.dat')

        # Psi4 STARTS ########################
        dmadict = None
        psi4.set_num_threads(cpu)
        psi4.set_memory(mem)
        if not quiet:
            psi4.core.set_output_file(outdir+'/'+prefname, False)
        else:
            psi4.core.be_quiet()
        
        xyz='%s %s\n' %(rescharge,multiplicity)
        geoline = ""
        for key,value in atomposi.items():
            geoline = geoline + value[1] + "  " + str(value[3][0]) + "  " + str(value[3][1]) + "  " + str(value[3][2]) + " \n"
            if value[1].upper() in ["K","CA","BR","I"]: obasis = "6-311G(d,p)"
        xyz=xyz+geoline
        orientline = ""
        if not symm: orientline = orientline + "symmetry c1\n"
        if not reorient: orientline = orientline + "noreorient\n"
        if not recenter: orientline = orientline + "nocom\n"
        psi4_xyz="""%s %s"""%(xyz,orientline)
        print (psi4_xyz)
        mol=psi4.geometry(psi4_xyz)
        mol.update_geometry() 
        if qopt:
            mol = opt(olot,obasis,mol)
            for i in range(mol.natom()):
                posiang = np.array([mol.x(i),mol.y(i),mol.z(i)])*float(0.529177249)
                self.molinfo["atomposiang"][i+1][3] = posiang
            for i in range(mol.natom()):
                posiau =np.array([mol.x(i),mol.y(i),mol.z(i)])
                self.molinfo["atomposiau"][i+1][3] = posiau
            mol.update_geometry() 
        if qpol:
           dentype = "SCF" if plot.lower() == "scf" else "CC"
           dmadict = pol(plot,pbasis)
           self.molinfo["apol"] = self.atomic_pol(self.molinfo["atomposiau"],self.molinfo["bondnums"],dmadict) 
        if qlp: 
           lonepinfo = self.createlonepair(self.molinfo["atomposiang"],self.molinfo["atomnames"],self.molinfo["bonds"])
           self.molinfo["nlps"] = lonepinfo["nlps"]
           self.molinfo["lpnames"] = lonepinfo["lpnames"]
           self.molinfo["lpposi"] = lonepinfo["lpposi"]
           self.molinfo["lpbonds"] = lonepinfo["lpbonds"] 
           self.molinfo["allnames"] = OrderedDict(**(self.molinfo["atomnames"]),**(self.molinfo["lpnames"]))
           self.molinfo["allposi"] = OrderedDict(**(self.molinfo["atomposiang"]),**(self.molinfo["lpposi"]))
           self.molinfo["allbonds"] = self.molinfo["bonds"]  
           for key, value in self.molinfo["lpbonds"].items():
               for v in value:
                   self.molinfo["allbonds"].update({v:[key]})
                   self.molinfo["allbonds"][key].append(v)  
           _,self.molinfo["allbondnums"] = self.findbonds(self.molinfo["allnames"],self.molinfo["allbonds"])
           _,self.molinfo["allanglnums"] = self.findangles(self.molinfo["allnames"],self.molinfo["allbonds"])
           _,self.molinfo["alldihenums"] = self.finddihedrals(self.molinfo["allnames"],self.molinfo["allbonds"])
        if qresp and qlp:
           self.molinfo["resp"] = calcresp(rlot,rbasis,mol,self.molinfo["lpposi"],self.molinfo["lpbonds"])
        elif qresp and not qlp:
           self.molinfo["resp"] = calcresp(rlot,rbasis,mol) 

        #esppol(rlot,rbasis)
        #self.esp_atomic_pol(atomposi)

    def createdma(self,fchkname,densitype,nmultipoles):
        towrite = """FILE %s DENSITY %s \nMULTIPOLES \nLIMIT %s \nSTART \nFINISH"""%(fchkname,densitype,nmultipoles) 
        return(towrite)

    def atomic_pol(self,atomposi,bondlist,dma,field=0.0008,ang_unit=0.529177249**3,au_unit=1.0**3): 
        natoms = len(atomposi) 
        nrings = 0
        nbonds = len(bondlist) 
        gq=np.zeros((natoms,6))                    # Create empty charge array (+zero rows for ring conditions)
        gd=np.zeros((natoms,3,6))                  # Create empty atomic dipole array
        for key,val in dma.items():
            for i in range(len(val)): 
                gq[i,key]   = dma[key][i][0] 
                gd[i,0,key] = dma[key][i][1] 
                gd[i,1,key] = dma[key][i][2] 
                gd[i,2,key] = dma[key][i][3] 
        #print("Substract overall charge ("+str(gq[:,0].sum())+")?")
        #answer=input("............ yes/no   ")
        for j in range(6):
            ch=gq[:,j].sum()/natoms
            for i in range(natoms):
                gq[i,j]-=ch

        #print("------------------Atomic Polarizability------------------")
        #========================================================================================
        #   Atomic polarizability
        #========================================================================================
        #This part calculates the polarizability arising from non-uniform
        # distribution of electrons around the core
        #========================================================================================
        
        a_xx=(gd[:,0,0]-gd[:,0,3])/(2*field)*(-1)*au_unit     #numeric differentiation, yields polarizability
        a_yy=(gd[:,1,1]-gd[:,1,4])/(2*field)*(-1)*au_unit
        a_zz=(gd[:,2,2]-gd[:,2,5])/(2*field)*(-1)*au_unit
        a_tot_p=(a_xx+a_yy+a_zz)/3
        #print("Polarization contribution:")
        #print("%4s %7s %7s %7s %7s" % ("Name","a_xx","a_yy","a_zz","a_tot"))
        #for i in range(natoms):
        #    print("%7.2f %7.2f %7.2f %7.2f " % (a_xx[i],a_yy[i],a_zz[i],a_tot_p[i]))
        #print("Summed up contributions:")
        #print(a_tot_p[:].sum())
        #print("---------------------------------------------------------")
        #print("---------------------Charge Transfer---------------------")
        #=============================================================================================
        #   CHARGE TRANSFER
        #=============================================================================================
        #This part calculates the connectivity matrix "n", the matrix with indices 
        #of each bond charge "index" the bond charges "b" and then the atomic 
        #dipoles "mu" and the polarizability "a" for the charge transfer
        #=============================================================================================
        #print (bondlist) 
        n=np.zeros((natoms,natoms))                                        # Create empty connectivity matrix
        for i in range(nbonds):
            first=bondlist[i][0]-1                   # Read atom numbers of each bond
            second=bondlist[i][1]-1
            if first<second:                                             # Write entry in antisymmetric connectivity matrix
                n[first,second]=1
                n[second,first]=-1
            else:
                n[first,second]=-1
                n[second,first]=1
        #print (n)
        index=np.zeros((nbonds,2))                                        # Create index matrix (which bond charge contains which atoms)
        ctr=0
        for i in range(natoms):
            for j in range(i,natoms):
                if n[i,j]==1:
                    index[ctr,0]=i
                    index[ctr,1]=j
                    ctr+=1
        #print (index)
        a=np.zeros((natoms+nrings,nbonds))                                  # Create matrix for linear equations ab=q
        for i in range(natoms):
            for j in range(nbonds):
                if i==index[j,0]:
                    a[i,j]=1
                if i==index[j,1]:
                    a[i,j]=-1         
        #print (a)
        for i in range(nrings):                                           # Write ring conditions into matrix a                                 
            structure=re.findall(r"\d+",nring[i])
            for j in range(len(structure)):
                if j ==len(structure)-1:
                    k=0
                else:
                    k=j+1
                first=int(structure[j])-1
                second=int(structure[k])-1
        
                factor=1
                if second<first:
                    save=first
                    first=second
                    second=save
                    factor=-1
                # Find the correct bond charge which is involved in the ring
                element=np.where(np.all(index==np.array([[first,second]]),axis=1))[0][0]              
                a[natoms+i,element]=factor                                  # Write entry in a
        #Calculate bond charges and mu
        mu=np.zeros((natoms,3,6))
        for k in range(6):
            b=np.linalg.lstsq(a,gq[:,k],rcond=-1)[0]                                 # Solve linear equations ab=q for b
         #   print (b) 
        
            for i in range(natoms):                                         # Calculate atomic dipole from charge transfer as sum of bond charges times vector of the
                for j in range(nbonds):                                     # atom in direction of each bond 
                    if i==index[j,0]:
                        mu[i,:,k]+=(atomposi[i+1][3]-(atomposi[i+1][3]+atomposi[int(index[j,1])+1][3])/2)*b[j]
                    if i==index[j,1]:
                        mu[i,:,k]+=(atomposi[i+1][3]-(atomposi[i+1][3]+atomposi[int(index[j,0])+1][3])/2)*b[j]*(-1)
        
        #a_xx=(mu[:,0,0]-mu[:,0,3])/(2*field)*1.889725989*(-1)*unit   #numeric differentiation, yields polarizability
        #a_yy=(mu[:,1,1]-mu[:,1,4])/(2*field)*1.889725989*(-1)*unit
        #a_zz=(mu[:,2,2]-mu[:,2,5])/(2*field)*1.889725989*(-1)*unit
        a_xx=(mu[:,0,0]-mu[:,0,3])/(2*field)*(-1)*au_unit   #numeric differentiation, yields polarizability
        a_yy=(mu[:,1,1]-mu[:,1,4])/(2*field)*(-1)*au_unit
        a_zz=(mu[:,2,2]-mu[:,2,5])/(2*field)*(-1)*au_unit
        a_tot_c=(a_xx+a_yy+a_zz)/3
        #print("")
        #print("Results:")
        #print("")
        #print("Charge transfer contribution:")
        #print("%4s %7s %7s %7s %7s" % ("Name","a_xx","a_yy","a_zz","a_tot"))
        #for i in range(natoms):
        #    print("%4s %7.2f %7.2f %7.2f %7.2f " % (atomposi[i+1][0],a_xx[i],a_yy[i],a_zz[i],a_tot_c[i]))
        #print("Summed up contributions:")
        #print(a_tot_c[:].sum())
        
        #print("Total polarizability:")
        #print("%4s %7s" % ("Name","a"))
        apoldict=OrderedDict()
        for i in range(natoms):
             apoldict[i+1] = a_tot_p[i]+a_tot_c[i]
        #for i in range(natoms):
        #     print("%4s %7.2f " % (atomposi[i+1][0],a_tot_p[i]+a_tot_c[i]))
        #print("Summed up contributions:")
        #print(a_tot_p[:].sum()+a_tot_c[:].sum())
        
        np.savetxt("atomic_pol.dat",np.c_[a_tot_p,a_tot_c,a_tot_p+a_tot_c])
        
        #print("---------------------------------------------------------")
        #print("-------------------------Goodbye-------------------------")
        #print("---------------------------------------------------------")
        return(apoldict)

   # def esp_atomic_pol(self,atomposi,xesp="./x.esp",yesp="./y.esp",zesp="./z.esp",tesp="./0.esp",grid="./grid.dat",field=0.0008,ang_unit=0.529177249**3,au_unit=1.0**3): 
   #     symbols=[]
   #     natoms = len(atomposi) 
   #     coor = []
   #     for i in range(natoms):
   #         coor.append(atomposi[i+1][3]) 
   #     coor = np.array(coor)
   #     print (coor) 
        #x=np.loadtxt("x.esp")
        #y=np.loadtxt("y.esp")
        #z=np.loadtxt("z.esp")
        #grid=np.loadtxt('1_stage1_grid.dat')
        #no=np.loadtxt('1_stage1_grid_esp.dat')
      #  n_gridpoints=grid.shape[0]
      #  r=np.zeros((n_atoms,n_gridpoints,4))
      #  units=1.6022*100/(4*np.pi*8.854188*2.7211385)
      #  X=np.zeros((n_atoms,n_gridpoints,3))
      #  field=0.0008
      #  
      #  for k in range(n_atoms):
      #      for i in range(n_gridpoints):
      #          for j in range(3):
      #              r[k,i,j]=coor[k,j]-grid[i,j]
      #          r[k,i,3]=np.sqrt(r[k,i,0]**2+r[k,i,1]**2+r[k,i,2]**2)
      #  for k in range(n_atoms):
      #      for i in range(n_gridpoints):
      #          for j in range(3):
      #              X[k,i,j]=units*r[k,i,j]/(r[k,i,3]**3)
      #  
      #  phi_ind_x=x-no
      #  phi_ind_y=y-no
      #  phi_ind_z=z-no
      #  
      #  print('%6s %7s %7s %7s %10s' %("Name","a_xx", "a_yy", "a_zz", "a_iso"))
      #  print('-----------------------------------------')
      #  if n_atoms>1:
      #      mu_ind=np.zeros((n_atoms,3))
      #      mu_ind[:,0]=np.linalg.lstsq(X[:,:,0].T,phi_ind_x)[0]
      #      mu_ind[:,1]=np.linalg.lstsq(X[:,:,1].T,phi_ind_y)[0]
      #      mu_ind[:,2]=np.linalg.lstsq(X[:,:,2].T,phi_ind_z)[0]
      #      for i in range(n_atoms):
      #          a_xx=mu_ind[i,0]/field*0.529177249**2
      #          a_yy=mu_ind[i,1]/field*0.529177249**2
      #          a_zz=mu_ind[i,2]/field*0.529177249**2
      #          print('%6s %7.3f %7.3f %7.3f %10.3f' %(symbols[i],a_xx,a_yy,a_zz,(a_xx+a_yy+a_zz)/3))
      #  else:
      #      mu_ind=np.zeros(3)
      #      mu_ind[0]=np.linalg.lstsq(np.vstack([X[0,:,0],np.zeros(n_gridpoints)]).T,phi_ind_x)[0][0]
      #      mu_ind[1]=np.linalg.lstsq(np.vstack([X[0,:,1],np.zeros(n_gridpoints)]).T,phi_ind_y)[0][0]
      #      mu_ind[2]=np.linalg.lstsq(np.vstack([X[0,:,2],np.zeros(n_gridpoints)]).T,phi_ind_z)[0][0]
      #      
      #      a_xx=mu_ind[0]/field*0.529177249**2
      #      a_yy=mu_ind[1]/field*0.529177249**2
      #      a_zz=mu_ind[2]/field*0.529177249**2
      #  
      #      print('%6s %7.3f %7.3f %7.3f %10.3f' %(symbols[0],a_xx,a_yy,a_zz,(a_xx+a_yy+a_zz)/3))

    def _printxyz(self,outdir,prefname,cor):
        f = open(outdir+"/"+prefname,"w") 
        f.write(str(len(cor))+"\n\n")
        for key,value in cor.items():
            f.write("{:4s}   {:12.6f} {:12.6f} {:12.6f}\n".format(value[0],value[3][0],value[3][1],value[3][2]))
        f.close() 
    
    
    def _printpdb(self,outdir,prefname,cor,resi="RESI"):
        f = open(outdir+"/"+prefname,"w") 
        n = 0
        for key,value in cor.items():
            n = n + 1
            f.write("{:6s}{:5d} {:^4s}{:4s}  {:4d}    {:8.3f}{:8.3f}{:8.3f}{:6.2f}{:6.2f}          {:4s}\n".format('ATOM',n,value[1][0:4],resi,1,value[3][0],value[3][1],value[3][2],0.0,0.0,resi))
        f.write("{:6s}{:5d}     {:4s}  {:4d}\n".format('TER',n+1,resi,1))
        f.write("END")
        f.close() 
    
    def _printbad(self,outdir,prefname):
        f = open(outdir+"/"+prefname,"w") 
        f.write("BONDS\n")
        for l in self.molinfo["bondnums"]:
            f.write("  ".join(map(str,l))+"\n")
        f.write("ANGLES\n")
        for l in self.molinfo["anglnums"]:
            f.write("  ".join(map(str,l))+"\n")
        f.write("DIHEDRALS\n")
        for l in self.molinfo["dihenums"]:
            f.write("  ".join(map(str,l))+"\n")
        f.close() 

    def _printbadlp(self,outdir,prefname):
        f = open(outdir+"/"+prefname,"w") 
        f.write("BONDS\n")
        for l in self.molinfo["allbondnums"]:
            f.write("  ".join(map(str,l))+"\n")
        f.write("ANGLES\n")
        for l in self.molinfo["allanglnums"]:
            f.write("  ".join(map(str,l))+"\n")
        f.write("DIHEDRALS\n")
        for l in self.molinfo["alldihenums"]:
            f.write("  ".join(map(str,l))+"\n")
        f.close() 

    def _printcrp(self,outdir,prefname,atplist="allposi"):
        fcrp=open(outdir+"/"+prefname,"w")
        for key,value in self.molinfo[atplist].items(): 
            if not qresp and not qpol:
                fcrp.write("{:4s}   {:12.6f} {:12.6f} {:12.6f}\n".format(value[0],value[3][0],value[3][1],value[3][2]))
            elif qresp and not qpol:
                fcrp.write("{:4s}   {:12.6f} {:12.6f} {:12.6f} {:7.3f}\n".format(value[0],value[3][0],value[3][1],value[3][2],self.molinfo["resp"][key]))
            elif not qresp and qpol:
                fcrp.write("{:4s}   {:12.6f} {:12.6f} {:12.6f} {:7.3f}\n".format(value[0],value[3][0],value[3][1],value[3][2],self.molinfo["apol"][key]))
            elif qresp and qpol:
                try:
                    fcrp.write("{:4s}   {:12.6f} {:12.6f} {:12.6f} {:7.3f} {:7.3f}\n".format(value[0],value[3][0],value[3][1],value[3][2],self.molinfo["resp"][key],self.molinfo["apol"][key]))
                except KeyError:
                    fcrp.write("{:4s}   {:12.6f} {:12.6f} {:12.6f} {:7.3f}\n".format(value[0],value[3][0],value[3][1],value[3][2],self.molinfo["resp"][key]))
        fcrp.close()

class LoadFromFile (argparse.Action):
    def __call__ (self, parser, namespace, values, option_string = None):
        rsarg = []
        with values as f:
            argline = f.read()
            arglist = argline.split()
      
        parser.parse_args(nrsarg, namespace)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-mol2","--mol2file",help="Required Argument: Provide Mol2 File",required=True)
    parser.add_argument('-noqm','--noqm', action='store_true',default=False,help='Insert this flag if you do not want to perform qm calculation.')
    parser.add_argument('-noopt','--noopt', action='store_true',default=False,help='Insert this flag if you do not want to perform optimization.')
    parser.add_argument("-nopol","--nopol", action='store_true',default=False,help="Insert this flag if you do not want to calculate atomic polarizability.")
    parser.add_argument("-nolp","--nolp",   action='store_true',default=False,help="Insert this flag if you do not want to attach lone pairs to the acceptor atoms.")
    parser.add_argument("-noresp","--noresp",action='store_true',default=False,help="Insert this flag if you do not want to perform resp calculation.")
    parser.add_argument('-quiet','--quiet', action='store_true',default=False,help='Insert this flag if you want to suppress qm output file.')
    parser.add_argument("-dir","--workdir",type=str,default=".",help="Enter were the output files will be saved")
    parser.add_argument("-mem","--memory",type=str,default="2000Mb",help="Memory")
    parser.add_argument("-cpu","--nthreads",type=int,default=4,help="Number of threads")
    parser.add_argument("-olot","--opttheory",type=str,default="mp2",help="Enter level of theory")
    parser.add_argument("-obasis","--optbasis",type=str,default="6-31+g*",help="Basis set")
    parser.add_argument("-rlot","--resptheory",type=str,default="mp2",help="Enter level of theory")
    parser.add_argument("-rbasis","--respbasis",type=str,default="Sadlej",help="Basis set")
    parser.add_argument("-plot","--poltheory",type=str,default="mp2",help="Enter level of theory")
    parser.add_argument("-pbasis","--polbasis",type=str,default="Sadlej",help="Basis set")
    parser.add_argument("-c","--charge",type=int,default=None,help="Charge of the molecule, default is 0")
    parser.add_argument("-m","--multiplicity",type=int,default=None,help="Multiplicity of the molecule, default is 1")
    parser.add_argument('-qwxyz','--qwxyz', action='store_true',default=False,help='Insert this flag if you want to write output coordinate xyz file.')
    parser.add_argument('-qwpdb','--qwpdb', action='store_true',default=False,help='Insert this flag if you want to write output coordinate pdb file.')
    parser.add_argument('-nobad','--nobad', action='store_true',default=False,help='Insert this flag if you want to write bond angle dihedral record.')
    parser.add_argument('-symm','--symm', action='store_true',default=False,help='Insert this flag if you want Psi4 to determine molecular symmetry.')
    parser.add_argument('-reorient','--reorient', action='store_true',default=False,help='Insert this flag if you want Psi4 to reorient the molecule.')
    parser.add_argument('-recenter','--recenter', action='store_true',default=False,help='Insert this flag if you want Psi4 to recenter the molecule.')
    parser.add_argument("-f","--file",type=open,action=LoadFromFile)
    args = parser.parse_args()
    Psi4input(args.mol2file,chrg=args.charge,mult=args.multiplicity,olot=args.opttheory,obasis=args.optbasis,rlot=args.resptheory,rbasis=args.respbasis,plot=args.poltheory,pbasis=args.polbasis,mem=args.memory,cpu=args.nthreads,outdir=args.workdir,noqm=args.noqm,noopt=args.noopt,nopol=args.nopol,nolp=args.nolp,noresp=args.noresp,quiet=args.quiet,qwxyz=args.qwxyz,qwpdb=args.qwpdb,nobad=args.nobad,symm=args.symm,reorient=args.reorient,recenter=args.recenter)    

if __name__ == "__main__":
   main()

#    def _masses(self,fil="atomic_info.dat"):
#        f = open(fil,"r")
#        poo = f.readlines()
#        
#        atinfo = OrderedDict()
#        n = 0
#        for line in poo:
#            if line.startswith("Atomic Number"):
#               atnum = line.split()[-1]   
#               n = n + 1
#            if line.startswith("Atomic Symbol"):
#               atsym  = line.split()[-1] 
#               n = n + 1
#            if line.startswith("Mass Number"):
#               atmss  = line.split()[-1] 
#               n = n + 1   
#            if n%3 == 0:
#                atinfo[atsym] = (atnum,atmss)
#        return(atinfo)        
#def _readpdbpsf(self,pdbname,psfname):
#    bndlst = {}
#    anam = []
#    pos = []
#    filein = open(pdbname, "r") 
#    for d in filein:
#        if d[:4] == 'ATOM' or d[:6] == "HETATM":
#            splitted_line = [d[:6], d[6:11], d[12:16], d[17:21], d[21], d[22:26], d[30:38], d[38:46], d[46:54]]
#            resi = splitted_line[3]
#            anam.append(splitted_line[2].strip()) 
#            pos.append(splitted_line[6:9])
#    filein.close()
#    filein = open(psfname, "r") 
#    data = [line.split() for line in filein]
#    filein.close()
#    
#    # get charges and bondlist from psf
#    readbond = False
#    for ind,field in enumerate(data):
#        if len(field) > 2 and field[1] == "!NBOND:":
#            readbond = True
#            strtread = ind + 1
#    
#        if len(field) > 2 and field[1] == "!NBOND:":
#            readbond = True
#            strtread = ind + 1
#        if len(field) > 2 and field[1] == "!NTHETA:":
#            readbond = False
#            break
#        if readbond and ind >= strtread:
#            for i in range(0,len(field),2):
#                if 'LP' not in [anam[int(field[i])-1][:2], anam[int(field[i+1])-1][:2]] and 'D' not in [anam[int(field[i])-1][:1], anam[int(field[i+1])-1][:1]]:
#                    try:
#                        bndlst[anam[int(field[i])-1]].append(anam[int(field[i+1])-1])
#                    except KeyError:
#                        bndlst[anam[int(field[i])-1]]=[anam[int(field[i+1])-1]]
#                    try:
#                        bndlst[anam[int(field[i+1])-1]].append(anam[int(field[i])-1])
#                    except KeyError:
#                        bndlst[anam[int(field[i+1])-1]]=[anam[int(field[i])-1]]
#    
#    return (resi, anam, pos, bndlst) 
#
#
    





