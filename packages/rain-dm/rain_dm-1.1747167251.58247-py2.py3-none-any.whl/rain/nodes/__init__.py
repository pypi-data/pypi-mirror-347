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

from rain.nodes.custom import *
from rain.nodes.pandas import *


# Modular import of nodes: it is never correct to pass the exceptions
# but it is the only way I found to have both the modular import
# and the code completion by IDEs.
try:
    from rain.nodes.sklearn import *
except ModuleNotFoundError or ImportError:
    pass

try:
    from rain.nodes.mongodb import *
except ModuleNotFoundError or ImportError:
    pass

try:
    from rain.nodes.spark import *
except ModuleNotFoundError or ImportError:
    pass

try:
    from rain.nodes.tpot import *
except ModuleNotFoundError or ImportError:
    pass

try:
    from rain.nodes.pysad import *
except ModuleNotFoundError or ImportError:
    pass

try:
    from rain.nodes.pm4py import *
except ModuleNotFoundError or ImportError:
    pass

try:
    from rain.nodes.google_cloud_bigquery import *
except ModuleNotFoundError or ImportError:
    pass

try:
    from rain.nodes.google_cloud_storage import *
except ModuleNotFoundError or ImportError:
    pass

try:
    from rain.nodes.pytorch import *
except ModuleNotFoundError or ImportError:
    pass
