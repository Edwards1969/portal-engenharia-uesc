# -*- coding: utf-8 -*-
"""
LABORATORIO 3 - EXERCICIO 2 - TURMA DE SEXTA-FEIRA
CONTROLE PROPORCIONAL DO NIVEL DE AGUA EM UMA CALDEIRA

"""
#%%
# ============================================================
# IMPORTACAO DAS BIBLIOTECAS
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#%%
# ============================================================
# EXIBICAO DAS FIGURAS DO LABORATORIO 
# ============================================================

# ------------------------------------------------------------
# Primeira figura - Equipamento e instrumentacao
# Nome da Figura: Controle do Nível de Água em uma Caldeira Aquatubular.
# ------------------------------------------------------------

# caminho1 = "figuras/diagrama-controle-caldeira-aquatubular-turmaB.png"

# img1 = mpimg.imread(caminho1)

# plt.figure(figsize=(14, 9))
# plt.imshow(img1)
# plt.axis("off")
# plt.tight_layout()
# plt.show()

# # ------------------------------------------------------------
# # Segunda figura - Dados operacionais
# # Nome da Figura: Dados Operacioais do Exercício 2
# # ------------------------------------------------------------

# caminho2 = "figuras/infografico-controle-caldeira-aquatubular-turmaB.png"

# img2 = mpimg.imread(caminho2)

# plt.figure(figsize=(14, 9))
# plt.imshow(img2)
# plt.axis("off")
# plt.tight_layout()
# plt.show()

# # ------------------------------------------------------------
# # Terceira figura - Equacoes e sequencia de resolucao
# # Nome da Figura: Equações e Sequência de Resolução (Exercício 2)
# # ------------------------------------------------------------

# caminho3 = "figuras/infografico-equacoes-resolução-turmaB.png"

# img3 = mpimg.imread(caminho3)

# plt.figure(figsize=(14, 9))
# plt.imshow(img3)
# plt.axis("off")
# plt.tight_layout()
# plt.show()

# # ------------------------------------------------------------
# # Quarta figura - Infograma e equações de resolução
# # Nome da Figura: Resultados da Simulação - Exercício 2
# # ------------------------------------------------------------

# caminho4 = "figuras/resultados-simulacao-control-caldeira-turmaB.png"

# img4 = mpimg.imread(caminho4)

# plt.figure(figsize=(14, 9))
# plt.imshow(img4)
# plt.axis("off")
# plt.tight_layout()
# plt.show()

#%%
# ------------------------------------------------------------
# 1. DADOS DE ENTRADA
# ------------------------------------------------------------

hsp = 0.80
h0 = 0.80

ma0 = 10.00
mv0 = 9.50
mp = 0.50

rho = 950.0
A = 5.00
Kc = 50.00

mv1 = 7.50

tp = 60.0
tf = 300.0
dt = 0.10

# ------------------------------------------------------------
# 2. RESOLUCAO ALGEBRICA DO PROBLEMA
# ------------------------------------------------------------

# Passo 1 - Verificacao do equilibrio inicial

entrada_inicial = ma0
saida_inicial = mv0 + mp

balanco_inicial = entrada_inicial - saida_inicial

# Passo 2 - Perturbacao na demanda de vapor

delta_mv = mv1 - mv0

# Passo 3 - Modelo dinamico do nivel
#
# dh/dt = (ma - mv - mp)/(rho*A)

# Passo 4 - Controlador proporcional
#
# ma = ma0 + Kc*(hsp - h)

# Passo 5 - Taxa inicial de variacao do nivel

dhdt_inicial = (ma0 - mv1 - mp)/(rho*A)

# Passo 6 - Nova vazao de alimentacao no equilibrio

ma_eq = mv1 + mp

# Passo 7 - Novo nivel de equilibrio

h_eq = hsp - (ma_eq - ma0)/Kc

# Passo 8 - Erro estacionario

erro_ss = hsp - h_eq

# Passo 9 - Constante de tempo

tau = rho*A/Kc

print("\nRESULTADOS ANALITICOS")

print(f"Balanco inicial: {balanco_inicial:.4f} kg/s")
print(f"Perturbacao: {delta_mv:.4f} kg/s")
print(f"Derivada inicial: {dhdt_inicial:.8f} m/s")
print(f"Vazao de equilibrio: {ma_eq:.4f} kg/s")
print(f"Nivel de equilibrio: {h_eq:.4f} m")
print(f"Erro estacionario: {erro_ss:.4f} m")
print(f"Constante de tempo: {tau:.4f} s")

# ------------------------------------------------------------
# 3. SOLUCAO ANALITICA DO NIVEL
# ------------------------------------------------------------

t = np.arange(0.0, tf + dt/2.0, dt)

