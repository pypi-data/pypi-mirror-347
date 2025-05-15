"""
Main Homestock Module.
"""

import csv
import requests
from tabulate import tabulate
from census import Census
import us
import pandas as pd
import ipyleaflet
import folium
import rasterio
import localtileserver
import ipywidgets as widgets
from ipywidgets import Dropdown, Button, VBox
from ipyleaflet import WidgetControl, basemaps, basemap_to_tiles
from ipyleaflet import WMSLayer, VideoOverlay, TileLayer, LocalTileLayer
import os
from typing import List, Union

class Map(ipyleaflet.Map):
    def __init__(self, center=[20, 0], zoom=2, **kwargs):
        super(Map, self).__init__(center=center, zoom=zoom, **kwargs)

    def add_basemap(self, basemap="Esri.WorldImagery"):
        """
        Args:
            basemap (str): Basemap name. Default is "Esri.WorldImagery".
        """
        """Add a basemap to the map."""
        basemaps = [
            "OpenStreetMap.Mapnik",
            "Stamen.Terrain",
            "Stamen.TerrainBackground",
            "Stamen.Watercolor",
            "Esri.WorldImagery",
            "Esri.DeLorme",
            "Esri.NatGeoWorldMap",
            "Esri.WorldStreetMap",
            "Esri.WorldTopoMap",
            "Esri.WorldGrayCanvas",
            "Esri.WorldShadedRelief",
            "Esri.WorldPhysical",
            "Esri.WorldTerrain",
            "Google.Satellite",
            "Google.Street",
            "Google.Hybrid",
            "Google.Terrain",
        ]
        url = eval(f"ipyleaflet.basemaps.{basemap}").build_url()
        basemap_layer = ipyleaflet.TileLayer(url=url, name=basemap)
        self.add(basemap_layer)

    def layer(self, layer) -> None:
        """
        Args:
            layer (str or dict): Layer to be added to the map.
            **kwargs: Additional arguments for the layer.
        Returns:
            None
        Raises:
            ValueError: If the layer is not a valid type.
        """
        """ Convert url to layer"""
        if isinstance(layer, str):
            layer = ipyleaflet.TileLayer(url=layer)
        elif isinstance(layer, dict):
            layer = ipyleaflet.GeoJSON(data=layer)
        elif not isinstance(layer, ipyleaflet.Layer):
            raise ValueError("Layer must be an instance of ipyleaflet.Layer")
        return layer

    def add_layer_control(self, position="topright") -> None:
        """Adds a layer control to the map.

        Args:
            position (str, optional): The position of the layer control. Defaults to 'topright'.
        """

        self.add(ipyleaflet.LayersControl(position=position))

    def add_geojson(self, geojson, **kwargs):
        """
        Args:
            geojson (dict): GeoJSON data.
            **kwargs: Additional arguments for the GeoJSON layer.
        """
        """Add a GeoJSON layer to the map."""
        geojson_layer = ipyleaflet.GeoJSON(data=geojson, **kwargs)
        self.add(geojson_layer)

    def set_center(self, lat, lon, zoom=6, **kwargs):
        """
        Args:
            lat (float): Latitude of the center.
            lon (float): Longitude of the center.
            zoom (int): Zoom level.
            **kwargs: Additional arguments for the map.
        """
        """Set the center of the map."""
        self.center = (lat, lon)
        self.zoom = zoom

    def center_object(self, obj, zoom=6, **kwargs):
        """
        Args:
            obj (str or dict): Object to center the map on.
            zoom (int): Zoom level.
            **kwargs: Additional arguments for the map.
        """
        """Center the map on an object."""
        if isinstance(obj, str):
            obj = ipyleaflet.GeoJSON(data=obj, **kwargs)
        elif not isinstance(obj, ipyleaflet.Layer):
            raise ValueError("Object must be an instance of ipyleaflet.Layer")
        self.center = (obj.location[0], obj.location[1])
        self.zoom = zoom

    def add_vector(self, vector, **kwargs):
        """
        Args:
            vector (dict): Vector data.
            **kwargs: Additional arguments for the GeoJSON layer.
        """
        """Add a vector layer to the map from Geopandas."""
        vector_layer = ipyleaflet.GeoJSON(data=vector, **kwargs)
        self.add(vector_layer)

    def add_raster(self, filepath, name=None, colormap="greys", opacity=1, **kwargs):
        """
        Add a raster (COG) layer to the map.

        Parameters:
        filepath (str): Path or URL to the cloud-optimized GeoTIFF (COG).
        name (str, optional): Display name for the layer.
        colormap (dict or str, optional): A colormap dictionary or a string identifier.
        opacity (float, optional): Transparency level (default is 1 for fully opaque).
        **kwargs: Additional keyword arguments to pass to the tile layer generator.
        """
        import rasterio
        from localtileserver import TileClient, get_leaflet_tile_layer

        # Open the raster with rasterio to inspect metadata.
        with rasterio.open(filepath) as src:
            # If no colormap is provided (i.e., None), try extracting it from the raster's first band.
            if colormap is None:
                try:
                    colormap = src.colormap(1)
                except Exception:
                    # Leave colormap unchanged if extraction fails.
                    colormap = "greys"

        # Create the tile client from the provided file path.
        client = TileClient(filepath)

        # Generate the leaflet tile layer using the provided parameters.
        tile_layer = get_leaflet_tile_layer(
            client, name=name, colormap=colormap, opacity=opacity, **kwargs
        )

        # Add the layer to the viewer and update the center and zoom based on the raster metadata.
        self.add(tile_layer)

    def add_image(self, url, bounds, opacity=1, **kwargs):
        """
        Adds an image or animated GIF overlay to the map.

        Parameters:
            url (str): The URL of the image or GIF.
            bounds (tuple): Geographic coordinates as ((south, west), (north, east)).
            opacity (float, optional): The transparency level of the overlay (default is 1, fully opaque).
            **kwargs: Additional keyword arguments for ipyleaflet.ImageOverlay.

        Raises:
            ValueError: If bounds is not provided or is improperly formatted.
        """

        # Validate bounds: It should be a tuple of two coordinate tuples, each of length 2.
        if not (
            isinstance(bounds, tuple)
            and len(bounds) == 2
            and all(isinstance(coord, tuple) and len(coord) == 2 for coord in bounds)
        ):
            raise ValueError(
                "bounds must be a tuple in the format ((south, west), (north, east))"
            )

        # Create the image overlay using ipyleaflet.ImageOverlay.
        overlay = ipyleaflet.ImageOverlay(
            url=url, bounds=bounds, opacity=opacity, **kwargs
        )

        # Add the overlay to the map.
        self.add(overlay)
        self.center = [
            (bounds[0][0] + bounds[1][0]) / 2,
            (bounds[0][1] + bounds[1][1]) / 2,
        ]

    def add_video(self, url, bounds, opacity=1.0, **kwargs):
        """
        Adds a video overlay to the map using ipyleaflet.VideoOverlay.

        Parameters:
            url (str or list): The URL or list of URLs for the video file(s).
            bounds (tuple): Geographic bounds in the format ((south, west), (north, east)).
            opacity (float): Transparency level of the overlay (0 = fully transparent, 1 = fully opaque).
            **kwargs: Additional keyword arguments for ipyleaflet.VideoOverlay.
        """

        # Validate and normalize bounds format
        if not (
            isinstance(bounds, (tuple, list))
            and len(bounds) == 2
            and all(
                isinstance(coord, (tuple, list)) and len(coord) == 2 for coord in bounds
            )
        ):
            raise ValueError(
                "bounds must be provided as ((south, west), (north, east))"
            )

        # Convert bounds to tuple of tuples
        bounds = tuple(tuple(coord) for coord in bounds)

        # Create and add the VideoOverlay
        overlay = VideoOverlay(url=url, bounds=bounds, opacity=opacity, **kwargs)
        self.add(overlay)

        # Center the map on the video bounds
        south, west = bounds[0]
        north, east = bounds[1]
        self.center = [(south + north) / 2, (west + east) / 2]

    def add_wms_layer(self, url, layers, name, format, transparent, **kwargs):
        """
        Adds a WMS (Web Map Service) layer to the map using ipyleaflet.WMSLayer.

        Parameters:
            url (str): Base WMS endpoint.
            layers (str): Comma-separated layer names.
            name (str): Display name for the layer.
            format (str): Image format (e.g., 'image/png').
            transparent (bool): Whether the WMS layer should be transparent.
            **kwargs: Additional keyword arguments for ipyleaflet.WMSLayer.
        """

        # Create the WMS layer using the provided parameters.
        wms_layer = WMSLayer(
            url=url,
            layers=layers,
            name=name,
            format=format,
            transparent=transparent,
            **kwargs,
        )

        # Add the WMS layer to the map.
        self.add(wms_layer)

    def add_basemap_dropdown(self):
        """
        Adds a dropdown + hide button as a map control.
        Keeps track of the current basemap layer so that selecting
        a new one removes the old and adds the new immediately.

        Returns:
            None
        """
        # 1. define your choices
        basemap_dict = {
            "OpenStreetMap": basemaps.OpenStreetMap.Mapnik,
            "OpenTopoMap": basemaps.OpenTopoMap,
            "Esri.WorldImagery": basemaps.Esri.WorldImagery,
            "CartoDB.DarkMatter": basemaps.CartoDB.DarkMatter,
        }

        # 2. build widgets
        dropdown = widgets.Dropdown(
            options=list(basemap_dict.keys()),
            value="OpenStreetMap",
            layout={"width": "180px"},
            description="Basemap:",
        )
        hide_btn = widgets.Button(description="Hide", button_style="danger")
        container = widgets.VBox([dropdown, hide_btn])

        # 3. add the initial basemap layer and remember it
        initial = basemap_dict[dropdown.value]
        self._current_basemap = basemap_to_tiles(initial)
        self.add_layer(self._current_basemap)

        # 4. when user picks a new basemap, swap layers
        def _on_change(change):
            if change["name"] == "value":
                new_tiles = basemap_to_tiles(basemap_dict[change["new"]])
                # remove old
                self.remove_layer(self._current_basemap)
                # add new & store reference
                self._current_basemap = new_tiles
                self.add_layer(self._current_basemap)

        dropdown.observe(_on_change, names="value")

        # 5. hide control if needed
        hide_btn.on_click(lambda _: setattr(container.layout, "display", "none"))

        # 6. wrap in a WidgetControl and add to map
        ctrl = WidgetControl(widget=container, position="topright")
        self.add_control(ctrl)

