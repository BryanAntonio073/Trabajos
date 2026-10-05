import math

try:
    import matplotlib.pyplot as plt  # type: ignore[reportMissingModuleSource]
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

# 3. Prueba de Corridas Arriba y Abajo
secuencia_signos = []
for i in range(n - 1):
    secuencia_signos.append('+' if numeros_u[i + 1] >= numeros_u[i] else '-')

b = 1
for i in range(len(secuencia_signos) - 1):
    if secuencia_signos[i] != secuencia_signos[i + 1]:
        b += 1

mu_b = (2 * n - 1) / 3
var_b = (16 * n - 29) / 90
sigma_b = math.sqrt(var_b)
z_corridas = (b - mu_b) / sigma_b
z_critico = 1.96
cumple = abs(z_corridas) < z_critico

print("\n" + "=" * 65)
print("     EVALUACIÓN DE ALEATORIEDAD (CORRIDAS)     ")
print("=" * 65)
print(f"Corridas observadas (b):   {b}")
print(f"Estadístico Z_0 calculado: {z_corridas:.4f}")
print(f"Valor crítico |Z_α/2|:     {z_critico}")
print("-" * 65)
if cumple:
    print("DECISIÓN FINAL: ✔️ ACEPTADO (Es Aleatorio)")
else:
    print("DECISIÓN FINAL: ✘ RECHAZADO (No es Aleatorio)")
print("=" * 65)

# 4. Gráfica protegida
if TIENE_MATPLOTLIB:
    try:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(range(1, n + 1), numeros_u, marker='o', markersize=3, linestyle='-', color='purple', alpha=0.7)
        ax.axhline(0.5, color='gray', linestyle='--', label='Media (0.5)')

        simbolo = "✔️ ACEPTADO" if cumple else "✘ RECHAZADO"
        color_titulo = 'green' if cumple else 'red'

        ax.set_title(f"LFSR (4 Dígitos): Prueba de Corridas (Aleatoriedad)\nEstado del Método: {simbolo}", fontsize=14, fontweight='bold', color=color_titulo)
        ax.set_xlabel("Iteración (i)")
        ax.set_ylabel("Valor U_i")
        ax.legend()
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"\n[Aviso]: No se pudo mostrar la gráfica ({e})")