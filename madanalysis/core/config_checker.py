################################################################################
#  
#  Copyright (C) 2012-2013 Eric Conte, Benjamin Fuks
#  The MadAnalysis development team, email: <ma5team@iphc.cnrs.fr>
#  
#  This file is part of MadAnalysis 5.
#  Official website: <https://launchpad.net/madanalysis5>
#  
#  MadAnalysis 5 is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  MadAnalysis 5 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with MadAnalysis 5. If not, see <http://www.gnu.org/licenses/>
#  
################################################################################


import logging
import glob
import os
import commands
import sys
import re

class ConfigChecker:

    @staticmethod
    def AddIfValid(path,container):
        dirs=glob.glob(path)
        for item in dirs:
            if not (item in container):
                container.append(item)
        

    def __init__(self,configLinux,ma5dir,script=False):

        # Getting parameter from the main program
        self.configLinux=configLinux
        self.ma5dir=ma5dir
        self.script=script

        self.paths = []
        self.fillPaths()

        self.libs = []
        self.fillLibraries()

        self.includes = []
        self.fillHeaders()


    def ReadUserOptions(self):

        # Open the user options
        filename = self.ma5dir+'/madanalysis/input/installation_options.dat'
        try:
            input = open(filename)
        except:
            logging.error('impossible to open the file: '+filename)
            return False

        # Loop over the file
        for rawline in input:

            if '#' in rawline:
                line = rawline.split('#')[0]
            if line=='':
                continue
            words=line.split('=')
            if len(words)!=2:
                logging.warning(filename+': the following line is incorrect and is skipped:')
                logging.warning(line)
            words[0]=words[0].lstrip()
            words[0]=words[0].rstrip()
            words[1]=words[1].lstrip()
            words[1]=words[1].rstrip()

            if words[0]=='root_includes':
                self.configLinux.useroptions.root_includes==words[1]
            elif words[0]=='root_libs':
                self.configLinux.useroptions.root_libs=words[1]
            elif words[0]=='delphes_veto':
                self.configLinux.useroptions.delphes_veto=words[1]
            elif words[0]=='delphes_includes':
                self.configLinux.useroptions.delphes_includes=words[1]
            elif words[0]=='delphes_libs':
                self.configLinux.useroptions.delphes_libs=words[1]
            elif words[0]=='delfes_veto':
                self.configLinux.useroptions.delfes_veto=words[1]
            elif words[0]=='delfes_includes':
                self.configLinux.useroptions.delfes_includes=words[1]
            elif words[0]=='delfes_libs':
                self.configLinux.useroptions.delfes_libs=words[1]
            elif words[0]=='zlib_veto':
                self.configLinux.useroptions.zlib_veto=words[1]
            elif words[0]=='zlib_includes':
                self.configLinux.useroptions.zlib_includes=words[1]
            elif words[0]=='zlib_libs':
                self.configLinux.useroptions.zlib_libs=words[1]
            elif words[0]=='fastjet_veto':
                self.configLinux.useroptions.fastjet_veto=words[1]
            elif words[0]=='fastjet_includes':
                self.configLinux.useroptions.fastjet_includes=words[1]
            elif words[0]=='fastjet_libs':
                self.configLinux.useroptions.fastjet_libs=words[1]
            elif words[0]=='pdflatex_veto':
                self.configLinux.useroptions.pdflatex_veto=words[1]
            elif words[0]=='latex_veto':
                self.configLinux.useroptions.latex_veto=words[1]
            elif words[0]=='dvipdf_veto':
                self.configLinux.useroptions.dvipdf_veto=words[1]
            else:
                logging.warning(filename+': the options called "'+words[0]+'" is not found')

        # Close the file
        input.close()
        
        # Ok
        return True
    

    def FillMA5Path(self):
        os.environ['MA5_BASE']=self.ma5dir


    def fillPaths(self):
        # Filling container with paths included in $PATH
        try:
            self.paths = os.environ['PATH'].split(':')
        except:
            os.environ['PATH']=''

    def PrintOK(self):
        sys.stdout.write('\x1b[32m'+'[OK]'+'\x1b[0m'+'\n')
        sys.stdout.flush()

    def PrintFAIL(self,warning=False):
        if warning:
            sys.stdout.write('\x1b[35m'+'[DISABLED]'+'\x1b[0m'+'\n')
        else:
            sys.stdout.write('\x1b[31m'+'[FAILURE]'+'\x1b[0m'+'\n')
        sys.stdout.flush()    

    def PrintLibrary(self,text,tab=5,width=25):
        mytab = '%'+str(tab)+'s'
        mytab = mytab % ' '
        mytab += '- '
        mywidth = '%-'+str(width)+'s'
        mywidth = mywidth % text
        sys.stdout.write(mytab+mywidth)
        sys.stdout.flush()
                
        
    def fillHeaders(self):
        # Filling container with paths included in CPLUS_INCLUDE_PATH
        try:
            cplus_include_path = os.environ['CPLUS_INCLUDE_PATH'].split(':')
            for item in cplus_include_path:
                ConfigChecker.AddIfValid(item,self.includes)
        except:
            os.environ['CPLUS_INCLUDE_PATH']=''

        # Filling container with standard include paths
        ConfigChecker.AddIfValid('/usr/include',self.includes)
        ConfigChecker.AddIfValid('/usr/local/include',self.includes)
        ConfigChecker.AddIfValid('/local/include',self.includes)
        ConfigChecker.AddIfValid('/opt/local/include',self.includes)


    def fillLibraries(self):
        # Filling container with paths included in LD_LIBRARY_PATH
        try:
            ld_library_path = os.environ['LD_LIBRARY_PATH'].split(':')
            for item in ld_library_path:
                ConfigChecker.AddIfValid(item,self.libs)
        except:
            os.environ['LD_LIBRARY_PATH']=''

        # Filling container with paths included in DYLD_LIBRARY_PATH
        try:
            ld_library_path = os.environ['DYLD_LIBRARY_PATH'].split(':')
            for item in ld_library_path:
                ConfigChecker.AddIfValid(item,self.libs)
        except:
            os.environ['DYLD_LIBRARY_PATH']=''
                
        # Filling container with paths included in LIBRARY_PATH
        try:
            library_path = os.environ['LIBRARY_PATH'].split(':')
            for item in library_path:
                ConfigChecker.AddIfValid(item,self.libs)
        except:
            os.environ['LIBRARY_PATH']=''

        # Filling container with standard library paths
        ConfigChecker.AddIfValid('/usr/lib*',self.libs)
        ConfigChecker.AddIfValid('/usr/local/lib*',self.libs)
        ConfigChecker.AddIfValid('/local/lib*',self.libs)
        ConfigChecker.AddIfValid('/opt/local/lib*',self.libs)


    def checkTextEditor(self):
        try:
            self.configLinux.editor = os.environ['EDITOR']
        except KeyError:
            self.configLinux.editor = 'vi'

    def checkROOT(self):
        # Checking if ROOT is present
        self.PrintLibrary('Root')

        # Trying to call root-config
        rootdirs = commands.getstatusoutput('root-config --libdir --incdir')
        if rootdirs[0]>0:
            self.PrintFAIL(warning=False)
            logging.error('ROOT module called "root-config" is not detected.\n'\
		          +'Two explanations :n'\
		          +' - ROOT is not installed. You can download it '\
		          +'from http://root.cern.ch\n'\
		          +' - ROOT binary folder must be placed in the '\
                          +'global environment variable $PATH')
            return False

        # Extracting ROOT library and header path
        root_tmp = rootdirs[1].split() 
        self.includes.append(root_tmp[1])
        self.libs.append(root_tmp[0])
        os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + \
                    		        ":" + root_tmp[0]
        os.environ['DYLD_LIBRARY_PATH'] = os.environ['DYLD_LIBRARY_PATH'] + \
                    		        ":" + root_tmp[0]
        os.environ['LIBRARY_PATH'] = os.environ['LIBRARY_PATH'] + \
                    		        ":" + root_tmp[0]
        os.environ['CPLUS_INCLUDE_PATH'] = os.environ['CPLUS_INCLUDE_PATH'] + \
                    		        ":" + root_tmp[1]

        # Adding ROOT library path to Python path
        sys.path.append(root_tmp[0])

        # Looking for libPyROOT.so
        find=False
        for item in self.libs:
            files=glob.glob(item+"/libPyROOT.so")
            if len(files)!=0:
	        self.configLinux.libraries['PyROOT']=files[0]+":"+str(os.stat(files[0]).st_mtime)
    	        find=True
   	        break
        if not find:
            self.PrintFAIL(warning=False)
	    logging.error("ROOT library called 'libPyROOT.so' not found. Please check that ROOT is properly installed.")
            return False

        # Looking for ROOT.py
        find=False
        for item in self.libs:
            files=glob.glob(item+"/ROOT.py")
            if len(files)!=0:
	        self.configLinux.libraries['ROOT']=files[0]+":"+str(os.stat(files[0]).st_mtime)
	        find=True
	        break
        if not find:
            self.PrintFAIL(warning=False)
	    logging.error("ROOT file called 'ROOT.py' not found. Please check that ROOT is properly installed.")
            return False

        # Looking for TH1F.h
        find=False
        for item in self.includes:
            files=glob.glob(item+"/TH1F.h")
            if len(files)!=0:
	        self.configLinux.headers['ROOT']=files[0]+":"+str(os.stat(files[0]).st_mtime)
	        find=True
	        break
        if not find:
            self.PrintFAIL(warning=False)
	    logging.error("ROOT headers are not found. " +\
		 "Please check that ROOT is properly installed.")
            return False
        self.PrintOK()


        # Loading ROOT library
        self.PrintLibrary("PyRoot libraries")
        try :
	    from ROOT import gROOT
        except:
            self.PrintFAIL(warning=False)
            logging.error("'root-config --libdir' indicates a wrong path for ROOT"\
	                  +" libraries. Please specify the ROOT library path"\
		          +" into the environnement variable $PYTHONPATH")
            return False

        # Setting ROOT batch mode
        if not self.script:
            from ROOT import TApplication
            from ROOT import gApplication
            TApplication.NeedGraphicsLibs()
            gApplication.InitializeGraphics()
        gROOT.SetBatch(True)
        

        # Checking ROOT release
        RootVersion = str(gROOT.GetVersionInt())
        if len(RootVersion)<3:
            self.PrintFAIL(warning=False)
	    logging.error('Bad release of ROOT : '+gROOT.GetVersion()+\
                          '. MadAnalysis5 needs ROOT 5.27 or higher.\n Please upgrade your version of ROOT.')
            return False

        RootVersionA = int(RootVersion[0])
        RootVersionB = int(RootVersion[1]+RootVersion[2])
        if RootVersionA!=5 or RootVersionB<27:
            self.PrintFAIL(warning=False)
	    logging.error('Bad release of ROOT : '+gROOT.GetVersion()+\
                          '. MadAnalysis5 needs ROOT 5.27 or higher.\n Please upgrade your version of ROOT.')
            return False

        self.configLinux.root_version   = RootVersion
        self.PrintOK()
        return True


    def checkGPP(self):
        # Checking g++ release
        self.PrintLibrary('g++')
        gcc_version = commands.getstatusoutput('g++ -dumpversion')
        if gcc_version[0]>0:
            self.PrintFAIL(warning=False)
            logging.error('g++ compiler not found. Please install it before ' + \
	             'using MadAnalysis 5')
            return False
        else:
            self.PrintOK()
            self.configLinux.gcc_version = gcc_version[1]
            return True

    def checkMake(self):
        # Checking GNU Make
        self.PrintLibrary('GNU Make')
        make_version = commands.getstatusoutput('make --version')
        if make_version[0]>0:
            self.PrintFAIL(warning=False)
            logging.error('GNU Make not found. Please install it before ' + \
	             'using MadAnalysis 5')
            return False
        else:
            self.PrintOK()
            lines=make_version[1].split('\n')
            if len(lines)==0:
                logging.error('command "make --version" seems to not give the GNU Make version')
                return False
            line=lines[0]
            line=line.replace(' ','')
            line=line.lstrip()
            line=line.rstrip()
            self.configLinux.make_version = line
            return True

    def checkGF(self):
        self.PrintLibrary("gfortran")
        gfortran_version = commands.getstatusoutput('gfortran -dumpversion')
        gfortran_version = gfortran_version[1].split('\n')[0]
        gfor = (re.search(r'((\d.)(\d.)\d)',gfortran_version))
        if gfor:
            gfortran_version = gfor.group(1)
        else:
             gfor = (re.search(r'((\d.)\d)',gfortran_version))
             if gfor:
                 gfortran_version = gfor.group(1)
             else:
                 self.PrintFAIL(warning=True)
                 logging.warning('gfortran compiler not found.' + \
                   ' aMCatNLO cannot be used.')
                 return True
        ver = gfortran_version.split('.')
        if (int(ver[0])<4) or (int(ver[0])==4 and int(ver[1])<4):
            self.PrintFAIL(warning=True)
            logging.warning('gfortran ' + gfortran_version + ' older than 4.4.0.')
            return True
            
        self.configLinux.gfortran_version = gfortran_version
        self.PrintOK()
        return True


    def checkZLIB(self):

        self.PrintLibrary("zlib library")
        
        # User veto
        if self.configLinux.useroptions.zlib_veto=='1':
            self.PrintFAIL(warning=True)
	    logging.warning("Library called 'zlib' disabled. Gzip format will be disabled.")
            return False

        # Checking library libz.so
        find=False
        for item in self.libs:
            files=glob.glob(item+"/libz.so")
            files.extend(glob.glob(item+"/libz.a"))
            files.extend(glob.glob(item+"/libz.dylib"))
            if len(files)!=0:
	        self.configLinux.libraries['ZLib']=files[0]+":"+str(os.stat(files[0]).st_mtime)
   	        find=True
                os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + \
                    		        ":" + item
                os.environ['DYLD_LIBRARY_PATH'] = os.environ['DYLD_LIBRARY_PATH'] + \
                    		        ":" + item
                os.environ['LIBRARY_PATH'] = os.environ['LIBRARY_PATH'] + \
                    		        ":" + item
	        break

        # If not, test if it is there locally 
        if not find: 
            item = self.ma5dir+'/tools/zlib/lib/'
            files=glob.glob(item+"/libz.so")
            files.extend(glob.glob(item+"/libz.a"))
            files.extend(glob.glob(item+"/libz.dylib"))
            if len(files)!=0:
	        self.configLinux.libraries['ZLib']=files[0]+":"+str(os.stat(files[0]).st_mtime)
   	        find=True
                os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + \
                    		        ":" + item
                os.environ['DYLD_LIBRARY_PATH'] = os.environ['DYLD_LIBRARY_PATH'] + \
                    		        ":" + item
                os.environ['LIBRARY_PATH'] = os.environ['LIBRARY_PATH'] + \
                    		        ":" + item
        # Not fail -> Warning
        if not find:
            self.PrintFAIL(warning=True)
	    logging.warning("Library called 'zlib' not found. Gzip format will be disabled.")
            logging.warning("To enable this format, please type 'install zlib' package.")
            return False

	# Checking header file zlib.h
        find=False
        for item in self.includes:
            files=glob.glob(item+"/zlib.h")
            if len(files)!=0:
  	        self.configLinux.headers['ZLib']=files[0]+":"+str(os.stat(files[0]).st_mtime)
	        find=True
                os.environ['CPLUS_INCLUDE_PATH'] = os.environ['CPLUS_INCLUDE_PATH'] + ":" + item
   	        break

        # If not, test if it is there locally 
        if not find: 
            find=os.path.isfile(self.ma5dir+'/tools/zlib/include/zlib.h')
            if find:
                os.environ['CPLUS_INCLUDE_PATH'] = os.environ['CPLUS_INCLUDE_PATH'] + ":" + \
                                                   self.ma5dir+'/tools/zlib/include/'

        if not find:
            self.PrintFAIL(warning=True)
	    logging.warning("Header file called 'zlib.h' not found. Gzip format will be disabled.")
            logging.warning("To enable this format, please type 'install zlib' package.")
            return False
        else:
            self.PrintOK()
 
        return True


    def checkDelphes(self):

        self.PrintLibrary("delphes library")
        
        # User veto
        if self.configLinux.useroptions.delphes_veto=='1':
            self.PrintFAIL(warning=True)
	    logging.warning("Library called 'delphes' disabled. Delphes ROOT format will be disabled.")
            return False

        # Checking library libDelphes.so
        find=False
        for item in self.libs:
            files=glob.glob(item+"/libDelphes.so")
            files.extend(glob.glob(item+"/libDelphes.a"))
            files.extend(glob.glob(item+"/libDelphes.dylib"))
            files = [ x for x in files if "delfes" not in x ]
            if len(files)!=0:
	        self.configLinux.libraries['Delphes']=files[0]+":"+str(os.stat(files[0]).st_mtime)
   	        find=True
                os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + \
                    		        ":" + item
                os.environ['DYLD_LIBRARY_PATH'] = os.environ['DYLD_LIBRARY_PATH'] + \
                    		        ":" + item
                os.environ['LIBRARY_PATH'] = os.environ['LIBRARY_PATH'] + \
                    		        ":" + item
	        break

        # If not, test if it is there locally 
        if not find: 
            item = self.ma5dir+'/tools/delphes'
            files=glob.glob(item+"/libDelphes.so")
            files.extend(glob.glob(item+"/libDelphes.a"))
            files.extend(glob.glob(item+"/libDelphes.dylib"))
            if len(files)!=0:
	        self.configLinux.libraries['Delphes']=files[0]+":"+str(os.stat(files[0]).st_mtime)
   	        find=True
                os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + \
                    		        ":" + item
                os.environ['DYLD_LIBRARY_PATH'] = os.environ['DYLD_LIBRARY_PATH'] + \
                    		        ":" + item
                os.environ['LIBRARY_PATH'] = os.environ['LIBRARY_PATH'] + \
                    		        ":" + item
        # Not fail -> Warning
        if not find:
            self.PrintFAIL(warning=True)
	    logging.warning("Library called 'delphes' not found. Delphes ROOT format will be disabled.")
            logging.warning("To enable this format, please type 'install delphes'.")
            return False

	# Checking header file 
        find=False
        for item in self.includes:
            files=glob.glob(item+"/modules/ParticlePropagator.h")
            files = [ x for x in files if "delfes" not in x ]
            if len(files)!=0:
  	        self.configLinux.headers['Delphes']=files[0]+":"+str(os.stat(files[0]).st_mtime)
	        find=True
                os.environ['CPLUS_INCLUDE_PATH'] = os.environ['CPLUS_INCLUDE_PATH'] + ":" + item
   	        break

        # If not, test if it is there locally 
        if not find: 
            find=os.path.isfile(self.ma5dir+'/tools/delphes/modules/ParticlePropagator.h')
            if find:
                os.environ['CPLUS_INCLUDE_PATH'] = os.environ['CPLUS_INCLUDE_PATH'] + ":" + \
                                                   self.ma5dir+'/tools/delphes/'
                os.environ['CPLUS_INCLUDE_PATH'] = os.environ['CPLUS_INCLUDE_PATH'] + ":" + \
                                                   self.ma5dir+'/tools/delphes/external/'

        if not find:
            self.PrintFAIL(warning=True)
	    logging.warning("Header file called 'modules/ParticlePropagator.h' not found. Delphes ROOT format will be disabled.")
            logging.warning("To enable this format, please type 'install delphes' package.")
            return False
        else:
            self.PrintOK()
 
        return True


    def checkDelfes(self):

        # User veto
        if self.configLinux.useroptions.delfes_veto=='1':
