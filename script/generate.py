import os

intro = {
    '🐺': '**邶柒EvATive7**',
    '💐': 'Enciodes SilverAsh',
    '⚪': '「 lex parsimoniae 」'
}
badges = {
    'I use': [
        [
            ('Spring', 'spring', '6DB33F'),
            ('Vue', 'vuedotjs', '4FC08D'),
            ('.NET', 'dotnet', '512BD4'),
            ('Android', 'android', '34A853'),
            ('Flutter', 'flutter', '02569B'),
            ('Nginx', 'nginx', '009639'),
            ('TensorFlow', 'tensorflow', 'FF6F00'),
        ]
    ],
    'with': [
        [
            ('Python', 'python', '3776AB'),
            ('JavaScript', 'javascript', 'F7DF1E'),
            ('TypeScript', 'typescript', '3178C6'),
            ('C%23', 'csharp', '512BD4'),
            ('C++', 'cplusplus', '00599C'),
            ('Java', 'oracle', 'F80000'),
            ('Dart', 'dart', '0175C2')
        ],
        [
            ('Material_Design', 'materialdesign', '757575')
        ],
        [
            ('Code', 'visualstudiocode', '007ACC'),
            ('Git', 'git', 'F05032'),
            ('Firefox', 'firefoxbrowser', 'FF7139')
        ],
    ],
    'on': [
        [
            ('Windows', 'windows', '0078D4'),
            ('Ubuntu', 'ubuntu', 'E95420'),
            ('Nvidia', 'nvidia', '76B900'),
            ('Intel', 'intel', '0071C5')
        ]
    ]
}
footer = [
    'Avatar ©-Ask--'
]
extra = "「 如果一次花开就是一次告白 你看那片紫罗兰已开成了海 」"

intro_str = []
for index, value in enumerate(intro.items()):
    intro_str.append('{} {}'.format(*value))
intro_str = '  \n'.join(intro_str)

table_str = []
for index, (header, value) in enumerate(badges.items()):
    value: list[list[str]]
    table_str.append(
        '| {} | {} |'.format(
            header,
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
        )
    )
    if index == 0:
        table_str.append('| :-- | :-- |')
table_str = '  \n'.join(table_str)

footer_str = '  \n'.join(['###### ' + _footer for _footer in footer])

result = \
    f'''<div align="center">

# 🥰Nice to meet you!
{intro_str}  

{extra}

<div style="margin-left: auto; margin-right: auto; display: table;">

{table_str}
</div>

</div>'''

open(os.path.join(__file__, '../../', 'README.md'), 'w', encoding='utf-8').write(result)
