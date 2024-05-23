from os import path
from dataclasses import dataclass, field
import yaml

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
                    f'![](https://img.shields.io/badge/{badge[0]}-white?logo={badge[1]}&logoColor={badge[2]})'
                    for badge in line
                ]
            )
            for line in value
        ]
    )
    for header, value in config.badge.items()
}

footer_str = '  \n'.join(['###### ' + _footer for _footer in config.footer])

result = \
    f'''<div align="center">

# 🥰Nice to meet you!
{intro_str}  

{config.extra}

<div style="margin-left: auto; margin-right: auto; display: table;">

{render_nohead_table(config.badge)}
</div>

{footer_str}
</div>'''
open(readme_path, 'w', encoding='utf-8').write(result)
