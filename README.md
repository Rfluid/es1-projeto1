# Fight Drill

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Compile reports

### Entrega 1

Compilation command available at `compile-entrega1.txt`:

```bash
pandoc entrega1.md -o entrega1.pdf --pdf-engine=xelatex --citeproc
```

## Manage dependencies

```bash
# Adicionar pacote: editar requirements.in, depois:
pip-compile requirements.in -o requirements.txt
pip install -r requirements.txt
```
