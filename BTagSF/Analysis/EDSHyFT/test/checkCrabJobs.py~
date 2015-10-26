#!/usr/bin/env python

import sys, os, shutil, re
from optparse import OptionParser


def main():
  # usage description
  usage = "Usage: checkCrabJobs.py [options] \nExample: ./checkCrabJobs.py -w CRAB_Jobs"

  # input parameters
  parser = OptionParser(usage=usage)

  parser.add_option("-w", "--main_workdir", dest="main_workdir",
                    help="Main working directory",
                    metavar="MAIN_WORKDIR")

  parser.add_option("-s", "--submit",
                    action="store_true", dest="submit", default=False,
                    help="Submit CRAB jobs (This parameter is optional)")

  parser.add_option("-g", "--getoutput",
                    action="store_true", dest="getoutput", default=False,
                    help="Get output from CRAB jobs (This parameter is optional)")

  parser.add_option("-r", "--report",
                    action="store_true", dest="report", default=False,
                    help="Get CRAB report (This parameter is optional)")

  parser.add_option("-k", "--kill",
                    action="store_true", dest="kill", default=False,
                    help="Kill CRAB jobs (This parameter is optional)")

  (options, args) = parser.parse_args()

  # make sure all necessary input parameters are provided
  if not options.main_workdir:
    print usage
    sys.exit()

  if len(sys.argv)>4:
    print 'Only one optional parameter at a time is allowed'
    sys.exit()

  main_workdir = options.main_workdir
  cfg_file = options.main_workdir + '/cfg_files/*_crab.py'

  # redefine main_workdir as an absolute path (if not defined in such form already)
  if not re.search("^/", main_workdir):
    main_workdir = os.path.join(os.getcwd(),main_workdir)

  # open and read the dataset_list file
  dataset_list_file = open(os.path.join(main_workdir,'datasetList.txt'),"r")
  dataset_list_lines = dataset_list_file.readlines()

  # loop over datasets
  for line in dataset_list_lines:
    line_elements = line.split()
    if (len(line_elements)==0 or line_elements[0][0]=='#'): continue

    workdir2 = 'crab_'+line_elements[0].lstrip('/').replace('/','__')
    workdir = os.path.join(main_workdir,'crab_'+line_elements[0].lstrip('/').replace('/','__'))

    if(options.submit):
      os.system('crab submit -c ' + cfg_file)
      shutil.move(workdir2, main_workdir)
    elif(options.getoutput):
      os.system('crab getoutput ' + workdir)
    elif(options.report):
      os.system('crab status ' + workdir)
      os.system('crab report ' + workdir)
    elif(options.kill):
      os.system('crab kill all ' + workdir)
    else:
      os.system('crab status ' + workdir)


if __name__ == "__main__":
  main()
