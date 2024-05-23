# Copyright (c) 2024 EvATive7
# All rights reserved.
#
# This file is not open source and not licensed for use by any party.
# Unauthorized copying, modification, or distribution of this file,
# via any medium, is strictly prohibited.

from os import path
from dataclasses import dataclass, field
from urllib.parse import quote
import yaml
import requests

config_path = path.join(path.dirname(path.realpath(__file__)), 'config.yml')
readme_path = path.join(path.dirname(path.dirname(path.realpath(__file__))), 'README.md')


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
        table_str.append(
            '| {} | {} |'.format(
                header,
                value
            )
        )
        if index == 0:
            table_str.append('| :-- | :-- |')
    table_str = '  \n'.join(table_str)
    return table_str


icon_data: dict[str, dict[str, object]] = None


def fetch_icon_url(args):
    def dofetch(icon_name, icon_id=None, icon_color=None):
        global icon_data

        def parse_id(name: str):
            return name.lower().replace(' ', '').replace('+', 'plus').replace('.', 'dot').replace('&', 'and')

        if not icon_data:
            try:
                _data = requests.get('https://raw.githubusercontent.com/simple-icons/simple-icons/develop/_data/simple-icons.json', timeout=5).json()['icons']
                icon_data = {}
                for _icon in _data:
                    title = _icon.get('slug')
                    if not title:
                        title = _icon['title']
                    icon_data[parse_id(title)] = _icon
            except Exception as e:
                raise RuntimeError(f'Unable to fetch logo details from github.com/simple-icons/simple-icons: {e}')

        if not icon_color:
            if not icon_id:
                icon_id = parse_id(icon_name)
            if _detail := icon_data.get(icon_id):
                icon_color = _detail['hex']
            else:
                raise RuntimeError(f'Unable to find the corresponding icon information for {icon_name}')

        return f'https://img.shields.io/badge/{quote(icon_name)}-white?logo={quote(icon_id)}&logoColor={icon_color}'

    if type(args) == str:
        return dofetch(args)
    elif type(args) == list:
        return dofetch(*args)


config = Config(**yaml.safe_load(open(config_path, 'r')))

intro_str = []
for index, value in enumerate(config.introduction.items()):
    intro_str.append('{} {}'.format(*value))
intro_str = '  \n'.join(intro_str)

config.badge = {
    header:
    '<br>'.join(
        [
            ' '.join(
                [
                    f'![]({fetch_icon_url(badge)})'
                    for badge in line
                ]
            )
            for line in value
        ]
    )
    for header, value in config.badge.items()
}

footer_str = '  \n'.join(['###### ' + _footer for _footer in config.footer])

result = f'''
<div align="center">

# 🥰Nice to meet you!
{intro_str}  

{config.extra}

<div style="margin-left: auto; margin-right: auto; display: table;">

{render_nohead_table(config.badge)}
</div>

{footer_str}
</div>
'''
open(readme_path, 'w', encoding='utf-8').write(result)
