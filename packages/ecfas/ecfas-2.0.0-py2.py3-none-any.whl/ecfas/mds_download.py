import logging
import os
import sys

import copernicusmarine as mds
import ecfas.cmems_datasets as dsets
import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


def mds_download(usr, pwd, t_start, t_end, out_dir, data_sets, dset_type, region=None, label='analysis'):
    """ Downloads hydro or wave data from CMEMS using copernicusmarine API """
    log.info(f'>> Downloading data for {dset_type}')

    max_time = 1
    tot_time = pd.Timestamp(t_end) - pd.Timestamp(t_start)
    if tot_time.total_seconds() < 0:
        log.error('The total time is negative, something is wrong with the dates')
        sys.exit(1)
    num_time_intervals = np.ceil(tot_time.days / max_time)

    times = []
    for tt in range(0, int(num_time_intervals)):
        times.append([pd.Timestamp(t_start) + pd.Timedelta(days=int(max_time * tt)), pd.Timestamp(t_start) + pd.Timedelta(days=int(max_time * (tt + 1)))])

    setsel = []
    if region is None:
        setsel.append(list(data_sets.keys()))
    elif region == 'ARC' and dset_type == 'PHY':
        setsel.append('ARC_ocean')
        setsel.append('ARC')
    else:
        setsel.append(region)

    for dseti in setsel:
        log.info(f'>> Region {dseti}')
        dsets = data_sets[dseti]
        out = os.path.join(out_dir, '%s' % dseti)
        out = os.path.join(out, 'data')

        if not os.path.exists(out):
            os.makedirs(out)
        
        for tt in range(0, int(num_time_intervals)):
            tmin = times[tt][0]
            tmax = times[tt][1]
            out_file = get_file_name(tmin, tmax, label, dset_type, dsets['var'])
            if os.path.isfile(os.path.join(out, out_file)):
                log.info(f'File {out_file} already exists')
                continue
            try:
                log.info(f'Downloading {out_file}')
                mds.subset(dataset_id=dsets['product'],
                                        variables=list(np.ravel(dsets['var'])),
                                        minimum_longitude=dsets['lon_min'],
                                        maximum_longitude=dsets['lon_max'],
                                        minimum_latitude=dsets['lat_min'],
                                        maximum_latitude=dsets['lat_max'],
                                        coordinates_selection_method='nearest',
                                        start_datetime=str(tmin),
                                        end_datetime=str(tmax),
                                        output_filename=out_file,
                                        output_directory=out,
                                        username=usr,
                                        password=pwd
                                        ) 
            except Exception as e:
                log.error(f'Download failed: {str(e)}')
                sys.exit(1)

     
def get_file_name(tmin, tmax, label, dset_type, ds_vars):
        """ Returns output filename """
        tmin_str = str(tmin).replace(':', '-').replace(' ', '_')
        tmax_str = str(tmax).replace(':', '-').replace(' ', '_')
        file_name = label + '_' + tmin_str + '_' + tmax_str + '.nc'

        if ds_vars is None:
            file_name = 'all' + '_' + file_name
        elif isinstance(ds_vars, list):
            if isinstance(ds_vars[0], list):
                file_name = dset_type + 'subset' + '_' + file_name
            else:
                if ds_vars[0] != None:
                    file_name = ds_vars[0] + '_' + file_name
        else:
            file_name = ds_vars + '_' + file_name

        return file_name
