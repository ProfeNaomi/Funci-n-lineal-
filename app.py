import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página estilo "Premium"
st.set_page_config(page_title="Simulador de Función Lineal", layout="wide")

st.title("📉 Simulador Interactivo de Función Lineal")
st.markdown("---")

# --- BARRA LATERAL (Controles) ---
st.sidebar.header("Configuración de la Función")
st.sidebar.info("Ajusta los parámetros para ver los cambios en tiempo real.")

# 1. Pendiente (m)
m = st.sidebar.slider("Pendiente (m)", min_value=-10.0, max_value=10.0, value=1.0, step=0.1)

# 2. Coeficiente de posición (n)
n = st.sidebar.slider("Coeficiente de posición (n)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)

# --- OPCIONES ADICIONALES ---
st.sidebar.subheader("Opciones Adicionales")
mostrar_puntos = st.sidebar.checkbox("Mostrar puntos clave", value=True)
color_linea = st.sidebar.color_picker("Color de la línea", "#1E90FF")

# --- CÁLCULOS MATEMÁTICOS ---
# Definir el rango del eje x (de -10 a 10)
x = np.linspace(-10, 10, 400)
# Calcular la función y = mx + n
y = m * x + n

# --- LÓGICA DEL GRÁFICO (Estilo GeoGebra) ---
fig, ax = plt.subplots(figsize=(10, 8))

# Dibujar la función
ax.plot(x, y, color=color_linea, linewidth=3, label=f'y = {m}x + {n}')

# Configurar el estilo de los ejes (Eje X e Y en el centro)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

# Ajustar los límites para que se vea como un plano cartesiano
ax.set_xlim([-11, 11])
ax.set_ylim([-11, 11])
ax.grid(True, linestyle='--', alpha=0.6)

# Marcar puntos clave si la opción está activada
if mostrar_puntos:
    # Punto de corte con el eje Y (0, n)
    ax.scatter(0, n, color='red', s=50, zorder=5, label=f'Corte eje Y: (0, {n})')
    # Punto de corte con el eje X (-n/m, 0) si m != 0
    if m != 0:
        x_intercept = -n/m
        ax.scatter(x_intercept, 0, color='green', s=50, zorder=5, label=f'Corte eje X: ({x_intercept:.2f}, 0)')

ax.legend()

# --- MOSTRAR RESULTADOS EN LA WEB ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Análisis Matemático")
    st.write(f"**Ecuación:** $y = {m}x + {n}$")
    st.write(f"**Tipo de pendiente:** {'Creciente' if m > 0 else 'Decreciente' if m < 0 else 'Constante'}")
    st.latex(rf"f(x) = {m}x + {n}")

with col2:
    st.pyplot(fig)

st.markdown("---")
st.write("Creado por Naomi y su equipo para fines pedagógicos.")
