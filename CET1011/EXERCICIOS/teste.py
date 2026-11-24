import math
import matplotlib.pyplot as plt

L = 8.0
Dmax = 2.5
Dmin = 2.0

a = Dmax / 2
b = Dmin / 2
H_MIN = 0.0
H_MAX = 2 * b 

print("Parâmetros do tanque:")
print(f"L    = {L:.3f} m")
print(f"Dmax = {Dmax:.3f} m")
print(f"Dmin = {Dmin:.3f} m")
print(f"a    = {a:.3f} m  (semi-eixo horizontal)")
print(f"b    = {b:.3f} m  (semi-eixo vertical)")
print("\nIntervalo permitido para h:")
print(f"h_min = {H_MIN:.3f} m")
print(f"h_max = {H_MAX:.3f} m")

def A(h):
    if h <= 0:    return 0.0
    if h >= 2*b:  return math.pi * a * b
    s = max(-1.0, min(1.0, (h - b) / b))
    return a * b * (math.pi/2 + math.asin(s) + s * math.sqrt(max(0.0, 1 - s*s)))

def V(h):
    return A(h) * L

def grafico_completo_marcando(h_user, n=201):
    hs = [H_MIN + i*(H_MAX - H_MIN)/(n - 1) for i in range(n)]
    Vs = [V(x) for x in hs]
    vx = V(h_user)

    plt.figure()
    plt.plot(hs, Vs, label="V × h")
    plt.plot([h_user], [vx], 'o', label=f"Ponto: h={h_user:.3f} m, V={vx:.3f} m³")
    plt.xlabel("h(m)")
    plt.ylabel("V(m³)")
    plt.title("Variação de V em função de h")
    plt.grid(True)
    plt.legend()
    plt.show()

def h_de_V(V_alvo, tol=1e-6, max_iter=60):
    V_alvo = max(0.0, min(V_alvo, V(H_MAX)))
    lo, hi = H_MIN, H_MAX
    for _ in range(max_iter):
        mid = 0.5*(lo + hi)
        if V(mid) < V_alvo:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5*(lo + hi)

def simular_esvaziamento(h_ini, Q_out, dt=1.0):
    if Q_out <= 0:
        print("Q_out deve ser positivo.\n")
        return
    if dt <= 0:
        print("dt inválido; usando dt = 1.0 s.\n")
        dt = 1.0

    V0 = V(h_ini)
    t_final = V0 / Q_out
    n = max(1, int(t_final // dt) + 1)
    ts = [i*dt for i in range(n)]
    hs = [h_de_V(max(V0 - Q_out*t, 0.0)) for t in ts]

    if ts[-1] < t_final:
        ts.append(t_final)
        hs.append(h_de_V(0.0))

    plt.figure()
    plt.plot(ts, hs, label="h(t)")

    if dt < t_final:
        h_star = h_de_V(max(V0 - Q_out*dt, 0.0))
        plt.plot([dt], [h_star], 'o', label=f"t={dt:.2f} s, h={h_star:.3f} m")
    else:
        print(f"(Aviso) dt = {dt:.2f} s ≥ t_final = {t_final:.2f} s. Ponto não marcado.\n")

    plt.xlabel("t(s)")
    plt.ylabel("h(m)")
    plt.title("Esvaziamento: altura do fluido h(t) x vazão de saída (Q_out)")
    plt.grid(True)
    plt.legend()
    plt.show()

while True:
    try:
        h = float(input(f"\nDigite h (m) entre {H_MIN:.3f} e {H_MAX:.3f}: ").strip())
        if not (H_MIN <= h <= H_MAX):
            print("Fora do intervalo do tanque.\n"); continue
    except ValueError:
        print("Valor inválido.\n"); continue

    print(f"A(h) = {A(h):.6f} m²")
    print(f"V(h) = {V(h):.6f} m³\n")

    grafico_completo_marcando(h)

    if input("Deseja simular o esvaziamento? (s/n): ").strip().lower() in ("s", "sim"):
        try:
            Q = float(input("\nInforme a vazão de saída (Q_out (m³/s)_: ").strip())
            dt = float(input("Informe o passo de tempo (dt (s)): ").strip() or "1.0")
            simular_esvaziamento(h, Q, dt)
        except ValueError:
            print("Valores inválidos para Q_out/dt.\n")

    if input("\nDeseja inserir um novo valor de h? (s/n): ").strip().lower() not in ("s", "sim"):
        print("Programa encerrado.")
        break