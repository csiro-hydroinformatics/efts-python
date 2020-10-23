import os
import numpy as np
import pandas as pd
import sys
from datetime import datetime

pkg_dir = os.path.join(os.path.dirname(__file__),'..')
sys.path.insert(0, pkg_dir)

from efts_io.data_wrapper import *

def test_read_thing():
    fn = '/home/per202/src/csiro/stash/rr-ml/pkg/efts-io/tests/data/hourly_test.nc'
    ds = EftsDataSet(fn)
    assert set(ds.get_dim_names()) == set(['ens_member', 'lead_time', 'station', 'str_len', 'time'])
if __name__ == "__main__":
    test_read_thing()
