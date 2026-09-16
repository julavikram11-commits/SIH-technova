"""
press_kit_generator.py - Generates official media press kit ZIP packages for journalists & broadcasters.
Packages authentic high-resolution photography assets, official press release dossiers,
licensing manifest, and station factsheets for NCPOR / MoES polar expeditions.
"""

import io
import os
import json
import zipfile
from typing import Dict, Any, List


def generate_press_kit_zip(pk: Dict[str, Any], media_assets: List[Dict[str, Any]], static_dir: str) -> bytes:
    """
    Builds an in-memory ZIP archive for the requested press kit containing:
    1. Authentic image assets included in this press release dossier.
    2. Sidecar metadata TXT files for each asset.
    3. Official PRESS_RELEASE_DOSSIER.txt with institutional header and statements.
    4. Machine-readable MEDIA_MANIFEST.json with credits, coordinates, and license.
    5. ATTRIBUTION_AND_LICENSING.txt with open-access government broadcasting terms.
    6. EXPEDITION_STATION_FACTSHEET.txt detailing polar station specifications.
    """
    buffer = io.BytesIO()

    # Index available media assets by ID (case-insensitive)
    media_by_id = {a["id"].upper(): a for a in media_assets}
    included_ids = pk.get("assets_included", [])
    matched_assets = [media_by_id[aid.upper()] for aid in included_ids if aid.upper() in media_by_id]

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. Official PRESS_RELEASE_DOSSIER.txt
        dossier_content = f"""================================================================================
NATIONAL CENTRE FOR POLAR AND OCEAN RESEARCH (NCPOR)
Ministry of Earth Sciences (MoES), Government of India
Headquarters: Headland Sada, Vasco-da-Gama, Goa 403804, India
================================================================================
OFFICIAL PRESS RELEASE DOSSIER & ACCREDITED MEDIA PACK
================================================================================

PRESS KIT IDENTIFIER : {pk.get('id')}
RELEASE DATE         : {pk.get('release_date')}
EMBARGO STATUS       : {pk.get('embargo', 'None (Immediate Release)')}
MINISTERIAL LEAD     : {pk.get('lead_minister', 'Ministry of Earth Sciences, Govt. of India')}
PORTAL REFERENCE     : SIH26063 Polar Portal Media Dissemination Hub

--------------------------------------------------------------------------------
1. HEADLINE
--------------------------------------------------------------------------------
{pk.get('title')}

--------------------------------------------------------------------------------
2. EXECUTIVE BRIEFING & DISSEMINATION STATEMENT
--------------------------------------------------------------------------------
{pk.get('summary')}

--------------------------------------------------------------------------------
3. ACCREDITED MEDIA ASSETS INCLUDED IN THIS ARCHIVE ({len(matched_assets)} Items)
--------------------------------------------------------------------------------
"""
        for idx, asset in enumerate(matched_assets, 1):
            dossier_content += f"""
[{idx}] ASSET ID    : {asset.get('id')}
    Title       : {asset.get('title')}
    Type        : {str(asset.get('type', 'Photography')).capitalize()}
    Category    : {asset.get('category')}
    Station     : {asset.get('station')}
    Expedition  : {asset.get('expedition')}
    Location    : {asset.get('location')} ({asset.get('coordinates')})
    Resolution  : {asset.get('resolution', '4K UHD')}
    Credit Line : {asset.get('credit')}
    License     : {asset.get('license')}
    Description : {asset.get('description')}
"""

        dossier_content += f"""
--------------------------------------------------------------------------------
4. BROADCAST & EDITORIAL CLEARANCE GUIDELINES
--------------------------------------------------------------------------------
- All high-resolution images contained in this press kit are cleared for editorial,
  broadcast television, documentary, digital web, and print newspaper publication.
- Attribution Line Required: "Courtesy: NCPOR / Ministry of Earth Sciences, Govt. of India"
- Commercial merchandise resale of raw imagery is prohibited without MoES clearance.
- For high-definition raw footage or interview requests with wintering expedition leaders,
  contact: media-relations@ncpor.res.in / pio@moes.gov.in

================================================================================
(C) National Centre for Polar and Ocean Research | Government of India Open Data
================================================================================
"""
        zf.writestr("PRESS_RELEASE_DOSSIER.txt", dossier_content.strip())

        # 2. MEDIA_MANIFEST.json
        manifest = {
            "press_kit_id": pk.get("id"),
            "title": pk.get("title"),
            "release_date": pk.get("release_date"),
            "embargo": pk.get("embargo"),
            "lead_minister": pk.get("lead_minister"),
            "summary": pk.get("summary"),
            "curated_asset_count": len(matched_assets),
            "advertised_download_size": pk.get("download_size"),
            "portal_code": "SIH26063",
            "issuer": "National Centre for Polar and Ocean Research (NCPOR), MoES India",
            "assets": [
                {
                    "id": a.get("id"),
                    "title": a.get("title"),
                    "station": a.get("station"),
                    "expedition": a.get("expedition"),
                    "category": a.get("category"),
                    "coordinates": a.get("coordinates"),
                    "resolution": a.get("resolution"),
                    "aspect_ratio": a.get("aspect_ratio", "16:9"),
                    "credit": a.get("credit"),
                    "license": a.get("license"),
                    "filename": f"{a.get('id')}_{os.path.basename(a.get('url', 'photo.jpg'))}",
                    "tags": a.get("tags", []),
                    "description": a.get("description")
                }
                for a in matched_assets
            ]
        }
        zf.writestr("MEDIA_MANIFEST.json", json.dumps(manifest, indent=2))

        # 3. ATTRIBUTION_AND_LICENSING.txt
        license_text = """================================================================================
GOVERNMENT OF INDIA OPEN DATA & BROADCAST LICENSING MANIFEST
================================================================================
National Centre for Polar and Ocean Research (NCPOR)
Ministry of Earth Sciences, Government of India

TERMS OF DISSEMINATION:
1. Editorial & Media Broadcasters:
   These assets are published under the Government Open Access / CC-BY 4.0 license.
   Journalists, news organizations, television networks, educators, and science
   communicators are granted non-exclusive, worldwide rights to publish, broadcast,
   reproduce, and distribute these assets with appropriate credit.

2. Mandatory Credit Line:
   Every reproduction must state:
   "Photo / Media: NCPOR / Ministry of Earth Sciences, Govt. of India"
   (or individual photographer specified in MEDIA_MANIFEST.json).

3. Integrity of Scientific Context:
   Images, videos, and figures must not be manipulated or placed in a manner that
   misrepresents polar scientific research, station coordinates, or climate data.

4. Contact for Media Inquiries:
   Public Relations Officer & Media Cell
   National Centre for Polar and Ocean Research, Vasco-da-Gama, Goa 403804
   Email: media-cell@ncpor.res.in | Website: https://ncpor.res.in
================================================================================
"""
        zf.writestr("ATTRIBUTION_AND_LICENSING.txt", license_text.strip())

        # 4. EXPEDITION_STATION_FACTSHEET.txt
        stations_brief = """================================================================================
NCPOR POLAR AND HIGH-ALTITUDE RESEARCH STATIONS FACTSHEET
================================================================================

1. BHARATI RESEARCH STATION (Antarctica)
   - Location: Larsemann Hills, East Antarctica (69°24'28" S, 76°11'14" E)
   - Established: 2012 (31st Indian Scientific Expedition to Antarctica)
   - Architecture: Aerodynamic stilt design engineered to withstand 200 km/h blizzards
   - Focus: Atmospheric physics, geomagnetism, paleoclimate, satellite ground station

2. MAITRI RESEARCH STATION (Antarctica)
   - Location: Schirmacher Oasis, Queen Maud Land (70°45'58" S, 11°44'09" E)
   - Established: 1989 (Succeeded Dakshin Gangotri)
   - Freshwater Source: Lake Priyadarshini
   - Focus: Meteorology, human physiology in extreme cold, seismology, glaciology

3. HIMADRI RESEARCH STATION (Arctic)
   - Location: Ny-Ålesund, Spitsbergen, Svalbard (78°55'25" N, 11°55'40" E)
   - Established: 2008
   - Milestone: First year-round wintering presence achieved in 2023-2024
   - Focus: Arctic-Indian monsoon teleconnections, aerosol radiative forcing, fjord dynamics

4. HIMANSH HIGH-ALTITUDE RESEARCH STATION (Himalayas / Third Pole)
   - Location: Sutri Dhaka, Chandra Basin, Spiti Valley, HP (32°25'41" N, 77°37'32" E)
   - Elevation: 4,050 metres above sea level
   - Established: 2016
   - Focus: Benchmark glacier mass balance (Batal, Samudra Tapu), hydrometeorology

5. OCEAN RESEARCH VESSEL (ORV) SAGAR NIDHI
   - Type: Ice-strengthened multidisciplinary oceanographic research vessel
   - Operations: Southern Ocean Expeditions, CTD casts, bio-optical profiling to 65°S
================================================================================
"""
        zf.writestr("EXPEDITION_STATION_FACTSHEET.txt", stations_brief.strip())

        # 5. Pack individual media asset files into assets/ folder
        for asset in matched_assets:
            url_path = asset.get("url", "")
            clean_rel = url_path.lstrip("/").replace("/", os.sep)
            local_path = os.path.join(static_dir, clean_rel)

            asset_filename = f"{asset.get('id')}_{os.path.basename(url_path)}"

            if os.path.isfile(local_path):
                with open(local_path, "rb") as img_f:
                    img_data = img_f.read()
                zf.writestr(f"assets/{asset_filename}", img_data)
            else:
                zf.writestr(
                    f"assets/{asset_filename}.txt",
                    f"Asset {asset.get('id')}: {asset.get('title')}\nSource URL: {url_path}"
                )

            # Asset-specific metadata card
            asset_meta = f"""ASSET IDENTIFIER: {asset.get('id')}
Title          : {asset.get('title')}
Expedition     : {asset.get('expedition')}
Station        : {asset.get('station')}
Location       : {asset.get('location')}
Coordinates    : {asset.get('coordinates')}
Resolution     : {asset.get('resolution', '4K UHD')}
Credit Line    : {asset.get('credit')}
License        : {asset.get('license')}
Tags           : {', '.join(asset.get('tags', []))}
Description    : {asset.get('description')}
"""
            zf.writestr(f"assets/{asset.get('id')}_METADATA.txt", asset_meta.strip())

    return buffer.getvalue()
