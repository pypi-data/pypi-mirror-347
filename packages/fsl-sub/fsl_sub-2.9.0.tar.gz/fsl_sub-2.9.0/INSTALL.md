# Installation

## Installation within FSL

FSL 6.0.6 and newer ships with fsl_sub and the SGE and SLURM backends installed and ready to use.

FSL 6.0.5 ships with fsl_sub pre-installed but lacking any grid backends. If you wish to use fsl_sub with a supported cluster backend you can use the command `fsl_sub_plugin` to query and install the appropriate FSL distributed backend.

### Install backend

The command:

~~~bash
fsl_sub_plugin --install
~~~

will search for and allow you to install a plugin. Note that this command is only supported in FSL 6.0.5 and older - it will not work with versions of FSL newer than 6.0.5.

## Standalone Installation

Where fsl_sub is to be used outside of the FSL distribution it is recommended that it is installed within a Conda or virtual environment.

### Requirements

fsl_sub requires Python >=3.8 (3.12 recommended) and ruamel.yaml >=0.16.7

### Installation with Conda

First, install Miniconda from <https://conda.io/miniconda.html>, install as per their instructions then create an environment and activate:

~~~bash
conda create -n fsl_sub python=3
source activate fsl_sub
~~~

and install fsl\_sub with the following (note that the package names are delimited with hyphens and not underscores):

~~~bash
conda install -c https://fsl.fmrib.ox.ac.uk/fsldownloads/fslconda/public -c conda-forge fsl-sub
~~~

Plugins can be installed with:

Grid Engine...

~~~bash
conda install -c https://fsl.fmrib.ox.ac.uk/fsldownloads/fslconda/public -c conda-forge fsl-sub-plugin-sge
~~~

SLURM...

~~~bash
conda install -c https://fsl.fmrib.ox.ac.uk/fsldownloads/fslconda/public -c conda-forge fsl-sub-plugin-slurm
~~~

### Installation in a virtual environment

Using Python 3.8+, create a virtual environment with:

~~~bash
python -m venv /path/to/my/venv
~~~

(if you have multiple Python versions available, you can often choose with e.g. _python3.11_)

Now activate this virtual environment with:

~~~bash
source activate /path/to/my/venv/bin/activate
~~~

and fsl_sub can be installed with:

~~~bash
pip install fsl-sub
~~~

To install a plugin, ensure your environment is activated and then install the plugin with:

Grid Engine:

~~~bash
pip install fsl-sub-plugin-sge
~~~

SLURM:

~~~bash
pip install fsl-sub-plugin-slurm.git
~~~
