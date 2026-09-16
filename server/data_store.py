"""
data_store.py - Complete Scientific, Educational, Media, and Governance Store for MoES / NCPOR Portal (SIH26063)
Provides high-fidelity polar science data, stations telemetry, outreach articles, educational toolkits, events, and CRUD methods.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional

# India's Polar Research Stations
STATIONS_DATA: List[Dict[str, Any]] = [
    {
        "id": "bharati",
        "name": "Bharati Research Station",
        "region": "Antarctica",
        "location": "Larsemann Hills, East Antarctica",
        "coordinates": {"lat": -69.4078, "lng": 76.1872},
        "lat_display": "69°24'28\" S",
        "lng_display": "76°11'14\" E",
        "commissioned": 2012,
        "status": "Active Year-Round",
        "elevation": "35 m above sea level",
        "capacity": "47 personnel (Summer) / 25 (Winter)",
        "image": "/assets/images/bharati.jpg",
        "description": "India's third Antarctic research facility, constructed from 134 prefabricated shipping containers on stilts to minimize snow drifting and environmental footprint. Focuses on oceanography, continental breakup (Gondwanaland), atmospheric physics, and satellite telemetry.",
        "scientific_focus": ["Paleoclimatology", "Atmospheric Aerosols", "Satellite Ground Station (ISRO)", "Biogeochemistry", "Ocean Dynamics"],
        "telemetry": {
            "temp_c": -18.4,
            "wind_speed_knots": 24,
            "wind_direction": "ESE",
            "pressure_hpa": 986.2,
            "daylight_hours": "Polar Night Transition (4.5 hrs twilight)",
            "solar_radiation": "38 W/m²",
            "geomagnetic_index": "Kp 3 (Quiet to Unsettled)"
        },
        "highlights": [
            "Thermal envelope reduces energy consumption by 40%",
            "Direct optical line-of-sight satellite downlinks for NRSC/ISRO",
            "Advanced zero-discharge greywater treatment unit"
        ]
    },
    {
        "id": "maitri",
        "name": "Maitri Research Station",
        "region": "Antarctica",
        "location": "Schirmacher Oasis, Queen Maud Land",
        "coordinates": {"lat": -70.7661, "lng": 11.7358},
        "lat_display": "70°45'58\" S",
        "lng_display": "11°44'09\" E",
        "commissioned": 1989,
        "status": "Active Year-Round",
        "elevation": "117 m above sea level",
        "capacity": "65 personnel (Summer) / 25 (Winter)",
        "image": "/assets/images/maitri.jpg",
        "description": "India's historic second Antarctic station, located in the rocky ice-free oasis of Schirmacher Hills. Serves as a vital hub for earth sciences, geomagnetism, atmospheric monitoring, and limnological research in freshwater lakes like Lake Priyadarshini.",
        "scientific_focus": ["Geomagnetism", "Ozone Hole Monitoring", "Lake Sediment Records", "Meteorology", "Glaciology"],
        "telemetry": {
            "temp_c": -23.1,
            "wind_speed_knots": 31,
            "wind_direction": "SE",
            "pressure_hpa": 978.4,
            "daylight_hours": "6.2 hrs light",
            "solar_radiation": "45 W/m²",
            "geomagnetic_index": "Kp 4 (Active Auroral Arc)"
        },
        "highlights": [
            "Supplied by freshwater Lake Priyadarshini created by Indian engineers",
            "Continuous 35+ year meteorological and geomagnetic time-series",
            "Key launch base for continental traverse ice-core drilling"
        ]
    },
    {
        "id": "himadri",
        "name": "Himadri Research Station",
        "region": "Arctic",
        "location": "Ny-Ålesund, Spitsbergen, Svalbard (Norway)",
        "coordinates": {"lat": 78.9236, "lng": 11.9278},
        "lat_display": "78°55'25\" N",
        "lng_display": "11°55'40\" E",
        "commissioned": 2008,
        "status": "Active (Expanded to Year-Round 2023-24)",
        "elevation": "12 m above sea level",
        "capacity": "8 scientists simultaneously",
        "image": "/assets/images/himadri.jpg",
        "description": "India's dedicated northern outpost in the world's northernmost scientific settlement. Focuses on Arctic warming amplification, Kongsfjorden fjord hydrology, microbial communities in permafrost, and teleconnections between Arctic sea ice decline and the Indian Summer Monsoon.",
        "scientific_focus": ["Arctic Amplification", "Fjord Oceanography", "Atmospheric Black Carbon", "Cryo-Microbiology", "Monsoon Teleconnections"],
        "telemetry": {
            "temp_c": -4.2,
            "wind_speed_knots": 14,
            "wind_direction": "NNW",
            "pressure_hpa": 1012.8,
            "daylight_hours": "24h Midnight Sun",
            "solar_radiation": "210 W/m²",
            "geomagnetic_index": "Kp 2 (Quiet)"
        },
        "highlights": [
            "World's northernmost permanent international research community",
            "Underwater moored observatory (IndARC) in Kongsfjorden",
            "First Indian winter expedition conducted successfully in 2023–2024"
        ]
    },
    {
        "id": "himansh",
        "name": "Himansh High-Altitude Station",
        "region": "Himalayas (Third Pole)",
        "location": "Sutri Dhaka, Spiti Valley, Himachal Pradesh",
        "coordinates": {"lat": 32.4281, "lng": 77.6256},
        "lat_display": "32°25'41\" N",
        "lng_display": "77°37'32\" E",
        "commissioned": 2016,
        "status": "Active (Field Seasons)",
        "elevation": "4,050 m above sea level",
        "capacity": "15 researchers",
        "image": "/assets/images/himansh.jpg",
        "description": "Recognizing the Himalayas as Earth's 'Third Pole', NCPOR established Himansh to study Himalayan cryospheric dynamics, glacier mass balance (Samudra Tapu, Batal, Gepang Gath), snowmelt hydrology, and black carbon deposition impacting Indian river basins.",
        "scientific_focus": ["Glacier Mass Balance", "Ground Penetrating Radar (GPR)", "Black Carbon Deposition", "Discharge Hydrology", "Permafrost Thaw"],
        "telemetry": {
            "temp_c": 1.5,
            "wind_speed_knots": 18,
            "wind_direction": "W",
            "pressure_hpa": 612.0,
            "daylight_hours": "13.8 hrs light",
            "solar_radiation": "840 W/m²",
            "geomagnetic_index": "Nominal"
        },
        "highlights": [
            "Monitors 6 key glaciers directly feeding Indus and Ganges tributaries",
            "Real-time DGPS automated ice flow tracking network",
            "Provides baseline calibration for ISRO RISAT & NISAR satellite missions"
        ]
    }
]

# Structured Scientific Papers & Expedition Reports
PUBLICATIONS_DATA: List[Dict[str, Any]] = [
    {
        "id": "NCPOR-ISEA41-01",
        "title": "Microplastic Contamination and Polymer Fingerprinting in Supraglacial Lakes and Benthic Sediments around Schirmacher Oasis, East Antarctica",
        "authors": "Dr. Ananya Sharma, Dr. K. Ramanathan, Dr. Suresh Babu",
        "affiliation": "National Centre for Polar and Ocean Research, Goa",
        "year": 2023,
        "expedition": "41st Indian Scientific Expedition to Antarctica (ISEA)",
        "station": "Maitri",
        "vertical": "Biogeochemistry",
        "topic": "Microplastics & Pollution",
        "doi": "10.1016/j.polar.2023.102844",
        "abstract": "During the 41st ISEA, pristine surface snow, supraglacial meltwater lakes, and benthic sediment cores from Lake Priyadarshini and 11 proglacial water bodies in the Schirmacher Oasis were analyzed using Micro-FTIR and Raman Spectroscopy. Airborne transport of polyethylene and polyester microfibers was confirmed at concentrations ranging from 3.2 to 14.8 particles/L in meltwater, demonstrating long-range atmospheric transport into interior Antarctic ecosystems.",
        "keywords": ["Microplastics", "Schirmacher Oasis", "Lake Priyadarshini", "41st ISEA", "FTIR Spectroscopy", "Cryosphere Pollution"],
        "dataset_attached": "DS-PL-2023-01",
        "file_type": "PDF & NetCDF",
        "plain_summary": "Scientists from India's 41st Antarctic Expedition discovered microscopic plastic fibers even in remote Antarctic freshwater lakes near Maitri. The study proves that human synthetic fibers travel through high-altitude jet streams across oceans and settle on pristine polar ice sheets.",
        "citation_count": 34,
        "bibtex": """@article{sharma2023microplastic,
  title={Microplastic Contamination and Polymer Fingerprinting in Supraglacial Lakes around Schirmacher Oasis},
  author={Sharma, Ananya and Ramanathan, K. and Babu, Suresh},
  journal={Polar Science Journal},
  volume={37},
  pages={102844},
  year={2023},
  publisher={Elsevier / NCPOR}
}"""
    },
    {
        "id": "NCPOR-ISEA42-02",
        "title": "High-Resolution 100-Meter Ice Core Chronology from Central Dronning Maud Land: Volcanic Horizons and Medieval Warm Anomaly Signatures",
        "authors": "Dr. Vikram Sengupta, Dr. Meenakshi Sundaram, Dr. Thamban Meloth",
        "affiliation": "Ice Core Laboratory, NCPOR",
        "year": 2024,
        "expedition": "42nd Indian Scientific Expedition to Antarctica (ISEA)",
        "station": "Maitri",
        "vertical": "Glaciology",
        "topic": "Paleoclimate & Ice Cores",
        "doi": "10.1029/2023JD039821",
        "abstract": "A 100.4-meter shallow firn/ice core recovered during the inland traverse from Maitri toward the South Pole was analyzed for oxygen isotopes (δ18O), methanesulfonic acid (MSA), and sulfate aerosol tephra layers. The record yields an uninterrupted 850-year paleo-thermometry reconstruction. Notable sulfate spikes correlate with the 1257 Samalas and 1815 Tambora volcanic eruptions, confirming rigorous annual layer dating.",
        "keywords": ["Ice Core", "Paleoclimate", "Central Dronning Maud Land", "Volcanic Eruptions", "Oxygen Isotopes", "Glaciology"],
        "dataset_attached": "DS-IC-2024-02",
        "file_type": "PDF, CSV & Core Scans",
        "plain_summary": "By drilling 100 meters into ancient Antarctic ice, Indian scientists read 850 years of planetary climate history like tree rings. The ice core trapped ash from historical mega-volcanoes like Tambora (1815) and reveals how natural temperature oscillations compare to present-day global warming.",
        "citation_count": 19,
        "bibtex": """@article{sengupta2024icecore,
  title={High-Resolution 100-Meter Ice Core Chronology from Central Dronning Maud Land},
  author={Sengupta, Vikram and Sundaram, Meenakshi and Meloth, Thamban},
  journal={Journal of Geophysical Research: Atmospheres},
  volume={129},
  number={4},
  year={2024}
}"""
    },
    {
        "id": "NCPOR-ARCTIC-03",
        "title": "Kongsfjorden Fjord Hydrology and Atlantic Water Intrusion: Moored IndARC Observatory Multi-Year Time Series",
        "authors": "Dr. K. P. Krishnan, Dr. N. V. Vidya, Dr. Mahesh BS",
        "affiliation": "Arctic Science Group, NCPOR Goa",
        "year": 2024,
        "expedition": "Indian Arctic Scientific Expedition 2023-24",
        "station": "Himadri",
        "vertical": "Oceanography",
        "topic": "Arctic Warming & Atlantification",
        "doi": "10.1038/s41558-024-01928-1",
        "abstract": "Data from India's underwater moored observatory IndARC stationed at 192 m depth in Kongsfjorden, Svalbard reveals unprecedented winter episodic pulses of warm, saline Atlantic Water (AW) displacing polar waters. The resulting delayed sea-ice formation alters light availability for primary phytoplankton blooms in early spring, demonstrating the rapid progression of 'Atlantification' of the European Arctic.",
        "keywords": ["IndARC", "Kongsfjorden", "Himadri", "Svalbard", "Atlantification", "Ocean Warming", "Arctic Moorings"],
        "dataset_attached": "DS-INDARC-2024-01",
        "file_type": "NetCDF & Timeseries CSV",
        "plain_summary": "India's permanent underwater observatory in the Arctic (IndARC) recorded warm Atlantic ocean currents surging deeper into Svalbard's fjords during winter. This warm salt water stops Arctic ice from freezing, triggering profound food-web shifts from microscopic algae up to polar marine mammals.",
        "citation_count": 42,
        "bibtex": """@article{krishnan2024kongsfjorden,
  title={Kongsfjorden Fjord Hydrology and Atlantic Water Intrusion: IndARC Time Series},
  author={Krishnan, K. P. and Vidya, N. V. and Mahesh, BS},
  journal={Nature Climate Change / NCPOR},
  volume={14},
  pages={312--320},
  year={2024}
}"""
    },
    {
        "id": "NCPOR-SOE-04",
        "title": "Air-Sea Carbon Dioxide Fluxes and Carbonate Saturation States across the Polar Front in the Indian Sector of the Southern Ocean",
        "authors": "Dr. Neelu Singh, Dr. R. K. Mishra, Dr. Amit Kumar",
        "affiliation": "Ocean & Atmospheric Sciences, MoES",
        "year": 2023,
        "expedition": "12th Indian Scientific Expedition to the Southern Ocean (SOE)",
        "station": "ORV Sagar Nidhi",
        "vertical": "Oceanography",
        "topic": "Carbon Sink & Acidification",
        "doi": "10.1029/2023GB007712",
        "abstract": "Continuous underway pCO2, surface pH, total alkalinity, and dissolved inorganic carbon (DIC) were quantified along a meridional transect from 40°S to 68°S during the 12th Indian SOE. The Subtropical Front (STF) acted as an intensive carbon sink (-4.8 mmol C m⁻² d⁻¹), whereas upwelling regions south of the Polar Front exhibited seasonal degassing, highlighting delicate thermodynamic feedbacks under changing Westerly wind regimes.",
        "keywords": ["Southern Ocean", "pCO2 Flux", "Carbon Sink", "Ocean Acidification", "ORV Sagar Nidhi", "SOE-12"],
        "dataset_attached": "DS-SOE-2023-CO2",
        "file_type": "CSV & Hydrographic Profiles",
        "plain_summary": "The Southern Ocean absorbs nearly 40% of all human-produced carbon emissions on Earth. Indian oceanographers cruising between South Africa and Antarctica mapped the exact zones where icy waters swallow greenhouse gases, and where shifting sub-polar winds threaten to release it back into the atmosphere.",
        "citation_count": 28,
        "bibtex": """@article{singh2023southernco2,
  title={Air-Sea Carbon Dioxide Fluxes across the Polar Front in the Indian Sector of the Southern Ocean},
  author={Singh, Neelu and Mishra, R. K. and Kumar, Amit},
  journal={Global Biogeochemical Cycles},
  volume={37},
  number={9},
  year={2023}
}"""
    },
    {
        "id": "NCPOR-MONSOON-05",
        "title": "Teleconnection Between Arctic Sea-Ice Decline in the Barents-Kara Seas and Indian Summer Monsoon Rainfall Variability",
        "authors": "Dr. Sourav Chatterjee, Dr. M. Ravichandran, Dr. C. M. Shenoy",
        "affiliation": "MoES Polar-Tropical Climate Modelling Group",
        "year": 2024,
        "expedition": "MoES Polar-Tropical Climate Modelling Initiative",
        "station": "Himadri",
        "vertical": "Atmospheric",
        "topic": "Monsoon Teleconnections",
        "doi": "10.1007/s00382-024-07119-x",
        "abstract": "Using coupled ocean-atmosphere reanalysis and in-situ aerosol data from Himadri, this study shows that late spring sea-ice loss in the Barents-Kara Seas excites planetary Rossby wave trains that propagate equatorward. This alters the mid-latitude jet stream, inducing an anomalous cyclonic circulation over Central Asia which modulates the onset and distribution of the Indian Summer Monsoon precipitation.",
        "keywords": ["Arctic Teleconnections", "Indian Summer Monsoon", "Barents-Kara Sea Ice", "Rossby Waves", "Climate Linkage"],
        "dataset_attached": "DS-TEL-2024-MON",
        "file_type": "GeoTIFF & NetCDF",
        "plain_summary": "Why should Indian farmers care about melting Arctic ice? This groundbreaking research proves that when sea ice melts in the Arctic during April-May, it ripples atmospheric pressure waves across Eurasia that directly shift the timing and heavy rain patterns of the monsoon in India.",
        "citation_count": 51,
        "bibtex": """@article{chatterjee2024teleconnection,
  title={Teleconnection Between Arctic Sea-Ice Decline and Indian Summer Monsoon Rainfall Variability},
  author={Chatterjee, Sourav and Ravichandran, M. and Shenoy, C. M.},
  journal={Climate Dynamics},
  volume={62},
  pages={1455--1472},
  year={2024}
}"""
    },
    {
        "id": "NCPOR-HIMALAYA-06",
        "title": "Glacier Surface Velocity and Thinning Rates on Samudra Tapu Glacier, Western Himalayas, Derived from Multi-Temporal DGPS and Satellite InSAR",
        "authors": "Dr. Parmanand Sharma, Dr. Bhanu Pratap, Dr. Lavkush Patel",
        "affiliation": "Himansh Cryosphere Division, NCPOR",
        "year": 2023,
        "expedition": "Himansh Western Himalayan Glaciology Campaign",
        "station": "Himansh",
        "vertical": "Third Pole",
        "topic": "Glacier Retreat & Hydrology",
        "doi": "10.5194/tc-17-4105-2023",
        "abstract": "Continuous monitoring from Himansh Station (4,050 m a.s.l.) over the Samudra Tapu Glacier (Chandra Basin) indicates an average surface retreat rate of 18.2 ± 2.1 m a⁻¹ and ice thinning of -0.74 m w.e. a⁻¹ between 2016 and 2023. Debris cover significantly insulates the tongue while supraglacial ponds accelerate localized thermo-karst downwasting.",
        "keywords": ["Himansh", "Samudra Tapu", "Himalayas", "Glacier Thinning", "Third Pole", "DGPS"],
        "dataset_attached": "DS-HIM-2023-STG",
        "file_type": "GeoJSON & Point Cloud",
        "plain_summary": "Monitoring India's 'Third Pole' from the high-altitude Himansh station in Spiti Valley reveals that glaciers feeding northern India's rivers are losing nearly three-quarters of a meter of ice thickness every year, with critical implications for downstream water security.",
        "citation_count": 22,
        "bibtex": """@article{sharma2023samudratapu,
  title={Glacier Surface Velocity and Thinning Rates on Samudra Tapu Glacier},
  author={Sharma, Parmanand and Pratap, Bhanu and Patel, Lavkush},
  journal={The Cryosphere},
  volume={17},
  pages={4105--4122},
  year={2023}
}"""
    },
    {
        "id": "NCPOR-BHARATI-07",
        "title": "Crustal Evolution and Tectonic Linkages of the Prydz Belt, East Antarctica with Eastern Ghats Mobile Belt of India",
        "authors": "Dr. N. C. Pant, Dr. Amit Dharwadkar, Dr. S. K. Bhowmik",
        "affiliation": "Geological Survey of India & NCPOR",
        "year": 2023,
        "expedition": "42nd ISEA",
        "station": "Bharati",
        "vertical": "Glaciology",
        "topic": "Gondwanaland Breakup & Geology",
        "doi": "10.1016/j.precamres.2023.106981",
        "abstract": "Petrological and U-Pb zircon geochronology of ultra-high temperature granulites exposed in the Larsemann Hills adjacent to Bharati Station reveals a shared metamorphic evolution with the Rayner Complex and India's Eastern Ghats, providing critical evidence for the Rodinia and Gondwana supercontinental reconstructions.",
        "keywords": ["Bharati", "Larsemann Hills", "Gondwana", "Eastern Ghats", "Geology", "Tectonics"],
        "dataset_attached": "DS-BH-2023-GEO",
        "file_type": "PDF & Geochemical Data",
        "plain_summary": "Rocks sampled right beneath India's Bharati station in Antarctica are geological twins to rocks found in Odisha and Andhra Pradesh. Millions of years ago, India and Antarctica were glued together in a giant supercontinent called Gondwanaland.",
        "citation_count": 15,
        "bibtex": """@article{pant2023crustal,
  title={Crustal Evolution and Tectonic Linkages of the Prydz Belt with Eastern Ghats},
  author={Pant, N. C. and Dharwadkar, Amit and Bhowmik, S. K.},
  journal={Precambrian Research},
  volume={392},
  pages={106981},
  year={2023}
}"""
    },
    {
        "id": "NCPOR-ARCTIC-08",
        "title": "Winter Dynamics of Black Carbon Aerosols and Boundary Layer Inversion at Ny-Ålesund, Svalbard",
        "authors": "Dr. Rupesh Kumar, Dr. C. P. Roy, Dr. V. P. Sharma",
        "affiliation": "Atmospheric Sciences Division, NCPOR",
        "year": 2024,
        "expedition": "Arctic Winter Expedition 2023-24",
        "station": "Himadri",
        "vertical": "Atmospheric",
        "topic": "Black Carbon & Aerosols",
        "doi": "10.1016/j.atmosenv.2024.120411",
        "abstract": "The first winter-long continuous aethalometer and LIDAR measurements at Himadri during the polar night (Nov 2023 - Feb 2024) identify episodic long-range transport of industrial black carbon from mid-latitudes, trapped under strong surface temperature inversions, accelerating subsequent spring snow-albedo reduction.",
        "keywords": ["Black Carbon", "Aerosols", "Himadri", "Arctic Winter", "Polar Night", "Snow Albedo"],
        "dataset_attached": "DS-HIM-2024-BC",
        "file_type": "NetCDF & TimeSeries CSV",
        "plain_summary": "During India's first historic winter expedition at Himadri, scientists monitored soot particles traveling thousands of miles in the 24-hour polar dark. The soot settles on pure white snow, darkening it and making it melt much faster when spring sunlight returns.",
        "citation_count": 12,
        "bibtex": """@article{kumar2024blackcarbon,
  title={Winter Dynamics of Black Carbon Aerosols at Ny-Alesund},
  author={Kumar, Rupesh and Roy, C. P. and Sharma, V. P.},
  journal={Atmospheric Environment},
  volume={318},
  pages={120411},
  year={2024}
}"""
    }
]

# Structured Scientific Datasets Catalog
DATASETS_DATA: List[Dict[str, Any]] = [
    {
        "id": "DS-PL-2023-01",
        "title": "Schirmacher Oasis Limnological Microplastic Abundance & Polymer Spectral Signatures",
        "expedition": "41st ISEA",
        "station": "Maitri",
        "format": "CSV & NetCDF-4",
        "size": "48.2 MB",
        "parameters": ["Particle Count/L", "Polymer Class (PE, PET, PP)", "Spectral Library Match %", "GPS Coordinates", "Sampling Depth"],
        "license": "Government Open Data License (GODL-India)",
        "published_date": "2023-11-15",
        "records_count": "1,420 water & sediment samples",
        "download_url": "/api/repository/download/DS-PL-2023-01"
    },
    {
        "id": "DS-IC-2024-02",
        "title": "Central Dronning Maud Land 100m Ice Core High-Resolution Geochemical & Stable Isotope Profile",
        "expedition": "42nd ISEA",
        "station": "Maitri Inland Traverse",
        "format": "CSV, NetCDF & High-Res Core TIF",
        "size": "142.6 MB",
        "parameters": ["Depth (m)", "Water Equivalent Age (B.P.)", "δ18O (‰)", "δD (‰)", "Excess Deuterium", "SO4²⁻ (ppb)", "MSA (ppb)"],
        "license": "GODL-India / Creative Commons Attribution 4.0",
        "published_date": "2024-02-10",
        "records_count": "10,040 depth intervals (1 cm resolution)",
        "download_url": "/api/repository/download/DS-IC-2024-02"
    },
    {
        "id": "DS-INDARC-2024-01",
        "title": "IndARC Moored Underwater Arctic Observatory Kongsfjorden Multi-Sensor Oceanographic Records",
        "expedition": "Arctic Expeditions (2014-2024)",
        "station": "Himadri (Kongsfjorden Mooring)",
        "format": "NetCDF-4 & ASCII TimeSeries",
        "size": "384.1 MB",
        "parameters": ["Sea Temperature (°C)", "Practical Salinity (PSU)", "Pressure/Depth (dbar)", "Acoustic Doppler Current Velocities (u,v,w)", "Dissolved Oxygen (μmol/kg)", "Turbidity"],
        "license": "MoES / NCPOR Open Data",
        "published_date": "2024-04-05",
        "records_count": "87,600 hourly measurements",
        "download_url": "/api/repository/download/DS-INDARC-2024-01"
    },
    {
        "id": "DS-SOE-2023-CO2",
        "title": "12th Indian Southern Ocean Expedition Underway Surface Seawater pCO2 and Atmospheric CO2 Molar Fraction",
        "expedition": "12th SOE",
        "station": "ORV Sagar Nidhi Cruise",
        "format": "CSV & SOCAT Standard Format",
        "size": "24.5 MB",
        "parameters": ["Latitude", "Longitude", "Sea Surface Temp (°C)", "Sea Surface Salinity", "xCO2 atmospheric (ppm)", "pCO2 seawater (μatm)", "Wind Speed (m/s)"],
        "license": "GODL-India / SOCAT Compliant",
        "published_date": "2023-08-20",
        "records_count": "28,940 underway data points",
        "download_url": "/api/repository/download/DS-SOE-2023-CO2"
    }
]

# Media Hub Assets (Photos, Videos, Audio Soundscapes, and Press Kits)
MEDIA_ASSETS: List[Dict[str, Any]] = [
    # --- 4K Photography ---
    {
        "id": "MED-01",
        "title": "Bharati Station Under the Aurora Australis Glow",
        "type": "photo",
        "category": "Antarctica",
        "expedition": "42nd ISEA",
        "station": "Bharati",
        "location": "Larsemann Hills, East Antarctica",
        "coordinates": "69°24'28\" S, 76°11'14\" E",
        "url": "/assets/images/bharati.jpg",
        "thumbnail": "/assets/images/bharati.jpg",
        "resolution": "3840 x 2160 (4K UHD)",
        "aspect_ratio": "16:9",
        "credit": "NCPOR Expedition Media Cell / Dr. R. Verma",
        "license": "Government Open Access / CC-BY 4.0",
        "tags": ["Bharati", "AuroraAustralis", "PolarNight", "LarsemannHills", "AntarcticaStation"],
        "description": "Long-exposure capture of India's aerodynamic Bharati research outpost elevated on hydraulic pillars during polar winter, illuminated by ribbons of green auroral geomagnetic display.",
        "press_kit_eligible": True,
        "date": "2024-03-12"
    },
    {
        "id": "MED-02",
        "title": "Himadri Station Summer Campaign and Kongsfjorden Glacial Fjord",
        "type": "photo",
        "category": "Arctic",
        "expedition": "Arctic Summer Expedition",
        "station": "Himadri",
        "location": "Ny-Ålesund, Svalbard (Norway)",
        "coordinates": "78°55'25\" N, 11°55'40\" E",
        "url": "/assets/images/himadri.jpg",
        "thumbnail": "/assets/images/himadri.jpg",
        "resolution": "3840 x 2160 (4K UHD)",
        "aspect_ratio": "16:9",
        "credit": "NCPOR Arctic Wing / MoES India",
        "license": "Government Open Access / CC-BY 4.0",
        "tags": ["Himadri", "Arctic", "NyAlesund", "Svalbard", "Fjord", "ClimateResearch"],
        "description": "The Indian National Flag flying proudly at Himadri station in Ny-Ålesund, with atmospheric meteorological sensors in foreground and glacier-calving icebergs adrift in Kongsfjorden.",
        "press_kit_eligible": True,
        "date": "2024-04-18"
    },
    {
        "id": "MED-03",
        "title": "Continental Polar Plateau 100m Ice Core Extraction Operation",
        "type": "photo",
        "category": "Antarctica",
        "expedition": "42nd ISEA Inland Traverse",
        "station": "Maitri",
        "location": "Central Dronning Maud Land",
        "coordinates": "71°12'04\" S, 12°33'10\" E",
        "url": "/assets/images/ice_core.jpg",
        "thumbnail": "/assets/images/ice_core.jpg",
        "resolution": "3840 x 2160 (4K UHD)",
        "aspect_ratio": "16:9",
        "credit": "NCPOR Paleoclimate Drilling Unit",
        "license": "Government Open Access / CC-BY 4.0",
        "tags": ["IceCore", "Glaciology", "DrillingRig", "Paleoclimate", "MaitriTraverse"],
        "description": "Glaciologists in extreme thermal survival suits cataloging pristine cylindrical ice core segments extracted from the polar ice sheet for 850-year paleo-atmosphere chemical analysis.",
        "press_kit_eligible": True,
        "date": "2024-02-04"
    },
    {
        "id": "MED-04",
        "title": "ORV Sagar Nidhi Navigating Southern Ocean Pack Ice & Icebergs",
        "type": "photo",
        "category": "Southern Ocean",
        "expedition": "12th Indian SOE",
        "station": "ORV Sagar Nidhi",
        "location": "Prydz Bay / 65°S Southern Ocean",
        "coordinates": "65°18'00\" S, 74°42'10\" E",
        "url": "/assets/images/vessel.jpg",
        "thumbnail": "/assets/images/vessel.jpg",
        "resolution": "3840 x 2160 (4K UHD)",
        "aspect_ratio": "16:9",
        "credit": "Chief Scientist & Crew, 12th SOE",
        "license": "Government Open Access / CC-BY 4.0",
        "tags": ["SouthernOcean", "ORVSagarNidhi", "PackIce", "Iceberg", "Oceanography"],
        "description": "Aerial view of India's polar research vessel maneuvering through fracturing sea ice floes in the icy Southern Ocean while deploying deep-sea CTD rosettes and bio-optical sensors.",
        "press_kit_eligible": True,
        "date": "2024-01-29"
    },
    {
        "id": "MED-05",
        "title": "Maitri Station in Ice-Free Schirmacher Oasis",
        "type": "photo",
        "category": "Antarctica",
        "expedition": "43rd ISEA",
        "station": "Maitri",
        "location": "Schirmacher Oasis, Queen Maud Land",
        "coordinates": "70°45'58\" S, 11°44'09\" E",
        "url": "/assets/images/maitri.jpg",
        "thumbnail": "/assets/images/maitri.jpg",
        "resolution": "3840 x 2160 (4K UHD)",
        "aspect_ratio": "16:9",
        "credit": "NCPOR Antarctic Operations Cell",
        "license": "Government Open Access / CC-BY 4.0",
        "tags": ["Maitri", "SchirmacherOasis", "LakePriyadarshini", "AntarcticaStation"],
        "description": "Panoramic view of Maitri station nestled in the rocky oasis, overlooking the pristine freshwater Lake Priyadarshini and surrounding blue ice fields.",
        "press_kit_eligible": True,
        "date": "2024-01-15"
    },
    {
        "id": "MED-06",
        "title": "Himansh High-Altitude Glacier Station in Spiti Valley",
        "type": "photo",
        "category": "Himalayas",
        "expedition": "Himansh Glaciology Campaign",
        "station": "Himansh",
        "location": "Sutri Dhaka, Spiti, Himachal Pradesh (4,050m)",
        "coordinates": "32°25'41\" N, 77°37'32\" E",
        "url": "/assets/images/himansh.jpg",
        "thumbnail": "/assets/images/himansh.jpg",
        "resolution": "3840 x 2160 (4K UHD)",
        "aspect_ratio": "16:9",
        "credit": "Himansh Field Wing / NCPOR",
        "license": "Government Open Access / CC-BY 4.0",
        "tags": ["Himansh", "ThirdPole", "Spiti", "Himalayas", "SamudraTapu"],
        "description": "High-altitude view of the Himansh observatory overlooking the rugged moraines and glacier snouts of the Chandra-Bhaga river basin.",
        "press_kit_eligible": True,
        "date": "2023-09-20"
    },

    # --- Polar Science Videos ---
    {
        "id": "VID-01",
        "title": "Bharati: India's Aerodynamic Antarctic Research Base",
        "type": "video",
        "category": "Antarctica",
        "expedition": "43rd ISEA",
        "station": "Bharati",
        "location": "Larsemann Hills, East Antarctica",
        "coordinates": "69°24'28\" S, 76°11'14\" E",
        "youtube_id": "lNhK69S_LLM",
        "url": "https://www.youtube.com/embed/lNhK69S_LLM",
        "thumbnail": "/assets/images/bharati.jpg",
        "duration": "14:20",
        "resolution": "4K UHD / 1080p",
        "credit": "Polar Man Studio / NCPOR Expedition",
        "license": "Educational Broadcast / CC-BY 4.0",
        "tags": ["Bharati", "Antarctica", "LarsemannHills", "PolarExpedition"],
        "description": "Comprehensive field walkthrough exploring the aerodynamic container stilt architecture, living modules, satellite receiving systems, and year-round research at Bharati Station in East Antarctica.",
        "press_kit_eligible": True,
        "date": "2024-02-15"
    },
    {
        "id": "VID-02",
        "title": "40th Indian Scientific Expedition to Antarctica: Voyage to Maitri & Bharati",
        "type": "video",
        "category": "Antarctica",
        "expedition": "40th ISEA",
        "station": "Maitri & Bharati",
        "location": "Schirmacher Oasis, Queen Maud Land",
        "coordinates": "70°45'58\" S, 11°44'09\" E",
        "youtube_id": "he35dQfayAU",
        "url": "https://www.youtube.com/embed/he35dQfayAU",
        "thumbnail": "/assets/images/maitri.jpg",
        "duration": "22:15",
        "resolution": "1080p HD",
        "credit": "Ministry of Earth Sciences / NCPOR",
        "license": "Public Broadcast",
        "tags": ["Maitri", "40thISEA", "AntarcticProgram", "NCPOR"],
        "description": "Documentary covering the scientific objectives, logistics, wintering-over protocols, and environmental research of the Indian Antarctic Program at Maitri and Bharati stations.",
        "press_kit_eligible": True,
        "date": "2024-01-10"
    },
    {
        "id": "VID-03",
        "title": "Himadri: India's First Arctic Research Station at Ny-Ålesund",
        "type": "video",
        "category": "Arctic",
        "expedition": "Arctic Summer Expedition",
        "station": "Himadri",
        "location": "Ny-Ålesund, Spitsbergen, Svalbard",
        "coordinates": "78°55'25\" N, 11°55'40\" E",
        "youtube_id": "BMUn8U4tLfU",
        "url": "https://www.youtube.com/embed/BMUn8U4tLfU",
        "thumbnail": "/assets/images/himadri.jpg",
        "duration": "16:45",
        "resolution": "1080p HD",
        "credit": "Ministry of Earth Sciences (MoES GoI)",
        "license": "Educational",
        "tags": ["Himadri", "Arctic", "NyAlesund", "Svalbard", "MoES"],
        "description": "Official MoES film documenting India's Arctic presence at Ny-Ålesund in Svalbard (79°N), profiling long-term atmospheric, oceanic, and glaciological monitoring.",
        "press_kit_eligible": True,
        "date": "2024-03-05"
    },
    {
        "id": "VID-04",
        "title": "IndARC & Arctic Ocean Sea Ice Research: NCPOR Scientific Study",
        "type": "video",
        "category": "Arctic",
        "expedition": "IndARC Mooring Campaign",
        "station": "Himadri",
        "location": "Kongsfjorden Deep Basin (192m)",
        "coordinates": "78°57' N, 11°50' E",
        "youtube_id": "9qezdBidoGw",
        "url": "https://www.youtube.com/embed/9qezdBidoGw",
        "thumbnail": "/assets/images/himadri.jpg",
        "duration": "09:30",
        "resolution": "1080p HD",
        "credit": "National Centre for Polar and Ocean Research (NCPOR)",
        "license": "Government Open Access",
        "tags": ["IndARC", "Kongsfjorden", "ArcticSeaIce", "NCPOR", "Oceanography"],
        "description": "NCPOR scientific investigation on Arctic sea ice dynamics, fjord oceanography, and multi-sensor underwater moored observatories in Kongsfjorden.",
        "press_kit_eligible": True,
        "date": "2024-02-28"
    },
    {
        "id": "VID-05",
        "title": "HIMANSH: High-Altitude Himalayan Glaciology Research Station",
        "type": "video",
        "category": "Himalayas",
        "expedition": "Western Himalayan Glaciology",
        "station": "Himansh",
        "location": "Sutri Dhaka, Spiti Valley",
        "coordinates": "32°25'41\" N, 77°37'32\" E",
        "youtube_id": "4DGp4MuUbzc",
        "url": "https://www.youtube.com/embed/4DGp4MuUbzc",
        "thumbnail": "/assets/images/himansh.jpg",
        "duration": "18:10",
        "resolution": "1080p HD",
        "credit": "National Centre for Polar and Ocean Research (NCPOR)",
        "license": "Educational",
        "tags": ["Himansh", "ThirdPole", "SpitiValley", "NCPOR", "Glaciers"],
        "description": "Official NCPOR documentary on Himansh station situated at 4,050 meters in Spiti Valley, Himachal Pradesh, monitoring benchmark glacier mass balance in the Chandra basin.",
        "press_kit_eligible": True,
        "date": "2023-10-12"
    },
    {
        "id": "VID-06",
        "title": "Southern Ocean Climate Cruise & Indian Scientific Expedition to Antarctica",
        "type": "video",
        "category": "Southern Ocean",
        "expedition": "12th Indian SOE",
        "station": "ORV Sagar Nidhi / Southern Ocean",
        "location": "Polar Frontal Zone, 60°S",
        "coordinates": "60°15' S, 68°30' E",
        "youtube_id": "W7-C3Zxzpc8",
        "url": "https://www.youtube.com/embed/W7-C3Zxzpc8",
        "thumbnail": "/assets/images/sagarnidhi.jpg",
        "duration": "12:50",
        "resolution": "1080p HD",
        "credit": "India Science / Department of Science & Technology",
        "license": "Government Open Access",
        "tags": ["SouthernOcean", "ORVSagarNidhi", "Expedition", "IndiaScience"],
        "description": "Expedition documentary following Indian scientists aboard ice-class research vessels navigating the Southern Ocean across the Roaring Forties to study carbon fluxes and marine biomes.",
        "press_kit_eligible": True,
        "date": "2024-01-20"
    },

    # --- Audio Soundscapes & Expedition Logs ---
    {
        "id": "AUD-01",
        "title": "Arctic Tidewater Glacier Calving & Underwater Ice Creaks",
        "type": "audio",
        "category": "Soundscapes",
        "sound_preset": "glacier_calving",
        "expedition": "IndARC Mooring Deployment",
        "station": "Himadri",
        "location": "Kongsfjorden Fjord Underwater (190m)",
        "coordinates": "78°57' N, 11°50' E",
        "url": "/assets/audio/glacier_calving.mp3",
        "thumbnail": "/assets/images/himadri.jpg",
        "duration": "03:45",
        "resolution": "Lossless 24-bit 96kHz / Web MP3",
        "credit": "NCPOR Underwater Acoustics Group",
        "license": "CC-BY 4.0 Educational",
        "tags": ["Hydrophone", "Soundscape", "IceCalving", "MarineAcoustics", "Arctic"],
        "description": "Sub-surface hydrophone recording capturing the sharp resonant cracks and deep rumble of Kongsfjorden tidewater glaciers calving into the icy fjord.",
        "press_kit_eligible": False,
        "date": "2024-03-01"
    },
    {
        "id": "AUD-02",
        "title": "Antarctic Katabatic Blizzard Winds over Schirmacher Oasis",
        "type": "audio",
        "category": "Soundscapes",
        "sound_preset": "polar_blizzard",
        "expedition": "42nd ISEA Winter Campaign",
        "station": "Maitri",
        "location": "Schirmacher Oasis, Queen Maud Land",
        "coordinates": "70°45'58\" S, 11°44'09\" E",
        "url": "/assets/audio/polar_blizzard.mp3",
        "thumbnail": "/assets/images/maitri.jpg",
        "duration": "04:20",
        "resolution": "Lossless 24-bit 96kHz / Web MP3",
        "credit": "Maitri Meteorological Observatory",
        "license": "CC-BY 4.0 Educational",
        "tags": ["Blizzard", "KatabaticWinds", "Maitri", "AntarcticaWind"],
        "description": "Ambient field recording of 75-knot katabatic winds sweeping across the frozen surface of Lake Priyadarshini and Maitri station's living modules.",
        "press_kit_eligible": False,
        "date": "2024-02-18"
    },
    {
        "id": "AUD-03",
        "title": "Weddell Seal Underwater Chirps & Bio-Acoustic Calls",
        "type": "audio",
        "category": "Interviews",
        "sound_preset": "seal_chirp",
        "expedition": "43rd ISEA Coastal Survey",
        "station": "Bharati",
        "location": "Prydz Bay Sea Ice, East Antarctica",
        "coordinates": "69°22' S, 76°15' E",
        "url": "/assets/audio/seal_chirps.mp3",
        "thumbnail": "/assets/images/bharati.jpg",
        "duration": "02:50",
        "resolution": "Lossless 24-bit 96kHz / Web MP3",
        "credit": "NCPOR Marine Bio-Acoustic Unit",
        "license": "CC-BY 4.0 Educational",
        "tags": ["WeddellSeal", "BioAcoustics", "PrydzBay", "AntarcticaWildlife"],
        "description": "Fascinating sci-fi like frequency sweeps and vocalizations produced by Weddell seals communicating beneath solid fast ice in Prydz Bay.",
        "press_kit_eligible": True,
        "date": "2024-01-25"
    },
    {
        "id": "AUD-04",
        "title": "IndARC Mooring Acoustic Pingers & Ocean Current Flow",
        "type": "audio",
        "category": "Soundscapes",
        "sound_preset": "ocean_hydrophone",
        "expedition": "Arctic Oceanographic Mission",
        "station": "Himadri",
        "location": "Kongsfjorden 192m Deep Basin",
        "coordinates": "78°55' N, 11°52' E",
        "url": "/assets/audio/ocean_currents.mp3",
        "thumbnail": "/assets/images/himadri.jpg",
        "duration": "05:15",
        "resolution": "Lossless 24-bit 96kHz / Web MP3",
        "credit": "NCPOR Ocean Observation Group",
        "license": "CC-BY 4.0 Educational",
        "tags": ["IndARC", "AcousticPinger", "OceanCurrents", "Kongsfjorden"],
        "description": "Acoustic Doppler current profiler (ADCP) acoustic pulses mixed with deep fjord ocean currents flowing between the Atlantic and Arctic basins.",
        "press_kit_eligible": False,
        "date": "2024-03-10"
    },
    {
        "id": "AUD-05",
        "title": "Scientist Voice Log: 43rd Antarctic Expedition Departure",
        "type": "audio",
        "category": "Interviews",
        "sound_preset": "scientist_log",
        "expedition": "43rd ISEA Launch",
        "station": "ORV Sagar Nidhi",
        "location": "Cape Town Harbor to Southern Ocean",
        "coordinates": "34°S, 18°E Transit Corridor",
        "url": "/assets/audio/scientist_log.mp3",
        "thumbnail": "/assets/images/vessel.jpg",
        "duration": "03:30",
        "resolution": "128kbps Podcast Audio",
        "credit": "MoES Expedition Podcast Cell",
        "license": "Public Release",
        "tags": ["Podcast", "ExpeditionLog", "43rdISEA", "CapeTown"],
        "description": "Field audio interview with lead scientists as the ice-class vessel sets sail across the Roaring Forties toward Maitri and Bharati stations.",
        "press_kit_eligible": True,
        "date": "2024-01-05"
    },
    {
        "id": "AUD-06",
        "title": "High-Altitude Himalayan Wind & Snowmelt Streams at Himansh",
        "type": "audio",
        "category": "Soundscapes",
        "sound_preset": "himalayan_stream",
        "expedition": "Himansh Western Himalaya",
        "station": "Himansh",
        "location": "Sutri Dhaka, Spiti Valley (4,050m)",
        "coordinates": "32°25'41\" N, 77°37'32\" E",
        "url": "/assets/audio/himalayan_stream.mp3",
        "thumbnail": "/assets/images/ice_core.jpg",
        "duration": "04:10",
        "resolution": "Lossless 24-bit 96kHz / Web MP3",
        "credit": "Himansh Cryosphere Wing / NCPOR",
        "license": "CC-BY 4.0 Educational",
        "tags": ["Himansh", "ThirdPole", "Snowmelt", "SpitiValley"],
        "description": "Pristine mountain wind gusts and rapid glacial meltwater streams rushing through the moraines of the Samudra Tapu glacier in Spiti Valley.",
        "press_kit_eligible": False,
        "date": "2023-09-18"
    }
]

# Science Outreach Articles (Explaining complex science for various audiences)
OUTREACH_ARTICLES: List[Dict[str, Any]] = [
    {
        "id": "ART-01",
        "title": "The Third Pole: Why Himalayan Glaciers Are Critical for 1.3 Billion People",
        "audience": "General Public",
        "topic": "Himalayan Cryosphere",
        "read_time": "6 min",
        "published_date": "2024-04-10",
        "image": "/assets/images/ice_core.jpg",
        "summary": "The Hindu Kush-Himalayan ice reservoirs feed the Indus, Ganges, and Brahmaputra river basins. Learn how NCPOR's high-altitude research station Himansh in Spiti tracks the pulse of these frozen lifelines.",
        "content": "Known as the Third Pole, the Himalayas hold the largest volume of ice outside the polar caps. Scientists from Himansh station monitor the Samudra Tapu and Batal glaciers. Changes in snow accumulation and black carbon deposition directly affect water security, irrigation, and hydroelectric power across northern India.",
        "key_takeaways": [
            "Himalayan glaciers feed 10 major Asian river systems",
            "Himansh station operates at 4,050 meters in Himachal Pradesh",
            "Ablation stake networks record annual ice mass loss"
        ]
    },
    {
        "id": "ART-02",
        "title": "Decoding 850 Years of Climate from a Cylinder of Antarctic Ice",
        "audience": "School Students",
        "topic": "Paleoclimatology",
        "read_time": "4 min",
        "published_date": "2024-03-15",
        "image": "/assets/images/ice_core.jpg",
        "summary": "How do snowflakes that fell during the Mughal empire tell us about global warming today? Step inside the ice-core freezer labs of NCPOR in Goa.",
        "content": "When snow falls in Antarctica, it traps tiny bubbles of atmospheric air. Year after year, fresh snow compresses into solid glacial ice. By drilling a 100-meter core, Indian scientists can count annual layers like tree rings, measure carbon dioxide ratios, and detect chemical signatures from volcanic eruptions that happened centuries ago.",
        "key_takeaways": [
            "Ice cores act as Earth's natural time machines",
            "Ancient air bubbles preserve historical atmosphere samples",
            "Volcanic ash from Tambora (1815) helps date the ice layers"
        ]
    },
    {
        "id": "ART-03",
        "title": "Arctic Warming Amplification & The Indian Monsoon: An Atmospheric Bridge",
        "audience": "Educators & College",
        "topic": "Climate Teleconnections",
        "read_time": "8 min",
        "published_date": "2024-05-02",
        "image": "/assets/images/himadri.jpg",
        "summary": "A deep-dive technical explainer on the fluid dynamic linkages between Barents-Kara sea-ice decline and Rossby wave propagation influencing Indian Summer Monsoon rainfall.",
        "content": "The Arctic is warming nearly four times faster than the global average — a phenomenon known as Arctic Amplification. In-situ measurements from India's Himadri station in Ny-Ålesund, paired with atmospheric models, reveal that spring ice retreat creates thermal anomalies. These anomalies trigger planetary-scale Rossby wave trains that distort the subtropical westerly jet stream, leading to erratic monsoon dry-spells.",
        "key_takeaways": [
            "Arctic warming is 4x faster than the global average",
            "Rossby waves connect high-latitude pressure to tropical rain bands",
            "Helps IMD improve extended-range monsoon forecasting"
        ]
    },
    {
        "id": "ART-04",
        "title": "India's Antarctic Architecture: Engineering Bharati Station on Hydraulic Stilts",
        "audience": "Policy Makers",
        "topic": "Polar Engineering",
        "read_time": "5 min",
        "published_date": "2024-01-20",
        "image": "/assets/images/bharati.jpg",
        "summary": "How cutting-edge sustainable engineering from 134 modular shipping containers created India's zero-emission research hub in East Antarctica.",
        "content": "Bharati station stands proudly on Larsemann Hills. To withstand hurricane-force katabatic winds reaching 200 km/h and prevent catastrophic snow burial, the entire structure is raised on stilts. Its aerodynamic outer skin channels wind harmlessly underneath, while an advanced greywater recycling system ensures zero environmental contamination.",
        "key_takeaways": [
            "Constructed from 134 prefabricated ISO modular units",
            "Elevated on stilts to allow snow drifts to blow underneath",
            "Features direct satellite downlinks for ISRO space telemetry"
        ]
    }
]

# Educational Toolkits & Classroom Resources
EDUCATIONAL_TOOLKITS: List[Dict[str, Any]] = [
    {
        "id": "ED-KIT-01",
        "title": "Polar Cryosphere Classroom Activity Pack (Grade 6–10)",
        "grade": "Middle & High School",
        "category": "Activity Sheet & Guide",
        "downloads": "2,480",
        "file_size": "14.2 MB",
        "summary": "Interactive student worksheet covering polar food webs (phytoplankton to blue whales), glacier mass balance simulations, and ice-albedo experiment guidelines using simple ice and soil cups."
    },
    {
        "id": "ED-KIT-02",
        "title": "India in Antarctica: 40 Years of Science Infographic Poster Pack",
        "grade": "All Educators",
        "category": "High-Res Posters",
        "downloads": "4,120",
        "file_size": "28.5 MB",
        "summary": "Set of 5 printable A2 posters highlighting the journey from Dakshin Gangotri (1983) to Maitri (1989) and Bharati (2012), with timelines, station blueprints, and Indian Antarctic wildlife."
    },
    {
        "id": "ED-KIT-03",
        "title": "Undergraduate Polar Oceanography Lab Manual: CTD Data Analysis",
        "grade": "College / University",
        "category": "Python / Jupyter Notebooks",
        "downloads": "980",
        "file_size": "8.4 MB",
        "summary": "Open-source computational lab containing Python scripts to plot temperature-salinity (T-S) diagrams, sound velocity profiles, and mixed layer depth from actual Southern Ocean CTD casts."
    }
]

# Upcoming & Recent Polar Science Events / Announcements
EVENTS_ANNOUNCEMENTS: List[Dict[str, Any]] = [
    {
        "id": "EVT-01",
        "title": "Call for Research Proposals: 44th Indian Scientific Expedition to Antarctica (ISEA)",
        "date": "2024-07-15",
        "status": "Active / Accepting Submissions",
        "category": "Expedition Call",
        "organizer": "NCPOR Expedition Directorate",
        "summary": "Inviting proposals from Indian universities, CSIR/DST institutes, and DRDO laboratories for atmospheric, geological, biological, and medical research during the upcoming summer campaign."
    },
    {
        "id": "EVT-02",
        "title": "National Polar Science Webinar: Advances from India's Arctic Winter Presence",
        "date": "2024-06-21",
        "status": "Registration Open",
        "category": "Webinar",
        "organizer": "MoES Outreach Cell",
        "summary": "Lead scientists from the 2023-24 Himadri winter campaign present findings on Svalbard polar night atmospheric chemistry, aerosol optical depths, and fjord marine biology."
    },
    {
        "id": "EVT-03",
        "title": "Concluding Plenary of the 46th Antarctic Treaty Consultative Meeting (ATCM 46)",
        "date": "2024-05-30",
        "status": "Completed Milestone",
        "category": "International Conference",
        "organizer": "MoES & Ministry of External Affairs",
        "summary": "Historic gathering in Kochi where India and consultative party member nations adopted new resolutions on environmental monitoring, cruise tourism safety, and scientific cooperation."
    }
]

# Curated Press Kits for Journalists & Media Dissemination
PRESS_KITS: List[Dict[str, Any]] = [
    {
        "id": "PK-ISEA43",
        "title": "43rd Indian Scientific Expedition to Antarctica (ISEA) Official Press Pack",
        "release_date": "2024-01-18",
        "embargo": "None (Immediate Release)",
        "lead_minister": "Dr. Jitendra Singh, Hon'ble Union Minister of State for Earth Sciences",
        "summary": "Complete media dossier on the departure of 48 scientists and logistical personnel for Maitri and Bharati stations, highlighting new climate-change monitoring sensors and India's leadership in the Antarctic Treaty Consultative Meeting (ATCM 46).",
        "asset_count": 8,
        "assets_included": ["MED-01", "MED-03", "MED-05"],
        "download_size": "218 MB"
    },
    {
        "id": "PK-ARCTIC-WINTER",
        "title": "Historic First Indian Winter Expedition to the Arctic (Himadri) Milestone Dossier",
        "release_date": "2024-03-22",
        "embargo": "None (Immediate Release)",
        "lead_minister": "Ministry of Earth Sciences (MoES) & NCPOR Goa",
        "summary": "Detailed press kit marking the completion of India's first ever winter-long continuous presence in Ny-Ålesund, Svalbard, monitoring Arctic polar night atmospheric chemistry and sea-ice teleconnections with the Indian monsoon.",
        "asset_count": 6,
        "assets_included": ["MED-02", "MED-06"],
        "download_size": "164 MB"
    },
    {
        "id": "PK-SOE-HIMALAYA",
        "title": "Southern Ocean Carbon Sinks & Himalayan Third Pole Glaciology Media Briefing",
        "release_date": "2024-05-14",
        "embargo": "None (Immediate Release)",
        "lead_minister": "NCPOR Polar Science & Dissemination Directorate",
        "summary": "Official press and broadcaster package detailing ORV Sagar Nidhi Southern Ocean hydrographic cruises and high-altitude Himansh station benchmark glacier mass balance datasets across the Chandra basin.",
        "asset_count": 7,
        "assets_included": ["MED-04", "MED-06"],
        "download_size": "188 MB"
    }
]

# Student Science Quiz Questions
QUIZ_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "question": "What is the name of India's first permanent research station in Antarctica, established in 1983?",
        "options": ["Maitri", "Dakshin Gangotri", "Bharati", "Himadri"],
        "correct_index": 1,
        "explanation": "Dakshin Gangotri was established in 1983 during the 3rd Indian Antarctic Expedition. It served as India's first permanent base before being succeeded by Maitri in 1989."
    },
    {
        "id": 2,
        "question": "Where is India's dedicated Arctic research station 'Himadri' located?",
        "options": ["Greenland", "Ny-Ålesund, Svalbard (Norway)", "Northern Alaska", "Baffin Island (Canada)"],
        "correct_index": 1,
        "explanation": "Himadri is located in Ny-Ålesund, Spitsbergen, Svalbard — the world's northernmost functional international scientific research settlement."
    },
    {
        "id": 3,
        "question": "How does Arctic sea-ice melting directly connect to India's climate?",
        "options": [
            "It triggers tsunamis in the Bay of Bengal",
            "It causes planetary Rossby wave changes that alter the Indian Summer Monsoon rainfall",
            "It has zero scientific correlation with India",
            "It immediately increases temperature in the Thar desert"
        ],
        "correct_index": 1,
        "explanation": "Studies from NCPOR and MoES prove that springtime Barents-Kara sea ice decline creates mid-latitude atmospheric pressure waves that modulate monsoon onset and precipitation over India."
    },
    {
        "id": 4,
        "question": "Which lake in Antarctica provides essential freshwater and paleoclimate records for India's Maitri station?",
        "options": ["Lake Vostok", "Lake Priyadarshini", "Lake Ellsworth", "Lake Concordia"],
        "correct_index": 1,
        "explanation": "Lake Priyadarshini is a freshwater lake in the Schirmacher Oasis named after Prime Minister Indira Priyadarshini Gandhi, tapped by Indian engineers to sustain Maitri station."
    },
    {
        "id": 5,
        "question": "What unique design feature allows India's Bharati Station to endure fierce Antarctic blizzards and minimize snow burial?",
        "options": [
            "It is buried 50 meters under solid ice",
            "It is built on aerodynamic hydraulic stilts from 134 modular containers",
            "It is anchored only by steel ropes to granite boulders",
            "It is a geodesic canvas dome"
        ],
        "correct_index": 1,
        "explanation": "Bharati was designed as a modern two-story modular facility elevated on stilts, allowing high-speed katabatic winds and drifting snow to pass underneath without burying the station."
    }
]

# Admin Publishing & Moderation Queue
ADMIN_QUEUE: List[Dict[str, Any]] = [
    {
        "id": "SUB-2024-001",
        "title": "Benthic Foraminiferal Assemblages in Prydz Bay and Southern Ocean Holocene Carbonate Deposition",
        "submitter": "Dr. Rajeshwar Rao, Senior Geologist, NCPOR",
        "submitted_date": "2024-05-10",
        "type": "Research Paper & Dataset",
        "expedition": "43rd ISEA",
        "station": "Bharati",
        "status": "APPROVED",
        "reviewed_by": "Scientific Review Committee (MoES)",
        "gigw_compliance": "Verified (Alt text, GIGW Level AA, Metadata standard schema)",
        "ai_enriched": True,
        "ai_suggested_tags": ["Prydz Bay", "Foraminifera", "Holocene", "Carbonate Deposition", "Bharati"],
        "plain_summary": "Microscopic shell fossils recovered from seabed mud off Bharati station show how ocean currents shifted over the last 10,000 years."
    },
    {
        "id": "SUB-2024-002",
        "title": "Winter Aerosol Optical Depth and Black Carbon Deposition at Himadri during 2023-24 Polar Night",
        "submitter": "Dr. Pooja Nambiar, Atmospheric Scientist",
        "submitted_date": "2024-05-18",
        "type": "Research Paper",
        "expedition": "Arctic Winter 2023-24",
        "station": "Himadri",
        "status": "PENDING_REVIEW",
        "reviewed_by": "Editorial Review Queue",
        "gigw_compliance": "Pending Accessibility Check",
        "ai_enriched": True,
        "ai_suggested_tags": ["Aerosol Optical Depth", "Black Carbon", "Arctic Winter", "Himadri", "Atmospheric Chemistry"],
        "plain_summary": "First measurements of soot and industrial smog carried into the 24-hour dark Arctic winter, darkening snow surfaces and accelerating spring thaw."
    },
    {
        "id": "SUB-2024-003",
        "title": "High-Definition 4K Drone Aerial Survey of Maitri Sastrugi and Blue Ice Runway",
        "submitter": "Logistics & Aviation Cell, 43rd ISEA",
        "submitted_date": "2024-05-20",
        "type": "Media Asset (Video)",
        "expedition": "43rd ISEA",
        "station": "Maitri",
        "status": "PENDING_REVIEW",
        "reviewed_by": "Outreach & Press Bureau",
        "gigw_compliance": "Pending Closed-Captioning Check",
        "ai_enriched": True,
        "ai_suggested_tags": ["Drone", "Blue Ice Runway", "ALCI Logistics", "Maitri", "Antarctica Aviation"],
        "plain_summary": "Drone footage of the blue ice airstrip in Queen Maud Land that allows heavy transport aircraft (IL-76) to land directly on Antarctic glacial ice."
    }
]


class PolarDataStore:
    """Manages active queries, filtering, submissions, outreach content, and publishing."""

    def __init__(self):
        self.stations = STATIONS_DATA
        self.publications = PUBLICATIONS_DATA
        self.datasets = DATASETS_DATA
        self.media = MEDIA_ASSETS
        self.press_kits = PRESS_KITS
        self.quiz = QUIZ_QUESTIONS
        self.admin_queue = ADMIN_QUEUE
        self.articles = OUTREACH_ARTICLES
        self.toolkits = EDUCATIONAL_TOOLKITS
        self.events = EVENTS_ANNOUNCEMENTS

    def get_stations(self) -> List[Dict[str, Any]]:
        return self.stations

    def get_station_by_id(self, station_id: str) -> Optional[Dict[str, Any]]:
        for s in self.stations:
            if s["id"].lower() == station_id.lower():
                return s
        return None

    def search_publications(
        self,
        query: str = "",
        station: str = "",
        vertical: str = "",
        year: Optional[int] = None,
        sort_by: str = "newest"
    ) -> List[Dict[str, Any]]:
        results = []
        q = query.lower().strip()
        for p in self.publications:
            if q:
                combined_text = (
                    f"{p['title']} {p['abstract']} {' '.join(p['keywords'])} {p['authors']} {p.get('topic', '')} {p['expedition']}"
                ).lower()
                if q not in combined_text:
                    continue
            if station and station.lower() not in p.get("station", "").lower():
                continue
            if vertical and vertical.lower() not in p.get("vertical", "").lower():
                continue
            if year and p.get("year") != year:
                continue
            results.append(p)

        # Sorting logic
        if sort_by == "oldest":
            results.sort(key=lambda x: x.get("year", 0))
        elif sort_by == "citations":
            results.sort(key=lambda x: x.get("citation_count", 0), reverse=True)
        elif sort_by == "title":
            results.sort(key=lambda x: x.get("title", "").lower())
        else:  # newest default
            results.sort(key=lambda x: x.get("year", 0), reverse=True)

        return results

    def get_publication_by_id(self, pub_id: str) -> Optional[Dict[str, Any]]:
        for p in self.publications:
            if p["id"].lower() == pub_id.lower():
                return p
        return None

    def add_publication(self, pub_data: Dict[str, Any]) -> Dict[str, Any]:
        """Directly add a publication resource."""
        pub_id = pub_data.get("id") or f"NCPOR-PUB-{datetime.now().year}-{len(self.publications) + 1:03d}"
        new_pub = {
            "id": pub_id,
            "title": pub_data["title"],
            "authors": pub_data.get("authors", "NCPOR Research Scientist"),
            "affiliation": pub_data.get("affiliation", "NCPOR, Ministry of Earth Sciences"),
            "year": pub_data.get("year", datetime.now().year),
            "expedition": pub_data.get("expedition", "43rd ISEA"),
            "station": pub_data.get("station", "Bharati"),
            "vertical": pub_data.get("vertical", "Glaciology"),
            "topic": pub_data.get("topic", "Polar Cryosphere"),
            "doi": pub_data.get("doi", f"10.1007/ncpor.{pub_id.lower()}"),
            "abstract": pub_data["abstract"],
            "keywords": pub_data.get("keywords", ["Polar Science", "NCPOR"]),
            "dataset_attached": pub_data.get("dataset_attached", f"DS-{pub_id}"),
            "file_type": pub_data.get("file_type", "PDF & NetCDF"),
            "plain_summary": pub_data.get("plain_summary", "Summary auto-generated by Polar AI engine."),
            "citation_count": 0,
            "bibtex": f"""@article{{{pub_id.lower()},
  title={{{pub_data['title']}}},
  author={{{pub_data.get('authors', 'NCPOR')}}},
  journal={{NCPOR Scientific Publications}},
  year={{{datetime.now().year}}},
  publisher={{MoES / NCPOR}}
}}"""
        }
        self.publications.insert(0, new_pub)
        return new_pub

    def delete_publication(self, pub_id: str) -> bool:
        for idx, p in enumerate(self.publications):
            if p["id"].lower() == pub_id.lower():
                self.publications.pop(idx)
                return True
        return False

    def get_datasets(self) -> List[Dict[str, Any]]:
        return self.datasets

    def get_dataset_by_id(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        for d in self.datasets:
            if d.get("id", "").strip().lower() == dataset_id.strip().lower():
                return d
        return None

    def get_media_assets(
        self,
        media_type: str = "",
        station: str = "",
        tag: str = "",
        search: str = ""
    ) -> List[Dict[str, Any]]:
        results = []
        s_lower = search.lower().strip()
        for m in self.media:
            if media_type and m["type"].lower() != media_type.lower():
                continue
            if station and station.lower() not in m.get("station", "").lower():
                continue
            if tag and not any(tag.lower() in t.lower() for t in m.get("tags", [])):
                continue
            if s_lower:
                combined = f"{m['title']} {m['description']} {' '.join(m.get('tags', []))} {m.get('category', '')}".lower()
                if s_lower not in combined:
                    continue
            results.append(m)
        return results

    def add_media_asset(self, asset: Dict[str, Any]) -> Dict[str, Any]:
        med_id = f"MED-{len(self.media) + 1:02d}"
        new_asset = {
            "id": med_id,
            "title": asset["title"],
            "type": asset.get("type", "photo"),
            "category": asset.get("category", "General"),
            "expedition": asset.get("expedition", "Polar Campaign"),
            "station": asset.get("station", "Bharati"),
            "location": asset.get("location", "Polar Outpost"),
            "coordinates": asset.get("coordinates", "Polar Region"),
            "url": asset.get("url", "/assets/images/bharati.jpg"),
            "thumbnail": asset.get("thumbnail", "/assets/images/bharati.jpg"),
            "resolution": asset.get("resolution", "1080p Web"),
            "credit": asset.get("credit", "NCPOR Media Wing"),
            "license": asset.get("license", "Government Open Access / CC-BY 4.0"),
            "tags": asset.get("tags", ["PolarScience"]),
            "description": asset.get("description", "Expedition asset documentation."),
            "press_kit_eligible": asset.get("press_kit_eligible", False),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.media.insert(0, new_asset)
        return new_asset

    def delete_media_asset(self, asset_id: str) -> bool:
        for idx, m in enumerate(self.media):
            if m["id"].lower() == asset_id.lower():
                self.media.pop(idx)
                return True
        return False

    def get_press_kits(self) -> List[Dict[str, Any]]:
        return self.press_kits

    def get_press_kit_by_id(self, pk_id: str) -> Optional[Dict[str, Any]]:
        for pk in self.press_kits:
            if pk["id"].lower() == pk_id.lower():
                return pk
        return None

    def get_outreach_articles(self, audience: str = "", topic: str = "") -> List[Dict[str, Any]]:
        results = []
        for a in self.articles:
            if audience and audience.lower() not in a["audience"].lower():
                continue
            if topic and topic.lower() not in a["topic"].lower():
                continue
            results.append(a)
        return results

    def add_outreach_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        art_id = f"ART-{len(self.articles) + 1:02d}"
        new_art = {
            "id": art_id,
            "title": article["title"],
            "audience": article.get("audience", "General Public"),
            "topic": article.get("topic", "Polar Science"),
            "read_time": article.get("read_time", "5 min"),
            "published_date": datetime.now().strftime("%Y-%m-%d"),
            "image": article.get("image", "/assets/images/bharati.jpg"),
            "summary": article.get("summary", ""),
            "content": article.get("content", ""),
            "key_takeaways": article.get("key_takeaways", ["Key insight on polar dynamics"])
        }
        self.articles.insert(0, new_art)
        return new_art

    def delete_outreach_article(self, article_id: str) -> bool:
        for idx, a in enumerate(self.articles):
            if a["id"].lower() == article_id.lower():
                self.articles.pop(idx)
                return True
        return False

    def get_educational_toolkits(self) -> List[Dict[str, Any]]:
        return self.toolkits

    def get_toolkit_by_id(self, toolkit_id: str) -> Optional[Dict[str, Any]]:
        for k in self.toolkits:
            if k.get("id", "").strip().lower() == toolkit_id.strip().lower():
                return k
        return None

    def get_events(self) -> List[Dict[str, Any]]:
        return self.events

    def add_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        evt_id = f"EVT-{len(self.events) + 1:02d}"
        new_evt = {
            "id": evt_id,
            "title": event["title"],
            "date": event.get("date", datetime.now().strftime("%Y-%m-%d")),
            "status": event.get("status", "Upcoming"),
            "category": event.get("category", "General Event"),
            "organizer": event.get("organizer", "NCPOR / MoES"),
            "summary": event.get("summary", "")
        }
        self.events.insert(0, new_evt)
        return new_evt

    def delete_event(self, event_id: str) -> bool:
        for idx, e in enumerate(self.events):
            if e["id"].lower() == event_id.lower():
                self.events.pop(idx)
                return True
        return False

    def get_admin_queue(self) -> List[Dict[str, Any]]:
        return self.admin_queue

    def add_submission(self, submission: Dict[str, Any]) -> Dict[str, Any]:
        sub_id = f"SUB-{datetime.now().year}-{len(self.admin_queue) + 1:03d}"
        new_sub = {
            "id": sub_id,
            "title": submission["title"],
            "submitter": submission.get("submitter", "NCPOR Research Associate"),
            "submitted_date": datetime.now().strftime("%Y-%m-%d"),
            "type": submission.get("type", "Research Paper"),
            "expedition": submission.get("expedition", "43rd ISEA"),
            "station": submission.get("station", "Bharati"),
            "status": "PENDING_REVIEW",
            "reviewed_by": "Pending Review",
            "gigw_compliance": "Verification in progress",
            "ai_enriched": True,
            "ai_suggested_tags": submission.get("tags", ["Polar Science", "NCPOR", "Cryosphere"]),
            "plain_summary": submission.get("plain_summary", "Summary auto-generated by Polar AI engine.")
        }
        self.admin_queue.insert(0, new_sub)
        return new_sub

    def approve_and_publish(self, sub_id: str) -> Optional[Dict[str, Any]]:
        for item in self.admin_queue:
            if item["id"] == sub_id:
                item["status"] = "PUBLISHED"
                item["reviewed_by"] = "MoES Scientific Secretary / Approved"
                item["gigw_compliance"] = "Passed GIGW Level AA"

                new_pub = {
                    "id": f"NCPOR-{sub_id}",
                    "title": item["title"],
                    "authors": item["submitter"],
                    "affiliation": "National Centre for Polar and Ocean Research",
                    "year": datetime.now().year,
                    "expedition": item["expedition"],
                    "station": item["station"],
                    "vertical": "Glaciology",
                    "topic": "Polar Cryosphere",
                    "doi": f"10.1007/ncpor.{sub_id.lower()}",
                    "abstract": f"Official expedition findings published following MoES peer-review and GIGW clearance: {item['title']}. Documenting ongoing long-term observations in polar and cryospheric dynamics.",
                    "keywords": item["ai_suggested_tags"],
                    "dataset_attached": f"DS-{sub_id}",
                    "file_type": "PDF & Data Annex",
                    "plain_summary": item["plain_summary"],
                    "citation_count": 0,
                    "bibtex": f"""@article{{{sub_id.lower()},
  title={{{item['title']}}},
  author={{{item['submitter']}}},
  journal={{NCPOR Official Scientific Bulletins}},
  year={{{datetime.now().year}}},
  publisher={{MoES / NCPOR}}
}}"""
                }
                self.publications.insert(0, new_pub)
                return item
        return None

    def get_analytics_summary(self) -> Dict[str, Any]:
        """Provides dashboard statistics for the admin management console."""
        return {
            "total_publications": len(self.publications),
            "total_datasets": len(self.datasets),
            "total_media_assets": len(self.media),
            "total_outreach_articles": len(self.articles),
            "total_toolkits": len(self.toolkits),
            "total_events": len(self.events),
            "pending_queue_count": len([q for q in self.admin_queue if q["status"] == "PENDING_REVIEW"]),
            "active_stations": len(self.stations),
            "total_downloads": "14,890",
            "rag_queries_answered": "3,412"
        }


# Global Singleton Store
data_store = PolarDataStore()
