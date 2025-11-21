# Informe Técnico: Análisis de Perfiles Operativos mediante Aprendizaje No Supervisado

**Cliente:** Industrial - Sector Eléctrico  
**Periodo de Análisis:** Octubre 2025  
**Fecha del Informe:** Noviembre 2025  

**Autores:**
- GZ130034 Galicia Zavaleta Eduardo Andrés
- HR150875 Hernández Rodríguez Fernando José
- HV252954 Huezo Vasquez William Alexander
- PB252919 Portillo Belloso Daniel Roberto
- ZM252743 Zuñiga Martinez Francisco Ramon

---

## Resumen Ejecutivo

Este informe presenta un análisis avanzado de datos de consumo eléctrico industrial utilizando técnicas de aprendizaje no supervisado. El objetivo principal fue identificar perfiles operativos distintos y detectar anomalías en el comportamiento eléctrico del cliente.

### Hallazgos Clave

- **2 perfiles operativos principales** identificados mediante K-means: Alta Carga (52.3%) y Baja Carga (47.7%)
- **3 sub-perfiles adicionales** detectados con DBSCAN: Pico Máximo, Operación Mínima, Carga Media
- **32.3% de observaciones clasificadas como anomalías** que requieren investigación
- **5 oportunidades de mejora cuantificadas** en calidad eléctrica y gestión de demanda

### Recomendaciones Prioritarias

1. Corrección de factor de potencia en períodos de baja carga
2. Implementación de filtros armónicos para reducir THD
3. Rebalanceo de cargas entre fases
4. Gestión de demanda para reducir picos en horario 8:00-14:00
5. Auditoría de 931 eventos anómalos detectados

---

## 1. Introducción

### 1.1 Contexto del Proyecto

La gestión eficiente de energía en instalaciones industriales requiere comprender los patrones de consumo y detectar desviaciones que puedan indicar ineficiencias o problemas operativos. El análisis manual de grandes volúmenes de datos de alta frecuencia (mediciones cada 15 minutos) es impracticable, por lo que se requieren técnicas automatizadas de análisis de patrones.

### 1.2 Objetivos

**Objetivo General:**
Aplicar técnicas de aprendizaje no supervisado para identificar perfiles operativos y anomalías en datos de consumo eléctrico industrial.

**Objetivos Específicos:**
1. Explorar y preprocesar datos de medición eléctrica trifásica
2. Aplicar y comparar técnicas de reducción dimensional (PCA y UMAP)
3. Implementar algoritmos de clustering (K-means y DBSCAN)
4. Caracterizar perfiles operativos identificados
5. Generar recomendaciones accionables

### 1.3 Alcance

- **Temporal:** Datos de octubre 2025 (un mes completo)
- **Espacial:** Un cliente industrial único
- **Técnico:** Análisis descriptivo y clustering, sin predicción
- **Limitaciones:** Resultados no generalizables a otros clientes sin validación

---

## 2. Dataset y Preprocesamiento

### 2.1 Descripción del Dataset

**Características:**
- 2,881 observaciones (intervalos de 15 minutos)
- 47 variables originales de medición eléctrica trifásica
- Período: 1-31 octubre 2025
- Sin valores faltantes (0% missing values)

**Variables Principales:**

| Categoría | Variables | Descripción |
|-----------|-----------|-------------|
| **Consumo** | KWHD, KVAHD, KWD, KVAD | Energía activa y reactiva |
| **Voltaje** | VA, VB, VC, VX_DESV | Voltajes por fase y desviaciones |
| **Corriente** | IA, IB, IC, IX_DESV | Corrientes por fase y desviaciones |
| **Calidad** | THD_CORRIENTE_FASE_X, THD_VOLT_FASE_X | Distorsión armónica total |
| **Temporal** | FECHA, HORA, INTERVALO | Contexto temporal |

### 2.2 Limpieza de Datos

