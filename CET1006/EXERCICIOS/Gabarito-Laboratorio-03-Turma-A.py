# -*- coding: utf-8 -*-
"""
LABORATORIO 3 - EXERCICIO 1

CONTROLE PROPORCIONAL DO NIVEL DE AGUA
EM UMA CALDEIRA INDUSTRIAL

Resolucao algebrica e computacional
utilizando NumPy, pandas e Matplotlib.
"""

#%%
# ============================================================
# IMPORTACAO DAS BIBLIOTECAS
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# #%%
# # ============================================================
# # EXIBICAO DAS FIGURAS DO LABORATORIO
# # ============================================================

# # ------------------------------------------------------------
# # Primeira figura - Equipamento e instrumentacao
# # Nome da Figura: Caldeira Aquatubular -Controle de Nível de água Tubulão
# # ------------------------------------------------------------

# caminho1 = "figuras/diagrama-controle-nível-caldeira-aquatubular.png"

# img1 = mpimg.imread(caminho1)

# plt.figure(figsize=(14, 9))
# plt.imshow(img1)
# plt.axis("off")
# plt.tight_layout()
# plt.show()

# # ------------------------------------------------------------
# # Segunda figura - Dados operacionais
# # Nome da Figura: Dados Operacionais da Caldeira (Exercício 1)
# # ------------------------------------------------------------

# caminho2 = "figuras/dados-operacionais-caldeira.png"

# img2 = mpimg.imread(caminho2)

# plt.figure(figsize=(14, 9))
# plt.imshow(img2)
# plt.axis("off")
# plt.tight_layout()
# plt.show()

# # ------------------------------------------------------------
# # Terceira figura - Equacoes e sequencia de resolucao
# # Nome da Figura: Equações e Sequência de Resolução (Exercício 1)
# # ------------------------------------------------------------

# caminho3 = "figuras/sequencia-resolucao-equacoes.png"

# img3 = mpimg.imread(caminho3)

# plt.figure(figsize=(14, 9))
# plt.imshow(img3)
# plt.axis("off")
# plt.tight_layout()
# plt.show()

#%%
# ============================================================
# 1. DADOS DE ENTRADA
# ============================================================

# ------------------------------------------------------------
# Condicoes iniciais de operacao (regime permanente)
# ------------------------------------------------------------

hsp = 0.80       # Nivel de referencia (set point) (m)
h0 = 0.80        # Nivel inicial (m)
ma0 = 10.00      # Vazao massica de alimentacao inicial (kg/s)
mv0 = 9.50       # Vazao massica de vapor inicial (kg/s)
mp = 0.50        # Vazao massica de purga (kg/s)

# ------------------------------------------------------------
# Parametros do processo
# ------------------------------------------------------------

rho = 950.0      # Densidade da agua (kg/m3)
A = 4.00         # Area transversal efetiva do tubulao (m2)

# ------------------------------------------------------------
# Parametro do controlador proporcional
# ------------------------------------------------------------

Kc = 50.00       # Ganho proporcional (kg/(s.m))

# ------------------------------------------------------------
# Perturbacao na operacao
# ------------------------------------------------------------

mv1 = 12.00      # Demanda de vapor apos perturbacao (kg/s)
tp = 60.0        # Instante da perturbacao (s)

# ------------------------------------------------------------
# Condicoes da simulacao computacional
# ------------------------------------------------------------

tf = 300.0       # Tempo total de simulacao (s)
dt = 0.10        # Intervalo de tempo para avaliar a solucao (s)

#%%
# ============================================================
# 2. RESOLUCAO ALGEBRICA DO PROBLEMA
# ============================================================

# ------------------------------------------------------------
# PASSO 1 - Verificar a condicao inicial de equilibrio
# ------------------------------------------------------------

entrada_inicial = ma0

saida_inicial = mv0 + mp

balanco_inicial = entrada_inicial - saida_inicial


# ------------------------------------------------------------
# PASSO 2 - Determinar a perturbacao na demanda de vapor
# ------------------------------------------------------------

delta_mv = mv1 - mv0

# ------------------------------------------------------------
# PASSO 3 - Modelo dinamico do nivel
# ------------------------------------------------------------

# Equacao do balanco de massa:
#
# dh/dt = (ma - mv - mp)/(rho*A)
#
# A equacao sera utilizada para determinar
# a taxa inicial de variacao do nivel.

# ------------------------------------------------------------
# PASSO 4 - Modelo do controlador proporcional
# ------------------------------------------------------------

# Equacao do controlador:
#
# ma = ma0 + Kc*(hsp - h)
#
# O controlador aumenta a alimentacao quando
# o nivel fica abaixo da referencia.

# ------------------------------------------------------------
# PASSO 5 - Taxa inicial de variacao do nivel
# ------------------------------------------------------------

dhdt_inicial = (ma0 - mv1 - mp)/(rho*A)

# ------------------------------------------------------------
# PASSO 6 - Nova vazao de alimentacao no equilibrio
# ------------------------------------------------------------

ma_eq = mv1 + mp

# ------------------------------------------------------------
# PASSO 7 - Novo nivel de equilibrio
# ------------------------------------------------------------

h_eq = hsp - (ma_eq - ma0)/Kc

# ------------------------------------------------------------
# PASSO 8 - Erro estacionario
# ------------------------------------------------------------

