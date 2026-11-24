"""
UNIVERSIDADE ESTADUAL DE SANTA CRUZ - UESC
CET1011 - Engenharia Auxiliada por Computador
Dimensionamento de Vasos de Pressão: Resolução Algébrica Passo a Passo

Sequência: Compreender -> Calcular -> Programar -> Modelar -> Analisar -> Decidir
(Sem uso de funções 'def' ou abstrações - cálculo linear como no caderno)
"""

import numpy as np
import matplotlib.pyplot as plt

print("=" * 65)
print("UNIVERSIDADE ESTADUAL DE SANTA CRUZ - UESC")
print("CET1011 - ENGENHARIA AUXILIADA POR COMPUTADOR")
print("=" * 65)

# =====================================================================
# EXERCÍCIO 1 — DIMENSIONAMENTO BÁSICO DO CASCO
# =====================================================================
print("\n>>> EXERCÍCIO 1: DIMENSIONAMENTO BÁSICO DO CASCO")
print("-" * 65)

# Dados de entrada do problema
P = 1.5        # Pressão interna de projeto [MPa]
D_i = 800.0    # Diâmetro interno [mm]
S = 125.0      # Tensão admissível [MPa]
E = 0.85       # Eficiência de junta soldada
CA = 2.5       # Sobreespessura de corrosão [mm]

print(f"Dados: P = {P} MPa | Di = {D_i} mm | S = {S} MPa | E = {E} | CA = {CA} mm\n")

# Item 1: Raio interno do vaso
R = D_i / 2
print(f"1) Raio interno R = {R:.1f} mm")

# Item 2: Espessura necessária para suportar a pressão interna (t_P)
# Fórmula: t_P = (P * R) / (S * E - 0.6 * P)
numerador = P * R
denominador = S * E - 0.6 * P
t_P = numerador / denominador
print(f"2) Espessura para pressão t_P = {t_P:.3f} mm")

# Item 3: Espessura mínima requerida (t_min)
# Fórmula: t_min = t_P + CA
t_min = t_P + CA
print(f"3) Espessura mínima requerida t_min = {t_min:.3f} mm")

# Item 4: Espessura comercial a ser adotada
# Chapas hipotéticas: 6, 8, 10, 12, 16 mm
# Como t_min = 8.195 mm > 8 mm, adota-se 10 mm
t_adot = 10.0
print(f"4) Espessura comercial adotada t_adot = {t_adot:.1f} mm")

# Item 5: Diâmetro externo correspondente
D_o = D_i + 2 * t_adot
print(f"5) Diâmetro externo D_o = {D_o:.1f} mm")
print("=" * 65)

# =====================================================================
# EXERCÍCIO 2 — INFLUÊNCIA DA PRESSÃO NO DIMENSIONAMENTO
# =====================================================================
print("\n>>> EXERCÍCIO 2: INFLUÊNCIA DA PRESSÃO")
print("-" * 65)

# Dados do Exercício 2
D_i_2 = 1000.0   # Diâmetro interno [mm]
R_2 = D_i_2 / 2  # Raio interno [mm] (500 mm)
S_2 = 140.0      # Tensão admissível [MPa]
E_2 = 0.90       # Eficiência de junta
CA_2 = 3.0       # Sobreespessura de corrosão [mm]

# Pressões analisadas
P_valores = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])

# Cálculo das espessuras
t_P_valores = (P_valores * R_2) / (S_2 * E_2 - 0.6 * P_valores)
t_min_valores = t_P_valores + CA_2

# Tabela organizada de resultados
print("P (MPa)  |   t_P (mm)   |   t_min (mm)")
print("-" * 38)
for i in range(len(P_valores)):
    print(f"  {P_valores[i]:.1f}    |    {t_P_valores[i]:.3f}     |     {t_min_valores[i]:.3f}")
print("-" * 38)

# Gráfico t_min vs P
plt.figure(figsize=(8, 5))
plt.plot(P_valores, t_min_valores, marker='o', color='blue', linewidth=2, label='t_min (mm)')
for i in range(len(P_valores)):
    plt.annotate(f"{t_min_valores[i]:.2f} mm", (P_valores[i], t_min_valores[i] + 0.3), ha='center', fontsize=9)

plt.title("Exercício 2: Influência da Pressão na Espessura Mínima", fontsize=12, fontweight='bold')
plt.xlabel("Pressão de Projeto P (MPa)")
plt.ylabel("Espessura Mínima t_min (mm)")
plt.ylim(0, max(t_min_valores) + 3)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('grafico_exercicio2_CET1011.png', dpi=300)
print("\n[OK] Gráfico salvo como 'grafico_exercicio2_CET1011.png'.")
