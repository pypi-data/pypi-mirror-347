"""
 Copyright (C) 2023 Università degli Studi di Camerino.
 Authors: Alessandro Antinori, Rosario Capparuccia, Riccardo Coltrinari, Flavio Corradini, Marco Piangerelli, Barbara Re, Marco Scarpetta, Luca Mozzoni, Vincenzo Nucci

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as
 published by the Free Software Foundation, either version 3 of the
 License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <https://www.gnu.org/licenses/>.
 """

"""Top-level package for SIMPLE Repository."""

__author__ = """Università degli Studi di Camerino."""
__version__ = "0.1.0"

from . import _version

__version__ = _version.get_versions()["version"]

hard_dependencies = ["networkx", "numpy", "pandas"]
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError:
        missing_dependencies.append(dependency)

if missing_dependencies:
    raise ImportError(f"Missing required dependencies:{','.join(missing_dependencies)}")

from rain.core.base import *  # noqa: E402
from rain.nodes import *  # noqa: E402
