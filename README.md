
<div style="text-align:center"><img src="./icon.png" /></div>
# Integrate - Derivação e Integração

Programa que permite resolver e mostrar graficos de funções derivadas e integrais

### Prerequisites

Software potencialmente necessario

```
    matplotlib -> For tk ploting
    Microsoft Visual C++ Build Tools -> Needed by matplotlib and numpy
    pathlib
    screeninfo
    sympy -> For some math libs
    pyinstaller --> For binary executable creation. Needs to be compiled on the platform of destination, cross compiling for diferent platforms not supported!
```
### Compilação
    Windows:
        Executar "build_windows.ps1" 
        ou
        python -m PyInstaller .\main.py --onefile --name=Integrate -w

    Linux:
        Executar "build_linux.bash"
        ou
        python -m PyInstaller .\main.py --onefile --name=Integrate -w

## Autor

* **Hélder Braga** -  - [hfmmb](https://github.com/hfmmb)
