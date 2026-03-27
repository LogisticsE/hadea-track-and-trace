from flask import Flask, jsonify, request, redirect, url_for, session
from flask_cors import CORS
from functools import wraps
import requests
import msal
import os

app = Flask(__name__)
# Must be a fixed value on Vercel — set SECRET_KEY as an environment variable
app.secret_key = os.environ.get('SECRET_KEY', 'change-me-before-deploying')
CORS(app)

# --- Auth ---
USERS = {
    os.environ.get('APP_USERNAME', 'admin'): os.environ.get('APP_PASSWORD', 'admin')
}

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# Configuration — override via Vercel environment variables
CONFIG = {
    'client_id':     os.environ.get('PBI_CLIENT_ID',     'bf4e6c9c-2fe5-4eb2-9e05-2785f8c2c42a'),
    'client_secret': os.environ.get('PBI_CLIENT_SECRET', ''),   # REQUIRED: set in Vercel dashboard
    'tenant_id':     os.environ.get('PBI_TENANT_ID',     'c94e2732-29d6-41d6-89d9-08c9798a6601'),
    'workspace_id':  os.environ.get('PBI_WORKSPACE_ID',  '7e8075a9-3b1f-430a-827e-b7f65d591c69'),
    'report_id':     os.environ.get('PBI_REPORT_ID',     '6d7bf2e6-e8b1-4d92-814d-1120d38053fb'),
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if USERS.get(username) == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        error = 'Invalid username or password.'
    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HaDEA – Track-and-Trace</title>
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to bottom right, #0f1b2d, #1a3552);
            color: white;
            overflow: hidden;
            position: relative;
        }}
        .blob {{
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
        }}
        .blob-1 {{
            top: -15%; left: -10%;
            width: 50%; height: 60%;
            background: rgba(0, 120, 212, 0.10);
            filter: blur(120px);
        }}
        .blob-2 {{
            bottom: -15%; right: -10%;
            width: 40%; height: 50%;
            background: rgba(6, 182, 212, 0.05);
            filter: blur(100px);
        }}
        .card {{
            position: relative;
            z-index: 10;
            width: 100%;
            max-width: 420px;
            margin: 0 20px;
            padding: 48px 40px;
            border-radius: 16px;
            background: rgba(255,255,255,0.02);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255,255,255,0.12);
            box-shadow: 0 16px 40px -12px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 9999px;
            background: rgba(0, 120, 212, 0.15);
            border: 1px solid rgba(0, 120, 212, 0.30);
            color: #0078d4;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            box-shadow: 0 0 15px rgba(0,120,212,0.15);
            margin-bottom: 20px;
        }}
        h1 {{
            color: white;
            font-size: 28px;
            font-weight: 600;
            letter-spacing: -0.02em;
            margin-bottom: 6px;
        }}
        .subtitle {{
            color: #9ca3af;
            font-size: 13px;
            font-weight: 500;
            letter-spacing: 0.04em;
            margin-bottom: 32px;
        }}
        form {{ width: 100%; display: flex; flex-direction: column; gap: 20px; }}
        .field {{ display: flex; flex-direction: column; gap: 6px; }}
        label {{
            color: #d1d5db;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-left: 4px;
        }}
        .input-wrap {{
            position: relative;
            display: flex;
            align-items: center;
        }}
        .input-icon {{
            position: absolute;
            left: 14px;
            pointer-events: none;
            color: #6b7280;
            transition: color 0.2s;
        }}
        input[type="text"], input[type="password"] {{
            width: 100%;
            border-radius: 8px;
            padding: 10px 16px 10px 44px;
            font-size: 14px;
            color: white;
            background: rgba(0,0,0,0.25);
            border: 1px solid rgba(255,255,255,0.10);
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
            outline: none;
            transition: border 0.2s, background 0.2s;
            font-family: inherit;
        }}
        input[type="text"]::placeholder,
        input[type="password"]::placeholder {{ color: #6b7280; }}
        input[type="text"]:focus,
        input[type="password"]:focus {{
            border-color: #0078d4;
            background: rgba(0,0,0,0.40);
        }}
        input:-webkit-autofill,
        input:-webkit-autofill:hover,
        input:-webkit-autofill:focus {{
            -webkit-box-shadow: 0 0 0 30px #111a28 inset !important;
            -webkit-text-fill-color: white !important;
            transition: background-color 5000s ease-in-out 0s;
        }}
        .pw-label-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-left: 4px;
        }}
        .toggle-pw {{
            position: absolute;
            right: 12px;
            background: none;
            border: none;
            color: #6b7280;
            cursor: pointer;
            padding: 4px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: color 0.2s, background 0.2s;
        }}
        .toggle-pw:hover {{ color: #d1d5db; background: rgba(255,255,255,0.05); }}
        .error-msg {{
            background: rgba(220,53,69,0.15);
            border: 1px solid rgba(220,53,69,0.40);
            color: #ff8080;
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 13px;
            text-align: center;
        }}
        .submit-btn {{
            width: 100%;
            margin-top: 16px;
            padding: 10px;
            background: linear-gradient(to right, #0078d4, #005a9e);
            color: white;
            border: 1px solid #005a9e;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 4px 14px rgba(0,120,212,0.39);
            transition: box-shadow 0.2s, transform 0.1s, background 0.2s;
            font-family: inherit;
        }}
        .submit-btn:hover {{
            box-shadow: 0 6px 20px rgba(0,120,212,0.5);
            transform: translateY(-1px);
            background: linear-gradient(to right, #0078d4, #004c87);
        }}
        .submit-btn:active {{ transform: translateY(0); }}
        .page-footer {{
            position: absolute;
            bottom: 24px;
            width: 100%;
            text-align: center;
            z-index: 10;
            font-size: 10px;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            font-weight: 500;
            color: rgba(255,255,255,0.28);
        }}
    </style>
</head>
<body>
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>

    <main class="card">
        <header style="display:flex;flex-direction:column;align-items:center;width:100%;">
            <div class="badge">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="#0078d4" viewBox="0 0 256 256">
                    <path d="M208,40H48A16,16,0,0,0,32,56V200a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V56A16,16,0,0,0,208,40Zm0,160H48V56H208V200ZM82.34,141.66a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35a8,8,0,0,1,11.32,11.32l-56,56a8,8,0,0,1-11.32,0Z"/>
                </svg>
                HaDEA
            </div>
            <h1>Track-and-Trace</h1>
            <p class="subtitle">Power BI Monitoring Dashboard</p>
        </header>

        {"<div class='error-msg'>" + error + "</div>" if error else ""}

        <form method="POST" style="width:100%;">
            <div class="field">
                <label for="username">Username</label>
                <div class="input-wrap">
                    <svg class="input-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 256 256">
                        <path d="M230.93,220a8,8,0,0,1-6.93,4H32a8,8,0,0,1-6.92-12c15.23-26.33,38.7-45.21,66.09-54.16a72,72,0,1,1,73.66,0c27.39,8.95,50.86,27.83,66.09,54.16A8,8,0,0,1,230.93,220Z"/>
                    </svg>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        placeholder="admin"
                        autocomplete="username"
                        required
                        onfocus="this.previousElementSibling.style.color='#0078d4'"
                        onblur="if(!this.value)this.previousElementSibling.style.color='#6b7280'"
                        oninput="this.previousElementSibling.style.color=this.value?'#0078d4':'#6b7280'"
                    >
                </div>
            </div>

            <div class="field">
                <div class="pw-label-row">
                    <label for="password">Password</label>
                </div>
                <div class="input-wrap">
                    <svg class="input-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 256 256">
                        <path d="M208,80H176V56a48,48,0,0,0-96,0V80H48A16,16,0,0,0,32,96V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V96A16,16,0,0,0,208,80ZM96,56a32,32,0,0,1,64,0V80H96ZM208,208H48V96H208V208Zm-68-56a12,12,0,1,1-12-12A12,12,0,0,1,140,152Z"/>
                    </svg>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        placeholder="&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;"
                        autocomplete="current-password"
                        required
                        style="padding-right:44px;"
                        onfocus="this.previousElementSibling.style.color='#0078d4'"
                        onblur="if(!this.value)this.previousElementSibling.style.color='#6b7280'"
                        oninput="this.previousElementSibling.style.color=this.value?'#0078d4':'#6b7280'"
                    >
                    <button type="button" class="toggle-pw" onclick="togglePw()" id="toggle-pw-btn" title="Show/hide password">
                        <svg id="eye-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 256 256">
                            <path d="M247.31,124.76c-.35-.79-8.82-19.58-27.65-38.41C194.57,61.26,162.88,48,128,48S61.43,61.26,36.34,86.35C17.51,105.18,9,124,8.69,124.76a8,8,0,0,0,0,6.5c.35.79,8.82,19.57,27.65,38.4C61.43,194.74,93.12,208,128,208s66.57-13.26,91.66-38.34c18.83-18.83,27.3-37.61,27.65-38.4A8,8,0,0,0,247.31,124.76ZM128,192c-30.78,0-57.67-11.19-80-33.22a133.47,133.47,0,0,1-23-30.78,133.33,133.33,0,0,1,23-30.78C70.33,75.19,97.22,64,128,64s57.67,11.19,80,33.22a133.46,133.46,0,0,1,23,30.78A133.33,133.33,0,0,1,208,158.78C185.67,180.81,158.78,192,128,192Zm0-112a48,48,0,1,0,48,48A48.05,48.05,0,0,0,128,80Zm0,80a32,32,0,1,1,32-32A32,32,0,0,1,128,160Z"/>
                        </svg>
                    </button>
                </div>
            </div>

            <button type="submit" class="submit-btn">
                Sign In
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 256 256">
                    <path d="M221.66,133.66l-72,72a8,8,0,0,1-11.32-11.32L196.69,136H40a8,8,0,0,1,0-16H196.69L138.34,61.66a8,8,0,0,1,11.32-11.32l72,72A8,8,0,0,1,221.66,133.66Z"/>
                </svg>
            </button>
        </form>
    </main>

    <footer class="page-footer">2026 &copy; Eurofins Analytico BV</footer>

    <script>
        function togglePw() {{
            const pw = document.getElementById('password');
            const icon = document.getElementById('eye-icon');
            if (pw.type === 'password') {{
                pw.type = 'text';
                icon.innerHTML = '<path d="M53.92,34.62A8,8,0,1,0,42.08,45.38L61.32,66.55C25,88.84,9.38,123.2,8.69,124.76a8,8,0,0,0,0,6.5c.35.79,8.82,19.57,27.65,38.4C61.43,194.74,93.12,208,128,208a127.11,127.11,0,0,0,52.07-10.83l22,24.21a8,8,0,1,0,11.84-10.76Zm47.33,75.84,41.67,45.85a32,32,0,0,1-41.67-45.85ZM128,192c-30.78,0-57.67-11.19-80-33.22A133.16,133.16,0,0,1,25.28,128c4.69-8.79,19.66-33.37,47.35-49.38l18,19.75a48,48,0,0,0,63.66,70l14.73,16.2A112,112,0,0,1,128,192Zm6-95.43a8,8,0,0,1,3-15.72,48.16,48.16,0,0,1,38.77,42.64,8,8,0,0,1-7.22,8.71,6.39,6.39,0,0,1-.76,0,8,8,0,0,1-8-7.26A32.09,32.09,0,0,0,134,96.57Zm113.28,34.69c-.42.94-10.55,23.37-33.36,43.8a8,8,0,1,1-10.67-11.91A132.77,132.77,0,0,0,230.57,128a133.15,133.15,0,0,0-22.7-30.77C185.67,75.19,158.78,64,128,64a118.37,118.37,0,0,0-19.36,1.57A8,8,0,0,1,106.1,49.85,134,134,0,0,1,128,48c34.88,0,66.57,13.26,91.66,38.35,18.83,18.83,27.3,37.62,27.65,38.41A8,8,0,0,1,247.31,131.26Z"/>';
            }} else {{
                pw.type = 'password';
                icon.innerHTML = '<path d="M247.31,124.76c-.35-.79-8.82-19.58-27.65-38.41C194.57,61.26,162.88,48,128,48S61.43,61.26,36.34,86.35C17.51,105.18,9,124,8.69,124.76a8,8,0,0,0,0,6.5c.35.79,8.82,19.57,27.65,38.4C61.43,194.74,93.12,208,128,208s66.57-13.26,91.66-38.34c18.83-18.83,27.3-37.61,27.65-38.4A8,8,0,0,0,247.31,124.76ZM128,192c-30.78,0-57.67-11.19-80-33.22a133.47,133.47,0,0,1-23-30.78,133.33,133.33,0,0,1,23-30.78C70.33,75.19,97.22,64,128,64s57.67,11.19,80,33.22a133.46,133.46,0,0,1,23,30.78A133.33,133.33,0,0,1,208,158.78C185.67,180.81,158.78,192,128,192Zm0-112a48,48,0,1,0,48,48A48.05,48.05,0,0,0,128,80Zm0,80a32,32,0,1,1,32-32A32,32,0,0,1,128,160Z"/>';
            }}
        }}
    </script>
</body>
</html>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Track-and-Trace – Power BI</title>
    <script src="https://cdn.jsdelivr.net/npm/powerbi-client@2.21.0/dist/powerbi.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        .report-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .report-wrapper {
            width: 100%;
            max-width: 1140px;
        }
        .report-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        #reportContainer {
            width: 100%;
            height: 80vh;
            border: none;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            border-radius: 8px;
            background: white;
        }
        .loading {
            text-align: center;
            padding: 50px;
            color: #666;
        }
        .error {
            text-align: center;
            padding: 50px;
            color: #d32f2f;
        }
        @media (max-width: 768px) {
            #reportContainer { height: 70vh; }
        }
    </style>
</head>
<body>
    <div class="report-container">
        <div class="report-wrapper">
            <div class="report-header">
                <h3>Power BI Report</h3>
                <a href="/logout" style="font-size:13px;color:#666;text-decoration:none;border:1px solid #ccc;padding:6px 14px;border-radius:6px;">Sign out</a>
            </div>
            <div id="reportContainer">
                <div class="loading">Loading report...</div>
            </div>
        </div>
    </div>

    <script>
        async function embedReport() {
            try {
                const response = await fetch('/api/embed-info');
                const embedInfo = await response.json();

                if (embedInfo.error) throw new Error(embedInfo.error);

                if (typeof powerbi === 'undefined') throw new Error('Power BI library not loaded');

                const models = window['powerbi-client'].models;
                const config = {
                    type: 'report',
                    tokenType: models.TokenType.Embed,
                    accessToken: embedInfo.embedToken,
                    embedUrl: embedInfo.embedUrl,
                    id: embedInfo.reportId,
                    permissions: models.Permissions.Read,
                    settings: {
                        panes: { filters: { expanded: false, visible: false } },
                        background: models.BackgroundType.Transparent
                    }
                };

                const reportContainer = document.getElementById('reportContainer');
                const report = powerbi.embed(reportContainer, config);

                report.on('loaded', () => console.log('Report loaded successfully!'));
                report.on('error', (event) => {
                    console.error('Report error:', event.detail);
                    reportContainer.innerHTML = '<div class="error">Error loading report. Check console for details.</div>';
                });

            } catch (error) {
                console.error('Error embedding report:', error);
                document.getElementById('reportContainer').innerHTML =
                    `<div class="error">Failed to load report: ${error.message}</div>`;
            }
        }

        document.addEventListener('DOMContentLoaded', embedReport);
    </script>
</body>
</html>
    '''

@app.route('/api/embed-info')
@login_required
def get_embed_info():
    try:
        authority = f"https://login.microsoftonline.com/{CONFIG['tenant_id']}"
        scope = ['https://analysis.windows.net/powerbi/api/.default']

        app_msal = msal.ConfidentialClientApplication(
            CONFIG['client_id'],
            authority=authority,
            client_credential=CONFIG['client_secret']
        )

        result = app_msal.acquire_token_for_client(scopes=scope)

        if 'access_token' not in result:
            error_msg = result.get('error_description', 'Unknown error acquiring token')
            return jsonify({'error': f'Failed to get access token: {error_msg}'}), 500

        access_token = result['access_token']

        embed_url = (
            f"https://api.powerbi.com/v1.0/myorg/groups/{CONFIG['workspace_id']}"
            f"/reports/{CONFIG['report_id']}/GenerateToken"
        )

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        body = {'accessLevel': 'View', 'allowSaveAs': False}

        response = requests.post(embed_url, json=body, headers=headers)

        if response.status_code != 200:
            return jsonify({'error': f'Failed to generate embed token: {response.text}'}), response.status_code

        embed_data = response.json()

        return jsonify({
            'embedToken': embed_data['token'],
            'embedUrl': embed_data.get(
                'embedUrl',
                f"https://app.powerbi.com/reportEmbed?reportId={CONFIG['report_id']}&groupId={CONFIG['workspace_id']}"
            ),
            'reportId': CONFIG['report_id'],
            'expiresAt': embed_data.get('expiration')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
