# from typing import Any, Callable, Dict, Tuple
# from IPython.core.display import display
# import xarray as xr
# import cftime

# # from bqplot import Axis, Figure, Lines, LinearScale
# # from bqplot.interacts import IndexSelector
# # from bqplot import pyplot as plt

# # from ipyleaflet import basemaps, FullScreenControl, LayerGroup, Map, MeasureControl, Polyline, Marker, MarkerCluster, CircleMarker, WidgetControl
# # from ipywidgets import Button, HTML, HBox, VBox, Checkbox, FileUpload, Label, Output, IntSlider, Layout, Image, link
# from ipywidgets import Output, HTML
# from ipyleaflet import Map, Marker, MarkerCluster, basemaps

# # Had unexpected issues with displaying matplotlib in output widgets.
# # https://github.com/jupyter-widgets/ipywidgets/issues/1853#issuecomment-349201240 seems to do the job...
# from ipywidgets.widgets.interaction import show_inline_matplotlib_plots

# class GeoViewer:
#     def __init__(self, x_data:xr.Dataset, lat:str='lat', lon:str='lon', key:str='station'):
#         # TODO: checks on inputs
#         self.marker_info:Dict[Tuple[float,float],str] = dict()
#         self.x_data = x_data
#         lats = x_data[lat].values
#         lons = x_data[lon].values
#         self.lat_key = lat
#         self.lon_key = lon
#         self.key = key
#         values = x_data[key].values
#         n= len(lats)
#         for i in range(n):
#             self.add_marker_info(lats[i], lons[i], values[i])
#         self.create_popup = self._simple_html_popup()
    
#     def add_marker_info(self, lat:float, lon:float, code:str):
#         self.marker_info[(lat, lon)] = code
    
#     def get_code(self, lat, lon):
#         return self.marker_info[(lat, lon)]

#     def data_for_identifier(self, ident):
#         raise NotImplementedError()

#     def popup_factory(self, func:Callable[[Tuple[float,float]],HTML]):
#         self.create_popup = func

#     def _simple_html_popup(self) -> Callable:
#         def f(location):
#             message = HTML()
#             message.description = "Station ID"
#             message.value = str(self.marker_info[location])
#             message.placeholder = ""
#             return message
#         return f

#     def build_map(self, click_handler:Callable[[Dict[str,Any]], None]) -> Map:
#         mean_lat = self.x_data[self.lat_key].values.mean()
#         mean_lng = self.x_data[self.lon_key].values.mean()
#         # create the map
#         m = Map(center=(mean_lat, mean_lng), zoom=4, basemap=basemaps.Stamen.Terrain)
#         m.layout.height = '1200px'
#         # show trace
#         markers = []
#         for k in self.marker_info:
#             lat, lon = k
#             message = self.create_popup(k)
#             marker = Marker(location=k)
#             marker.on_click(click_handler)
#             marker.popup = message
#             markers.append(marker)
#         marker_cluster = MarkerCluster(
#             markers=markers
#         )
#         # not sure whether we could register once instead of each marker:
#         # marker_cluster.on_click(click_handler)
#         m.add_layer(marker_cluster)
#         # m.add_control(FullScreenControl())
#         return m

#     def plot_series(self, out_widget:Output, variable, loc_id):
#         """
#         """
#         dim_id = None
#         if dim_id is None:
#             dim_id = self.key
#         tts = self.x_data[variable].sel({dim_id: loc_id})
#         # if using bqplot down the track, see https://github.com/jtpio/voila-gpx-viewer
#         out_widget.clear_output()
#         with out_widget:
#             display(tts.plot(figsize=(16,8)))
#             show_inline_matplotlib_plots()

#     def mk_click_handler_plot_ts(self, out_widget:Output, variable='q_obs_mm'):
#         def click_handler_plot_ts(**kwargs):
#             xy = kwargs['coordinates']
#             ident = self.get_code(xy[0], xy[1])
#             self.plot_series(out_widget, variable=variable, loc_id=ident)
#         return click_handler_plot_ts



# # If printing a data frame straight to an output widget
# # def raw_print(out, ident):
# #     x_data = globalthing.data_for_identifier(ident)
# #     out.clear_output()
# #     with out:
# #         print(ident)        
# #         print(x_data)
        
# # def click_handler_rawprint(**kwargs):
# #     blah = dict(**kwargs)
# #     xy = blah['coordinates']
# #     ident = globalthing.get_code(xy[0], xy[1])
# #     raw_print(out, ident)

# def click_handler_no_op(**kwargs):
#     return
