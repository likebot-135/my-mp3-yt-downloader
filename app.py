from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Main UI Page - YTMP3.GG Clone Style
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Download Long YouTube Videos</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            body { background-color: #f4f7f6; padding: 20px; display: flex; flex-direction: column; align-items: center; }
            
            .header-banner { background-color: #1a73e8; color: white; width: 100%; max-width: 480px; padding: 15px; text-align: center; border-radius: 8px 8px 0 0; font-size: 14px; font-weight: bold; }
            
            .main-box { background: white; width: 100%; max-width: 480px; padding: 25px; border-radius: 0 0 8px 8px; box-shadow: 0px 4px 12px rgba(0,0,0,0.08); text-align: center; border: 1px solid #e0e0e0; }
            
            h2 { color: #1a365d; font-size: 18px; margin-bottom: 20px; font-weight: 600; }
            
            .input-group { position: relative; margin-bottom: 15px; }
            input[type="text"] { width: 100%; padding: 12px 40px 12px 12px; border: 1px solid #ccd0d5; border-radius: 6px; font-size: 14px; outline: none; }
            
            .format-selector { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
            select { padding: 8px; border-radius: 6px; border: 1px solid #ccd0d5; width: 65%; font-size: 14px; }
            
            .toggle-buttons { display: flex; gap: 8px; }
            .toggle-btn { padding: 8px 15px; border: 1px solid #ccc; border-radius: 20px; background: #f0f2f5; cursor: pointer; font-weight: bold; font-size: 12px; }
            .toggle-btn.active { background: #000; color: white; border-color: #000; }
            
            .download-btn { width: 100%; padding: 12px; background: #1a202c; color: white; border: none; border-radius: 25px; font-size: 14px; font-weight: bold; cursor: pointer; margin-bottom: 15px; }
            
            .disclaimer-box { display: flex; align-items: flex-start; text-align: left; font-size: 12px; color: #4a5568; line-height: 1.4; margin-bottom: 15px; background: #f8fafc; padding: 10px; border-radius: 6px; }
            .disclaimer-box input { margin-right: 8px; margin-top: 3px; }
            
            .result-zone { margin-top: 15px; font-size: 14px; }
            .dl-link { display: inline-block; margin-top: 10px; padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; }
            
            .footer-links { width: 100%; max-width: 480px; margin-top: 15px; }
            .footer-item { background: white; padding: 12px; margin-bottom: 8px; border-radius: 6px; text-align: left; font-size: 13px; color: #1a73e8; border: 1px solid #e0e0e0; display: flex; align-items: center; cursor: pointer; font-weight: 500; }
        </style>
    </head>
    <body>

        <div class="header-banner">
            YTMP3 - Long YouTube Video Downloader
        </div>

        <div class="main-box">
            <h2>Download Long YouTube Videos Without Time Limits</h2>
            
            <div class="input-group">
                <input type="text" id="videoUrl" placeholder="Paste URL here...">
            </div>

            <div class="format-selector">
                <select id="qualitySelect">
                    <option value="1080">MP4 - 1080P</option>
                    <option value="720">MP4 - 720P</option>
                    <option value="360">MP4 - 360P</option>
                    <option value="mp3">MP3 - Best Quality</option>
                </select>
                
                <div class="toggle-buttons">
                    <button class="toggle-btn" id="btnMp3" onclick="setFormat('mp3')">MP3</button>
                    <button class="toggle-btn active" id="btnMp4" onclick="setFormat('mp4')">MP4</button>
                </div>
            </div>

            <div class="disclaimer-box">
                <input type="checkbox" id="agreeCheck" checked>
                <label for="agreeCheck">I confirm that I have read and agree to the standards in the Copyright Disclaimer and will not download copyrighted content.</label>
            </div>

            <button class="download-btn" onclick="startDownload()">Download</button>

            <div class="result-zone" id="statusOutput"></div>
        </div>

        <div class="footer-links">
            <div class="footer-item">🎵 Convert Playlists now</div>
            <div class="footer-item">📦 All Video Downloader</div>
            <div class="footer-item">🎧 Best Quality MP3</div>
        </div>

        <script>
            let currentFormat = 'mp4';

            function setFormat(fmt) {
                currentFormat = fmt;
                document.getElementById('btnMp3').classList.toggle('active', fmt === 'mp3');
                document.getElementById('btnMp4').classList.toggle('active', fmt === 'mp4');
                
                const qSelect = document.getElementById('qualitySelect');
                if(fmt === 'mp3') {
                    qSelect.value = 'mp3';
                } else {
                    qSelect.value = '1080';
                }
            }

            async function startDownload() {
                const url = document.getElementById('videoUrl').value;
                const checkbox = document.getElementById('agreeCheck').checked;
                const quality = document.getElementById('qualitySelect').value;
                const statusOutput = document.getElementById('statusOutput');

                if (!url) { alert('कृपया यूट्यूब लिंक पेस्ट करें!'); return; }
                if (!checkbox) { alert('आगे बढ़ने के लिए आपको नियम स्वीकार करने होंगे.'); return; }

                statusOutput.innerHTML = '<p style="color:#1a73e8;">Processing video... Please wait...</p>';

                try {
                    const response = await fetch('/download', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ url: url, format: currentFormat, quality: quality })
                    });
                    const data = await response.json();
                    
                    if(data.success) {
                        statusOutput.innerHTML = `<p style="color:green; font-weight:bold;">सफलतापूर्वक लिंक जनरेट हो गया!</p><a class="dl-link" href="${data.download_url}" target="_blank" download>Click to Save File</a>`;
                    } else {
                        statusOutput.innerHTML = `<p style="color:red;">त्रुटि: ${data.message}</p>`;
                    }
                } catch (err) {
                    statusOutput.innerHTML = '<p style="color:red;">सर्वर रिस्पॉन्स नहीं दे रहा है.</p>';
                }
            }
        </script>
    </body>
    </html>
    '''

# Backend Processing Node
@app.route('/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url')
    fmt = data.get('format', 'mp4')
    quality = data.get('quality', '720')
    
    if not video_url:
        return jsonify({'success': False, 'message': 'No URL found'})
        
    try:
        # High speed scraping server request (Cobalt API integration)
        api_url = "https://cobalt.tools"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        
        payload = {
            "url": video_url,
            "vQuality": quality,
            "isAudioOnly": True if fmt == 'mp3' else False
        }
        
        res = requests.post(api_url, json=payload, headers=headers)
        res_data = res.json()
        
        if res.status_code == 200 and 'url' in res_data:
            return jsonify({
                'success': True,
                'download_url': res_data.get('url')
            })
        else:
            return jsonify({'success': False, 'message': 'Video conversion failed. Try another link.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
	