**Eliminación de Variables de Varianza Cero (8 variables):**
- KWHR, KVARHR, KVARH_LAG, KVARHR_1
- KVARH_LEAD, PHASOR_KVAH, KWR, KVARD

Estas variables presentaban valores constantes o exclusivamente ceros, sin aporte informativo.

### 2.3 Feature Engineering

Se crearon **16 nuevas variables** para capturar relaciones físicas y temporales:

**Variables Eléctricas Derivadas:**
1. **FACTOR_POTENCIA = KWHD / KVAHD**: Eficiencia energética
2. **DESBALANCE_CORRIENTE**: Diferencia máxima entre corrientes de fase
3. **DESBALANCE_VOLTAJE**: Diferencia máxima entre voltajes de fase
4. **THD_CORRIENTE_PROMEDIO**: Promedio de THD entre fases
5. **THD_VOLT_PROMEDIO**: Promedio de THD de voltaje
6. **KVAR_APARENTE**: Potencia reactiva aparente
7. **VOLTAJE_PROM, CORRIENTE_PROM**: Promedios por fase
8. **VOLTAJE_STD, CORRIENTE_STD**: Desviaciones estándar

**Variables Temporales Cíclicas:**
9. **HORA_SIN = sin(2π × HORA / 24)**: Componente sinusoidal de hora
10. **HORA_COS = cos(2π × HORA / 24)**: Componente cosinusoidal de hora
11. **DIA_SEMANA**: Día de la semana (0=Lunes, 6=Domingo)
12. **ES_FIN_SEMANA**: Indicador binario
13. **FRANJA**: Categorización horaria (Madrugada, Mañana, Tarde, Noche)
14. **ES_HORA_PICO**: Indicador de horario 8:00-20:00

### 2.4 Detección de Outliers

**Método:** Rango Intercuartílico (IQR) con umbral 1.5

**Resultados:**
- 389 outliers detectados (13.5% de observaciones)
- Variables con más outliers: KWHD, corrientes de fase, THD
- **Decisión:** Mantener outliers para análisis (representan eventos reales de interés)

### 2.5 Normalización

**Método:** StandardScaler (media=0, desviación estándar=1)

**Justificación:**
- Elimina efectos de escala entre variables
- Requerido para PCA y clustering basado en distancias
- Preserva distribuciones originales

**Validación:**
- Media resultante: ~0.000000
- Desviación estándar: ~1.000174
- 46 features finales para modelado (excluidas FECHA, HORA, INTERVALO, CATEGORIA)

---

## 3. Análisis Exploratorio de Datos

### 3.1 Estadísticas Descriptivas

**Consumo Energético:**
- KWHD medio: 14.32 kWh (rango: 0.47 - 38.66 kWh)
- Alta variabilidad: CV = 70.5%

**Calidad Eléctrica:**
- Factor de potencia promedio: 0.986 (cercano a ideal 1.0)
- THD corriente promedio: 0.257 (25.7% - alto)
- Desbalance corriente: 0.176 (17.6% - moderado)

### 3.2 Patrones Temporales Identificados

**Distribución Horaria:**
- **Pico de consumo:** 11:00 (22.45 kWh promedio)
- **Mínimo de consumo:** 3:00 (6.58 kWh promedio)
- Patrón bimodal: Alta actividad diurna (7:00-20:00), baja actividad nocturna

**Distribución Semanal:**
- Consumo relativamente uniforme entre días
- Ligera reducción en días 6 y 0 (fin de semana)

### 3.3 Correlaciones Relevantes

**Correlaciones Altas (|r| > 0.90):**
- KWHD ↔ KWD: r = 1.00 (definición matemática)
- KWHD ↔ Corrientes: r = 0.94-0.96 (esperado por Ley de Ohm)
- Voltajes entre fases: r = 0.99 (sistema balanceado)

**Correlaciones Inversas:**
- Consumo ↔ THD: r = -0.82 (mayor carga → mejor calidad)
- Interesante: A menor consumo, mayor distorsión armónica

