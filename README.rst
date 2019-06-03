====
c3dp
====
  
.. image:: https://anaconda.org/fi0/c3dp/badges/version.svg   
        :target: https://anaconda.org/fi0/c3dp
        
.. image:: https://anaconda.org/fi0/c3dp/badges/platforms.svg   
        :target: https://anaconda.org/fi0/c3dp
    
.. image:: https://img.shields.io/pypi/v/c3dp.svg
        :target: https://pypi.python.org/pypi/c3dp

.. image:: https://img.shields.io/travis/fahima-islam/c3dp.svg
        :target: https://travis-ci.org/fahima-islam/c3dp

.. image:: https://readthedocs.org/projects/c3dp/badge/?version=latest
        :target: https://c3dp.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/fahima-islam/c3dp/shield.svg
     :target: https://pyup.io/repos/github/fahima-islam/c3dp/
     :alt: Updates

mcstas: http://mcstas.org/
MCViNE: https://mcvine.org

design of 3D printed high pressure cell collimator
-----------------------------------------------------------

.. image:: https://raw.githubusercontent.com/Fahima-Islam/c3dp/master/figures/Screenshot%20from%202019-04-23%2011-51-49.png
   :width: 300pt

.. image:: https://raw.githubusercontent.com/Fahima-Islam/c3dp/master/figures/coll_performance.png
   :width: 300pt
   
gauge volume example: https://github.com/Fahima-Islam/c3dp/blob/gauge_volume/notebooks/gauge_volume.ipynb

.. image:: https://raw.githubusercontent.com/Fahima-Islam/c3dp/gauge_volume/figures/gauge_volume.png
   :width: 300pt

Features
--------

* Simulation of the the diffractometer
* SImulation of the pressure cell
* Optimization of  the collimator for the given pressure cell
* Produced the .stl or .scad file of the collimator to be 3D printed
* Produced the comparison in the diffraction pattern for with and without collimator

Installation
-------------
* Clone the repository and execute from within and execute:

.. code-block:: shell

    $ git clone git@github.com:Fahima-Islam/c3dp.git
    $ cd c3dp
    
* Anaconda (Recommended)
.. code-block:: shell

    $ conda install -c fi0 c3dp
    
* Pypi
.. code-block:: shell

    $ pip install c3dp
    
* Install mcvine 

.. code-block:: shell

    $ conda create -n mcvine python=2.7         # create an environment for mcvine
    $ source activate mcvine                    # activate mcvine environment
    $ conda config --add channels conda-forge   # add conda channels
    $ conda config --add channels diffpy
    $ conda config --add channels mantid
    $ conda config --add channels mcvine
    $ conda install numpy                       # install
    $ conda install mcvine

* Install mcstast

    `mcstas <http://downloads.mcstas.org/>`_
    
* Install shapely

   `shapely <https://pypi.org/project/Shapely/>`_

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