erro_ss = hsp - h_eq

# ------------------------------------------------------------
# PASSO 9 - Constante de tempo em malha fechada
# ------------------------------------------------------------

tau = rho*A/Kc

# ============================================================
# APRESENTACAO DOS RESULTADOS ANALITICOS
# ============================================================

print("\nRESULTADOS ANALITICOS")
print("-"*55)

print(f"Balanco inicial: {balanco_inicial:.4f} kg/s")
print(f"Perturbacao: {delta_mv:.4f} kg/s")
print(f"Derivada inicial: {dhdt_inicial:.8f} m/s")
print(f"Vazao de equilibrio: {ma_eq:.4f} kg/s")
print(f"Nivel de equilibrio: {h_eq:.4f} m")
print(f"Erro estacionario: {erro_ss:.4f} m")
print(f"Constante de tempo: {tau:.4f} s")

#%%
# ============================================================
# 3. SOLUCAO ANALITICA DO NIVEL
# ============================================================

# ------------------------------------------------------------
# PASSO 10 - Calcular a resposta temporal do nivel
# ------------------------------------------------------------

# Vetor de tempo

t = np.arange(0.0, tf + dt/2.0, dt)

# ------------------------------------------------------------
# Demanda de vapor antes e depois da perturbacao
# ------------------------------------------------------------

mv = np.where(t < tp, mv0, mv1)

# ------------------------------------------------------------
# Tempo decorrido apos a perturbacao
# ------------------------------------------------------------

tempo_decorrido = np.maximum(t - tp, 0.0)

# ------------------------------------------------------------
# Solucao analitica do nivel
# ------------------------------------------------------------

# h(t) = h_eq + (h0 - h_eq)*exp(-(t-tp)/tau)

h = h_eq + (h0 - h_eq)*np.exp(-tempo_decorrido/tau)

# ------------------------------------------------------------
# Antes da perturbacao o nivel permanece constante
# ------------------------------------------------------------

h = np.where(t < tp, h0, h)

# ------------------------------------------------------------
# Erro de controle
# ------------------------------------------------------------

erro = hsp - h

# ------------------------------------------------------------
# Vazao de agua de alimentacao
# ------------------------------------------------------------

ma = ma0 + Kc*erro

#%%
# ============================================================
# 4. ORGANIZACAO DOS RESULTADOS COM PANDAS
# ============================================================

tabela = pd.DataFrame({

    "Tempo (s)": t,

    "Vapor (kg/s)": mv,

    "Nivel (m)": h,

    "Erro (m)": erro,

    "Alimentacao (kg/s)": ma,

    "Purga (kg/s)": np.full(t.shape, mp)

})

print("\nTABELA DE RESULTADOS")
print("-"*80)

print(tabela.head(10).to_string(
    index=False,
    float_format=lambda x: f"{x:.6f}"
))

#%%
# ============================================================
# 5. RESULTADOS EM INSTANTES SELECIONADOS
# ============================================================

instantes = np.array([
    0.0,
    60.0,
    76.0,
    136.0,
    212.0,
    300.0
])

indices = np.searchsorted(t, instantes)

tabela_resumo = tabela.iloc[indices].copy()


print("\nRESULTADOS EM INSTANTES SELECIONADOS")
print("-"*80)

print(tabela_resumo.to_string(
    index=False,
    float_format=lambda x: f"{x:.6f}"
))


#%%
# ============================================================
# 6. GRAFICO DO NIVEL DE AGUA
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    t,
    h,
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

plt.title("Resposta dinamica do nivel da caldeira")

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


#%%
# ============================================================
# 7. GRAFICO DAS VAZOES MASSICAS
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    t,
    ma,
    label="Agua de alimentacao",
    linewidth=2
)

plt.plot(
    t,
    mv,
    label="Demanda de vapor",
    linewidth=2
)

plt.plot(
    t,
    mv + mp,
    "--",
    label="Vapor + purga",
    linewidth=2
)

plt.axvline(
    tp,
    linestyle=":",
    label="Perturbacao"
)

plt.xlabel("Tempo (s)")
plt.ylabel("Vazao massica (kg/s)")

plt.title("Balanco de massa da caldeira")

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


#%%
# ============================================================
# 8. GRAFICO DO ERRO DE CONTROLE
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    t,
    erro,
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

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


#%%
# ============================================================
# 9. VERIFICACAO DO BALANCO DE MASSA
# ============================================================

# Taxa de variacao do nivel calculada pelo balanco de massa

dhdt_balanco = (ma - mv - mp)/(rho*A)


# Taxa de variacao do nivel calculada pela solucao analitica

dhdt_analitico = np.zeros_like(t)

mascara = t >= tp

dhdt_analitico[mascara] = (
    -(h0 - h_eq)/tau
    * np.exp(-(t[mascara] - tp)/tau)
)


# Diferenca entre as duas expressoes

diferenca_balanco = dhdt_balanco - dhdt_analitico

erro_balanco = np.max(np.abs(diferenca_balanco))


print("\nVERIFICACAO DO BALANCO DE MASSA")
print("-"*55)

print(f"Diferenca maxima: {erro_balanco:.12f} m/s")


#%%
# ============================================================
# 10. RESUMO FINAL DO EXERCICIO
# ============================================================

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

print("\nRESUMO FINAL")
print("-"*80)

print(resumo.to_string(index=False))