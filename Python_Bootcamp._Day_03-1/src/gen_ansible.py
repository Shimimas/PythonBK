import yaml

with open('../materials/todo.yml', 'r') as stream:
    data_loaded = yaml.safe_load(stream)
packages = data_loaded['server']['install_packages']
exploit_files = data_loaded['server']['exploit_files']
bad_guys = data_loaded['bad_guys']
packs = [{'name': f'Install {name}',
            'apt': {
                'pkg': f'{name}',
                'stat': 'present'
            }
            } for name in packages]
files = [{'name': f'Copy {name}',
            'copy': {
                'src': f'src/{name}',
                'dest': 'scripts/'
            }
            }
            for name in exploit_files
            ]
vars = {'vars': [{'bad_guys': bad_guys}]}
data = [
    {'hosts': 'web',
        'tasks':
            [
                packs,
                files,
                vars
            ]
        }
]

with open('./deploy.yml', 'w', encoding='utf8') as outfile:
    yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)