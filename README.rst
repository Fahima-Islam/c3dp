====
c3dp
====
  
.. image:: https://anaconda.org/fi0/c3dp/badges/version.svg 
        :target: https://anaconda.org/fi0/c3dp
        
.. image:: https://anaconda.org/fi0/c3dp/badges/platforms.svg   
        :target: https://anaconda.org/fi0/c3dp
    
.. image:: https://img.shields.io/pypi/v/c3dp.svg
        :target: https://pypi.python.org/pypi/c3dp


Automated design of 3D printed collimator optimized for high pressure diffraction
---------------------------------------------------------------------------------
Features
--------
 description of the simulation (https://github.com/Fahima-Islam/c3dp/blob/master/docs/poster_ICANS.pdf)
* Simulation of the the diffractometer (https://github.com/Fahima-Islam/McStas_SNAP/blob/master/SNAP_2018.instr)
* SImulation of the pressure cells (Diamond Anvil cell -https://github.com/Fahima-Islam/c3dp/blob/master/notebooks/DAC_geometry_creation-forSimulation.ipynb) and (clamp cell -https://github.com/Fahima-Islam/c3dp/blob/master/notebooks/clampCell_geometry.ipynb)
* Optimization of  the collimator for the given pressure cell (Diamond Anvil Cell- https://github.com/Fahima-Islam/c3dp/blob/master/notebooks/c3dp-Optimization_DAC%2BCOlli-50mmAway_from_Sample.ipynb, Clamp cell- https://github.com/Fahima-Islam/c3dp/blob/master/notebooks/c3dp-Optimization(cellbysample%20adding%20samplebyscattered%20N)-PerformanceIndex-length_channelGap.ipynb)
* Produced the .stl or .scad file of the collimator to be 3D printed (clamp cell - https://github.com/Fahima-Islam/c3dp/blob/master/notebooks/collimator_clampCell.ipynb, diamond anvil cell - https://github.com/Fahima-Islam/c3dp/blob/master/notebooks/collimator_differentBlade_threeSections_9n%2B1_chanels-splitting_correctly_DAC.ipynb)
* Produced the comparison in the diffraction pattern for with and without collimator
* Produced the gauge volume of the collimator (https://github.com/Fahima-Islam/c3dp/blob/master/notebooks/gauge_volume_collimator_cylinder.ipynb)

.. image:: https://raw.githubusercontent.com/Fahima-Islam/c3dp/master/figures/flow.png
   :width: 300pt

Examples
--------
* Clamp cell:

.. image:: https://raw.githubusercontent.com/Fahima-Islam/c3dp/master/figures/Screenshot%20from%202019-04-23%2011-51-49.png
   :width: 300pt


.. image:: https://raw.githubusercontent.com/Fahima-Islam/c3dp/master/figures/diffraction_pattern_clamp_cell.PNG
   :width: 300pt
   
* Diamond anvil cell:

.. image:: https://raw.githubusercontent.com/Fahima-Islam/c3dp/master/figures/dac.png
   :width: 300pt
   
.. image:: https://raw.githubusercontent.com/Fahima-Islam/c3dp/master/figures/DAC_diffraction_pattern.PNG
   :width: 300pt

* Gauge volume:
gauge volume example: https://github.com/Fahima-Islam/c3dp/blob/gauge_volume/notebooks/gauge_volume.ipynb

.. image:: https://raw.githubusercontent.com/Fahima-Islam/c3dp/master/figures/gauge.png
   :width: 300pt


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
    