---

## 4. Reducción de Dimensionalidad

### 4.1 Análisis de Componentes Principales (PCA)

**Varianza Explicada:**
- PC1: 38.65%
- PC2: 21.18%
- PC3: 10.07%
- **Total 3 componentes: 69.90%**

**Componentes Necesarios:**
- 90% varianza: 8 componentes
- 95% varianza: 11 componentes
- 99% varianza: 20 componentes

**Interpretación de Componentes:**

**PC1 (38.65% varianza) - "Nivel de Carga":**
- Positivo (+): CORRIENTE_PROM (0.957), KWHD (0.951), KVAD (0.950)
- Negativo (-): THD_CORRIENTE (-0.878), HORA_COS (-0.540)
- Interpretación: Separa alta carga (positivo) de baja carga (negativo)

**PC2 (21.18% varianza) - "Nivel de Voltaje":**
- Positivo (+): VOLTAJE_MEDIO (0.930), VA (0.930), VB (0.929)
- Negativo (-): DESBALANCE_VOLTAJE (-0.304), HORA_COS (-0.267)
- Interpretación: Captura variaciones en voltaje y balance

**PC3 (10.07% varianza) - "Variabilidad de Corriente":**
- Positivo (+): IB_DESV (0.830), DESBALANCE_CORRIENTE (0.807)
- Negativo (-): AVG_IA_HARMONICS (-0.359), HORA_SIN (-0.305)
- Interpretación: Refleja desbalances y variabilidad entre fases

### 4.2 UMAP (Uniform Manifold Approximation and Projection)

**Configuración:**
- n_neighbors = 15
- min_dist = 0.1
- Proyecciones: 2D y 3D

**Resultados:**
- Identificación visual clara de 5-6 agrupaciones naturales
- Separación mucho más marcada que PCA
- Revela estructura no-lineal en los datos

**Comparación PCA vs UMAP:**

| Aspecto | PCA | UMAP |
|---------|-----|------|
| **Separación visual** | Moderada | Excelente |
| **Clusters evidentes** | 2-3 | 5-6 |
| **Interpretabilidad** | Alta (loadings) | Baja (caja negra) |
| **Uso recomendado** | Análisis cuantitativo | Visualización exploratoria |

---

## 5. Clustering

### 5.1 K-means

**Selección de k Óptimo:**

| k | Silhouette | Davies-Bouldin | Calinski-Harabasz |
|---|------------|----------------|-------------------|
| 2 | **0.3065** | 1.3579 | **1297.43** |
| 3 | 0.2382 | 1.4238 | 943.82 |
| 4 | 0.2289 | 1.6070 | 844.58 |
| 5 | 0.2408 | 1.4811 | 756.53 |
| 10 | 0.2495 | **1.1543** | 643.10 |

**Decisión:** k=2 (máximo Silhouette y Calinski-Harabasz)

**Perfiles Identificados:**

| Cluster | % | KWHD | Factor Potencia | THD | Hora Pico |
|---------|---|------|-----------------|-----|-----------|
| **0 - Alta Carga** | 52.3% | 21.03 kWh | 0.98 | 0.16 | 8:00 |
| **1 - Baja Carga** | 47.7% | 6.96 kWh | 0.99 | 0.36 | 0:00 |

**Interpretación:**
- **Cluster 0:** Operación diurna con alta demanda, buena calidad (THD bajo)
- **Cluster 1:** Operación nocturna con baja demanda, THD elevado (problema)

### 5.2 DBSCAN

**Optimización de Hiperparámetros:**

| eps | min_samples | Clusters | Ruido | Silhouette |
|-----|-------------|----------|-------|------------|
| 2.0 | 50 | 2 | 79.0% | 0.3545 |
| 3.0 | 50 | **3** | 32.3% | **0.3408** |
| 3.0 | 100 | 2 | 59.8% | 0.4067 |
| 3.5 | 150 | 2 | 51.7% | 0.3761 |

