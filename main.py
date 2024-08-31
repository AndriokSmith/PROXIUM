import os
import random
import string
import subprocess
from datetime import datetime
import requests


public_ip = requests.get('https://ifconfig.me').text.strip()

uuid = subprocess.check_output(["xray", "uuid"]).decode().strip()

keys = subprocess.check_output(["xray", "x25519"]).decode().strip().split(" ")
private_key = keys[2].split('\n')[0]
print(f'Pricvate key: "{private_key}"')

public_key = keys[4]
print(f'Puclic  key: "{public_key}"')


short_id = ''.join(random.choices(string.hexdigits, k=4))


config = f'''
{{
  "log": {{
    "loglevel": "warning",
    "access": "./access.log"
  }},
  "routing": {{
    "domainStrategy": "IPIfNonMatch",
    "rules": [
      {{
        "inboundTag": [
          "api"
        ],
        "outboundTag": "api",
        "type": "field"
      }},
      {{
        "outboundTag": "blocked",
        "ip": [
          "geoip:private"
        ],
        "type": "field"
      }},
      {{
        "outboundTag": "blocked",
        "protocol": [
          "bittorrent"
        ],
        "type": "field"
      }}
    ]
  }},
  "dns": null,
  "inbounds": [
    {{
      "listen": "127.0.0.1",
      "port": 62789,
      "protocol": "dokodemo-door",
      "settings": {{
        "address": "127.0.0.1"
      }},
      "streamSettings": null,
      "tag": "api",
      "sniffing": null
    }},
    {{
      "listen": null,
      "port": 49649,
      "protocol": "vless",
      "settings": {{
        "clients": [
          {{
            "email": "lqawjan",
            "flow": "xtls-rprx-vision",
            "id": "{uuid}",
            "expire": 2592000 
          }}
        ],
        "decryption": "none",
        "fallbacks": []
      }},
      "streamSettings": {{
        "network": "tcp",
        "security": "reality",
        "tcpSettings": {{
          "acceptProxyProtocol": false,
          "header": {{
            "type": "none"
          }}
        }},
        "realitySettings": {{
          "show": false,
          "xver": 0,
          "fingerprint": "chrome",
          "dest": "tgju.org:443",
          "serverNames": [
            "tgju.org",
            "www.tgju.org"
          ],
          "privateKey": "{private_key}",
          "publicKey": "{public_key}",
          "minClient": "",
          "maxClient": "",
          "maxTimediff": 0,
          "shortIds": [
            "{short_id}"
          ]
        }}
      }},
      "tag": "inbound-49649",
      "sniffing": {{
        "enabled": false,
        "destOverride": [
          "http",
          "tls"
        ]
      }}
    }}
  ],
  "outbounds": [
    {{
      "protocol": "freedom",
      "settings": {{}}
    }},
    {{
      "protocol": "blackhole",
      "settings": {{}},
      "tag": "blocked"
    }}
  ],
  "transport": null,
  "policy": {{
    "levels": {{
      "0": {{
        "statsUserUplink": true,
        "statsUserDownlink": true
      }}
    }},
    "system": {{
      "statsInboundDownlink": true,
      "statsInboundUplink": true
    }}
  }},
  "api": {{
    "services": [
      "HandlerService",
      "LoggerService",
      "StatsService"
    ],
    "tag": "api"
  }},
  "stats": {{}},
  "reverse": null,
  "fakeDns": null
}}

'''
# url = 'vless://c2d78e07-d9bd-4328-a9c0-04269b6efa48@91.218.140.18:49649?type=tcp&security=reality&sni=tgju.org&pbk=-_7fMopYs-YfWsz_qh7_YWYalYpf0koc4AMk_J9WCXI&flow=xtls-rprx-vision&sid=d6961645&fp=chrome#reality-AamZ'
url = f"vless://{uuid}@{public_ip}:49649?type=tcp&security=reality&sni=tgju.org&pbk={public_key}&flow=xtls-rprx-vision&sid={short_id}&fp=chrome"

try:  
  os.mkdir(f'users')
except FileExistsError:
  pass

with open(f'users/1.json', 'w') as file:
  file.write(config)
  print(f'ССылка дял подклчюения: {url}')