class CensusData:
    def __init__(self, table_file="acs_tables.csv"):
        # Get absolute path to the CSV file
        self.table_path = Path(__file__).parent / table_file
        
        # Verify file exists at initialization
        if not self.table_path.exists():
            raise FileNotFoundError(f"ACS tables file not found at: {self.table_path}")

    def search_census_tables(self, keyword=None):
        """Search the Census tables based on a keyword.
        
        Args:
            keyword (str, optional): Keyword to search in table titles. If None, prompts user.
            
        Returns:
            pd.DataFrame: Contains columns 'Table ID', 'Table Title', and 'Year'.
        """
        # Get keyword input if not provided
        if keyword is None:
            keyword = input("Enter a keyword to search Census tables: ").lower()
        
        matching_tables = []
        
        # Read data using absolute path
        with open(self.table_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if keyword in row["Table Title"].lower():
                    matching_tables.append({
                        "Table ID": row["Table ID"],
                        "Table Title": row["Table Title"], 
                        "Year": row["Year"]
                    })
        
        # Convert to DataFrame
        result = pd.DataFrame(matching_tables)
        
        # Print formatted output
        if not result.empty:
            print(f"\nMatching Census Tables for '{keyword}':\n")
            print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
        else:
            print(f"\nNo matching tables found for '{keyword}'")
            
        return result
    
    def get_acs_data():
        """Fetch ACS data at various geographic levels with interactive prompts.
        
        Prompts user for inputs, fetches ACS data at various geographic levels, 
        supports multiple years, and offers CSV export option.
        
        Returns:
            pd.DataFrame: If one year requested
            dict: Dictionary of {year: pd.DataFrame} if multiple years requested
            
        Note: This interactive function prompts for:
            - API Key (required)
            - Table ID (e.g., "B19001")
            - Year(s) (comma-separated)
            - Survey type ("1" or "5")
            - Geography level
            - State/county details (when applicable)
            - CSV export options
        """
        print("Welcome to the ACS Data Fetcher!")
    
        # Get API key
        api_key = input("Enter your Census API key: ").strip()
        if not api_key:
            raise ValueError("API key is required.")
        
        # Get table ID
        table = input("Enter the ACS table ID (e.g., B19001): ").strip().upper()
        if not table:
            raise ValueError("Table ID is required.")
        
        # Get year(s) - support for multiple years
        year_input = input("Enter ACS year(s) (comma-separated for multiple, e.g., 2018,2019,2020): ").strip()
        if not year_input:
            years = [2020]
        else:
            try:
                years = [int(y.strip()) for y in year_input.split(",")]
            except ValueError:
                raise ValueError("Years must be comma-separated integers (e.g., '2018,2019,2020')")
        
        # Get survey type
        survey_type = input("Enter survey type ('5' for ACS 5-year, '1' for ACS 1-year): ").strip()
        if survey_type not in {'1', '5'}:
            raise ValueError("Survey type must be '1' or '5'.")
        acs_survey = f"acs{survey_type}"
        
        # Get geography level
        valid_geographies = {
            "acs5": [
                "Nation", "State", "County", "County Subdivision", "Place", "ZIP Code Tabulation Area",
                "Metropolitan/Micropolitan Statistical Area", "Census Tract", "Block", "Block Group"
            ],
            "acs1": [
                "Nation", "State", "County", "Metropolitan/Micropolitan Statistical Area", "Place"
            ]
        }
        
        print(f"\nAvailable geographic levels for {acs_survey}:")
        for idx, geo in enumerate(valid_geographies[acs_survey], 1):
            print(f"{idx}. {geo}")
        
        geo_selection = input("Enter the number corresponding to your desired geographic level: ").strip()
        if not geo_selection.isdigit() or int(geo_selection) not in range(1, len(valid_geographies[acs_survey]) + 1):
            raise ValueError("Invalid selection. Please enter a number from the list.")
        
        geography = valid_geographies[acs_survey][int(geo_selection) - 1]
        print(f"You selected: {geography}")
        
        # Get state input if needed
        state_fips = None
        state_name = None
        if geography in ["State", "County", "County Subdivision", "Place", "ZIP Code Tabulation Area", 
                        "Census Tract", "Block", "Block Group"]:
            state_name = input("Enter the full state name (e.g., Tennessee): ").strip()
            state_obj = us.states.lookup(state_name)
            if not state_obj:
                raise ValueError(f"Invalid state name: {state_name}")
            state_fips = state_obj.fips
        
        # Get additional geography-specific inputs
        geo_params = {}
        if geography == "County":
            county_name = input("Enter the county name (e.g., Knox) or * for all counties: ").strip()
            geo_params['county_name'] = county_name
        elif geography == "Place":
            place_id = input("Enter the Place ID or * for all places in the state: ").strip()
            geo_params['place_id'] = place_id
        elif geography == "Metropolitan/Micropolitan Statistical Area":
            metro_id = input("Enter the Metro/Micro area ID: ").strip()
            geo_params['metro_id'] = metro_id
        elif geography == "ZIP Code Tabulation Area":
            zip_id = input("Enter the ZIP Code Tabulation Area ID or * for all: ").strip()
            geo_params['zip_id'] = zip_id
        elif geography in ["Census Tract", "Block Group", "Block"]:
            county_name = input("Enter the county name (e.g., Knox) or * for all counties: ").strip()
            geo_params['county_name'] = county_name
            if geography == "Census Tract":
                tract_id = input("Enter the Census Tract number or * for all tracts in this county: ").strip()
                geo_params['tract_id'] = tract_id
            elif geography == "Block Group":
                tract_id = input("Enter the Census Tract number: ").strip()
                block_group_id = input("Enter the Block Group number or * for all: ").strip()
                geo_params['tract_id'] = tract_id
                geo_params['block_group_id'] = block_group_id
            elif geography == "Block":
                tract_id = input("Enter the Census Tract number: ").strip()
                block_group_id = input("Enter the Block Group number: ").strip()
                block_id = input("Enter the Block number or * for all: ").strip()
                geo_params['tract_id'] = tract_id
                geo_params['block_group_id'] = block_group_id
                geo_params['block_id'] = block_id
        
        # Ask about CSV export
        export_csv = input("Would you like to export the data to CSV? (y/n): ").strip().lower() == 'y'
        output_dir = None
        if export_csv:
            output_dir = input("Enter output directory path (leave blank for current directory): ").strip()
            if not output_dir:
                output_dir = os.getcwd()
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        
        # Initialize Census client
        c = Census(api_key)
        
        # Dictionary to hold DataFrames for each year
        dfs = {}
        
        for year in years:
            print(f"\nProcessing year {year}...")
            
            try:
                # Get metadata and variable labels
                metadata_url = f"https://api.census.gov/data/{year}/acs/{acs_survey}/variables.json"
                metadata_response = requests.get(metadata_url)
                if metadata_response.status_code != 200:
                    print(f"Warning: Failed to get table metadata for year {year}: {metadata_response.text}")
                    continue
                
                variables = metadata_response.json()['variables']
                fields = [var for var in variables if var.startswith(f"{table}_") and var.endswith("E")]
                
                if not fields:
                    print(f"Warning: No variables found for table {table} in year {year}")
                    continue
                
                # Build a label mapping for renaming columns later
                field_label_map = {
                    var: variables[var]['label'].replace("Estimate!!", "").replace("Estimate: ", "").strip()
                    for var in fields
                }
                
                # Fetch data based on geography
                data = fetch_geography_data(
                    c, acs_survey, geography, year, fields, state_fips, geo_params
                )
                
                if data is None:
                    print(f"Warning: No data retrieved for year {year}")
                    continue
                
                print(f"Successfully retrieved {len(data)} records for year {year}.")
                
                # Convert to DataFrame
                df = pd.DataFrame(data)
                
                # Rename ACS variable columns to descriptive labels
                df.rename(columns=field_label_map, inplace=True)
                
                # Sort columns: data fields first, geographic identifiers last
                geo_cols = [col for col in df.columns if any(geo in col.lower() for geo in 
                            ['state', 'county', 'tract', 'block', 'place', 'zip', 'msa'])]
                data_cols = sorted([col for col in df.columns if col not in geo_cols])
                df = df[data_cols + geo_cols]
                
                # Add year column
                df['year'] = year
                
                # Store DataFrame
                dfs[year] = df
                
                # Export to CSV if requested
                if export_csv:
                    filename = f"acs_{table}_{geography.replace('/', '_')}_{year}.csv"
                    filepath = os.path.join(output_dir, filename)
                    df.to_csv(filepath, index=False)
                    print(f"Data for year {year} saved to {filepath}")
                    
            except Exception as e:
                print(f"Error processing year {year}: {str(e)}")
                continue
        
        # Return appropriate result based on number of years requested
        if len(years) == 1:
            return dfs.get(years[0], pd.DataFrame())
        return dfs

    def fetch_geography_data(c, acs_survey, geography, year, fields, state_fips, geo_params, 
                        save_csv=False, output_dir=None):
        """Fetches ACS data for specific geography and returns a pandas DataFrame.
        
        Args:
            c: Initialized Census API client.
            acs_survey: Type of ACS survey, either 'acs1' (1-year) or 'acs5' (5-year).
            geography: Geographic level (e.g., 'State', 'County', 'Tract').
            year: Year of data to fetch (e.g., 2020).
            fields: List of ACS variable names to fetch (e.g., ['B01001_001E']).
            state_fips: 2-digit FIPS code for the state (required for most geographies).
            geo_params: Dictionary containing geography-specific parameters:
                - For counties: {'county_name': '*'}
                - For tracts: {'county_name': '001', 'tract_id': '*'}
                - For places: {'place_id': '12345'}
            save_csv: Whether to save results to CSV file. Defaults to False.
            output_dir: Directory path to save CSV. If None, uses current directory.
        
        Returns:
            pandas DataFrame containing:
            - Requested ACS variables
            - Geographic identifiers
            - Metadata columns (year, survey type, geography)
            """
        
        # Fetch the raw data
        raw_data = _fetch_raw_data(c, acs_survey, geography, year, fields, state_fips, geo_params)
        
        if not raw_data:
            print(f"No data returned for {geography} in {year}")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(raw_data)
        
        # Add metadata columns
        df['year'] = year
        df['survey'] = acs_survey
        df['geography'] = geography
        
        # Save to CSV if requested
        if save_csv:
            output_dir = output_dir or os.getcwd()
            os.makedirs(output_dir, exist_ok=True)
            
            # Create descriptive filename
            filename = f"acs_{year}_{acs_survey}_{geography.replace('/', '_')}.csv"
            filepath = os.path.join(output_dir, filename)
            
            df.to_csv(filepath, index=False)
            print(f"Data saved to {filepath}")
        
        return df
                            
    def _fetch_raw_data(c, acs_survey, geography, year, fields, state_fips, geo_params):
        """Helper function that contains the original fetching logic"""
        if geography == "Nation":
            print("Fetching data for the Nation...")
            return getattr(c, acs_survey).us(fields, year=year)
        
        elif geography == "State":
            print("Fetching data at State level...")
            return getattr(c, acs_survey).state(fields, state_fips, year=year)
        
        elif geography == "County":
            county_name = geo_params.get('county_name', '*')
            if county_name == '*':
                print("Fetching data for all counties...")
                return getattr(c, acs_survey).state_county(fields, state_fips, "*", year=year)
            else:
                counties_url = f'https://api.census.gov/data/{year}/acs/{acs_survey}?get=NAME&for=county:*&in=state:{state_fips}'
                response = requests.get(counties_url)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to fetch counties: {response.text}")
                counties_data = response.json()[1:]
                county_fips = next((row[2] for row in counties_data if county_name.lower() in row[0].lower()), None)
                if not county_fips:
                    raise ValueError(f"County '{county_name}' not found.")
                print(f"Fetching data for {county_name} County...")
                return getattr(c, acs_survey).state_county(fields, state_fips, county_fips, year=year)
        
        # ... [rest of the original geography handling code] ...
        
        return None