mv = np.where(t < tp, mv0, mv1)

tempo_decorrido = np.maximum(t - tp, 0.0)

h = h_eq + (h0 - h_eq)*np.exp(-tempo_decorrido/tau)

h = np.where(t < tp, h0, h)

erro = hsp - h

ma = ma0 + Kc*erro

# ------------------------------------------------------------
# 4. ORGANIZACAO DOS RESULTADOS COM PANDAS
# ------------------------------------------------------------

tabela = pd.DataFrame({
    "Tempo (s)": t,
    "Vapor (kg/s)": mv,
    "Nivel (m)": h,
    "Erro (m)": erro,
    "Alimentacao (kg/s)": ma,
    "Purga (kg/s)": np.full(t.shape, mp)
})

print("\nTABELA DE RESULTADOS - PRIMEIRAS 10 LINHAS")

print(
    tabela.head(10).to_string(
        index=False,
        float_format=lambda x: f"{x:.6f}"
    )
)

# ------------------------------------------------------------
# 5. RESULTADOS EM INSTANTES SELECIONADOS
# ------------------------------------------------------------

instantes = np.array([
    0.0,
    60.0,
    95.0,
    155.0,
    250.0,
    300.0
])

indices = np.searchsorted(t, instantes)

tabela_resumo = tabela.iloc[indices].copy()

print("\nRESULTADOS EM INSTANTES SELECIONADOS")

print(
    tabela_resumo.to_string(
        index=False,
        float_format=lambda x: f"{x:.6f}"
    )
)

# ------------------------------------------------------------
# 6. GRAFICO DO NIVEL DE AGUA
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    t, h,
    label="Solucao analitica",
    linewidth=2
)

plt.axhline(
    hsp,
    linestyle=":",
    label="Nivel de referencia"
)

plt.axhline(
    h_eq,
    linestyle="-.",
    label="Nivel de equilibrio"
)

plt.axvline(
    tp,
    linestyle=":",
    label="Perturbacao"
)

plt.xlabel("Tempo (s)")
plt.ylabel("Nivel de agua (m)")
plt.title("Resposta dinamica do nivel de agua")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 7. GRAFICO DAS VAZOES MASSICAS
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    t, ma,
    label="Agua de alimentacao",
    linewidth=2
)

plt.plot(
    t, mv,
    label="Demanda de vapor"
)

plt.plot(
    t, mv + mp,
    "--",
    label="Vapor + purga"
)

plt.axvline(
    tp,
    linestyle=":",
    label="Perturbacao"
)

plt.xlabel("Tempo (s)")
plt.ylabel("Vazao massica (kg/s)")
plt.title("Evolucao das vazoes massicas")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 8. GRAFICO DO ERRO DE CONTROLE
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    t, erro,
    label="Erro de controle",
    linewidth=2
)

plt.axhline(
    erro_ss,
    linestyle="--",
    label="Erro estacionario"
)

plt.axvline(
    tp,
    linestyle=":",
    label="Perturbacao"
)

plt.xlabel("Tempo (s)")
plt.ylabel("Erro de nivel (m)")
plt.title("Evolucao do erro de controle")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 9. VERIFICACAO DO BALANCO DE MASSA
# ------------------------------------------------------------

dhdt_balanco = (ma - mv - mp)/(rho*A)

dhdt_analitico = np.zeros_like(t)

mascara = t >= tp

dhdt_analitico[mascara] = (
    -(h0 - h_eq)/tau
    * np.exp(-(t[mascara] - tp)/tau)
)

diferenca_balanco = dhdt_balanco - dhdt_analitico

erro_balanco = np.max(np.abs(diferenca_balanco))

print("\nVERIFICACAO DO BALANCO DE MASSA")

print(
    f"Diferenca maxima: {erro_balanco:.12f} m/s"
)

# ------------------------------------------------------------
# 10. RESUMO FINAL DO EXERCICIO
# ------------------------------------------------------------

resumo = pd.DataFrame({
    "Grandeza": [
        "Balanco inicial",
        "Perturbacao na demanda de vapor",
        "Taxa inicial de variacao do nivel",
        "Vazao de alimentacao no equilibrio",
        "Nivel de equilibrio",
        "Erro estacionario",
        "Constante de tempo"
    ],
    "Valor": [
        balanco_inicial,
        delta_mv,
        dhdt_inicial,
        ma_eq,
        h_eq,
        erro_ss,
        tau
    ],
    "Unidade": [
        "kg/s",
        "kg/s",
        "m/s",
        "kg/s",
        "m",
        "m",
        "s"
    ]
})

print("\nRESUMO FINAL DO EXERCICIO")

print(
    resumo.to_string(
        index=False,
        float_format=lambda x: f"{x:.6f}"
    )
) 