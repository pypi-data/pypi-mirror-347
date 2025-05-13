.. image:: https://gitlab.com/maicos-devel/maicos/-/raw/main/docs/static/logo_MAICOS_small.png
   :align: left
   :alt: MAICoS

.. inclusion-readme-intro-start

**MAICoS** is the acronym for Molecular Analysis for Interfacial and Confined Systems.
It is an object-oriented python toolkit for analysing the structure and dynamics of
interfacial and confined fluids from molecular simulations. Combined with MDAnalysis_,
MAICoS can be used to extract density profiles, dielectric constants, structure factors,
or transport properties from trajectories files, including LAMMPS, GROMACS, CHARMM or
NAMD data. MAICoS is open source and is released under the GNU general public license
v3.0.

MAICoS is a tool for beginners of molecular simulations with no prior Python experience.
For these users MAICoS provides a descriptive command line interface. Also experienced
users can use the Python API for their day to day analysis or use the provided
infrastructure to build their own analysis for interfacial and confined systems.

Keep up to date with MAICoS news by following us on Twitter_. If you find an issue, you
can report it on Gitlab_. You can also join the developer team on Discord_ to discuss
possible improvements and usages of MAICoS.

.. _`MDAnalysis`: https://www.mdanalysis.org
.. _`Twitter`: https://twitter.com/maicos_analysis
.. _`Gitlab`: https://gitlab.com/maicos-devel/maicos
.. _`Discord`: https://discord.gg/mnrEQWVAed

.. inclusion-readme-intro-end

Basic example
=============

This is a simple example showing how to use MAICoS to extract the density profile from a
molecular dynamics simulation. The files ``conf.gro`` and ``traj.trr`` correspond to
simulation files from a GROMACS_ simulation package. In a Python environment, type:

.. code-block:: python

    import MDAnalysis as mda
    import maicos

    u = mda.Universe("conf.gro", "traj.trr")
    dplan = maicos.DensityPlanar(u.atoms).run()

The density profile can be accessed from ``dplan.results.profile`` and the position of
the bins from ``dplan.results.bin_pos``.

.. _`GROMACS` : https://www.gromacs.org/

Documentation
=============

For details, tutorials, and examples, please have a look at our documentation_. If you
are using an older version of MAICoS, you can access the corresponding documentation on
ReadTheDocs_.

.. _`documentation`: https://maicos-devel.gitlab.io/maicos/index.html
.. _`ReadTheDocs` : https://readthedocs.org/projects/maicos/

.. inclusion-readme-installation-start

Installation
============

Install MAICoS using `pip`_ with::

    pip install maicos

or using conda_ with::

    conda install -c conda-forge maicos

.. _`pip`: https://pip.pypa.io
.. _`conda`: https://www.anaconda.com

.. inclusion-readme-installation-end

List of analysis modules
========================

.. inclusion-marker-modules-start

Currently, MAICoS supports the following analysis modules in alphabetical order:

.. list-table::
   :widths: 25 50
   :header-rows: 1

   * - Module Name
     - Description

   * - DensityCylinder
     - Compute cylindrical partial densitiy profiles
   * - DensityPlanar
     - Compute cartesian partial density profiles
   * - DensitySphere
     - Compute spherical partial density profiles
   * - DielectricCylinder
     - Compute cylindrical dielectric profiles
   * - DielectricPlanar
     - Compute planar dielectric profiles
   * - DielectricSpectrum
     - Compute the linear dielectric spectrum
   * - DielectricSphere
     - Compute spherical dielectric profiles
   * - DipoleAngle
     - Compute angle timeseries of dipole moments
   * - DiporderCylinder
     - Compute cylindrical dipolar order parameters
   * - DiporderPlanar
     - Compute planar dipolar order parameters
   * - RDFDiporder
     - Spherical Radial Distribution function between dipoles
   * - DiporderSphere
     - Compute spherical dipolar order parameters
   * - DiporderStructureFactor
     - Structure factor for dipoles
   * - KineticEnergy
     - Compute the timeseries of energies
   * - PDFCylinder
     - Compute cylindrical shell-wise 1D pair distribution functions
   * - PDFPlanar
     - Compute slab-wise planar 2D pair distribution functions
   * - Saxs
     - Compute small angle X-Ray structure factors and scattering intensities (SAXS)
   * - TemperaturePlanar
     - Compute temperature profiles in a cartesian geometry
   * - VelocityCylinder
     - Compute the cartesian velocity profile across a cylinder
   * - VelocityPlanar
     - Compute the velocity profile in a cartesian geometry

.. inclusion-marker-modules-end
