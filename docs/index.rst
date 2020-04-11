Welcome to c3dp's documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   installation
   usage
   c3dp
   contributing
   authors
   history
The Python ecosystem is an ideal environment for developing full-circle applications for merging
collimator design, experimental planning and optimization, and 3D printing for neutron scattering
instruments. We present a Python package, c3dp, that uses numpy, scipy, h5py, shapely, and
Matplotlib to design, simulate, optimize and visualize a collimator’s performance quickly,
accurately, and finally convert the optimized configuration straight to a format ready for 3D
printing for diamond anvil or clamp pressure cells used in neutron diffraction experiments on the
SNAP beamline. The package includes Monte Carlo ray tracing of the SNAP instrument, the
collimator geometry, and simulates the neutron interaction with the collimator and the
optimization of the collimator geometry to produce the best configuration. A differential evolution
algorithm from the SciPy library was used for optimization with the objective of minimizing the
simulated background, and a Jupyter notebook is used to integrate each of the steps of the
package into a design and optimization work flow.

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
