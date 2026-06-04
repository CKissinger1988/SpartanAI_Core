import os
from playwright.sync_api import sync_playwright

def capture_preview():
    # 1. Create a temporary HTML file to preview the Login Portal aesthetic
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>SPARTAN_APEX PREVIEW</title>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 0;
                background: #000;
                color: #06b6d4;
                font-family: 'Orbitron', sans-serif;
                overflow: hidden;
                width: 3840px;
                height: 2160px;
            }
            .bg {
                position: fixed;
                inset: 0;
                background: url('login_bg.jpg') center/cover no-repeat;
                filter: brightness(0.6) blur(1px);
            }
            .overlay {
                position: fixed;
                inset: 0;
                background: radial-gradient(circle at center, transparent 0%, rgba(0,0,0,0.4) 100%);
                z-index: 1;
            }
            .grid {
                position: fixed;
                inset: 0;
                background-image: 
                    linear-gradient(to right, rgba(6, 182, 212, 0.1) 1px, transparent 1px),
                    linear-gradient(to bottom, rgba(6, 182, 212, 0.1) 1px, transparent 1px);
                background-size: 80px 80px;
                z-index: 2;
                opacity: 0.3;
            }
            .hud-panel {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) perspective(2000px) rotateX(5deg);
                width: 1200px;
                padding: 100px;
                background: rgba(0,0,0,0.6);
                backdrop-filter: blur(40px);
                border: 4px solid rgba(6, 182, 212, 0.4);
                box-shadow: 0 0 100px rgba(6, 182, 212, 0.2);
                text-align: center;
                z-index: 10;
            }
            h1 {
                font-size: 120px;
                font-weight: 900;
                letter-spacing: 0.5em;
                color: #fff;
                text-shadow: 0 0 50px #06b6d4;
                margin-bottom: 20px;
            }
            .sub {
                font-size: 30px;
                letter-spacing: 1em;
                color: rgba(6, 182, 212, 0.6);
                text-transform: uppercase;
            }
            .scan-line {
                position: fixed;
                top: 0; left: 0; width: 100%; height: 4px;
                background: rgba(6, 182, 212, 0.2);
                box-shadow: 0 0 20px #06b6d4;
                z-index: 100;
            }
        </style>
    </head>
    <body>
        <div class="bg"></div>
        <div class="overlay"></div>
        <div class="grid"></div>
        <div class="scan-line" style="top: 30%"></div>
        <div class="hud-panel">
            <h1>SPARTANAI</h1>
            <div class="sub">Neural_Uplink_v50.5</div>
            <div style="margin-top: 100px; color: #06b6d4; font-size: 20px; opacity: 0.8;">
                [ STATUS: OMNIPOTENT_SYNC_ACTIVE ]
            </div>
        </div>
    </body>
    </html>
    """
    
    # Path to the login_bg.jpg (it's in web_portal/public/)
    bg_path = os.path.abspath('web_portal/public/login_bg.jpg')
    html_content = html_content.replace('login_bg.jpg', bg_path.replace('\\', '/'))
    
    with open('temp_preview.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("[PREVIEW]: Rendering 4K Holographic Interface...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 3840, 'height': 2160})
        page = context.new_page()
        page.goto(f"file:///{os.path.abspath('temp_preview.html').replace('\\', '/')}")
        page.wait_for_timeout(2000) # Wait for fonts/styles
        page.screenshot(path='APEX_LOGIN_PREVIEW.png', full_page=True)
        browser.close()
    
    os.remove('temp_preview.html')
    print("[SUCCESS]: High-fidelity preview generated at APEX_LOGIN_PREVIEW.png")

if __name__ == "__main__":
    capture_preview()

