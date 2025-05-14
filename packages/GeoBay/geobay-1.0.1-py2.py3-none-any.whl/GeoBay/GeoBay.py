# Main module.

from ipyleaflet import Map as IpyleafletMap, TileLayer, GeoJSON, LayersControl, ImageOverlay, SearchControl, VideoOverlay, WMSLayer, WidgetControl, CircleMarker, MarkerCluster, Polyline, SplitMapControl, Marker, DrawControl
import geopandas as gpd
import ipywidgets as widgets
from IPython.display import display
import  geemap
from geemap import ee_tile_layer
from . import hydro
from .hydro import extract_streams

class gb_map(IpyleafletMap):
    """
    A custom wrapper around ipyleaflet.Map with additional helper methods
    for adding basemaps, vector data, raster layers, images, videos, and WMS layers.
    """

    def __init__(self, center, zoom=12, **kwargs):
        """
        Initialize the custom map.

        Args:
            center (tuple): Latitude and longitude of the map center.
            zoom (int, optional): Zoom level of the map. Defaults to 12.
            **kwargs: Additional keyword arguments for ipyleaflet.Map.
        """
        kwargs.setdefault("scroll_wheel_zoom", True)
        super().__init__(center=center, zoom=zoom, **kwargs)
            # ✅ Initialize control tracker
        self.layer_control = None
        self.mode_ui = None

    def add_basemap(self, basemap_name: str):
        """
        Add a basemap layer to the map.

        Args:
            basemap_name (str): Name of the basemap ('OpenStreetMap', 'Esri.WorldImagery', or 'OpenTopoMap').

        Raises:
            ValueError: If the basemap name is not supported.
        """
        basemap_urls = {
            "OpenStreetMap": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            "Esri.WorldImagery": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            "OpenTopoMap": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
        }

        if basemap_name not in basemap_urls:
            raise ValueError(f"Basemap '{basemap_name}' is not supported.")

        basemap = TileLayer(url=basemap_urls[basemap_name])
        self.add_layer(basemap)
        
    def add_basemap_gui(self, options=None, position="topright"):    
        """
        Adds a graphical user interface (GUI) for selecting basemaps.

        Args:
            -options (list, optional): A list of basemap options to display in the dropdown.
               ["OpenStreetMap.Mapnik", "OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter"].
            -position (str, optional): The position of the widget on the map. Defaults to "topright".

        Behavior:
            - A toggle button is used to show or hide the dropdown and close button.
            - The dropdown allows users to select a bsemap from the provided options.
            - The close button hides the widget from the map.

        Event Handlers:
            - `on_toggle_change`: Toggles the visibility of the dropdown and close button.
            - `on_button_click`: Closes the widget when button is clicked
            - `on_dropdown_change`: Updates the basemap when a new option is selected.
        """
        if options is None:
            options = [
                "OpenStreetMap.Mapnik",
                "OpenTopoMap",
                "Esri.WorldImagery",
                "CartoDB.DarkMatter",
            ]

        toggle = widgets.ToggleButton(
            value=True,
            button_style="",
            tooltip="Click me",
            icon="map",
        )
        toggle.layout = widgets.Layout(width="38px", height="38px")

        dropdown = widgets.Dropdown(
            options=options,
            value=options[0],
            description="Basemap:",
            style={"description_width": "initial"},
        )
        dropdown.layout = widgets.Layout(width="250px", height="38px")

        button = widgets.Button(
            icon="times",
        )
        button.layout = widgets.Layout(width="38px", height="38px")

        hbox = widgets.HBox([toggle, dropdown, button])

        def on_toggle_change(change):
            """
            On toggle change method.
            """
            if change["new"]:
                hbox.children = [toggle, dropdown, button]
            else:
                hbox.children = [toggle]

        toggle.observe(on_toggle_change, names="value")

        def on_button_click(b):
            """
            On button click method.
            """
            hbox.close()
            toggle.close()
            dropdown.close()
            button.close()

        button.on_click(on_button_click)

        def on_dropdown_change(change):
            """
            On dropdown change method.
            """
            if change["new"]:
                self.layers = self.layers[:-2]
                self.add_basemap(change["new"])

        dropdown.observe(on_dropdown_change, names="value")

        control = WidgetControl(widget=hbox, position=position)
        self.add(control)

    def add_widget(self, widget, position="topright", **kwargs):
        """Add a widget to the map.

        Args:
            widget (ipywidgets.Widget): The widget to add.
            position (str, optional): Position of the widget. Defaults to "topright".
            **kwargs: Additional keyword arguments for the WidgetControl.
        """
        control = ipyleaflet.WidgetControl(widget=widget, position=position, **kwargs)
        self.add(control)
        

    def add_vector(self, vector_data):
        """
        Add a vector layer to the map from a file path or GeoDataFrame.

        Args:
            vector_data (str or geopandas.GeoDataFrame): Path to a vector file or a GeoDataFrame.

        Raises:
            ValueError: If the input is not a valid file path or GeoDataFrame.
        """
        if isinstance(vector_data, str):
            gdf = gpd.read_file(vector_data)
        elif isinstance(vector_data, gpd.GeoDataFrame):
            gdf = vector_data
        else:
            raise ValueError("Input must be a file path or a GeoDataFrame.")

        geo_json_data = gdf.__geo_interface__
        geo_json_layer = GeoJSON(data=geo_json_data)
        self.add_layer(geo_json_layer)

    def add_raster(self, url, name=None, colormap=None, opacity=1.0):
        """
        Add a raster tile layer to the map.

        Args:
            url (str): URL template for the raster tiles.
            name (str, optional): Layer name. Defaults to "Raster Layer".
            colormap (optional): Colormap to apply (not used here but reserved).
            opacity (float, optional): Opacity of the layer (0.0 to 1.0). Defaults to 1.0.
        """
        tile_layer = TileLayer(
            url=url,
            name=name or "Raster Layer",
            opacity=opacity
        )
        self.add_layer(tile_layer)

    def add_image(self, url, bounds, opacity=1.0):
        """
        Add an image overlay to the map.

        Args:
            url (str): URL of the image.
            bounds (list): Bounding box of the image [[south, west], [north, east]].
            opacity (float, optional): Opacity of the image. Defaults to 1.0.
        """
        image_layer = ImageOverlay(
            url=url,
            bounds=bounds,
            opacity=opacity
        )
        self.add_layer(image_layer)

    def add_video(self, url, bounds, opacity=1.0):
        """
        Add a video overlay to the map.

        Args:
            url (str): URL of the video.
            bounds (list): Bounding box for the video [[south, west], [north, east]].
            opacity (float, optional): Opacity of the video. Defaults to 1.0.
        """
        video_layer = VideoOverlay(
            url=url,
            bounds=bounds,
            opacity=opacity
        )
        self.add_layer(video_layer)

    def add_wms_layer(self, url, layers, name=None, format='image/png', transparent=True, **extra_params):
        """
        Add a WMS (Web Map Service) layer to the map.

        Args:
            url (str): WMS base URL.
            layers (str): Comma-separated list of layer names.
            name (str, optional): Display name for the layer. Defaults to "WMS Layer".
            format (str, optional): Image format. Defaults to 'image/png'.
            transparent (bool, optional): Whether the background is transparent. Defaults to True.
            **extra_params: Additional parameters to pass to the WMSLayer.
        """
        wms_layer = WMSLayer(
            url=url,
            layers=layers,
            name=name or "WMS Layer",
            format=format,
            transparent=transparent,
            **extra_params
        )
        self.add_layer(wms_layer)

    def show_map(self):
        """
        Display the map in a Jupyter notebook or compatible environment.

        Returns:
            ipyleaflet.Map: The configured map.
        """
        return self

    def add_search_control(self, position="topleft", zoom=10):
        """
        Add a search bar to the map using Nominatim geocoder.
        """
        search = SearchControl(
            position=position,
            url='https://nominatim.openstreetmap.org/search?format=json&q={s}',
            zoom=zoom,
            marker=Marker()  # ✅ Provide a valid Marker object
        )
        self.add_control(search)

    
    def add_esa_worldcover(self, position="bottomright"):
        """
        Add esa worldcover method.
        """
        import ipywidgets as widgets
        from ipyleaflet import WMSLayer, WidgetControl
        import leafmap

        esa_layer = WMSLayer(
            url="https://services.terrascope.be/wms/v2?",
            layers="WORLDCOVER_2021_MAP",
            name="ESA WorldCover 2021",
            transparent=True,
            format="image/png"
        )
        self.add_layer(esa_layer)

        legend_dict = leafmap.builtin_legends['ESA_WorldCover']

        def format_legend_html(legend_dict, title="ESA WorldCover Legend"):
            """
            Format legend html method.
            """
            html = f"<div style='padding:10px;background:white;font-size:12px'><b>{title}</b><br>"
            for label, color in legend_dict.items():
                html += f"<span style='color:#{color}'>■</span> {label}<br>"
            html += "</div>"
            return html

        legend_html = format_legend_html(legend_dict)
        legend_widget = widgets.HTML(value=legend_html)
        legend_control = WidgetControl(widget=legend_widget, position=position)
        self.add_control(legend_control)

    def add_circle_markers_from_xy(self, gdf, radius=5, color="red", fill_color="yellow", fill_opacity=0.8):
        """
        Add circle markers from a GeoDataFrame with lat/lon columns using MarkerCluster.

        Args:
            gdf (GeoDataFrame): Must contain 'latitude' and 'longitude' columns.
            radius (int): Radius of each marker.
            color (str): Outline color.
            fill_color (str): Fill color.
            fill_opacity (float): Fill opacity.
        """
        if 'latitude' not in gdf.columns or 'longitude' not in gdf.columns:
            raise ValueError("GeoDataFrame must contain 'latitude' and 'longitude' columns")

        markers = []
        for _, row in gdf.iterrows():
            marker = CircleMarker(
                location=(row['latitude'], row['longitude']),
                radius=radius,
                color=color,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                stroke=True
            )
            markers.append(marker)

        cluster = MarkerCluster(markers=markers)
        self.add_layer(cluster)

    def add_choropleth(self, url, column, colormap="YlOrRd"):
        """
        Simulate a choropleth using GeoJSON layer and dynamic styling.

        Args:
            url (str): GeoJSON file URL.
            column (str): Attribute column to color by.
            colormap (str): Color ramp name (from branca.colormap).
        """
        import branca.colormap as cm
        import json

        gdf = gpd.read_file(url)
        gdf = gdf.to_crs("EPSG:4326")
        gdf["id"] = gdf.index.astype(str)

        values = gdf[column]
        cmap = cm.linear.__getattribute__(colormap).scale(values.min(), values.max())

        def style_dict(feature):
            """
            Style dict method.
            """
            value = gdf.loc[int(feature['id']), column]
            return {
                'fillColor': cmap(value),
                'color': 'black',
                'weight': 0.5,
                'fillOpacity': 0.7
            }

        geo_json = json.loads(gdf.to_json())
        layer = GeoJSON(
            data=geo_json,
            style={
                'color': 'black',
                'fillColor': 'blue',
                'weight': 0.5,
                'fillOpacity': 0.7
            },
            name="Choropleth"
        )
        self.add_layer(layer)

    def add_split_rasters_leafmap(self, pre_url, post_url, pre_name="Pre-event", post_name="Post-event", overwrite=True):
        """
        Use leafmap to split and visualize two remote raster .tif files.
        """
        import leafmap
        import rasterio
        import os

        def download_and_check(url, path):
            """
            Download and check method.
            """
            file = leafmap.download_file(url, path, overwrite=overwrite)  # ✅ Ensure overwrite is passed here
            try:
                with rasterio.open(file) as src:
                    _ = src.meta
                return file
            except Exception as e:
                raise ValueError(f"{path} is not a valid GeoTIFF: {e}")

        pre_tif = download_and_check(pre_url, "pre_event.tif")
        post_tif = download_and_check(post_url, "post_event.tif")

        m = leafmap.Map(center=self.center, zoom=self.zoom)
        m.split_map(left_layer=pre_tif, right_layer=post_tif, left_label=pre_name, right_label=post_name)
        return m

    def add_building_polygons(self, url):
        """
        Add building polygons with red outline and no fill.
        """
        gdf = gpd.read_file(url)
        geo_json = gdf.__geo_interface__

        style = {
            "color": "red",
            "weight": 1,
            "fill": False,
            "fillOpacity": 0.0
        }

        self.add_layer(GeoJSON(data=geo_json, style=style, name="Buildings"))
        
    def add_roads(self, url):
        """
        Add road polylines with red color and width 2.
        """
        gdf = gpd.read_file(url)
        geo_json = gdf.__geo_interface__

        style = {
            "color": "red",
            "weight": 2,
            "opacity": 1.0
        }

    def add_ee_layer(self, ee_object, vis_params=None, name=None):
        """
        Add an Earth Engine object to the ipyleaflet map.

        Parameters
        ----------
        ee_object : ee.Image or ee.FeatureCollection
            The Earth Engine object to display.
        vis_params : dict, optional
            Visualization parameters.
        name : str, optional
            Layer name for the legend and layer control.
        """
        import geemap
        layer = geemap.ee_tile_layer(ee_object, vis_params, name)
        self.add_layer(layer)


    def enable_draw_bbox(self, elevation_threshold=10, post_action=None, accumulation_threshold=1000):
        """
        Enable draw bbox method.
        """
        from ipyleaflet import DrawControl
        import ipywidgets as widgets
        from IPython.display import display
        import ee
        from . import hydro

        self.post_action = post_action

    
        # Only apply threshold if not in Streams mode
        if post_action in (None, "Flood") and elevation_threshold is None:
            elevation_threshold = getattr(self, "current_threshold", 30)

        self.active_threshold = elevation_threshold  # ✅ This replaces relying on a local var later
        
        if hasattr(self, 'draw_control') and self.draw_control in self.controls:
            self.remove_control(self.draw_control)

        draw_control = DrawControl(rectangle={"shapeOptions": {"color": "#0000FF"}})
        draw_control.polygon = {}
        draw_control.circle = {}
        draw_control.polyline = {}
        draw_control.marker = {}
        self.draw_control = draw_control

        output = widgets.Output()
        display(output)

        def handle_draw(event_dict):
            """
            Handle draw method.
            """
            geo_json = event_dict.get("geo_json")
            if not geo_json:
                print("No geometry found.")
                return

            coords = geo_json['geometry']['coordinates'][0]
            lon_min = min(pt[0] for pt in coords)
            lon_max = max(pt[0] for pt in coords)
            lat_min = min(pt[1] for pt in coords)
            lat_max = max(pt[1] for pt in coords)

            bbox = ee.Geometry.BBox(lon_min, lat_min, lon_max, lat_max)
            self.bbox = bbox

            mode = getattr(self, "post_action", None)
            threshold = getattr(self, "active_threshold", None)

            if mode in (None, "Flood"):
                if threshold is not None:
                    flood_mask = hydro.simulate_flood(bbox, threshold)
                    self.add_ee_layer(flood_mask, vis_params={"palette": ["0000FF"]}, name="Simulated Flood")
                with output:
                    output.clear_output()
                    print("Flood simulation complete.")

            elif mode == "Streams":
                with output:
                    output.clear_output()
                    print("Stream network extracted.")
                self.show_streams(bbox, accumulation_threshold=accumulation_threshold)

            self.remove_control(draw_control)



        # ✅ Wrapper that absorbs either style
        def draw_wrapper(*args, **kwargs):
            """
            Draw wrapper method.
            """
            if args and isinstance(args[0], dict):
                handle_draw(args[0])  # called with a single event dict
            else:
                handle_draw(kwargs)  # called with keyword arguments (action=..., geo_json=...)

        draw_control.on_draw(draw_wrapper)
        self.add_control(draw_control)





    def on_draw(self, callback):
        """
        Register a callback function to be triggered on draw events.

        Parameters
        ----------
        callback : function
            A function that receives the draw event GeoJSON dictionary.
        """
        if hasattr(self, 'draw_control'):
            def safe_callback(event):
                """
                Safe callback method.
                """
                geo_json = event.get('geo_json')
                if geo_json:
                    callback(geo_json)
            self.draw_control.on_draw(safe_callback)
        else:
            raise AttributeError("Draw control not initialized. Call `add_draw_control()` first.")


    def show_streams(self, bbox, accumulation_threshold=10):
        """
        Show streams method.
        """
        import ee

        print("[DEBUG] Starting stream extraction")

        flow_acc = ee.Image("MERIT/Hydro/v1_0_1").select("upa").clip(bbox.buffer(500))

        # Show raw accumulation
        self.add_ee_layer(
            flow_acc,
            {"min": 0, "max": 1000, "palette": ["black", "cyan", "blue", "white"]},
            "Flow Accumulation"
        )

        # Attempt to show stream mask
        streams = flow_acc.gt(accumulation_threshold)
        streams_masked = streams.selfMask()
        self.add_ee_layer(streams_masked, {"palette": ["#00FFFF"]}, "Streams - Masked")

        print("[DEBUG] Streams layer added")






    def enable_mode_toggle(self, default_mode="Flood", elevation_threshold=10, accumulation_threshold=1000):
        """
        Create a toggle UI to switch between flood simulation and stream network extraction.
        """
        import ipywidgets as widgets
        from ipyleaflet import WidgetControl

        self.mode = default_mode

        # Create threshold slider
        threshold_slider = widgets.IntSlider(
            value=30,
            min=10,
            max=200,
            step=1,
            description='Flood Elevation (m):',
            continuous_update=False,
            layout=widgets.Layout(width="300px"),
            style={'description_width': '150px'}  # or however wide you want the label
        )

        self.threshold_slider = threshold_slider
        self.current_threshold = threshold_slider.value

        # Create toggle buttons
        mode_selector = widgets.ToggleButtons(
            options=["Flood", "Streams"],
            description="",
            value=default_mode,
            button_style='info',
            tooltips=["Simulate flood zones", "Show stream network"],
        )

        # Buttons and output
        clear_button = widgets.Button(description="🧹 Clear Layers", button_style="warning")
        reset_button = widgets.Button(description="🔄 Reset Map", button_style="danger")
        output = widgets.Output()

        # === Event Handlers ===

        def on_slider_change(change):
            """
            On slider change method.
            """
            if mode_selector.value == "Flood":
                self.current_threshold = change["new"]
                self.enable_draw_bbox(elevation_threshold=self.current_threshold)
                with output:
                    output.clear_output()
                    print(f"Flood threshold changed to {self.current_threshold}m")

        def on_mode_change(change):
            """
            On mode change method.
            """
            if change['name'] == 'value':
                self.mode = change['new']
                with output:
                    output.clear_output()
                    print(f"Switched to {change['new']} mode.")

                if self.mode == "Flood":
                    self.threshold_slider.layout.visibility = "visible"
                    self.enable_draw_bbox(elevation_threshold=self.current_threshold)
                elif self.mode == "Streams":
                    self.threshold_slider.layout.visibility = "hidden"
                    print("Draw a bounding box to extract stream network.")
                    self.enable_draw_bbox(elevation_threshold=None, post_action="Streams")

        def on_clear_clicked(b):
            """
            On clear clicked method.
            """
            self.clear_layers()
            self.reactivate_current_mode()
            with output:
                output.clear_output()
                print("Cleared all layers.")

        def on_reset_clicked(b):
            """
            On reset clicked method.
            """
            self.reset_map()
            with output:
                output.clear_output()
                print("Map reset (layers, bbox, and draw tools cleared).")

        # Attach event listeners
        threshold_slider.observe(on_slider_change, names="value")
        mode_selector.observe(on_mode_change)
        clear_button.on_click(on_clear_clicked)
        reset_button.on_click(on_reset_clicked)

        # === Layout ===
        ui = widgets.VBox([
            widgets.HBox([mode_selector, clear_button, reset_button]),
            threshold_slider,
            output
        ])

        # === Add to map (with duplication protection) ===
        if hasattr(self, "ui_control") and self.ui_control in self.controls:
            self.remove_control(self.ui_control)

        from IPython.display import display
        display(ui)

        self.ensure_layer_control()

        # === Initial draw setup ===
        if default_mode == "Flood":
            self.enable_draw_bbox(elevation_threshold=self.current_threshold)
        elif default_mode == "Streams":
            self.threshold_slider.layout.display = "none"
            self.enable_draw_bbox(elevation_threshold=None, post_action="Streams")



    def clear_layers(self):
        """
        Removes all layers from the map except the base layer(s).
        """
        base_layers = [layer for layer in self.layers if getattr(layer, 'base', False)]
        
        # ✅ Use super() to avoid recursion
        super().clear_layers()

        # Re-add preserved basemap(s)
        for layer in base_layers:
            self.add_layer(layer)


            
    def reset_map(self):
        """
        Reset map method.
        """
        self.clear_layers()

        if hasattr(self, "draw_control") and self.draw_control in self.controls:
            self.remove_control(self.draw_control)

        if hasattr(self, "bbox"):
            del self.bbox


        # Reactivate draw tool based on current mode
        self.reactivate_current_mode()

        
        # Remove any existing draw controls
        if hasattr(self, 'draw_control') and self.draw_control in self.controls:
            self.remove_control(self.draw_control)

        draw_control = DrawControl(marker={"shapeOptions": {"color": "#FF0000"}})
        draw_control.circle = {}
        draw_control.polygon = {}
        draw_control.polyline = {}
        draw_control.rectangle = {}
        self.draw_control = draw_control

        output = widgets.Output()
        display(output)

        def handle_draw(event_dict):
            """
            Handle draw method.
            """
            geo_json = event_dict.get("geo_json")
            if not geo_json:
                print("No geometry found.")
                return

            coords = geo_json['geometry']['coordinates']
            lon, lat = coords  # For a marker, it's a flat lon-lat pair
            pour_point = [lon, lat]

            try:
                self.show_watershed(bbox, pour_point)
                with output:
                    output.clear_output()
                    print("Watershed delineation complete.")
            except Exception as e:
                with output:
                    output.clear_output()
                    print(f"Error delineating watershed: {e}")

            self.remove_control(draw_control)

        draw_control.on_draw(handle_draw)
        self.add_control(draw_control)
        print("✅ Pour point draw tool activated")

    def add_layer_control(self, position="topright"):
        """
        Add layer control method.
        """

        # Remove any existing LayersControl, even if not tracked in self.layer_control
        for control in list(self.controls):
            if isinstance(control, LayersControl):
                self.remove_control(control)

        # Create and store the new control
        control = LayersControl(position=position)
        self.add_control(control)
        self.layer_control = control


    def ensure_layer_control(self):
        """
        Ensure layer control method.
        """
        # Remove any existing LayerControl safely
        self.add_layer_control()


    def reactivate_current_mode(self):
        """
        Reactivates the currently selected mode and re-enables the appropriate draw tools.
        """
        if hasattr(self, "mode"):
            if self.mode == "Watershed":
                print("Reactivating watershed mode after reset.")
                self.enable_draw_bbox(elevation_threshold=None, post_action="Watershed")
            elif self.mode == "Streams":
                print("Reactivating streams mode after reset.")
                self.threshold_slider.layout.visibility = 'hidden'  # ✅ Hide slider
                self.enable_draw_bbox(elevation_threshold=None, post_action="Streams")
            elif self.mode == "Flood":
                print(f"Reactivating flood mode after reset with threshold {self.current_threshold}m.")
                self.threshold_slider.layout.visibility = 'visible'  # ✅ Show slider
                self.enable_draw_bbox(elevation_threshold=self.current_threshold)