#            self.PrintFAIL(warning=True)
#	    logging.warning("Library called 'delphes' disabled. Delphes ROOT format will be disabled.")
            return False

        # Checking library libDelphes.so but lcoally only
        find=False
        item = self.ma5dir+'/tools/delfes'
        files=glob.glob(item+"/libDelphes.so")
        files.extend(glob.glob(item+"/libDelphes.a"))
        files.extend(glob.glob(item+"/libDelphes.dylib"))
        if len(files)!=0:
	    self.configLinux.libraries['Delfes']=files[0]+":"+str(os.stat(files[0]).st_mtime)
   	    find=True
            os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + \
                		        ":" + item
            os.environ['DYLD_LIBRARY_PATH'] = os.environ['DYLD_LIBRARY_PATH'] + \
                		        ":" + item
            os.environ['LIBRARY_PATH'] = os.environ['LIBRARY_PATH'] + \
                		        ":" + item

        # Not fail -> not telling anything
        if not find:
            return False

	# Checking header file 
        find=False
        find=os.path.isfile(self.ma5dir+'/tools/delfes/modules/ParticlePropagator.h')
        if find:
            os.environ['CPLUS_INCLUDE_PATH'] = os.environ['CPLUS_INCLUDE_PATH'] + ":" + \
                                               self.ma5dir+'/tools/delfes/'
            os.environ['CPLUS_INCLUDE_PATH'] = os.environ['CPLUS_INCLUDE_PATH'] + ":" + \
                                                   self.ma5dir+'/tools/delfes/external/'

        if not find:
            return False
        else:
            pass

        return True


    def checkMCatNLOUtils(self):

        self.PrintLibrary("MCatNLO-utilities")
        find = os.path.isfile(self.ma5dir+'/tools/MCatNLO-utilities/MCatNLO/lib/libstdhep.a')
        if not find:
            self.PrintFAIL(warning=True)
            logging.warning('MCatNLO-utilities not found. Showering aMCatNLO events deactivated.')
            logging.warning('To install the utilities, please type \'install MCatNLO-utilities\'.')
            return False
        else:
            self.PrintOK()

        return True


    def checkFastJet(self):

        self.PrintLibrary("FastJet")

        self.configLinux.fastjet_version = "none"

        # User veto
        if self.configLinux.useroptions.fastjet_veto=='1':
            self.PrintFAIL(warning=True)
	    logging.warning("The FastJet package is disabled. JetClustering algorithms are disabled.")
            return False

        # Checking if fastjet is installed on the system
        find = False
        for item in self.paths:
            files=glob.glob(item+"/fastjet-config")
            files.extend(glob.glob(item+"/fastjet-config"))
            if(len(files))!=0:
               find = True
               self.configLinux.fastjet_version = commands.getstatusoutput('fastjet-config --version')[1]

        # If not, test if it is there locally 
        if not find: 
            find=os.path.isfile(self.ma5dir+'/tools/fastjet/bin/fastjet-config')

        # If not there, print warning message; if there -> test it
        if not find:
            self.PrintFAIL(warning=True)
	    logging.warning("The FastJet package not found. JetClustering algorithms are disabled.")
            logging.warning("To enable this functionnality, please type 'install fastjet'.")
            return False
        else:
            self.configLinux.fastjet_version = commands.getstatusoutput(self.ma5dir+'/tools/fastjet/bin/fastjet-config --version')[1]
            os.environ['PATH'] = self.ma5dir+'/tools/fastjet/bin/:'+os.environ['PATH']
            self.PrintOK()

        return True


    def checkNumPy(self):

        self.PrintLibrary("python library: numpy")

        # Checking if fastjet is installed on the system
        try:
            import numpy
        except:
            self.PrintFAIL(warning=False)
            logging.error("The python library 'numpy' is not found. Please install it with the following command line:")
            logging.error("apt-get install python-numpy")
            return False
        
        self.PrintOK()
        return True


    def checkPdfLatex(self):
        self.PrintLibrary('pdflatex')

        if self.configLinux.useroptions.pdflatex_veto=='1':
            self.PrintFAIL(warning=True)
	    logging.warning("pdflatex disabled. Reports under the pdf format will not be compiled.")
            return False

        pdflatex_version = commands.getstatusoutput('pdflatex -version')
        if 'not found' in str(pdflatex_version) or 'no such file' in str(pdflatex_version):
            self.PrintFAIL(warning=True)
	    logging.warning("pdflatex not found. Reports under the pdf format will not be compiled.")
            return False
        else:
            self.PrintOK()
            return True
         
    def checkLatex(self):
        self.PrintLibrary('latex')

        if self.configLinux.useroptions.latex_veto=='1':
            self.PrintFAIL(warning=True)
	    logging.warning("latex disabled. Reports under the dvi format will not be compiled.")
            return False

        latex_version = commands.getstatusoutput('latex -version')
        if 'not found' in str(latex_version) or 'no such file' in str(latex_version):
            self.PrintFAIL(warning=True)
	    logging.warning("latex not found. Reports under the dvi format will not be compiled.")
            return False
        else:
            self.PrintOK()
            return True
         
    def checkdvipdf(self):
        self.PrintLibrary('dvipdf')

        if self.configLinux.useroptions.dvipdf_veto=='1':
            self.PrintFAIL(warning=True)
	    logging.warning("dvipdf disabled. DVI reports will not be converted to pdf files.")
            return False

        dvipdf_version = commands.getstatusoutput('dvipdf')
        if 'not found' in str(dvipdf_version) or 'no such file' in str(dvipdf_version):
            self.PrintFAIL(warning=True)
	    logging.warning("dvipdf not found. DVI reports will not be converted to pdf files.")
            return False
        else:
            self.PrintOK()
            return True
