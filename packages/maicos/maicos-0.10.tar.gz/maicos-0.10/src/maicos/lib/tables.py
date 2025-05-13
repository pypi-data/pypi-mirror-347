#!/usr/bin/env python
#
# Copyright (c) 2025 Authors and contributors
# (see the AUTHORS.rst file for the full list of names)
#
# Released under the GNU Public Licence, v3 or any higher version
# SPDX-License-Identifier: GPL-3.0-or-later
"""The module contains static lookup tables for atom typing etc.

The tables are dictionaries that are indexed by elements.
"""

from dataclasses import dataclass
from pathlib import Path

import numpy as np

_share_path = Path(__file__).parents[1] / "share"


#: Translation of
#: :py:class:`MDAnalysis.AtomGroup.types <MDAnalysis.core.topologyattrs.Atomtypes>` to
#: chemical elements.
atomtypes = {}
with Path(_share_path / "atomtypes.dat").open() as f:
    for line in f:
        if line[0] != "#":
            elements = line.split()
            atomtypes[elements[0]] = elements[1]


@dataclass
class CMParameter:
    """Cromer-Mann X-ray scattering factor parameters."""

    a: np.ndarray
    b: np.ndarray
    c: float


#: Cromer-Mann X-ray scattering factors computed from numerical
#: Hartree-Fock wave functions. See https://it.iucr.org/Cb/ch6o1v0001/
CM_parameters = {}
with Path(_share_path / "sfactor.dat").open() as f:
    for line in f:
        if line[0] != "#":
            params = line.split()
            element = params[0]

            CM_parameters[element] = CMParameter(
                a=np.array(params[1:5], dtype=np.double),
                b=np.array(params[5:9], dtype=np.double),
                c=float(params[9]),
            )
