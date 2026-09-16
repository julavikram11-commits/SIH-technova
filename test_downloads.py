"""
test_downloads.py - Automated Verification of Resource Downloads
Verifies:
1. Dataset downloads: all datasets in DATASETS_DATA return 200, attachment header, text/csv, non-empty content
2. Educational toolkit downloads: all toolkits in EDUCATIONAL_TOOLKITS return 200, attachment header, application/pdf, valid PDF magic bytes
3. Publication downloads: all publications in PUBLICATIONS_DATA return 200, attachment header, application/pdf, valid PDF magic bytes
4. Robustness: invalid IDs for datasets, toolkits, and publications return 404
"""

from fastapi.testclient import TestClient
from server.main import app
import server.data_store as ds

client = TestClient(app)

def run_download_tests():
    print("=" * 60)
    print("  VERIFYING RESOURCE DOWNLOAD ENDPOINTS")
    print("=" * 60)

    # 1. Datasets
    print("\n[1] Testing Dataset Downloads (/api/repository/download/{id})...")
    dataset_ids = [d["id"] for d in ds.DATASETS_DATA]
    assert len(dataset_ids) == 4, f"Expected 4 datasets, found {len(dataset_ids)}"
    for d_id in dataset_ids:
        res = client.get(f"/api/repository/download/{d_id}")
        assert res.status_code == 200, f"Expected 200 for {d_id}, got {res.status_code}"
        cd = res.headers.get("content-disposition", "")
        ct = res.headers.get("content-type", "")
        assert "attachment;" in cd, f"Missing attachment header in {cd}"
        assert f"{d_id}_dataset.csv" in cd, f"Filename mismatch in {cd}"
        assert "text/csv" in ct, f"Invalid content type {ct}"
        assert len(res.content) > 200, f"Payload unexpectedly small for {d_id}"
        # Verify CSV content contains required metadata fields
        text = res.text
        assert "NATIONAL CENTRE FOR POLAR AND OCEAN RESEARCH" in text
        assert d_id in text
        assert "Sample_ID" in text
        print(f"  [OK] Dataset {d_id}: OK ({len(res.content)} bytes, {cd})")

    # Invalid dataset
    res_404 = client.get("/api/repository/download/INVALID_DATASET_ID_999")
    assert res_404.status_code == 404, f"Expected 404, got {res_404.status_code}"
    print("  [OK] Invalid Dataset ID returns 404: OK")

    # 2. Educational Toolkits
    print("\n[2] Testing Educational Toolkit Downloads (/api/outreach/toolkits/download/{id})...")
    toolkit_ids = [k["id"] for k in ds.EDUCATIONAL_TOOLKITS]
    assert len(toolkit_ids) == 3, f"Expected 3 toolkits, found {len(toolkit_ids)}"
    for kit_id in toolkit_ids:
        res = client.get(f"/api/outreach/toolkits/download/{kit_id}")
        assert res.status_code == 200, f"Expected 200 for {kit_id}, got {res.status_code}"
        cd = res.headers.get("content-disposition", "")
        ct = res.headers.get("content-type", "")
        assert "attachment;" in cd, f"Missing attachment header in {cd}"
        assert f"{kit_id}_educational_toolkit.pdf" in cd, f"Filename mismatch in {cd}"
        assert "application/pdf" in ct, f"Invalid content type {ct}"
        assert res.content.startswith(b"%PDF-"), f"Invalid PDF magic header for {kit_id}"
        print(f"  [OK] Toolkit {kit_id}: OK ({len(res.content)} bytes, {cd})")

    # Invalid toolkit
    res_kit_404 = client.get("/api/outreach/toolkits/download/INVALID_TOOLKIT_ID_999")
    assert res_kit_404.status_code == 404, f"Expected 404, got {res_kit_404.status_code}"
    print("  [OK] Invalid Toolkit ID returns 404: OK")

    # 3. Publications
    print("\n[3] Testing Publication Downloads (/api/repository/publication/{id}/download)...")
    pub_ids = [p["id"] for p in ds.PUBLICATIONS_DATA]
    assert len(pub_ids) == 8, f"Expected 8 publications, found {len(pub_ids)}"
    for pub_id in pub_ids:
        res = client.get(f"/api/repository/publication/{pub_id}/download")
        assert res.status_code == 200, f"Expected 200 for {pub_id}, got {res.status_code}"
        cd = res.headers.get("content-disposition", "")
        ct = res.headers.get("content-type", "")
        assert "attachment;" in cd, f"Missing attachment header in {cd}"
        assert f"{pub_id}_publication.pdf" in cd, f"Filename mismatch in {cd}"
        assert "application/pdf" in ct, f"Invalid content type {ct}"
        assert res.content.startswith(b"%PDF-"), f"Invalid PDF magic header for {pub_id}"
        print(f"  [OK] Publication {pub_id}: OK ({len(res.content)} bytes, {cd})")

    # Invalid publication
    res_pub_404 = client.get("/api/repository/publication/INVALID_PUB_ID_999/download")
    assert res_pub_404.status_code == 404, f"Expected 404, got {res_pub_404.status_code}"
    print("  [OK] Invalid Publication ID returns 404: OK")

    # 4. Press Kit ZIP Packages
    import io
    import zipfile
    print("\n[4] Testing Press Kit ZIP Downloads (/api/media/press-kits/{id}/download)...")
    press_kits = ds.data_store.get_press_kits()
    assert len(press_kits) == 3, f"Expected 3 press kits, found {len(press_kits)}"
    for pk in press_kits:
        pk_id = pk["id"]
        res = client.get(f"/api/media/press-kits/{pk_id}/download")
        assert res.status_code == 200, f"Expected 200 for {pk_id}, got {res.status_code}"
        cd = res.headers.get("content-disposition", "")
        ct = res.headers.get("content-type", "")
        assert "attachment;" in cd, f"Missing attachment header in {cd}"
        assert f"{pk_id}_press_kit.zip" in cd, f"Filename mismatch in {cd}"
        assert "application/zip" in ct, f"Invalid content type {ct}"
        assert len(res.content) > 10000, f"Payload unexpectedly small for {pk_id}"
        
        # Verify valid ZIP content and expected dossier files
        zf = zipfile.ZipFile(io.BytesIO(res.content))
        namelist = zf.namelist()
        assert "PRESS_RELEASE_DOSSIER.txt" in namelist, f"Missing dossier in {pk_id}"
        assert "MEDIA_MANIFEST.json" in namelist, f"Missing manifest in {pk_id}"
        assert "ATTRIBUTION_AND_LICENSING.txt" in namelist, f"Missing licensing in {pk_id}"
        assert "EXPEDITION_STATION_FACTSHEET.txt" in namelist, f"Missing factsheet in {pk_id}"

        # Verify correct assets for this specific card
        for aid in pk.get("assets_included", []):
            matching_files = [n for n in namelist if aid.upper() in n.upper()]
            assert len(matching_files) >= 1, f"Missing asset {aid} in press kit {pk_id}"

        print(f"  [OK] Press Kit {pk_id}: OK ({len(res.content)} bytes, {len(namelist)} items in zip)")

    # Invalid press kit
    res_pk_404 = client.get("/api/media/press-kits/INVALID_PRESS_KIT_ID_999/download")
    assert res_pk_404.status_code == 404, f"Expected 404, got {res_pk_404.status_code}"
    print("  [OK] Invalid Press Kit ID returns 404: OK")

    print("\n" + "=" * 60)
    print("  ALL RESOURCE DOWNLOAD TESTS PASSED ACCURATELY (19/19 checks)!")
    print("=" * 60)

if __name__ == "__main__":
    run_download_tests()

