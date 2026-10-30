#!/usr/bin/env python3
"""Generate a complete, self-contained local Clash profile for FlClash / Mihomo."""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def generate():
    ip_file = ROOT / 'ip.txt'
    if not ip_file.exists():
        raise RuntimeError("Missing ip.txt")
    ip_line = ip_file.read_text().strip().splitlines()[0]
    ip = ip_line.split(':')[0]

    profile_file = ROOT / '.work' / 'node-profile.json'
    if not profile_file.exists():
        raise RuntimeError("Missing .work/node-profile.json")
    profile = json.loads(profile_file.read_text())

    clash_template = (ROOT / 'clients' / 'clash.yaml').read_text()

    host = (profile.get('transport', {}).get('headers', {}).get('Host') or
            profile.get('tls', {}).get('server_name', 'edgetunnel-trial.pages.dev'))
    sni = profile.get('tls', {}).get('server_name') or host
    uuid = profile.get('uuid', '')

    proxy_entry = f"""# FlClash / Mihomo 本地完整独立配置 (已内置当前优选节点，绝不提交至公开仓库)
port: 7890
socks-port: 7891
mixed-port: 7892
allow-lan: false
mode: rule
log-level: info
ipv6: false

proxies:
  - name: "CF-MEDIA"
    type: vless
    server: {ip}
    port: 443
    uuid: {uuid}
    network: ws
    tls: true
    udp: false
    servername: {sni}
    client-fingerprint: chrome
    ws-opts:
      path: /
      headers:
        Host: {host}

proxy-groups:
  - name: 日常流媒体
    type: select
    proxies:
      - "CF-MEDIA"
      - DIRECT
  - name: AI-专线
    type: select
    proxies:
      - "日常流媒体"
      - DIRECT
"""

    idx = clash_template.find('rule-providers:')
    if idx == -1:
        raise RuntimeError("Could not find rule-providers in clash.yaml")
    rules_and_providers = clash_template[idx:]

    full_config = proxy_entry + "\n" + rules_and_providers

    out_file = ROOT / 'clients' / 'flclash.local.yaml'
    out_file.write_text(full_config)
    print(f"Generated {out_file} successfully with entrance {ip}")


if __name__ == '__main__':
    generate()
