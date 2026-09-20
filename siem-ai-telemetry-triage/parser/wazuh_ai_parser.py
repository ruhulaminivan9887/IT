import json
import time
import urllib.request
import urllib.error

LOG_PATH = "/var/ossec/logs/alerts/alerts.json"
AI_API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = "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"

def analyze_with_ai(level, description):
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system", 
                "content": "You are a senior SOC analyst. Provide a concise 2-sentence threat assessment and a recommended remediation step for this Windows security event."
            },
            {
                "role": "user", 
                "content": f"Wazuh Alert Level {level}: {description}"
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        req = urllib.request.Request(
            AI_API_URL, 
            data=json.dumps(payload).encode('utf-8'), 
            headers=headers, 
            method="POST"
        )
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            ai_reply = res_data["choices"][0]["message"]["content"]
            return f"\n--- [AI THREAT TRIAGE REPORT] ---\n{ai_reply}\n---------------------------------"
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        return f"[AI API ERROR] HTTP {e.code}: {error_body}"
    except Exception as e:
        return f"[AI ERROR] Failed to connect to provider: {e}"

def monitor_windows_logs():
    print("[*] Listening for live Windows Server security logs with active OpenAI LLM integration...")
    try:
        with open(LOG_PATH, "r") as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                try:
                    alert = json.loads(line)
                    if alert.get("agent", {}).get("name") == "Windows-Server":
                        rule = alert.get("rule", {})
                        level = rule.get("level", 0)
                        desc = rule.get("description", "No description")
                        
                        print(f"\n[RAW ALERT] Level: {level} | {desc}")
                        ai_insight = analyze_with_ai(level, desc)
                        print(ai_insight)
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"[!] Error: Could not find {LOG_PATH}")

if __name__ == "__main__":
    monitor_windows_logs()
