from pathlib import Path
import json
import re

# Pasta principal do Portal Engenharia UESC
RAIZ = Path(__file__).resolve().parent.parent

# Dicionário de correções de palavras
CORRECOES = {
    # Acentuação e correções ortográficas
    "instalacao": "Instalação",
    "calculos": "Cálculos",
    "calculo": "Cálculo",
    "dinamica": "Dinâmica",
    "pressao": "Pressão",
    "vazao": "Vazão",
    "nivel": "Nível",
    "exercicio": "Exercício",
    "exercicios": "Exercícios",
    "temperatura": "Temperatura",
    "temperataura": "Temperatura",
    "transmissores": "Transmissores",
    "instrumentacao": "Instrumentação",
    "computacional": "Computacional",
    "modelagem": "Modelagem",
    "simulacao": "Simulação",
    "otimizacao": "Otimização",
    "controle": "Controle",
    "processos": "Processos",
    "quimica": "Química",
    "quimico": "Químico",
    "quimicos": "Químicos",
    "laboratorio": "Laboratório",
    "separadores": "Separadores",
    "trifasico": "Trifásico",
    "deducao": "Dedução",
    "area": "Área",
    "volume": "Volume",
    "tanque": "Tanque",
    "versao": "Versão",
    "pratica": "Prática",
    "equacoes": "Equações",
    "hidrociclone": "Hidrociclone",
    "eliptico": "Elíptico",
    "principio": "Princípio",
    "pecas": "Peças",

    # Nomes de programas e ferramentas
    "spyder": "Spyder",
    "anaconda": "Anaconda",
    "python": "Python",
    "solidworks": "SolidWorks",

    # Siglas técnicas e acadêmicas
    "pid": "PID",
    "rna": "RNA",
    "cae": "CAE",
    "asme": "ASME",
    "pdf": "PDF",
    "ta": "TA",
    "tb": "TB",
}

def sugerir_titulo(titulo):
    texto = titulo.replace("_", " ")
    texto = re.sub(r"\s+", " ", texto).strip()

    palavras = texto.split(" ")
    resultado = []

    for palavra in palavras:
        partes = re.split(r"(\W+)", palavra)
        novas_partes = []

        for parte in partes:
            chave = parte.lower()

            if chave in CORRECOES:
                novas_partes.append(CORRECOES[chave])

            elif re.fullmatch(r"CET\d+", parte, re.I):
                novas_partes.append(parte.upper())

            elif parte.isupper() and len(parte) > 1:
                novas_partes.append(parte.capitalize())

            else:
                novas_partes.append(parte)

        resultado.append("".join(novas_partes))

    return " ".join(resultado)


def analisar_catalogos():
    catalogos = sorted(RAIZ.glob("CET*/**/catalogo.json"))

    print("=" * 70)
    print("PORTAL ENGENHARIA UESC")
    print("RELATÓRIO DE PADRONIZAÇÃO DOS TÍTULOS")
    print("=" * 70)

    total = 0
    alteracoes = 0

    for caminho in catalogos:
        print(f"\nCATÁLOGO: {caminho.relative_to(RAIZ)}")

        try:
            with caminho.open("r", encoding="utf-8-sig") as f:
                dados = json.load(f)
        except (OSError, json.JSONDecodeError) as erro:
            print(f"  ERRO AO LER: {erro}")
            continue

        for assunto in dados.get("assuntos", []):
            for material in assunto.get("materiais", []):
                titulo = material.get("titulo", "")

                if not isinstance(titulo, str):
                    continue

                total += 1
                sugestao = sugerir_titulo(titulo)

                if titulo != sugestao:
                    alteracoes += 1
                    print(f"\n  ATUAL:    {titulo}")
                    print(f"  SUGESTÃO: {sugestao}")

    print("\n" + "=" * 70)
    print(f"Catálogos encontrados: {len(catalogos)}")
    print(f"Materiais analisados:   {total}")
    print(f"Títulos com sugestões:  {alteracoes}")
    print("=" * 70)

    print("\nNenhum arquivo foi modificado.")


if __name__ == "__main__":
    analisar_catalogos()
