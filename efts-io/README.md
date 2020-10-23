# efts_io

## RR modelling with ML

## License

TBD

## Documentation

Nope

## Installation 

DRAFT

The quickest way with conda. We recommend installing conda packages rather than pip packages whereever possible.

on Linux:

```bash
wget https://raw.githubusercontent.com/csiro-hydrogeology/pyefts_io/testing/configs/efts_io_environment.yml
my_env_name=ELA
# my_env_name=etuuser
conda env create -n $my_env_name -f ./efts_io_environment.yml python=3.7
conda activate $my_env_name 
```

This should be all to get a working environment. If you want to use 'efts_io' from jupyter lab:

```bash
conda install --name ${my_env_name} jupyterlab ipywidgets jupyter
jupyter-labextension install @jupyter-widgets/jupyterlab-manager
python -m ipykernel install --user --name ${my_env_name} --display-name "Py3 ELA"
```

Windows:

```bat
call C:\Users\xxxyyy\AppData\Local\Continuum\anaconda3\Scripts\activate.bat
REM curl should come with anaconda3. Perhaps not with miniconda though.
where curl
cd c:\tmp
curl -o efts_io_environment.yml https://raw.githubusercontent.com/csiro-hydrogeology/pyefts_io/testing/configs/efts_io_environment.yml
set my_env_name=ELA
conda env create -n %my_env_name% -f efts_io_environment.yml python=3.7
conda activate %my_env_name% 
```

```bat
This should be all to get a working environment. If you want to use 'efts_io' from jupyter lab:
```

```bat
conda install -c conda-forge --name %my_env_name% jupyterlab ipywidgets jupyter
jupyter-labextension install @jupyter-widgets/jupyterlab-manager
python -m ipykernel install --user --name %my_env_name% --display-name "Py3 ELA"
```

### Troubleshooting 

pip packages specified from the `environment.yaml` files may have not installed (under investigation). Check that pvgeo and "our" packages are installed e.g.

```bat
conda activate %my_env_name%
conda list | grep pvgeo
```

if not present:

```bat
REM make sure you have git in the PATH e.g.
set PATH=C:\Users\per202\AppData\Local\Atlassian\SourceTree\git_local\mingw32\bin\;%PATH%
where git

conda activate %my_env_name%
pip install --no-deps pvgeo
pip install -e git+https://github.com/jmp75/striplog@master#egg=striplog
pip install --no-deps -e git+https://github.com/jmp75/pyetu@master#egg=etu
```

### Manual installation

