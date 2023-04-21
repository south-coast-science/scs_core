# scs_core
The root of all South Coast Science environmental monitoring applications.

_Contains library classes only._


**Required libraries:** 

* Third party: AWSIoTPythonSDK, pytz, tzlocal


**Branches:**

The stable branch of this repository is master. For deployment purposes, use:

    git clone --branch=master https://github.com/south-coast-science/scs_core.git


**Python installation on Linux**

[How to install Python 3.7 with SSL?](https://raspberrypi.stackexchange.com/questions/88150/how-to-install-python-3-7-with-ssl)

[How To Install the Latest Python Version on Raspberry Pi?](https://raspberrytips.com/install-latest-python-raspberry-pi/)
  
wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz

[ImportError: No module named _ssl](https://stackoverflow.com/questions/5128845/importerror-no-module-named-ssl)
  
***scipy:***
  
as root...

apt-get install --reinstall python3-apt

apt install gfortran

apt install libopenblas-dev


as scs...

pip install cmake

pip install openblas

pip install scipy

[Unable to install Scipy with MKL using Meson](https://stackoverflow.com/questions/73628794/unable-to-install-scipy-with-mkl-using-meson)

[INSTALLATION](https://scipy.org/install/)

[ERROR: Failed building wheel for ninja #6381](https://github.com/freqtrade/freqtrade/issues/6381)

[Installing GFortran](https://fortran-lang.org/en/learn/os_setup/install_gfortran/)

