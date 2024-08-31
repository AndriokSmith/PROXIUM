#!/usr/bin/env python

import os
import sys
import subprocess
import random
import string
import json
import requests
import qrcode
from datetime import datetime

LOGGER = "XRAY-REALITY-SCRIPT"

COLORS = {
    "BLACK": "\033[0;30m",
    "RED": "\033[0;31m",
    "GREEN": "\033[0;32m",
    "YELLOW": "\033[0;33m",
    "BLUE": "\033[0;34m",
    "PURPLE": "\033[0;35m",
    "CYAN": "\033[0;36m",
    "WHITE": "\033[0;37m",
    "BGREEN": "\033[1;32m",
    "BRED": "\033[1;31m",
    "RESET": "\033[0m"
}

SCRIPT = os.path.basename(__file__)
CURDIR = os.path.dirname(os.path.abspath(__file__))
XRAY_ORIG_CONFIG = "/usr/local/etc/xray/config.json"
TEMPL_CONFIG = os.path.join(CURDIR, "configs", "config.json")
CONFIG = os.path.join(CURDIR, "config.json")
URL_FILE = os.path.join(CURDIR, "url.txt")

def log(level, msg):
    cur_date = f"{COLORS['BLUE']}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{COLORS['RESET']}"
    if level == "DEBUG":
        log_level = f"{COLORS['GREEN']} DEBUG{COLORS['RESET']}"
    elif level == "INFO":
        log_level = f"{COLORS['CYAN']} INFO{COLORS['RESET']}"
    elif level == "WARNING":
        log_level = f"{COLORS['YELLOW']}WARNING{COLORS['RESET']}"
    elif level == "ERROR":
        log_level = f"{COLORS['RED']} ERROR{COLORS['RESET']}"
        die(msg)
    elif level == "CRITICAL":
        log_level = f"{COLORS['BRED']}CRITICAL{COLORS['RESET']}"
        die(msg)
    else:
        log_level = f"{COLORS['WHITE']}NOLEVEL{COLORS['RESET']}"
    print(f"{cur_date} {LOGGER} {log_level}: {msg}")

def die(msg):
    log("CRITICAL", msg)
    exit(1)

def usage_msg():
    print(f"Usage: {SCRIPT} {{init (Default) | config [--url (Default) | --qrencode] | update | --help | -h}}")
    print("")
    print("init: Default, install, update required packages, generate a config, and start xray")
    print("config [--url | --qrencode]: generate a new config based on a template config")
    print(" --url: print to terminal the VLESS url")
    print(" --qrencode: print the url and also the QR encoded version to terminal")
    print("update: update the required packages, including xray-core")
    print("--help | -h: print this help message")
    print("")

def sanity_checks():
    log("INFO", "checking system requirements")
    if os.geteuid() != 0:
        die("must have root access to run the script!")
    if not os.path.exists("/usr/bin/systemctl"):
        die("systemd must be enabled as the init system!")

def install_pkgs():
    log("INFO", "updating & upgrading system")
    subprocess.run(["apt", "update", "-y"], check=True)
    subprocess.run(["apt", "upgrade", "-y"], check=True)
    pkgs = ["openssl", "qrencode", "jq", "curl", "xclip"]
    for pkg in pkgs:
        log("INFO", f"installing package: {pkg}")
        subprocess.run(["apt", "install", "-y", pkg], check=True)
    log("DEBUG", "installing latest beta version of xray")
    subprocess.run(["bash", "-c", "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)", "@", "install", "--beta"], check=True)
    log("DEBUG", "testing xray-core version")
    subprocess.run(["xray", "--version"], check=True)

