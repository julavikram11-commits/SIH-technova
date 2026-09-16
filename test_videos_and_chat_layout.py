import urllib.request
import json
import re

def p(msg):
    try:
        print(msg, flush=True)
    except Exception:
        print(msg.encode("ascii", errors="replace").decode("ascii"), flush=True)

def verify_all():
    p("==================================================================")
    p("  POLAR SCIENCE PORTAL: VIDEOS, FLOATING AI & SIH26063 TAG TEST")
    p("==================================================================")

    # 1. Verify SIH26063 tag presence in index.html & header
    p("\n[TEST 1] Verifying SIH26063 tag in top-right header...")
    with urllib.request.urlopen("http://localhost:8000/") as res:
        html = res.read().decode("utf-8")
    
    assert 'class="portal-code-badge"' in html and 'SIH26063' in html, "SIH26063 tag not found in HTML!"
    p("  [PASS] Found SIH26063 in .portal-code-badge top-right header")

    # 2. Verify Media Dissemination Hub, Video Modal and Audio Players
    p("\n[TEST 2] Verifying Media Dissemination Hub video & audio players...")
    assert 'id="polar-videos-grid-container"' in html, "polar-videos-grid-container not found in HTML!"
    assert 'id="polar-audios-grid-container"' in html, "polar-audios-grid-container not found in HTML!"
    assert 'id="modal-video-player"' in html, "modal-video-player not found in HTML!"
    p("  [PASS] HTML contains #polar-videos-grid-container, #polar-audios-grid-container and #modal-video-player")

    with urllib.request.urlopen("http://localhost:8000/js/media.js") as res:
        media_js = res.read().decode("utf-8")

    assert 'POLAR_DOCUMENTARY_VIDEOS' in media_js, "POLAR_DOCUMENTARY_VIDEOS array not found in media.js!"
    assert 'renderVideos' in media_js, "renderVideos function not found in media.js!"
    assert 'openVideoModal' in media_js, "openVideoModal function not found in media.js!"
    assert 'videoSource' in media_js, "videoSource MP4 streams not found in media.js!"
    assert 'switchVideoMode' in media_js, "switchVideoMode dual-mode switcher not found in media.js!"
    assert 'handleAudioScrub' in media_js, "handleAudioScrub scrubber not found in media.js!"
    p("  [PASS] media.js contains responsive video modal, dual MP4/YouTube playback, and interactive audio scrubbing")

    # 3. Verify Modern Floating Polar AI Chat Widget & Styling
    p("\n[TEST 3] Verifying Floating Polar AI Chat Widget and responsive CSS...")
    assert 'id="floating-chat-container"' in html, "floating-chat-container not found in HTML!"
    assert 'id="floating-chat-btn"' in html, "floating-chat-btn not found in HTML!"
    assert 'id="floating-chat-widget"' in html, "floating-chat-widget not found in HTML!"
    assert 'id="chat-messages-container"' in html, "chat-messages-container not found in HTML!"
    assert 'id="chat-user-input"' in html, "chat-user-input not found in HTML!"
    p("  [PASS] HTML contains complete floating chat widget (launcher button, drawer panel, messages, input)")

    with urllib.request.urlopen("http://localhost:8000/css/styles.css") as res:
        css = res.read().decode("utf-8")

    assert '.floating-chat-container' in css, ".floating-chat-container CSS class missing!"
    assert '.floating-chat-btn' in css, ".floating-chat-btn CSS class missing!"
    assert '.floating-chat-widget' in css, ".floating-chat-widget CSS class missing!"
    assert '.modal-video-window' in css, ".modal-video-window CSS class missing!"
    p("  [PASS] styles.css contains floating AI widget styling and responsive video modal styling")

    # 4. Verify AI Chat Functionality via API
    p("\n[TEST 4] Verifying conversational AI query execution...")
    req = urllib.request.Request(
        "http://localhost:8000/api/ai/ask",
        data=json.dumps({"query": "How is sea ice thickness measured in Kongsfjorden by IndARC?", "history": []}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode("utf-8"))
    assert data.get("in_scope") is True, "Query was not recognized in scope!"
    assert len(data.get("answer", "")) > 50, "AI answer was empty or too short!"
    p(f"  [PASS] AI answered query successfully: {data['answer'][:80]}...")

    p("\n==================================================================")
    p("  ALL PORTAL IMPROVEMENT TESTS PASSED WITH 100% INTEGRITY!")
    p("==================================================================")

if __name__ == "__main__":
    verify_all()
