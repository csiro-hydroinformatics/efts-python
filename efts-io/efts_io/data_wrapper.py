import xarray as xr
import pandas as pd
import numpy as np

def _byte_array_to_string(x:np.ndarray):
    return ''.join([str(s, encoding='UTF-8') for s in x])

def _byte_stations_to_str(byte_names:np.ndarray):
    return np.array([_byte_array_to_string(x) for x in byte_names])


def _cftime_to_pdtstamp(t):
    return pd.Timestamp(t.isoformat())

_ats = np.vectorize(_cftime_to_pdtstamp)

def cftimes_to_pdtstamps(cftimes):
    return _ats(cftimes)
    
TIME_DIMNAME = 'time'

stations_dim_name = "station"
lead_time_dim_name = "lead_time"
time_dim_name = "time"
ensemble_member_dim_name = "ens_member"
str_length_dim_name = "str_len"

# int station_id[station]   
station_id_varname = "station_id"
# char station_name[str_len,station]   
station_name_varname = "station_name"
# float lat[station]   
lat_varname = "lat"
# float lon[station]   
lon_varname = "lon"
# float x[station]   
x_varname = "x"
# float y[station]   
y_varname = "y"
# float area[station]   
area_varname = "area"
# float elevation[station]   
elevation_varname = "elevation"

conventional_varnames = [
  stations_dim_name ,
  lead_time_dim_name ,
  time_dim_name ,
  ensemble_member_dim_name ,
  str_length_dim_name ,
  station_id_varname ,
  station_name_varname ,
  lat_varname ,
  lon_varname ,
  x_varname ,
  y_varname ,
  area_varname ,
  elevation_varname
]

mandatory_global_attributes = ["title", "institution", "source", "catchment", "comment"]

def get_default_dim_order():
    return [lead_time_dim_name, stations_dim_name, ensemble_member_dim_name, time_dim_name]

