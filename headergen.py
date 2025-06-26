import requests
import random
import time
import base64
import json
import re

def get_latest_chrome_version():
    try:
        response = requests.get("https://www.whatismybrowser.com/guides/the-latest-version/chrome")
        response.raise_for_status()
        match = re.search(r"Chrome/(\d+\.\d+\.\d+\.\d+)", response.text)
        if match:
            return match.group(1)
    except requests.exceptions.RequestException:
        pass
    return "123.0.0.0"

def get_latest_discord_build_number():
    try:
        response = requests.get("https://discord.com/app")
        response.raise_for_status()
        match = re.search(r'build_number:\"(\d+)\"', response.text)
        if match:
            return match.group(1)
    except requests.exceptions.RequestException:
        pass
    return "288923"

def generate_discord_headers(token="token"):
    chrome_version = get_latest_chrome_version()
    build_num = get_latest_discord_build_number()

    os_list = ["Windows", "Mac OS X", "Linux"]
    os_name = random.choice(os_list)

    if os_name == "Windows":
        os_ver = random.choice(["10", "11"])
        ua_os_string = f"Windows NT {os_ver}.0; Win64; x64"
    elif os_name == "Mac OS X":
        os_ver = f"10_{random.randint(13, 15)}_{random.randint(0, 9)}"
        ua_os_string = f"Macintosh; Intel Mac OS X {os_ver.replace('_', '.')}"
    else:
        os_ver = ""
        ua_os_string = "X11; Linux x86_64"

    locales = {"en-US": "en-US,en;q=0.9", "en-GB": "en-GB,en;q=0.9", "es-ES": "es-ES,es;q=0.9", "fr-FR": "fr-FR,fr;q=0.9"}
    system_locale = random.choice(list(locales.keys()))
    accept_language = locales[system_locale]

    user_agent = f"Mozilla/5.0 ({ua_os_string}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/{chrome_version}"

    properties = {
        "os": os_name,
        "browser": "Chrome",
        "device": "",
        "system_locale": system_locale,
        "browser_user_agent": user_agent,
        "browser_version": chrome_version,
        "os_version": os_ver,
        "referrer": "",
        "referring_domain": "",
        "referrer_current": "",
        "referring_domain_current": "",
        "release_channel": "stable",
        "client_build_number": int(build_num),
        "client_event_source": None,
        "design_id": 0
    }
    super_properties = base64.b64encode(json.dumps(properties).encode()).decode()

    return {
        "accept": "*/*",
        "accept-language": accept_language,
        "authorization": token,
        "cache-control": "no-cache",
        "connection": "keep-alive",
        "content-type": "application/json",
        "origin": "https://discord.com",
        "pragma": "no-cache",
        "referer": "https://discord.com/channels/@me",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": user_agent,
        "x-super-properties": super_properties,
        "x-discord-locale": system_locale,
        "x-debug-options": "bugReporterEnabled"
    }

if __name__ == "__main__":
    headers = generate_discord_headers()
    print("headers = {")
    for key, value in headers.items():
        print(f"    '{key}': '{value}',")
    print("}")
    time.sleep(999999)


