#!/usr/bin/env python3
"""Gera catálogos de arquivos para o Portal Engenharia UESC.

Uso: python scripts/gerar_catalogos.py
Pastas vazias são ignoradas. Não altera PDFs, notebooks ou arquivos HTML.
"""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTS = {".pdf", ".ipynb", ".py", ".csv", ".pptx", ".ppt", ".xlsx", ".docx", ".mp4", ".webm"}
CATEGORIES = ("AULAS", "EXERCICIOS", "SLIDES", "VIDEOS")
IGNORE = {"img", "images", "imagens", "__pycache__", ".ipynb_checkpoints"}
LABELS = {"NIVEL": "Nível", "PRESSAO": "Pressão", "TEMPERATURA": "Temperatura",
          "VAZAO": "Vazão", "INTRODUCAO": "Introdução", "TRANSMISSORES": "Transmissores",
          "BOMBAS": "Bombas", "GERAL": "Geral"}
ORDER = {"INTRODUCAO": 0, "GERAL": 0, "NIVEL": 1, "VAZAO": 2,
         "PRESSAO": 3, "TEMPERATURA": 4}

def label(value):
    key = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().upper()
    return LABELS.get(key, value.replace("_", " ").replace("-", " ").title())

def title(filename):
    return re.sub(r"[-_]+", " ", Path(filename).stem).strip()

def collect(folder, category_root):
    items = []
    for file in sorted(folder.iterdir(), key=lambda x: x.name.casefold()):
        if file.is_file() and file.suffix.lower() in EXTS:
            items.append({"titulo": title(file.name), "arquivo": file.relative_to(category_root).as_posix(),
                          "tipo": file.suffix.lower().lstrip(".")})
    return items

def generate(category_dir):
    groups = []
    general = collect(category_dir, category_dir)
    if general:
        groups.append({"id": "GERAL", "nome": "Introdução" if category_dir.name == "AULAS" else "Geral",
                       "materiais": general})
    for folder in category_dir.iterdir():
        if not folder.is_dir() or folder.name.lower() in IGNORE or folder.name.startswith("."):
            continue
        items = collect(folder, category_dir)
        if items:
            groups.append({"id": folder.name, "nome": label(folder.name), "materiais": items})
    groups.sort(key=lambda group: (ORDER.get(group["id"].upper(), 99), group["nome"].casefold()))
    result = {"versao": 1, "disciplina": category_dir.parent.name,
              "categoria": category_dir.name, "assuntos": groups}
    destination = category_dir / "catalogo.json"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{destination.relative_to(ROOT)}: {len(groups)} assuntos")

def main():
    for course in sorted(ROOT.iterdir()):
        if not course.is_dir() or not re.fullmatch(r"CET\d+", course.name):
            continue
        for category in CATEGORIES:
            folder = course / category
            if folder.is_dir():
                generate(folder)

if __name__ == "__main__":
    main()