class EftsDataSet:
    # Reference class convenient for access to a Ensemble Forecast Time Series in netCDF file.
    # Description
    # Reference class convenient for access to a Ensemble Forecast Time Series in netCDF file.

    # Fields
    # time_dim
    # a cached POSIXct vector, the values for the time dimension of the data set.

    # time_zone
    # the time zone for the time dimensions of this data set.

    # identifiers_dimensions
    # a cache, list of values of the primary data identifiers; e.g. station_name or station_id

    # stations_varname
    # name of the variable that stores the names of the stations for this data set.

    def __init__(self, data):
        from xarray.coding import times
        self.time_dim = None
        self.time_zone = "UTC"
        self.stations_dim_name = "station"
        self.stations_varname = "station_id"
        self.lead_time_dim_name = "lead_time"
        self.ensemble_member_dim_name = "ens_member"
        self.identifiers_dimensions = list()
        if isinstance(data, str):
            # work around https://jira.csiro.au/browse/WIRADA-635
            # lead_time can be a problem with xarray, so do not decode "times"
            x = xr.open_dataset(data, decode_times=False)

            # replace the time and station names coordinates values
            # TODO This is probably not a long term solution for round-tripping a read/write or vice and versa
            decod = times.CFDatetimeCoder(use_cftime=True)
            var = xr.as_variable(x.coords[TIME_DIMNAME])
            time_coords = decod.decode(var, name=TIME_DIMNAME)
            time_coords.values = cftimes_to_pdtstamps(time_coords.values)
            stat_coords = x.coords[self.stations_dim_name]
            station_names = _byte_stations_to_str(x[station_name_varname].values)
            x = x.assign_coords({
                TIME_DIMNAME: time_coords,
                self.stations_dim_name: station_names})

            self.data = x
        else:
            self.data = data

    def get_all_series(self, variable_name = "rain_obs", dimension_id = None):
        # Return a multivariate time series, where each column is the series for one of the identifiers (self, e.g. rainfall station identifiers):
        return self.data[variable_name]
        # stopifnot(variable_name %in% names(ncfile$var))
        # td = self.get_time_dim()
        # if dimension_id is None: dimension_id = self.get_stations_varname()
        # identifiers = self._get_values(dimension_id)
        # ncdims = self.get_variable_dim_names(variable_name)
        # could be e.g.: double q_obs[lead_time,station,ens_member,time] float
        # rain_obs[station,time] lead_time,station,ens_member,time reordered
        # according to the variable present dimensions:
        # tsstart = splice_named_var(c(1, 1, 1, 1), ncdims)
        # tscount = splice_named_var(c(1, length(identifiers), 1, length(td)), ncdims)
        # rawData = ncdf4::ncvar_get(ncfile, variable_name, start = tsstart, count = tscount, 
        # collapse_degen = FALSE)
        # dim_names(rawData) = ncdims
        # # [station,time] to [time, station] for xts creation
        # # NOTE: why can this not be dimension_id instead of stations_dim_name?
        # tsData = reduce_dimensions(rawData,c(time_dim_name, stations_dim_name))
        # v = xts(x = tsData, order.by = td, tzone = tz(td))
        # colnames(v) = identifiers
        # return(v)

    def get_dim_names(self):
        # Gets the name of all dimensions in the data set
        return [x for x in self.data.dims.keys()]

    def get_ensemble_for_stations(self, variable_name = "rain_sim", identifier:str = None, dimension_id = "ens_member", start_time = None, lead_time_count = None):
        # Return a time series, representing a single ensemble member forecast for all stations over the lead time
        raise NotImplementedError()

    def get_ensemble_forecasts(self, variable_name = "rain_sim", identifier:str = None, dimension_id = None, start_time = None, lead_time_count = None):
        # Return a time series, ensemble of forecasts over the lead time
        if dimension_id is None: dimension_id = self.get_stations_varname()
        raise NotImplementedError()

    def get_ensemble_forecasts_for_station(self, variable_name = "rain_sim", identifier:str = None, dimension_id = None):
        # Return an array, representing all ensemble member forecasts for a single stations over all lead times
        if dimension_id is None: dimension_id = self.get_stations_varname()
        raise NotImplementedError()

    def get_ensemble_series(self, variable_name = "rain_ens", identifier:str = None, dimension_id = None):
        # Return an ensemble of point time series for a station identifier
        if dimension_id is None: dimension_id = self.get_stations_varname()
        raise NotImplementedError()

    def get_ensemble_size(self):
        # Length of the ensemble size dimension
        return self.data.dims[self.ensemble_member_dim_name]

    def get_lead_time_count(self):
        # Length of the lead time dimension
        return self.data.dims[self.lead_time_dim_name]

    def get_single_series(self, variable_name = "rain_obs", identifier:str = None, dimension_id = None):
        # Return a single point time series for a station identifier. Falls back on def get_all_series if the argument "identifier" is missing
        if dimension_id is None: dimension_id = self.get_stations_varname()
        return self.data[variable_name].sel({dimension_id: identifier})

    def get_station_count(self):
        # Length of the lead time dimension
        self.data.dims[self.stations_dim_name]

    def get_stations_varname(self):
        # Gets the name of the variable that has the station identifiers
        # TODO: station is integer normally in STF (Euargh)
        return self.data.station.values

    def get_time_dim(self):
        # Gets the time dimension variable as a vector of date-time stamps
        return self.data.time.values # but loosing attributes.

    def get_time_unit(self):
        # Gets the time units of a read time series, i.e. "hours since 2015-10-04 00:00:00 +1030". Returns the string "hours"
        return "dummy"

    def get_time_zone(self):
        # Gets the time zone to use for the read time series
        return "dummy"

    def get_utc_offset(self, as_string = True):
        # Gets the time zone to use for the read time series, i.e. "hours since 2015-10-04 00:00:00 +1030". Returns the string "+1030" or "-0845" if as_string is TRUE, or a lubridate Duration object if FALSE
        return None

    def _get_values(self, variable_name):
        # Gets (and cache in memory) all the values in a variable. Should be used only for dimension variables
        if not variable_name in conventional_varnames:
            raise Exception(variable_name+ " cannot be directly retrieved. Must be in " + ", ".join(conventional_varnames))
        return self.data[variable_name].values

    def get_variable_dim_names(self, variable_name):
        # Gets the names of the dimensions that define the geometry of a given variable
        return [x for x in self.data[[variable_name]].coords.keys()]

    def get_variable_names(self):
        # Gets the name of all variables in the data set
        return [x for x in self.data.variables.keys()]

    def index_for_identifier(self, identifier, dimension_id = None):
        # Gets the index at which an identifier is found in a dimension variable
        if dimension_id is None: dimension_id = self.get_stations_varname()
        raise NotImplementedError()

    def index_for_time(self, dateTime):
        # Gets the index at which a date-time is found in the main time axis of this data set
        raise NotImplementedError()

    def put_ensemble_forecasts(self, x, variable_name = "rain_sim", identifier:str = None, dimension_id = None, start_time = None):
        # Puts one or more ensemble forecast into a netCDF file
        if dimension_id is None: dimension_id = self.get_stations_varname()
        raise NotImplementedError()

    def put_ensemble_forecasts_for_station(self, x, variable_name = "rain_sim", identifier:str = None, dimension_id = "ens_member", start_time = None):
        # Puts a single ensemble member forecasts for all stations into a netCDF file
        raise NotImplementedError()

    def put_ensemble_series(self, x, variable_name = "rain_ens", identifier:str = None, dimension_id = None):
        # Puts an ensemble of time series, e.g. replicate rainfall series
        if dimension_id is None: dimension_id = self.get_stations_varname()
        raise NotImplementedError()

    def put_single_series(self, x, variable_name = "rain_obs", identifier:str = None, dimension_id = None, start_time = None):
        # Puts a time series, or part thereof
        if dimension_id is None: dimension_id = self.get_stations_varname()
        raise NotImplementedError()

    def put_values(self, x, variable_name):
        # Puts all the values in a variable. Should be used only for dimension variables
        raise NotImplementedError()

    def set_time_zone(self, tzone_id):
        # Sets the time zone to use for the read time series
        raise NotImplementedError()

    def summary(self):
        # Print a summary of this EFTS netCDF file
        raise NotImplementedError()

    # See Also
    # See create_efts and open_efts for examples on how to read or write EFTS netCDF files using this dataset.

