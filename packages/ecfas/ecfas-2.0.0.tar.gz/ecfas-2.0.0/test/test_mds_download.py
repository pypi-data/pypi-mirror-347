import os

import ecfas.cmems_datasets as ds
import ecfas.mds_download as mds
import ecfas.utils as utils


def setup_module():
    global out_dir
    out_dir = 'test_outputs'
    utils.clean_dir(out_dir)
    global user
    user = os.environ['COPERNICUSMARINE_SERVICE_USERNAME']
    global password
    password = os.environ['COPERNICUSMARINE_SERVICE_PASSWORD']


def test_download_hydroset():
    t_start = '2024-05-01 00:00:00'
    t_end = '2024-05-02 00:00:00'
    mds.mds_download(user, password, t_start, t_end, out_dir, ds.datasets_hydro, "PHY", region='NWS')


def test_download_waveset():
    t_start = '2024-05-01 00:00:00'
    t_end = '2024-05-02 00:00:00'
    mds.mds_download(user, password, t_start, t_end, out_dir, ds.datasets_wave, "WAV", region='NWS')
    
