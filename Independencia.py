import math

try:
    import matplotlib.pyplot as plt  # pyright: ignore[reportMissingModuleSource]
    TIENE_MATPLOTLIB = True
except ImportError:
    TIENE_MATPLOTLIB = False

# 1. Entrada y generación por LFSR (4 dígitos)
print("--- GENERADOR LFSR (4 DÍGITOS) ---")
semilla_input = input("Ingrese una semilla entera de 4 dígitos (ej. 4425): ")
try:
    estado = int(semilla_input)
    if estado <= 0 or estado > 9999:
        estado = 4425
except ValueError:
    estado = 4425

n = 200
numeros_u = []
semillas_historial = []

print(f"\n{'i':<5} {'Estado LFSR':<15} {'Cuatro Dígitos':<20} {'U_i (Normalizado)'}")
print("-" * 60)

for i in range(n):
    semillas_historial.append(estado)
    digitos_str = f"{estado % 10000:04d}"
    u_i = (estado % 10000) / 10000.0
    numeros_u.append(u_i)
    
    print(f"{i+1:<5} {estado:<15} {digitos_str:<20} {u_i:.4f}")
    
    bit = ((estado >> 0) ^ (estado >> 1) ^ (estado >> 2) ^ (estado >> 12)) & 1
    estado = ((estado >> 1) | (bit << 13)) % 10000
    if estado == 0:
        estado = 4425

# 2. Detección de Repetición
vistos = {}
inicio_ciclo = -1
fin_ciclo = -1

for idx, val in enumerate(semillas_historial):
    if val in vistos:
        inicio_ciclo = vistos[val]
        fin_ciclo = idx
        break
    vistos[val] = idx

print("\n" + "=" * 65)
print("     ANÁLISIS DE REPETICIÓN (PERIODO DE VIDA - LFSR)     ")
print("=" * 65)
if inicio_ciclo != -1:
    print(f"--> Los estados son ÚNICOS hasta la LÍNEA {fin_ciclo}.")
    print(f"--> En la LÍNEA {fin_ciclo + 1} se repite el valor {semillas_historial[fin_ciclo]:04d} (apareció en Línea {inicio_ciclo + 1}).")
else:
    print("--> No se detectaron repeticiones en las 200 líneas.")

# 3. Prueba de Autocorrelación
i_inicio = 1
m = 1
M = math.floor((n - i_inicio) / m) - 1

suma_productos = sum(numeros_u[k] * numeros_u[k + 1] for k in range(M + 1))
rho_im = (1 / (M + 1)) * suma_productos - 0.25
sigma_rho = math.sqrt((13 * M + 7) / (128 * (M + 1)**2))
z_autocorrelacion = rho_im / sigma_rho
z_critico = 1.96
cumple = abs(z_autocorrelacion) < z_critico

print("\n" + "=" * 65)
print("     EVALUACIÓN DE INDEPENDENCIA (AUTOCORRELACIÓN)     ")
print("=" * 65)
print(f"Autocorrelación (ρ_im):    {rho_im:.5f}")
print(f"Estadístico Z_0 calculado: {z_autocorrelacion:.4f}")
print(f"Valor crítico |Z_α/2|:     {z_critico}")
print("-" * 65)
if cumple:
    print("DECISIÓN FINAL: ✔️ ACEPTADO (Es Independiente)")
else:
    print("DECISIÓN FINAL: ✘ RECHAZADO (No es Independiente)")
print("=" * 65)

# 4. Gráfica protegida
if TIENE_MATPLOTLIB:
    try:
        fig, ax = plt.subplots(figsize=(6, 6))
        x_vals = numeros_u[:-1]
        y_vals = numeros_u[1:]

        ax.scatter(x_vals, y_vals, alpha=0.6, color='teal', edgecolors='k')

        simbolo = "✔️ ACEPTADO" if cumple else "✘ RECHAZADO"
        color_titulo = 'green' if cumple else 'red'

        ax.set_title(f"LFSR (4 Dígitos): Autocorrelación (U_i vs U_i+1)\nEstado del Método: {simbolo}", fontsize=14, fontweight='bold', color=color_titulo)
        ax.set_xlabel("U_i")
        ax.set_ylabel("U_{i+1}")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.grid(True, linestyle=':', alpha=0.6)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"\n[Aviso]: No se pudo mostrar la gráfica ({e})")