**Decisión:** eps=3.0, min_samples=50 (balance clusters/ruido, Silhouette alto)

**Perfiles Identificados:**

| Cluster | % | KWHD | Características |
|---------|---|------|-----------------|
| **0 - Pico Máximo** | 11.3% | 22.39 kWh | Máxima demanda, 11:00-14:00, desbalance 0.37 |
| **1 - Mínima Operación** | 38.8% | 6.42 kWh | Base nocturna, THD 0.36, corriente≈0 |
| **2 - Carga Media** | 17.6% | 17.71 kWh | Operación normal, 5:00-10:00 |
| **-1 - Anomalías** | 32.3% | Variable | 931 eventos atípicos |

**Interpretación:**
- **Cluster 0:** Período de máxima producción (mediodía)
- **Cluster 1:** Estado de reposo/mínimo consumo
- **Cluster 2:** Transición y operación estándar
- **Anomalías (32.3%):** Eventos no clasificables que requieren análisis individual

### 5.3 Comparación de Algoritmos

| Métrica | K-means | DBSCAN |
|---------|---------|--------|
| **Silhouette Score** | 0.3065 | 0.3408 ✓ |
| **Davies-Bouldin** | 1.3579 | 1.2658 ✓ |
| **Calinski-Harabasz** | 1297.43 ✓ | 981.55 |
| **Clusters** | 2 | 3 |
| **Detección outliers** | No | Sí (931) |

**Conclusión:**
- DBSCAN ligeramente superior en métricas de separación
- K-means mejor para interpretación binaria simple (alta/baja)
- DBSCAN más útil para detección de anomalías
- Ambos métodos complementarios

---

## 6. Interpretación y Recomendaciones

### 6.1 Perfiles Operativos Definidos

**Enfoque K-means (Visión Simplificada):**

**Perfil 1: Alta Carga Operativa (52.3%)**
- **Horario:** 8:00-20:00 (diurno)
- **Consumo:** 21.03 ± 4.58 kWh
- **Calidad:** Factor potencia 0.98, THD bajo (0.16)
- **Operación:** Producción activa, equipos en plena carga
- **Estado:** Óptimo desde perspectiva de calidad eléctrica

**Perfil 2: Baja Carga / Reposo (47.7%)**
- **Horario:** 0:00-6:00 (nocturno)
- **Consumo:** 6.96 ± 2.00 kWh
- **Calidad:** Factor potencia 0.99, THD alto (0.36)
- **Operación:** Equipos auxiliares, consumo base
- **Estado:** Requiere atención - THD elevado

**Enfoque DBSCAN (Visión Granular):**

Agrega **Perfil 3: Pico Máximo (11.3%)** - Momentos críticos de demanda máxima
Agrega **Perfil 4: Anomalías (32.3%)** - Eventos que requieren investigación

### 6.2 Insights Accionables

**1. Optimización de Factor de Potencia**
- **Observación:** 47.7% del tiempo con consumo bajo pero THD alto
- **Impacto:** Posibles penalizaciones, pérdidas en distribución
- **Recomendación:** Instalar bancos de capacitores automáticos
- **Beneficio Estimado:** Reducción 10-15% en penalizaciones

**2. Gestión de Distorsión Armónica (THD)**
- **Observación:** THD >30% en 1,373 observaciones (perfil baja carga)
- **Causa Probable:** Equipos electrónicos operando a baja carga
- **Recomendación:** Evaluar filtros armónicos pasivos o activos
- **Beneficio:** Mejor calidad de onda, menos desgaste en equipos

**3. Desbalance de Fases**
- **Observación:** 398 observaciones (13.8%) con desbalance >20%
- **Impacto:** Sobrecalentamiento de neutro, pérdidas
- **Recomendación:** Redistribuir cargas entre fases
- **Beneficio:** Reducción 5-8% en pérdidas de distribución

