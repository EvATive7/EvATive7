# 2025 EvATive7

import json
from os import path
from dataclasses import dataclass, field
from urllib.parse import quote, urlencode
import requests

config_path = path.join(path.dirname(path.realpath(__file__)), "config.json")
resource_path = path.join(
    path.dirname(path.dirname(path.realpath(__file__))), "resources"
)
readme_path = path.join(
    path.dirname(path.dirname(path.realpath(__file__))), "README.md"
)


@dataclass
class Config:
    introduction: dict[str, str] = field(default_factory=dict)
    badge: dict[str, list[list[list]]] = field(default_factory=dict)
    footer: list = field(default_factory=list)
    extra: str = ""


def render_nohead_table(table_data: dict[str, str]):
    table_str = []
    for index, (header, value) in enumerate(table_data.items()):
        value: list[list[str]]
        table_str.append("| {} | {} |".format(header, value))
        if index == 0:
            table_str.append("| :-- | :-- |")
    table_str = "  \n".join(table_str)
    return table_str


def parse_id(name: str):
    return (
        name.lower()
        .replace("_", " ")
        .replace(" ", "")
        .replace("+", "plus")
        .replace(".", "dot")
        .replace("&", "and")
    )


icon_data: dict[str, dict[str, object]] = {}

print("[INFO] Fetching simple-icons data from GitHub...")
try:
    _data = requests.get(
        "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/data/simple-icons.json",
        timeout=5,
    ).json()
    for _icon in _data:
        title = _icon.get("slug") or _icon["title"]
        icon_data[parse_id(title)] = _icon
    print(f"[INFO] Loaded {len(icon_data)} icons successfully.")
except Exception as e:
    raise RuntimeError(
        f"Unable to fetch logo details from github.com/simple-icons/simple-icons: {e}"
    )


def fetch_icon_url(args):
    def dofetch(icon_name: str, icon_id: str = None, icon_color: str = None):
        if not icon_color:
            if not icon_id:
                icon_id = parse_id(icon_name)
            if _detail := icon_data.get(icon_id):
                icon_color = _detail["hex"]
            else:
                icon_color = None

        base_url = f"https://img.shields.io/badge/{quote(icon_name)}-white"
        params = {}

        if icon_id.startswith("base64:"):
            icon_id = icon_id.removeprefix("base64:")
            if icon_id.startswith("png:"):
                icon_id = icon_id.removeprefix("png:")
                data_type = "png"
            elif icon_id.startswith("svg:"):
                icon_id = icon_id.removeprefix("svg:")
                data_type = "svg+xml"
            else:
                data_type = None
            b64_file_path = path.join(resource_path, "base64", icon_id + ".b64")

            if path.exists(b64_file_path):
                icon_b64_content = open(b64_file_path, "r", encoding="utf-8").read()

                if data_type:
                    icon_color = None
                    icon_id = f"data:image/{data_type};base64," + icon_b64_content
                else:
                    icon_id = None

        if icon_id:
            params["logo"] = icon_id
        if icon_color:
            params["logoColor"] = icon_color

        final_url = f"{base_url}?{urlencode(params)}" if params else base_url
        print(f"[INFO] Generated badge URL for '{icon_name}': {final_url[0:100]}...")
        return final_url

    if isinstance(args, str):
        return dofetch(args)
    elif isinstance(args, list):
        return dofetch(*args)


print(f"[INFO] Loading config from {config_path}...")
config = Config(**json.loads(open(config_path, "r", encoding="utf-8").read()))
print("[INFO] Config loaded successfully.")

intro_str = []
for index, value in enumerate(config.introduction.items()):
    intro_str.append("{} {}".format(*value))
intro_str = "  \n".join(intro_str)

print("[INFO] Rendering badges...")
config.badge = {
    header: "<br>".join(
        [
            " ".join([f"![]({fetch_icon_url(badge)})" for badge in line])
            for line in value
        ]
    )
    for header, value in config.badge.items()
}

footer_str = "  \n".join(["###### " + _footer for _footer in config.footer])

result = f"""
<div align="left">

# 🥰Nice to meet you~
{intro_str}  

{config.extra}

<div style="margin-left: auto; margin-right: auto; display: table;">

{render_nohead_table(config.badge)}
</div>

{footer_str}
</div>
"""

print(f"[INFO] Writing README.md to {readme_path}...")
open(readme_path, "w", encoding="utf-8").write(result)
print("[INFO] README.md generation completed successfully.")
