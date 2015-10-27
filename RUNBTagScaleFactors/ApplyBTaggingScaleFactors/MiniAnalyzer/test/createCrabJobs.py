#!/usr/bin/env python

import sys, os, shutil, re
from optparse import OptionParser


def main():
  # usage description
  usage = "Usage: createCrabJobs.py [options] \nExample: ./createCrabJobs.py -w CRAB_Jobs  -c MiniAOD_cfg.py -t crab_template.py"

  # input parameters
  parser = OptionParser(usage=usage)

  parser.add_option("-w", "--main_workdir", dest="main_workdir",
                    help="Main working directory",
                    metavar="MAIN_WORKDIR")

  parser.add_option("-c", "--cmssw_cfg", dest="cmssw_cfg",
                    help="CMSSW configuration file",
                    metavar="CMSSW_CFG")

  parser.add_option("-t", "--crab_cfg_template", dest="crab_cfg_template",
                    help="CRAB configuration file template",
                    metavar="CRAB_CFG_TEMPLATE")

  parser.add_option("-n", "--no_creation",
                    action="store_true", dest="no_creation", default=False,
                    help="Create the necessary configuration files and skip the job creation (This parameter is optional)")

  (options, args) = parser.parse_args()

  # make sure all necessary input parameters are provided
  if not (options.main_workdir and options.cmssw_cfg and options.crab_cfg_template):
    print usage
    sys.exit()

  main_workdir = options.main_workdir
  cmssw_cfg = options.cmssw_cfg
  crab_cfg_template = options.crab_cfg_template

  # redefine main_workdir as an absolute path (if not defined in such form already)
  if not re.search("^/", main_workdir):
    main_workdir = os.path.join(os.getcwd(),main_workdir)

  # define path for the cfg_files_dir
  cfg_files_dir = os.path.join(main_workdir,'cfg_files')
  print cfg_files_dir
  # create the main working directory and 'cfg_files' subdirectory
  os.mkdir(main_workdir)
  os.mkdir(cfg_files_dir)

  # copy the CMSSW cfg file to the cfg_files_dir
  shutil.copyfile(cmssw_cfg,os.path.join(cfg_files_dir,'CMSSW_cfg.py'))

  # copy the crab cfg file template to the cfg_files_dir
  shutil.copyfile(crab_cfg_template,os.path.join(cfg_files_dir,'crabConfig.py'))
  
if __name__ == "__main__":
  main()
