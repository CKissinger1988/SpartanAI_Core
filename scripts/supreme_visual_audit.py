import os
import time
from playwright.sync_api import sync_playwright

def supreme_visual_audit():
    panels = {
        "LOGIN": {
            "title": "SPARTANAI_LOGIN_v50.5",
            "content": """
                <div class="hud-panel" style="width: 1400px; height: 1800px;">
                    <h1>SPARTANAI</h1>
                    <div class="sub">Neural_Uplink_v50.5</div>
                    <div style="margin-top: 100px; border: 2px solid rgba(6, 182, 212, 0.2); padding: 50px; background: rgba(0,0,0,0.4);">
                        <div style="font-size: 24px; color: #06b6d4; letter-spacing: 0.5em;">[ ACCESS_CRYPT_TOKEN ]</div>
                    </div>
                </div>
            """
        },
        "DASHBOARD": {
            "title": "SYNAPTIC_OVERWATCH_v50.5",
            "content": """
                <div class="hud-panel" style="width: 2500px; height: 1400px;">
                    <h1>SYNAPTIC_OVERWATCH</h1>
                    <div class="sub">Neural_Core_Status: ASCENDED</div>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 50px; margin-top: 100px;">
                        <div class="stat-card"><h3>Neural Stability</h3><div class="value">98.4%</div></div>
                        <div class="stat-card" style="border-color: #ef4444;"><h3>Red-Team Pressure</h3><div class="value" style="color: #ef4444;">42.0%</div></div>
                        <div class="stat-card"><h3>Synaptic Load</h3><div class="value">24.1%</div></div>
                    </div>
                </div>
            """
        },
        "FINANCE": {
            "title": "FINANCE_DOMINANCE_v50.5",
            "content": """
                <div class="hud-panel" style="width: 2500px; height: 1400px; border-color: #10b981;">
                    <h1 style="color: #10b981;">YIELD_DOMINANCE</h1>
                    <div class="sub">Sovereign_Wealth_Management</div>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 50px; margin-top: 100px;">
                        <div class="stat-card" style="border-color: #10b981;"><h3>BTC_RESERVE</h3><div class="value">0.082</div></div>
                        <div class="stat-card" style="border-color: #10b981;"><h3>XMR_RESERVE</h3><div class="value">1422.8</div></div>
                        <div class="stat-card" style="border-color: #10b981;"><h3>DAILY_YIELD</h3><div class="value">+12.4%</div></div>
                        <div class="stat-card" style="border-color: #10b981;"><h3>MINING_POWER</h3><div class="value">42.8 TH/s</div></div>
                    </div>
                </div>
            """
        },
        "GHOST_CHAT": {
            "title": "GHOST_LINK_v2",
            "content": """
                <div class="hud-panel" style="width: 1200px; height: 1400px; border-color: #06b6d4;">
                    <h1>GHOST_LINK</h1>
                    <div class="sub">Clandestine_Comms_Engaged</div>
                    <div style="margin-top: 100px; text-align: left; background: rgba(0,0,0,0.5); padding: 40px; font-family: monospace; font-size: 20px; line-height: 1.6;">
                        <span style="color: #06b6d4;">[11:22:04] JARVIS:</span> Secure clandestine channel established. Transmission encrypted with AES-256-GCM. Awaiting sovereign query...
                    </div>
                </div>
            """
        },
        "SETTINGS": {
            "title": "SUPREME_CONFIG_v50.5",
            "content": """
                <div class="hud-panel" style="width: 3200px; height: 1800px; border-color: #a855f7;">
                    <h1 style="color: #a855f7;">SUPREME_CONFIGURATION</h1>
                    <div class="sub">Level_10_Neural_Overrides</div>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 100px; margin-top: 100px; text-align: left;">
                        <div class="stat-card"><h3>Synapse Sensitivity</h3><div class="value">0.84</div></div>
                        <div class="stat-card"><h3>Grok Aggression</h3><div class="value">MAX_LETHAL</div></div>
                        <div class="stat-card"><h3>Shadow Tunneling</h3><div class="value">1.2ms</div></div>
                        <div class="stat-card"><h3>Vault Rotation</h3><div class="value">ACTIVE</div></div>
                    </div>
                </div>
            """
        },
        "AEGIS_BROWSER": {
            "title": "AEGIS_BROWSER_v2",
            "content": """
                <div class="hud-panel" style="width: 3000px; height: 1600px; border-color: #06b6d4;">
                    <h1>AEGIS_</h1>
                    <div class="sub">Clandestine_Neural_Audit</div>
                    <div style="margin-top: 100px; background: rgba(0,0,0,0.8); height: 800px; border: 1px solid #06b6d4; padding: 50px;">
                        <div style="font-family: monospace; font-size: 24px; text-align: left;">
                           <div style="color: #10b981;">[SUCCESS] Uplink established. Scanning target...</div>
                           <div style="color: #ef4444;">[ERROR] DETECTED: Logic mismatch in CryptoShard loop.</div>
                        </div>
                    </div>
                </div>
            """
        },
        "OFFENSIVE": {
            "title": "VOID_OFFENSIVE_CORE_X20",
            "content": """
                <div class="hud-panel" style="width: 3200px; height: 1800px; border-color: #ef4444;">
                    <h1 style="color: #ef4444;">DARK_CORE_OFFENSIVE</h1>
                    <div class="sub">Shadow_Cortex_Singularity</div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 50px; margin-top: 100px;">
                        <div class="stat-card"><h3>HEXSTRIKE_VOC</h3><div class="value">ACTIVE</div></div>
                        <div class="stat-card"><h3>WHISPER_PAIR</h3><div class="value">TUNNELING</div></div>
                        <div class="stat-card"><h3>SHODAN_DEEP</h3><div class="value">RECON</div></div>
                    </div>
                </div>
            """
        },
        "DEFENSIVE": {
            "title": "PRISM_DEFENSIVE_MATRIX_X20",
            "content": """
                <div class="hud-panel" style="width: 3200px; height: 1800px; border-color: #10b981;">
                    <h1 style="color: #10b981;">LIGHT_CORE_DEFENSIVE</h1>
                    <div class="sub">Prism_Postural_Integrity</div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 50px; margin-top: 100px;">
                        <div class="stat-card"><h3>SELF_HEALING</h3><div class="value">STABLE</div></div>
                        <div class="stat-card"><h3>SENTINEL_X</h3><div class="value">OMNIPOTENT</div></div>
                    </div>
                </div>
            """
        },
        "METASPLOIT": {
            "title": "APEX_MSF_CONSOLE",
            "content": """
                <div class="hud-panel" style="width: 3000px; height: 1800px; border-color: #ef4444;">
                    <h1>APEX_MSF_SHELL</h1>
                    <div class="sub">Tactical_Exploit_Library</div>
                    <div style="margin-top: 50px; background: #000; height: 1000px; border: 1px solid #ef4444; padding: 40px; font-family: monospace; font-size: 20px; text-align: left;">
                        <div style="color: #ef4444;">msf6 > use exploit/windows/smb/ms17_010_eternalblue</div>
                        <div style="color: #fff;">[*] No payload configured, defaulting to windows/x64/meterpreter/reverse_tcp</div>
                        <div style="color: #10b981;">[*] Exploit completed, but no session was created.</div>
                        <div style="color: #ef4444;">msf6 > set LHOST 0.0.0.0</div>
                    </div>
                </div>
            """
        },
        "IDS_TUNNEL": {
            "title": "IDS_REVERSE_TUNNEL_X20",
            "content": """
                <div class="hud-panel" style="width: 2400px; height: 1600px; border-color: #06b6d4;">
                    <h1>IDS_TUNNEL_MATRIX</h1>
                    <div class="sub">C2_Traffic_Overwatch</div>
                    <div style="margin-top: 100px; height: 800px; border: 2px dashed #06b6d4; display: flex; align-items: center; justify-content: center;">
                        <div style="font-size: 40px; color: #06b6d4; font-weight: 900;">[ MESH_TOPOLOGY_LIVE ]</div>
                    </div>
                </div>
            """
        },
        "RTL_NODE": {
            "title": "RTL_CRYPTO_NODE_v50",
            "content": """
                <div class="hud-panel" style="width: 3200px; height: 1800px; border-color: #f59e0b;">
                    <h1 style="color: #f59e0b;">RTL_LIGHTNING_NODE</h1>
                    <div class="sub">Ride_The_Lightning_Sync</div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 50px; margin-top: 100px;">
                        <div class="stat-card" style="border-color: #f59e0b;"><h3>Active_Channels</h3><div class="value">24</div></div>
                        <div class="stat-card" style="border-color: #f59e0b;"><h3>Total_Capacity</h3><div class="value">1.24 BTC</div></div>
                        <div class="stat-card" style="border-color: #f59e0b;"><h3>Routing_Fees</h3><div class="value">12.4s</div></div>
                    </div>
                </div>
            """
        }
    }

    base_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0; padding: 0; background: #000; color: #06b6d4; font-family: 'Orbitron', sans-serif;
                width: 3840px; height: 2160px; overflow: hidden;
            }
            .bg { position: fixed; inset: 0; background: url('bg.webp') center/cover no-repeat; filter: brightness(0.4) blur(2px); }
            .grid {
                position: fixed; inset: 0;
                background-image: linear-gradient(to right, rgba(6, 182, 212, 0.1) 1px, transparent 1px),
                                  linear-gradient(to bottom, rgba(6, 182, 212, 0.1) 1px, transparent 1px);
                background-size: 60px 60px; opacity: 0.2;
            }
            .hud-panel {
                position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%) perspective(2000px) rotateX(2deg);
                background: rgba(0,0,0,0.7); backdrop-filter: blur(50px);
                border: 2px solid rgba(6, 182, 212, 0.3); box-shadow: 0 0 100px rgba(6, 182, 212, 0.15);
                padding: 100px; text-align: center;
            }
            h1 { font-size: 100px; font-weight: 900; letter-spacing: 0.4em; color: #fff; text-shadow: 0 0 40px currentColor; margin: 0; }
            .sub { font-size: 24px; letter-spacing: 0.8em; color: rgba(255,255,255,0.4); text-transform: uppercase; margin-top: 20px; }
            .stat-card {
                border: 1px solid rgba(6, 182, 212, 0.2); background: rgba(0,0,0,0.4); padding: 40px;
                text-align: left;
            }
            .stat-card h3 { font-size: 18px; color: rgba(255,255,255,0.3); margin: 0; }
            .stat-card .value { font-size: 48px; font-weight: 900; color: #fff; margin-top: 10px; }
            .scan-line {
                position: fixed; top: 0; left: 0; width: 100%; height: 2px;
                background: rgba(6, 182, 212, 0.4); box-shadow: 0 0 15px #06b6d4; z-index: 1000;
            }
        </style>
    </head>
    <body>
        <div class="bg"></div>
        <div class="grid"></div>
        <div class="scan-line" style="top: 40%"></div>
        {{CONTENT}}
    </body>
    </html>
    """

    bg_path = os.path.abspath('web_portal/public/bg.webp')
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 3840, 'height': 2160})
        page = context.new_page()

        for name, data in panels.items():
            print(f"[AUDIT]: Rendering {name} Interface...")
            html = base_html.replace('{{CONTENT}}', data['content']).replace('bg.webp', bg_path.replace('\\', '/'))
            
            with open(f'temp_{name.lower()}.html', 'w', encoding='utf-8') as f:
                f.write(html)
            
            page.goto(f"file:///{os.path.abspath(f'temp_{name.lower()}.html').replace('\\', '/')}")
            page.wait_for_timeout(1500)
            page.screenshot(path=f'APEX_{name}_SCREENSHOT.png', full_page=True)
            os.remove(f'temp_{name.lower()}.html')
            print(f"[SUCCESS]: {name} capture saved.")

        browser.close()

if __name__ == "__main__":
    supreme_visual_audit()

