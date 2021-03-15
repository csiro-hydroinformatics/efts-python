import xarray as xr
import cftime

# from bqplot import Axis, Figure, Lines, LinearScale
# from bqplot.interacts import IndexSelector
# from bqplot import pyplot as plt

# from ipyleaflet import basemaps, FullScreenControl, LayerGroup, Map, MeasureControl, Polyline, Marker, MarkerCluster, CircleMarker, WidgetControl
# from ipywidgets import Button, HTML, HBox, VBox, Checkbox, FileUpload, Label, Output, IntSlider, Layout, Image, link
from ipywidgets import Output, HTML
from ipyleaflet import Map, Marker, MarkerCluster, basemaps

# Had unexpected issues with displaying matplotlib in output widgets.
# https://github.com/jupyter-widgets/ipywidgets/issues/1853#issuecomment-349201240 seems to do the job...
from ipywidgets.widgets.interaction import show_inline_matplotlib_plots

class PropertyAdapter:
    def __init__(self, x_data:xr.Dataset, lat:str='lat', lon:str='lon', key:str='station'):
        self.marker_info = dict()
        self.x_data = x_data
        lats = x_data[lat].values
        lons = x_data[lon].values
        self.lat_key = lat
        self.lon_key = lon
        self.key = key
        values = x_data[key].values
        n= len(lats)
        for i in range(n):
            self.add_marker_info(lats[i], lons[i], values[i])
    
    def add_marker_info(self, lat, lon, code):
        self.marker_info[(lat, lon)] = code
    
    def get_code(self, lat, lon):
        return self.marker_info[(lat, lon)]

    def data_for_identifier(self, ident):
        raise NotImplementedError()

    def build_map(self, click_handler):
        mean_lat = self.x_data[self.lat_key].values.mean()
        mean_lng = self.x_data[self.lon_key].values.mean()
        # create the map
        m = Map(center=(mean_lat, mean_lng), zoom=4, basemap=basemaps.Stamen.Terrain)
        m.layout.height = '600px'
        # show trace
        markers = []
        for k in self.marker_info:
            lat, lon = k
            message = HTML()
            message.description = "Station ID"
            message.value = str(self.marker_info[k])
            message.placeholder = ""
            marker = Marker(location=(lat, lon))
            marker.on_click(click_handler)
            marker.popup = message
            markers.append(marker)
        marker_cluster = MarkerCluster(
            markers=markers
        )
        # not sure whether we could register once instead of each marker:
        # marker_cluster.on_click(click_handler)
        m.add_layer(marker_cluster)
        # m.add_control(FullScreenControl())
        return m

    def plot_series(self, out_widget, variable, loc_id):
        """
        """
        dim_id = None
        if dim_id is None:
            dim_id = self.key
        tts = self.x_data['q_obs_mm'].sel({dim_id: loc_id})
        # if using bqplot down the track:
        # points = gpx.get_points_data(distance_2d=True)
        # px = [p.distance_from_start / 1000 for p in points]
        # py = [p.point.elevation for p in points]

        # x_scale, y_scale = LinearScale(), LinearScale()
        # x_scale.allow_padding = False
        # x_ax = Axis(label='Time', scale=x_scale)
        # y_ax = Axis(label='Value', scale=y_scale, orientation='vertical')

        # lines = Lines(x=px, y=py, scales={'x': x_scale, 'y': y_scale})

        # elevation = Figure(title='Elevation Chart', axes=[x_ax, y_ax], marks=[lines])
        # elevation.layout.width = 'auto'
        # elevation.layout.height = 'auto'
        # elevation.layout.min_height = '500px'
        # elevation.interaction = IndexSelector(scale=x_scale)
        # with(out_widget):
        #     plt.plot(tts)
        out_widget.clear_output()
        with(out_widget):
            display(tts.plot(figsize=(16,8)))
            show_inline_matplotlib_plots()


# If printing a data frame straight to an output widget
# def raw_print(out, ident):
#     x_data = globalthing.data_for_identifier(ident)
#     out.clear_output()
#     with out:
#         print(ident)        
#         print(x_data)
        
# def click_handler_rawprint(**kwargs):
#     blah = dict(**kwargs)
#     xy = blah['coordinates']
#     ident = globalthing.get_code(xy[0], xy[1])
#     raw_print(out, ident)

def click_handler_no_op(**kwargs):
    return

def click_handler_plot_ts(**kwargs):
    blah = dict(**kwargs)
    xy = blah['coordinates']
    ident = globalthing.get_code(xy[0], xy[1])
    globalthing.plot_series(out, variable='q_obs_mm', loc_id=ident)

