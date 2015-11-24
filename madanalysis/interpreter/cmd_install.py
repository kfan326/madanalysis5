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


from madanalysis.interpreter.cmd_base          import CmdBase
from madanalysis.install.install_manager       import InstallManager
import logging
import os
import sys
import shutil
import urllib
import pwd

class CmdInstall(CmdBase):
    """Command INSTALL"""

    def __init__(self,main):
        CmdBase.__init__(self,main,"install")


    def do(self,args):

        # Checking argument number
        if len(args)!=1 and args[0]!='PADForMA5tunelocal':
            logging.error("wrong number of arguments for the command 'install'.")
            self.help()
            return

        # delphes preinstallation
        def inst_delphes(main,installer):
            if not installer.Deactivate('delphesMA5tune'):
                return False
            if os.path.isdir(os.path.normpath(main.archi_info.ma5dir+'/tools/DEACT_delphes')):
                logging.warning("Delphes deactivated. Activating it...")
                shutil.move(os.path.normpath(main.archi_info.ma5dir+'/tools/DEACT_delphes'),os.path.normpath(main.archi_info.ma5dir+'/tools/delphes'))
                return True
            elif not os.path.isdir(os.path.normpath(main.archi_info.ma5dir+'/tools/delphes')):
                logging.info("   A previous installation has not been found... installing...")
                return installer.Execute('delphes')
            logging.warning("A previous installation of Delphes has been found. Skipping the installation.")
            logging.warning("To update Delphes, please remove the tools/delphes directory")
            return True

        # ma5tune preinstallation
        def inst_ma5tune(main,installer):
            if not installer.Deactivate('delphes'):
                return False
            if os.path.isdir(os.path.normpath(self.main.archi_info.ma5dir+'/tools/DEACT_delphesMA5tune')):
                logging.warning("DelphesMA5tune deactivated. Activating it...")
                shutil.move(os.path.normpath(self.main.archi_info.ma5dir+'/tools/DEACT_delphesMA5tune'),os.path.normpath(self.main.archi_info.ma5dir+'/tools/delphesMA5tune'))
                return True
            elif not os.path.isdir(os.path.normpath(self.main.archi_info.ma5dir+'/tools/delphesMA5tune')):
                logging.warning("DelphesMA5tune not installed: installing it...")
                return installer.Execute('delphesMA5tune')
            logging.warning("A previous installation of DelphesMA5tune has been found. Skipping the installation.")
            logging.warning("To update DelphesMA5tune, please remove the tools/delphesMA5tune directory")
            return True

        # Calling selection method
        if args[0]=='samples':
            installer=InstallManager(self.main)
            return installer.Execute('samples')
        elif args[0]=='zlib':
            installer=InstallManager(self.main)
            return installer.Execute('zlib')
        elif args[0]=='delphes':
            installer=InstallManager(self.main)
            return inst_delphes(self.main,installer)
        elif args[0]=='delphesMA5tune':
            logging.warning("The package 'delphesMA5tune' is now obsolete. It is replaced by Delphes with special MA5-tuned cards.")
            if not self.main.forced:
              logging.warning("Are you sure to install this package? (Y/N)")
              allowed_answers=['n','no','y','yes']
              answer=""
              while answer not in  allowed_answers:
                 answer=raw_input("Answer: ")
                 answer=answer.lower()
              if answer=="no" or answer=="n":
                  return
            installer=InstallManager(self.main)
            return inst_ma5tune(self.main,installer)
        elif args[0]=='fastjet':
            installer=InstallManager(self.main)
            if installer.Execute('fastjet')==False:
                return False
            return installer.Execute('fastjet-contrib')
        elif args[0]=='gnuplot':
            installer=InstallManager(self.main)
            return installer.Execute('gnuplot')
        elif args[0]=='matplotlib':
            installer=InstallManager(self.main)
            return installer.Execute('matplotlib')
        elif args[0]=='root':
            installer=InstallManager(self.main)
            return installer.Execute('root')
        elif args[0]=='numpy':
            installer=InstallManager(self.main)
            return installer.Execute('numpy')
        elif args[0]=='RecastingTools':
            installer=InstallManager(self.main)
            return installer.Execute('RecastingTools')
        elif args[0]=='PADForMA5tune':
            installer=InstallManager(self.main)
            if inst_ma5tune(self.main,installer):
                return installer.Execute('PADForMA5tune')
        elif args[0]=='PAD':
            installer=InstallManager(self.main)
            if inst_delphes(self.main,installer):
                return installer.Execute('PAD')
        elif args[0]=='PADForMA5tunelocal' and len(args)==2:
            installer=InstallManager(self.main)
            if inst_ma5tune(self.main,installer):
                return installer.Execute('PADForMA5tunelocal_xxx_'+args[1])
        else:
            logging.error("the syntax is not correct.")
            self.help()
            return

    def help(self):
        logging.info("   Syntax: install <component>")
        logging.info("   Download and install a MadAnalysis component from the official site.")
        logging.info("   List of available components: samples zlib fastjet delphes delphesMA5tune RecastingTools PAD PADForMA5tune")


    def complete(self,text,args,begidx,endidx):

        nargs = len(args)
        if not text:
            nargs +=1

        if nargs>2:
            return []
        else:
            output = ["samples","zlib","fastjet", "delphes", "delphesMA5tune",\
                "gnuplot", "matplotlib", "root" , "numpy", "RecastingTools", "PAD", "PADForMA5tune"]
            return self.finalize_complete(text,output)