As of January 2019 [etu is on pypi](https://pypi.org/project/efts_io/). While `pip install efts_io` might work on some computers, it is _unlikely that all python geospatial dependencies will install_. *We highly recommend you set up a conda environment with all dependent packages* prior to installing efts_io with pip or from source.

'efts_io' relies on several external packages, and some can be fiddly to install depending on the version of Python and these external packages. This section thus has fairly prescriptive instructions, given in the hope of limiting the risk of issues.

### Debian packages for spatial projections

`cartopy` and possibly other python packages require `proj4` version 4.9+ to be installed (libproj-dev). If your debian/ubuntu repo does not suffice (older versions) you may try:

```bash
sudo apt-get install -y libc6  
wget http://en.archive.ubuntu.com/ubuntu/pool/universe/p/proj/proj-data_4.9.3-2_all.deb
sudo dpkg -i proj-data_4.9.3-2_all.deb
wget http://en.archive.ubuntu.com/ubuntu/pool/universe/p/proj/libproj12_4.9.3-2_amd64.deb
sudo dpkg -i libproj12_4.9.3-2_amd64.deb
wget http://en.archive.ubuntu.com/ubuntu/pool/universe/p/proj/proj-bin_4.9.3-2_amd64.deb
sudo dpkg -i proj-bin_4.9.3-2_amd64.deb
wget http://en.archive.ubuntu.com/ubuntu/pool/universe/p/proj/libproj9_4.9.2-2_amd64.deb 
sudo dpkg -i libproj9_4.9.2-2_amd64.deb
wget http://en.archive.ubuntu.com/ubuntu/pool/universe/p/proj/libproj-dev_4.9.3-2_amd64.deb
sudo dpkg -i libproj-dev_4.9.3-2_amd64.deb
```

### Installation of python packages dependencies

We recommend installing [Anaconda](http://docs.continuum.io/anaconda/install) to install dependencies. Note that I recommend to **not** let anaconda change your startup file and change the `PATH` environment. To activate Anaconda you first need: `source ~/anaconda3/bin/activate`. Then choose a conda environment name.

Optionally, if your anaconda installation is a bit dated, you may want to do `conda update -n base conda` and `conda update -n base anaconda-navigator`

To create the conda environment for efts_io on Linux:

```bash
# source ~/anaconda3/bin/activate
my_env_name=ELA
conda create --name ${my_env_name} python=3.7
conda install --name ${my_env_name} rasterio cartopy geopandas pandas nltk scikit-learn scikit-image matplotlib vtk
conda activate  ${my_env_name}
```

On Windows, using the DOS CMD prompt, assuming you installed Anaconda in user mode.

```bat
call %userprofile%\AppData\Local\Continuum\anaconda3\Scripts\activate.bat
set my_env_name=ELA
conda create --name %my_env_name% python=3.7
REM if using conda activate  %my_env_name%  I seem to loose conda from the command line, so:
conda install --name %my_env_name% conda 
conda install --name %my_env_name% rasterio cartopy geopandas pandas nltk scikit-learn scikit-image matplotlib vtk
conda activate  %my_env_name%
```

At this point we have installed all the python dependencies efts_io needs that are available via `conda`.

As of writing (2019-08) conda does not have pyqt5, and no suitable version of mayavi for python3. We resort to use `pip`. You may want to do first:

```bash
pip install --upgrade pip
```

For Python 3.x one needs to install pyqt5 for mayavi, as per [these instructions](https://docs.enthought.com/mayavi/mayavi/installation.html). As of Jan 2019 be aware that there is a [known issue in mayavi visual rendering with pyqt5 as a backend on Linux](https://github.com/enthought/mayavi/issues/656) and 'efts_io' is affected by this. Nevertheless this is not a commplete blocker for most 'efts_io' features so installation instructions are kept here.

```bash
pip search pyqt5 | sort -g
pip search mayavi
```

```bash
pip install pyqt5
pip install mayavi
```
For users without admin rights，

```bash
conda install pyqt5
pip install mayavi --user
```

At this point all mandatory dependencies for 'efts_io' are installed.

### Installing ELA

There are three options to access efts_io:

*  use the latest available on pip, 
*  clone and install with `setup.py`
*  direct import of the package directory (this is done at runtime from e.g. a notebook)

```bash
pip search efts_io
pip install efts_io
```

Alternatively, from source with `setup.py`

```bash
pip install -r requirements.txt
python setup.py install
```

#### Optional dependencies

As of 2019-05 you can find new features using deep learning for classification in the submodule `etu.experiment`. You will need the additional dependencies:

```bash
conda install --name ${my_env_name} gensim tensorflow keras
pip install wordcloud
```

If reading xls files using pandas, need pkg `xlrd` with e.g. `conda install xlrd`

### using Jupyter-lab

You may use efts_io as you prefer; we recomment using "Jupyter Lab" to write notebooks. See the [Jupyter lab doc](https://jupyterlab.readthedocs.io/en/stable/) for official information. 

The following should be enough otherwise to use 'efts_io'

Linux:

```bash
my_env_name=ELA
conda install --name ${my_env_name} jupyterlab ipywidgets jupyter
jupyter-labextension install @jupyter-widgets/jupyterlab-manager
python -m ipykernel install --user --name ${my_env_name} --display-name "Py3 ELA"
```

Windows: 

```bat
set my_env_name=ELA
conda install --name %my_env_name% jupyterlab ipywidgets jupyter
jupyter-labextension install @jupyter-widgets/jupyterlab-manager
python -m ipykernel install --user --name %my_env_name% --display-name "Py3 ELA"
```

## Retuted Geoscience packages

'efts_io' aims to complement other Python packages for geoscience, in particular for handling bore data . It already depends on the package ['striplog'](https://github.com/agile-geoscience/striplog) and is likely to depend on ['lasio'](https://github.com/kinverarity1/lasio) in the future.

You should also check the repository [hydrogeol_utils](https://github.com/Neil-Symington/hydrogeol_utils)

## Known issues

3D interactive visualisation - Using mayavi 4.6+ on python 3.6+ may be [visually buggy](https://github.com/enthought/mayavi/issues/656) on Linux. This appears to be a low level issue running on laptop with dual Intel/NVIDIA Graphic cards.

## Troubleshooting

If in a conda environment trying to use `pip` you get:

```text
ModuleNotFoundError: No module named 'pip._internal'
```

consider:

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --force-reinstall
```