def xray_new_config(args):
    log("DEBUG", "generating uuid")
    uuid = subprocess.check_output(["xray", "uuid"]).decode().strip()
    log("INFO", f"setting uuid: {uuid}")
    
    log("DEBUG", "generating X25519 private and public key pairs")
    keys = subprocess.check_output(["xray", "x25519"]).decode().strip().split(" ")
    private_key = keys[2]
    log("INFO", f"setting private key: {private_key}")
    public_key = keys[5]
    log("INFO", f"setting public key: {public_key}")
    
    log("DEBUG", "generating short id")
    short_id = ''.join(random.choices(string.hexdigits, k=4))
    log("INFO", f"setting short id: {short_id}")
    
    log("DEBUG", "resolving public ip")
    public_ip = requests.get('https://ifconfig.me').text.strip()
    log("INFO", f"setting public ip: {public_ip}")
    
    cmfgsite = "tgju.org"
    log("INFO", f"using camouflag website: {cmfgsite}")
    
    flow = "xtls-rprx-vision"
    log("INFO", f"using flow: {flow}")
    
    inbound_port = "49649"
    log("INFO", f"setting inbound listen port: {inbound_port}")
    
    protocol_type = "tcp"
    log("INFO", f"using {protocol_type}")
    
    security = "reality"
    log("INFO", f"setting security: {security}")
    
    fingerprint = "chrome"
    log("INFO", f"using fingerprint: {fingerprint}")
    
    with open(CONFIG, "r") as f:
        config = json.load(f)
    
    config["inbounds"][1]["streamSettings"]["realitySettings"]["publicKey"] = public_key
    config["inbounds"][1]["streamSettings"]["realitySettings"]["privateKey"] = private_key
    config["inbounds"][1]["streamSettings"]["realitySettings"]["shortIds"] = [short_id]
    
    if "--url" in args or not args:
        log("INFO", "generating url")
        url = f"vless://{uuid}@{public_ip}:{inbound_port}?type={protocol_type}&security={security}&sni={cmfgsite}&pbk={public_key}&flow={flow}&sid={short_id}&fp={fingerprint}#$name"
        print(url)
        log("INFO", f"saving url to: {URL_FILE}")
        with open(URL_FILE, "w") as f:
            f.write(url)
        copy_config(config)
    elif "--qrencode" in args:
        log("INFO", "generating url")
        url = f"vless://{uuid}@{public_ip}:{inbound_port}?type={protocol_type}&security={security}&sni={cmfgsite}&pbk={public_key}&flow={flow}&sid={short_id}&fp={fingerprint}#$name"
        print(url)
        log("INFO", f"saving url to: {URL_FILE}")
        with open(URL_FILE, "w") as f:
            f.write(url)
        log("DEBUG", "generating qr encoding of the url")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("qrcode.png")
        copy_config(config)
    else:
        usage_msg()

def copy_config(config):
    log("INFO", "backing up $XRAY_ORIG_CONFIG and replacing it with new config")
    xray_orig_config_dir = os.path.dirname(XRAY_ORIG_CONFIG)
    if os.path.exists(os.path.join(xray_orig_config_dir, "config.json.old")):
        log("WARNING", f"{xray_orig_config_dir}/config.json.old exists, replacing")
    os.rename(XRAY_ORIG_CONFIG, os.path.join(xray_orig_config_dir, "config.json.old"))
    with open(XRAY_ORIG_CONFIG, "w") as f:
        json.dump(config, f, indent=2)

def xray_run():
    copy_config()
    if not os.path.exists("/etc/systemd/system/xray.service"):
        log("DEBUG", "xray.service is not enabled, enabling now")
        subprocess.run(["systemctl", "enable", "xray.service"], check=True)
    if not os.path.exists("/etc/systemd/system/xray.service"):
        log("DEBUG", "xray.service is not running, starting now")
        subprocess.run(["systemctl", "start", "xray.service"], check=True)
    else:
        log("DEBUG", "xray.service is already running, restarting")
        subprocess.run(["systemctl", "restart", "xray.service"], check=True)
    log("DEBUG", "checking status on xray.service")
    subprocess.run(["systemctl", "status", "xray.service"], check=True)

def main(args):
    if "init" in args or not args:
        sanity_checks()
        install_pkgs()
        xray_new_config(["--qrencode"])
        xray_run()
    elif "config" in args:
        xray_new_config(args)
        xray_run()
    elif "update" in args:
        install_pkgs()
    elif "--help" in args or "-h" in args:
        usage_msg()
    else:
        usage_msg()

if __name__ == "__main__":
    main(sys.argv[1:])