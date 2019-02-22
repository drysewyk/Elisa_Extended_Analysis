#!/bin/bash
date
hostname
cd /data/user/drysewyk/llh_sandbox
eval export SROOTBASE="/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1" ;
export SROOT="/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/RHEL_7_x86_64" ;
export OS_ARCH="RHEL_7_x86_64" ;
export PATH="/data/user/drysewyk/software/meta-projects/icerec/V05-02-00/build/bin:/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/RHEL_7_x86_64/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/puppetlabs/bin:/home/drysewyk/bin" ;
export LD_LIBRARY_PATH="/data/user/drysewyk/software/meta-projects/icerec/V05-02-00/build/lib:/data/user/drysewyk/software/meta-projects/icerec/V05-02-00/build/lib/tools::/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/../distrib/OpenCL_RHEL_7_x86_64/lib/RHEL_7_x86_64:/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/../distrib/jdk1.6.0_24_RHEL_7_x86_64/lib:/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/../distrib/jdk1.6.0_24_RHEL_7_x86_64/jre/lib:/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/../distrib/jdk1.6.0_24_RHEL_7_x86_64/jre/lib/amd64:/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/../distrib/jdk1.6.0_24_RHEL_7_x86_64/jre/lib/amd64/server:/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/RHEL_7_x86_64/lib:/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/RHEL_7_x86_64/tools/gfortran" ;
export PYTHONPATH="/data/user/drysewyk/software/meta-projects/icerec/V05-02-00/build/lib:/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/RHEL_7_x86_64/lib/python2.7/site-packages::/data/user/drysewyk/software/external/skylab:/data/user/drysewyk/software/external/skylab" ;
export I3_DATA="/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/../data" ;
export I3_TESTDATA="/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/../data/i3-test-data" ;
export PKG_CONFIG_PATH="/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/RHEL_7_x86_64/lib/pkgconfig" ;
export PERL5LIB="/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/RHEL_7_x86_64/lib/perl" ;
export MANPATH="/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/RHEL_7_x86_64/man:/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/RHEL_7_x86_64/share/man" ;
export GCC_VERSION="4.8.5" ;
export ROOTSYS="/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/RHEL_7_x86_64" ;
export LHAPDF_DATA_PATH="/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/../data/lhapdfsets/5.9.1" ;
export GENIE="/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/RHEL_7_x86_64" ;
export GOTO_NUM_THREADS="1" ;
export GLOBUS_LOCATION="/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/RHEL_7_x86_64" ;
export X509_CERT_DIR="/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/RHEL_7_x86_64/share/certificates" ;
export OPENCL_VENDOR_PATH="/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/../distrib/OpenCL_RHEL_7_x86_64/etc/OpenCL/vendors" ;
/data/user/drysewyk/software/meta-projects/icerec/V05-02-00/build/env-shell.sh python Python_Elisa/disc_2.py
date
