## Espía qué hace tu sistema (bpytop, glances)

Aplicaciones para ver qué está ocurriendo en el sistema, y en varios de sus componentes (procesadores, discos duros, interfaces de red, etc.): [bpytop](https://github.com/aristocratos/bpytop), [glances](https://nicolargo.github.io/glances/).

```shell
python3 -m venv venv-bpytop
source venv-bpytop/bin/activate
pip install bpytop
bpytop
```

```shell
python3 -m venv venv-glances
source venv-glances/bin/activate
pip install glances
glances
```