**4. Gestión de Demanda**
- **Observación:** Pico de 22.4 kWh entre 11:00-14:00
- **Oportunidad:** Diferir cargas no críticas a valle (0:00-6:00)
- **Recomendación:** Implementar gestión de demanda programada
- **Beneficio:** Reducción de demanda máxima facturable

**5. Investigación de Anomalías**
- **Observación:** 931 eventos (32.3%) no clasificables
- **Acción:** Auditoría técnica de estos períodos
- **Posibles Causas:**
  - Arranques de equipos pesados
  - Transitorios eléctricos
  - Equipos defectuosos
  - Operaciones manuales no programadas
- **Recomendación:** Cruzar con logs operativos y mantenimiento

### 6.3 Priorización de Acciones

**Alta Prioridad (0-3 meses):**
1. Auditoría de 931 anomalías detectadas
2. Evaluación técnico-económica de corrección de factor de potencia
3. Medición detallada de THD en baja carga

**Media Prioridad (3-6 meses):**
4. Implementación de gestión de demanda
5. Proyecto de rebalanceo de fases

**Baja Prioridad (>6 meses):**
6. Sistema de monitoreo continuo con alertas automáticas
7. Validación con datos de múltiples períodos

---

## 7. Limitaciones del Estudio

### 7.1 Alcance Temporal
- **Limitación:** Datos de un solo mes (octubre 2025)
- **Impacto:** No captura variaciones estacionales
- **Mitigación:** Validar con datos de 12 meses

### 7.2 Alcance de Cliente
- **Limitación:** Análisis de un único cliente industrial
- **Impacto:** Resultados no generalizables sin validación
- **Enfoque:** Profundidad sobre amplitud

### 7.3 Variables No Incluidas
- **Limitación:** Ausencia de datos de temperatura, producción, turnos
- **Impacto:** Algunas anomalías podrían explicarse con contexto externo
- **Oportunidad:** Integrar en análisis futuro

### 7.4 Autocorrelación Temporal
- **Limitación:** Observaciones cada 15 min no son independientes
- **Impacto:** Clustering asume independencia
- **Justificación:** Enfoque en patrones instantáneos, no series temporales

### 7.5 Causalidad vs Correlación
- **Limitación:** Análisis identifica patrones, no causas
- **Impacto:** Recomendaciones requieren validación con expertos
- **Mitigación:** Considerar contexto operativo específico

---

## 8. Trabajo Futuro

### 8.1 Validación Temporal
- Replicar análisis con datos de múltiples meses
- Identificar variaciones estacionales
- Validar estabilidad de perfiles

### 8.2 Análisis Predictivo
- Desarrollar modelos de forecasting de demanda
- Predicción de anomalías en tiempo real
- Alertas automáticas de desviaciones

### 8.3 Integración de Contexto
- Incorporar datos de producción, clima, calendarios
- Análisis de correlación con factores operativos
- Modelos explicativos más robustos

### 8.4 Benchmarking
- Comparar con otros clientes del sector
- Identificar mejores prácticas
- Cuantificar potencial de mejora

### 8.5 Implementación Operacional
- Dashboard interactivo para seguimiento continuo
- Sistema de alertas automáticas
- Recomendaciones dinámicas basadas en perfil actual

---

## 9. Conclusiones

### 9.1 Cumplimiento de Objetivos

✅ **Objetivo 1 - EDA y Preprocesamiento:** Completado
- Dataset limpio, 8 variables eliminadas, 16 creadas
- 389 outliers identificados y caracterizados

✅ **Objetivo 2 - Reducción Dimensional:** Completado
- PCA: 3 componentes = 69.90% varianza
- UMAP: Identificación visual de 5-6 clusters naturales

