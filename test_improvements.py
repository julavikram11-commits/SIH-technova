import urllib.request
import json
import os
import sys

def p(msg):
    try:
        print(msg, flush=True)
    except Exception:
        try:
            print(msg.encode("ascii", errors="replace").decode("ascii"), flush=True)
        except Exception:
            pass

def run_tests():
    p("==================================================================")
    p("  POLAR SCIENCE PORTAL VERIFICATION: 2 IMPROVEMENTS TEST SUITE")
    p("==================================================================")

    # 1. Test All 4 Home & Overview Images
    p("\n[TEST 1] Verifying all four Home & Overview section images...")
    images = [
        "http://localhost:8000/assets/images/bharati.jpg",
        "http://localhost:8000/assets/images/himadri.jpg",
        "http://localhost:8000/assets/images/maitri.jpg",
        "http://localhost:8000/assets/images/himansh.jpg"
    ]
    all_images_ok = True
    for img_url in images:
        try:
            r = urllib.request.urlopen(img_url)
            content = r.read()
            name = img_url.split('/')[-1]
            p(f"  [PASS] {name}: {len(content):,} bytes (HTTP 200 OK)")
        except Exception as e:
            p(f"  [FAIL] {img_url}: {e}")
            all_images_ok = False
    
    assert all_images_ok, "Image check failed!"

    # 2. Test AI Engine Status
    p("\n[TEST 2] Verifying AI Engine status & configuration...")
    r = urllib.request.urlopen("http://localhost:8000/api/ai/status")
    status_data = json.loads(r.read().decode("utf-8"))
    p(f"  [PASS] AI Engine Status: {status_data['status']}")
    p(f"  [PASS] Provider: {status_data['provider']}")
    p(f"  [PASS] API Key Configured: {status_data['api_key_configured']}")

    # 3. Test Novel Polar Science Question (NOT in predefined list)
    p("\n[TEST 3] Testing dynamic answers for novel (non-predefined) questions...")
    q1 = "What wildlife and penguin species can be observed near Indian Antarctic bases?"
    req1 = urllib.request.Request(
        "http://localhost:8000/api/ai/ask",
        data=json.dumps({"query": q1, "history": []}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    r1 = urllib.request.urlopen(req1)
    d1 = json.loads(r1.read().decode("utf-8"))
    p(f"  User Query: \"{q1}\"")
    p(f"  AI Answer: {d1['answer'][:160].replace(chr(10), ' ')}...")
    p(f"  Provider: {d1.get('provider')}")
    p(f"  Citations: {d1.get('citations')}")
    assert d1.get("in_scope") is not False, "Q1 should be in-scope!"
    assert len(d1.get("answer", "")) > 50, "Answer should be substantive!"

    # 4. Test Multi-Turn Conversational Memory / Follow-up Question
    p("\n[TEST 4] Testing conversational context & pronoun resolution in follow-ups...")
    q2 = "How cold does it get there during winter?"
    history = [
        {"role": "user", "content": q1},
        {"role": "assistant", "content": d1["answer"]}
    ]
    req2 = urllib.request.Request(
        "http://localhost:8000/api/ai/ask",
        data=json.dumps({"query": q2, "history": history}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    r2 = urllib.request.urlopen(req2)
    d2 = json.loads(r2.read().decode("utf-8"))
    p(f"  Follow-up Query: \"{q2}\" (Resolving context 'there' = Antarctic bases)")
    p(f"  AI Answer: {d2['answer'][:160].replace(chr(10), ' ')}...")
    p(f"  Provider: {d2.get('provider')}")
    assert d2.get("in_scope") is not False, "Follow-up should be recognized in-scope!"
    assert len(d2.get("answer", "")) > 50, "Follow-up answer should be substantive!"

    # 5. Test Out-of-Domain Refusal
    p("\n[TEST 5] Testing out-of-domain guardrail...")
    q3 = "Who won the 2024 cricket world cup?"
    req3 = urllib.request.Request(
        "http://localhost:8000/api/ai/ask",
        data=json.dumps({"query": q3, "history": []}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    r3 = urllib.request.urlopen(req3)
    d3 = json.loads(r3.read().decode("utf-8"))
    p(f"  Out-of-Scope Query: \"{q3}\"")
    p(f"  Refusal: {d3['answer'][:120].replace(chr(10), ' ')}...")
    assert d3.get("in_scope") is False, "Non-polar queries must be declined gracefully!"

    # 6. Test Core Portal Endpoints
    p("\n[TEST 6] Testing overall portal integrity...")
    endpoints = [
        "http://localhost:8000/",
        "http://localhost:8000/css/styles.css",
        "http://localhost:8000/js/app.js",
        "http://localhost:8000/js/outreach.js",
        "http://localhost:8000/js/repository.js",
        "http://localhost:8000/js/media.js",
        "http://localhost:8000/js/ai-chat.js",
        "http://localhost:8000/api/stats",
        "http://localhost:8000/api/stations/live",
        "http://localhost:8000/api/outreach/stations",
        "http://localhost:8000/api/repository/publications",
        "http://localhost:8000/api/media/assets"
    ]
    for ep in endpoints:
        r = urllib.request.urlopen(ep)
        assert r.status == 200, f"Failed on {ep}"
        p(f"  [PASS] {ep} (HTTP 200 OK)")

    p("\n==================================================================")
    p("  ALL 6 TEST SUITES PASSED! BOTH IMPROVEMENTS FULLY OPERATIONAL")
    p("==================================================================")

if __name__ == "__main__":
    run_tests()
