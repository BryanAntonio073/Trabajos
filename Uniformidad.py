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
    
    # Formato de 4 dígitos (relleno con ceros a la izquierda)
    digitos_str = f"{estado % 10000:04d}"
    u_i = (estado % 10000) / 10000.0
    numeros_u.append(u_i)
    
    print(f"{i+1:<5} {estado:<15} {digitos_str:<20} {u_i:.4f}")
    
    # Retroalimentación LFSR (14 bits: Taps 14, 13, 12, 2)
    bit = ((estado >> 0) ^ (estado >> 1) ^ (estado >> 2) ^ (estado >> 12)) & 1
    estado = ((estado >> 1) | (bit << 13)) % 10000
    if estado == 0:
        estado = 4425  # Evitar estado muerto en cero

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

# 3. Prueba Chi-Cuadrada
k = 10
frecuencia_esperada = n / k
frecuencias_observadas = [0] * k

for u in numeros_u:
    idx = int(u * k)
    if idx == k:
        idx = k - 1
    frecuencias_observadas[idx] += 1

chi_calculado = sum(((o - frecuencia_esperada) ** 2) / frecuencia_esperada for o in frecuencias_observadas)
chi_critico = 16.919
cumple = chi_calculado < chi_critico

print("\n" + "=" * 65)
print("     EVALUACIÓN DE UNIFORMIDAD (CHI-CUADRADA)     ")
print("=" * 65)
print(f"Estadístico χ² calculado:  {chi_calculado:.4f}")
print(f"Valor crítico χ² (α=0.05): {chi_critico:.3f}")
print("-" * 65)
if cumple:
    print("DECISIÓN FINAL: ✔️ ACEPTADO (Es Uniforme)")
else:
    print("DECISIÓN FINAL: ✘ RECHAZADO (No es Uniforme)")
print("=" * 65)

# 4. Gráfica protegida
if TIENE_MATPLOTLIB:
    try:
        fig, ax = plt.subplots(figsize=(9, 5))
        intervalos = [f"[{i/10:.1f}-{(i+1)/10:.1f})" for i in range(k)]
        ax.bar(intervalos, frecuencias_observadas, color='skyblue', edgecolor='black', label='Frecuencia Observada')
        ax.axhline(frecuencia_esperada, color='red', linestyle='--', linewidth=2, label=f'Esperada ({frecuencia_esperada})')

        simbolo = "✔️ ACEPTADO" if cumple else "✘ RECHAZADO"
        color_titulo = 'green' if cumple else 'red'

        ax.set_title(f"LFSR (4 Dígitos): Prueba Chi-Cuadrada (Uniformidad)\nEstado del Método: {simbolo}", fontsize=14, fontweight='bold', color=color_titulo)
        ax.set_xlabel("Intervalos")
        ax.set_ylabel("Frecuencia de Números U_i")
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"\n[Aviso]: No se pudo mostrar la gráfica ({e})")