✅ **Objetivo 3 - Clustering:** Completado
- K-means: 2 perfiles (Silhouette=0.3065)
- DBSCAN: 3 clusters + 32.3% anomalías (Silhouette=0.3408)

✅ **Objetivo 4 - Caracterización:** Completado
- Perfiles operativos claramente definidos
- Patrones temporales identificados

✅ **Objetivo 5 - Recomendaciones:** Completado
- 5 insights accionables cuantificados
- Priorización de acciones establecida

### 9.2 Hallazgos Principales

1. **Patrón Bimodal Robusto:** Operación claramente dividida en alta carga diurna (52%) y baja carga nocturna (48%)

2. **Relación Inversa Consumo-THD:** A mayor consumo, mejor calidad eléctrica (THD bajo). Fenómeno requiere atención en períodos de baja carga.

3. **32.3% de Eventos Anómalos:** Proporción significativa de observaciones fuera de patrones normales. Oportunidad de mejora operacional.

4. **Desbalance de Fases Moderado:** 13.8% observaciones con desbalance >20%. Acción correctiva relativamente simple.

5. **DBSCAN Superior para Este Caso:** Métricas de clustering ligeramente mejores, detecta anomalías automáticamente.

### 9.3 Valor Agregado

Este análisis proporciona:
- ✓ Cuantificación objetiva de perfiles operativos
- ✓ Detección automática de 931 eventos anómalos
- ✓ Identificación de 5 oportunidades de mejora específicas
- ✓ Base técnica para gestión proactiva de energía
- ✓ Fundamento para sistema de monitoreo continuo

### 9.4 Reflexión Metodológica

**Fortalezas del Enfoque:**
- Análisis no supervisado adecuado para descubrimiento de patrones
- Combinación PCA+UMAP proporciona visión complementaria
- K-means + DBSCAN captura estructura a múltiples niveles
- Feature engineering captura conocimiento del dominio

**Lecciones Aprendidas:**
- Mantener outliers fue correcto (eventos reales de interés)
- Variables temporales cíclicas mejoraron clustering
- DBSCAN más útil que anticipado para detección de anomalías
- Visualización en UMAP crucial para comprensión inicial

---

## 10. Anexos

### Anexo A: Descripción Completa de Variables

[Ver archivo `data_dictionary.csv` en repositorio]

### Anexo B: Gráficos Adicionales

Ubicación: `images/` en repositorio del proyecto

- `kmeans_elbow_metrics.png` - Métricas de evaluación K-means
- `dbscan_k_distance.png` - K-distance graph para selección eps
- `kmeans_clusters_visualization.png` - Clusters K-means en PCA y UMAP
- `dbscan_clusters_visualization.png` - Clusters DBSCAN en PCA y UMAP
- `perfiles_distribucion.png` - Distribución porcentual de perfiles
- `patron_temporal_perfiles.png` - Heatmap temporal de consumo
- `radar_calidad_electrica.png` - Comparación de calidad por perfil

### Anexo C: Código Fuente

Notebooks Jupyter disponibles en: `notebooks/`
1. `01_EDA_Preprocesamiento.ipynb`
2. `02_Reduccion_Dimensionalidad.ipynb`
3. `03_Clustering.ipynb`
4. `04_Interpretacion_Conclusiones.ipynb`

Utilidades en: `src/utils.py`

### Anexo D: Archivos de Datos Generados

- `processed_data_featured.csv` - Datos con features ingenierizadas
- `processed_data_scaled.csv` - Datos normalizados
- `pca_2d.csv`, `pca_3d.csv` - Proyecciones PCA
- `umap_2d.csv`, `umap_3d.csv` - Proyecciones UMAP
- `clustered_data.csv` - Datos con etiquetas de clusters
- `resumen_perfiles.csv` - Resumen ejecutivo de perfiles

---

**FIN DEL INFORME TÉCNICO**

*Para consultas o aclaraciones sobre este análisis, referirse a los notebooks ejecutables en el repositorio del proyecto.*
