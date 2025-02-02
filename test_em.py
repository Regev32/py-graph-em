# -*- coding: utf-8 -*-

#
#    py-graph-em
#    Copyright (c) 2021 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#

import numpy as np
import json
# Workaround for NumPy 2.0 removing np.float_
np.float_ = np.float64

import os
from EM.run_em import run_em_def

if __name__ == "__main__":
    conf_file = "conf/minimal-em-configuration.json"
    with open(conf_file) as f:
        json_conf = json.load(f)
    output_dir = json_conf.get("output_dir", "output")
    os.makedirs(output_dir, exist_ok=True)
    run_em_def(conf_file)
