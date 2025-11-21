# Análisis de Perfiles Operativos en Cliente Industrial mediante Aprendizaje No Supervisado

## Descripción del Proyecto

Este proyecto aplica técnicas avanzadas de aprendizaje no supervisado para identificar **perfiles operativos** y **detectar anomalías** en datos de consumo eléctrico industrial de alta frecuencia (intervalos de 15 minutos). El análisis utiliza reducción de dimensionalidad y clustering para descubrir patrones ocultos en el comportamiento energético y la calidad de potencia.

### Objetivos Principales

1. **Identificar modos operativos** del cliente industrial mediante clustering temporal
2. **Comparar técnicas de reducción dimensional** (PCA vs UMAP) para visualización de patrones
3. **Detectar anomalías** en consumo y calidad de potencia
4. **Generar insights accionables** para optimización energética y mantenimiento predictivo

---

## Dataset

**Fuente:** Datos de medición eléctrica trifásica de cliente industrial  
**Periodo:** Octubre 2025  
**Registros:** 2,881 observaciones (intervalos de 15 minutos)  
**Variables:** 47 variables originales → 55 tras feature engineering → 46 features para modelado

### Variables Principales

- **Consumo energético:** KWHD, KVAHD, KWD, KVAD
- **Mediciones trifásicas:** Voltaje (VA, VB, VC), Corriente (IA, IB, IC)
- **Calidad de potencia:** THD (Total Harmonic Distortion) por fase, factor de potencia
- **Contexto temporal:** Fecha, hora, intervalo
- **Features ingenierizadas:** Factor de potencia, desbalances, promedios, variables temporales cíclicas

---

## Estructura del Proyecto

```
Proyecto no supervizado/
├── data/
│   └── set_Datos_electricos.csv          # Dataset original
├── notebooks/
│   ├── 01_EDA_Preprocesamiento.ipynb     # Exploración y limpieza de datos
│   ├── 02_Reduccion_Dimensionalidad.ipynb # PCA y UMAP
│   ├── 03_Clustering.ipynb                # K-means y DBSCAN
│   └── 04_Interpretacion_Conclusiones.ipynb # Insights y recomendaciones
├── src/
│   └── utils.py                           # Funciones auxiliares reutilizables
├── images/
│   └── (gráficos generados)
├── reports/
│   ├── Informe_Tecnico.md                # Informe completo
│   └── Presentacion_Ejecutiva.md         # Slides ejecutivos
├── requirements.txt                       # Dependencias Python
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Instalación y Reproducibilidad

### Prerequisitos

- Python 3.9+
- pip o conda

### Pasos de Instalación

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd "Proyecto no supervizado"

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar Jupyter
jupyter notebook
```

### Orden de Ejecución

Ejecutar los notebooks en secuencia:

1. `01_EDA_Preprocesamiento.ipynb` - Limpieza y feature engineering
2. `02_Reduccion_Dimensionalidad.ipynb` - PCA y UMAP
3. `03_Clustering.ipynb` - K-means y DBSCAN
4. `04_Interpretacion_Conclusiones.ipynb` - Análisis final

---

## 🔬 Metodología

### 1. Preprocesamiento

- Eliminación de 8 variables constantes/cero-varianza
- Feature engineering (16 nuevas variables):
  - Factor de potencia calculado
  - Desbalance de corriente y voltaje entre fases
  - THD promedios y KVAR aparente
  - Variables temporales cíclicas (sin/cos de hora, día semana, franja horaria)
- Detección de 389 outliers (13.5%) - mantenidos para análisis
- Normalización StandardScaler (media≈0, std≈1)

### 2. Reducción de Dimensionalidad

- **PCA:** 3 componentes principales explican 69.90% varianza
  - PC1 (38.65%): Consumo general vs THD
  - PC2 (21.18%): Niveles de voltaje
  - PC3 (10.07%): Desbalance de corriente
- **UMAP:** Proyección no-lineal revela 5-6 clusters naturales
- Visualizaciones comparativas en espacios 2D y 3D

### 3. Clustering

- **K-means (k=2):** Silhouette=0.3065
  - Cluster 0 (52.3%): Alta carga operativa (21 kWh)
  - Cluster 1 (47.7%): Baja carga / reposo (7 kWh)
- **DBSCAN (eps=3.0, min_samples=50):** Silhouette=0.3408
  - 3 clusters + 32.3% anomalías detectadas
  - Mejor separación de patrones complejos
- Evaluación con Silhouette, Davies-Bouldin, Calinski-Harabasz

### 4. Interpretación

- Perfiles operativos definidos por consumo y calidad eléctrica
- Patrones temporales: Alta carga 8:00-20:00, baja carga 0:00-6:00
- Identificación de oportunidades de mejora en calidad de potencia

---

## 📈 Resultados Principales

### Perfiles Operativos Identificados (K-means)

| Perfil | % Datos | Consumo Medio | Factor Potencia | THD | Horario Típico |
|--------|---------|---------------|-----------------|-----|----------------|
| **Alta Carga Operativa** | 52.3% | 21.03 kWh | 0.98 | 0.16 | 8:00-20:00 (diurno) |
| **Baja Carga / Reposo** | 47.7% | 6.96 kWh | 0.99 | 0.36 | 0:00-6:00 (nocturno) |

### Perfiles Operativos Identificados (DBSCAN)

| Perfil | % Datos | Consumo Medio | Características |
|--------|---------|---------------|-----------------|
| **Pico Máximo de Carga** | 11.3% | 22.39 kWh | Máxima demanda, THD bajo, 11:00-14:00 |
| **Operación Mínima** | 38.8% | 6.42 kWh | Consumo base, THD alto, madrugada |
| **Carga Media Estable** | 17.6% | 17.71 kWh | Operación normal, 5:00-10:00 |
| **Anomalías** | 32.3% | Variable | Eventos atípicos, requieren investigación |

### Insights Accionables

1. **Optimización de Calidad Eléctrica**
   - 47.7% observaciones con factor de potencia bajo durante reposo
   - Recomendación: Instalar bancos de capacitores

2. **Gestión de THD**
   - THD >30% en 47.7% de observaciones (perfil baja carga)
   - Recomendación: Evaluar filtros armónicos

3. **Desbalance de Fases**
   - 13.8% observaciones con desbalance >20%
   - Recomendación: Redistribuir cargas entre fases

4. **Gestión de Demanda**
   - Pico identificado: 8:00-14:00 (21-22 kWh)
   - Oportunidad: Diferir cargas no críticas a horarios valle

5. **Investigación de Anomalías**
   - 931 eventos atípicos detectados (32.3%)
   - Acción: Auditoría detallada para identificar causas

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.9+**
- **Pandas & NumPy:** Manipulación de datos
- **Scikit-learn:** PCA, K-means, DBSCAN, métricas
- **UMAP:** Reducción dimensional no lineal
- **Matplotlib, Seaborn, Plotly:** Visualizaciones
- **Jupyter Notebook:** Análisis interactivo

---

## 📚 Referencias

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [UMAP Documentation](https://umap-learn.readthedocs.io/)
- McInnes, L., Healy, J., & Melville, J. (2018). UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. arXiv:1802.03426
- Ester, M., et al. (1996). A density-based algorithm for discovering clusters. KDD-96 Proceedings

---

## 👤 Autor

**Proyecto Final - Aprendizaje No Supervisado**  
Fecha: Noviembre 2025

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
