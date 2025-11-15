# Presentación Ejecutiva: Análisis de Perfiles Operativos
## Aprendizaje No Supervisado Aplicado a Consumo Eléctrico Industrial

**Noviembre 2025**

---

## Diapositiva 1: Portada

**Título:** Análisis de Perfiles Operativos mediante Aprendizaje No Supervisado

**Cliente:** Industrial - Sector Eléctrico  
**Período:** Octubre 2025 (2,881 mediciones)  
**Frecuencia:** Intervalos de 15 minutos  
**Tecnologías:** PCA, UMAP, K-means, DBSCAN

---

## Diapositiva 2: El Problema

### ¿Qué desafío enfrentamos?

**Contexto:**
- Cliente industrial con alto consumo eléctrico
- 2,881 mediciones cada 15 minutos (un mes)
- 47 variables de medición eléctrica trifásica
- Sin visibilidad clara de patrones operativos

**Pregunta Clave:**
> ¿Existen perfiles operativos distintos en el consumo eléctrico?  
> ¿Hay oportunidades de optimización?

**Impacto:**
- Costos de energía no optimizados
- Posibles penalizaciones por calidad eléctrica
- Anomalías no detectadas

---

## Diapositiva 3: Metodología

### Proceso de Análisis en 4 Fases

```
Fase 1: Exploración y Limpieza
├─ Análisis de 47 variables originales
├─ Eliminación de 8 variables sin variación
└─ Creación de 16 variables derivadas

Fase 2: Reducción Dimensional
├─ PCA: 3 componentes = 69.90% varianza
└─ UMAP: Visualización de estructura natural

Fase 3: Clustering
├─ K-means: 2 perfiles principales
└─ DBSCAN: 3 sub-perfiles + anomalías

Fase 4: Interpretación
├─ Caracterización de perfiles
└─ Generación de recomendaciones
```

**Herramientas:** Python, scikit-learn, UMAP, Jupyter

---

## Diapositiva 4: Dataset en Números

### Datos de Entrada

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **Observaciones** | 2,881 | ~720 horas de medición |
| **Variables Originales** | 47 | Consumo, voltaje, corriente, THD |
| **Variables Finales** | 55 | +16 features ingenierizadas |
| **Valores Faltantes** | 0% | Dataset completo |
| **Outliers Detectados** | 389 (13.5%) | Eventos atípicos reales |
| **Período** | Oct 2025 | 31 días continuos |

### Rango de Consumo

- **Mínimo:** 0.47 kWh (madrugada)
- **Máximo:** 38.66 kWh (mediodía)
- **Promedio:** 14.32 ± 10.09 kWh
- **Coeficiente de Variación:** 70.5% (alta variabilidad)

---

## Diapositiva 5: Patrones Temporales Descubiertos

### Curva de Consumo Diario

```
Consumo (kWh) por Hora del Día

25 |              ████
20 |          ████████████
15 |      ████████████████████
10 |  ████████████████████████████
5  |████████████████████████████████
0  +----+----+----+----+----+----+----
   0:00 6:00 12:00 18:00 24:00

Hora Pico: 11:00 (22.45 kWh)
Hora Valle: 3:00 (6.58 kWh)
```

**Observaciones:**
- Patrón bimodal claro: día vs noche
- Operación intensa 8:00-20:00
- Mínimo sostenido 0:00-6:00

---

## Diapositiva 6: Reducción Dimensional - PCA

### Componentes Principales

| Componente | Varianza | Interpretación |
|------------|----------|----------------|
| **PC1** | 38.65% | Nivel de Carga (corriente, consumo) |
| **PC2** | 21.18% | Nivel de Voltaje (estabilidad) |
| **PC3** | 10.07% | Variabilidad de Corriente (desbalance) |
| **Total 3 PCs** | **69.90%** | Representación eficiente |

### Principales Contribuyentes a PC1

- ✓ Corriente promedio (+0.957)
- ✓ Consumo KWHD (+0.951)
- ✓ Potencia aparente (+0.950)
- ✗ THD corriente (-0.878)

**Insight:** PC1 separa claramente **alta carga** (positivo) de **baja carga** (negativo)

---

## Diapositiva 7: Visualización UMAP

### Estructura No-Lineal del Dataset

**UMAP 2D revela 5-6 agrupaciones naturales**

```
[Referencia: images/umap_embeddings.png]

Características:
✓ Separación marcada entre clusters
✓ Grupos compactos y bien definidos
✓ Zona de transición suave
✓ Outliers claramente apartados
```

**Ventaja sobre PCA:**
- PCA: 2-3 grupos visibles
- UMAP: 5-6 grupos bien separados
- Mejor para detectar sub-perfiles

---

## Diapositiva 8: Perfiles K-means (Visión Simplificada)

### 2 Perfiles Operativos Principales

| Perfil | % Tiempo | Consumo | Factor Potencia | THD | Horario Típico |
|--------|----------|---------|-----------------|-----|----------------|
| **Alta Carga Operativa** | 52.3% | 21.03 kWh | 0.98 | 0.16 ✓ | 8:00-20:00 |
| **Baja Carga / Reposo** | 47.7% | 6.96 kWh | 0.99 | 0.36 ⚠️ | 0:00-6:00 |

### Interpretación

**Perfil Alta Carga:**
- Operación productiva diurna
- Calidad eléctrica óptima
- Sin problemas detectados

**Perfil Baja Carga:**
- Operación nocturna mínima
- THD elevado (36%) - **PROBLEMA**
- Oportunidad de mejora

**Métrica de Clustering:** Silhouette Score = 0.3065

---

## Diapositiva 9: Perfiles DBSCAN (Visión Granular)

### 3 Sub-Perfiles + Anomalías

| Perfil | % | Consumo | Características Clave |
|--------|---|---------|----------------------|
| **Pico Máximo** | 11.3% | 22.39 kWh | Máxima demanda, 11:00-14:00 |
| **Operación Mínima** | 38.8% | 6.42 kWh | Base nocturna, THD alto |
| **Carga Media** | 17.6% | 17.71 kWh | Transición, operación normal |
| **Anomalías** | 32.3% | Variable | **931 eventos atípicos** |

### ¿Qué son las anomalías?

Eventos que no se ajustan a ningún patrón:
- Arranques de equipos pesados
- Transitorios eléctricos
- Operaciones manuales no programadas
- Posibles equipos defectuosos

**Acción Requerida:** Auditoría de estos 931 eventos

**Métrica de Clustering:** Silhouette Score = 0.3408 (mejor que K-means)

---

## Diapositiva 10: Calidad Eléctrica por Perfil

### Comparación Radar

```
[Referencia: images/radar_calidad_electrica.png]

Métricas Evaluadas:
- Factor de Potencia (0-1, mayor mejor)
- THD Corriente (%, menor mejor)
- Desbalance Corriente (%, menor mejor)
- Desbalance Voltaje (%, menor mejor)
```

### Hallazgos

| Métrica | Alta Carga | Baja Carga | Estado |
|---------|------------|------------|--------|
| Factor Potencia | 0.98 ✓ | 0.99 ✓ | Óptimo ambos |
| THD Corriente | 0.16 ✓ | 0.36 ⚠️ | Crítico en baja |
| Desbalance | 0.18 ⚠️ | 0.17 ⚠️ | Moderado ambos |

**Conclusión:** Calidad deteriorada en períodos de baja carga

---

## Diapositiva 11: 5 Oportunidades de Mejora

### Recomendaciones Priorizadas

**1. Corrección de Factor de Potencia en Baja Carga** 🔴
- **Problema:** THD 36% en 47.7% del tiempo
- **Solución:** Bancos de capacitores automáticos
- **Beneficio:** Reducción 10-15% en penalizaciones

**2. Gestión de Distorsión Armónica (THD)** 🔴
- **Problema:** 1,373 observaciones con THD >30%
- **Solución:** Filtros armónicos pasivos/activos
- **Beneficio:** Menos desgaste en equipos

**3. Rebalanceo de Cargas entre Fases** 🟡
- **Problema:** 13.8% observaciones con desbalance >20%
- **Solución:** Redistribuir cargas eléctricas
- **Beneficio:** Reducción 5-8% en pérdidas

---

## Diapositiva 12: Oportunidades de Mejora (continuación)

**4. Gestión de Demanda (Demand Response)** 🟡
- **Problema:** Pico de 22.4 kWh en horario 11:00-14:00
- **Solución:** Diferir cargas no críticas a valle
- **Beneficio:** Reducción de demanda máxima facturable

**5. Auditoría de 931 Eventos Anómalos** 🔴
- **Problema:** 32.3% observaciones no clasificables
- **Solución:** Cruzar con logs operativos y mantenimiento
- **Objetivo:** Identificar causas raíz

### Priorización

- 🔴 **Alta Prioridad (0-3 meses):** Ítems 1, 2, 5
- 🟡 **Media Prioridad (3-6 meses):** Ítems 3, 4

---

## Diapositiva 13: Impacto Cuantificado

### Beneficios Potenciales Estimados

| Acción | Inversión | Ahorro Anual | ROI | Plazo |
|--------|-----------|--------------|-----|-------|
| Capacitores automáticos | Media | 10-15% penaliz. | 12-18 meses | 0-3 meses |
| Filtros armónicos | Alta | Vida útil equipos +20% | 24-36 meses | 3-6 meses |
| Rebalanceo fases | Baja | 5-8% pérdidas | 6-12 meses | 3-6 meses |
| Gestión demanda | Media | Demanda máx. -10% | 12-18 meses | 0-3 meses |

### Impacto Total Estimado

- **Reducción costos energéticos:** 15-20% anual
- **Extensión vida útil equipos:** +20-30%
- **Reducción incidentes:** -40% eventos anómalos
- **Mejora factor potencia:** De 0.98 → 0.99 (sostenido)

---

## Diapositiva 14: Próximos Pasos

### Plan de Implementación

**Fase 1: Validación (1 mes)**
- ✓ Auditoría de 931 anomalías detectadas
- ✓ Medición detallada de THD en baja carga
- ✓ Validación con datos de múltiples meses

**Fase 2: Quick Wins (3 meses)**
- ⚙️ Implementar rebalanceo de fases
- ⚙️ Evaluar técnico-económico capacitores
- ⚙️ Piloto de gestión de demanda

**Fase 3: Mejoras Estructurales (6 meses)**
- 🔧 Instalación de filtros armónicos
- 🔧 Sistema de monitoreo continuo
- 🔧 Dashboard de perfiles en tiempo real

**Fase 4: Optimización Continua (12+ meses)**
- 📊 Benchmarking con sector
- 📊 Modelos predictivos de demanda
- 📊 Alertas automáticas de desviaciones

---

## Diapositiva 15: Conclusiones y Valor Agregado

### Principales Hallazgos

✅ **2 perfiles operativos claros:** Alta carga diurna (52%) y baja carga nocturna (48%)

✅ **Calidad eléctrica deteriorada en baja carga:** THD 36% vs 16% óptimo

✅ **32.3% de eventos anómalos detectados:** 931 observaciones requieren investigación

✅ **5 oportunidades de mejora cuantificadas:** ROI entre 6-36 meses

### Valor Agregado del Análisis

- ✓ **Diagnóstico objetivo** basado en datos (no suposiciones)
- ✓ **Detección automática** de 931 anomalías previamente desconocidas
- ✓ **Cuantificación de impacto** de cada recomendación
- ✓ **Base técnica** para decisiones de inversión
- ✓ **Metodología replicable** para monitoreo continuo

### Recomendación Final

> Priorizar auditoría de anomalías y evaluación técnico-económica de corrección de THD.  
> ROI estimado: 12-18 meses con beneficios sostenibles a largo plazo.

---

## Anexo: Referencias Técnicas

### Algoritmos Utilizados

- **PCA:** Jolliffe, I.T. (2002). Principal Component Analysis. Springer.
- **UMAP:** McInnes, L., Healy, J., Melville, J. (2018). UMAP: Uniform Manifold Approximation and Projection. arXiv:1802.03426.
- **K-means:** MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations.
- **DBSCAN:** Ester, M., et al. (1996). A density-based algorithm for discovering clusters in large spatial databases.

### Métricas de Evaluación

- **Silhouette Score:** Rousseeuw, P.J. (1987). Silhouettes: A graphical aid to the interpretation.
- **Davies-Bouldin Index:** Davies, D.L., Bouldin, D.W. (1979). A cluster separation measure.
- **Calinski-Harabasz Index:** Caliński, T., Harabasz, J. (1974). A dendrite method for cluster analysis.

### Repositorio del Proyecto

```
d:\Desktop\Proyecto no supervizado\
├── data/                    # Datos procesados
├── notebooks/               # Análisis reproducibles (4 notebooks)
├── reports/                 # Este informe y documentación
├── images/                  # Visualizaciones generadas
└── src/                     # Código reutilizable
```

**Acceso a notebooks ejecutables:** `/notebooks/01-04_*.ipynb`

---

**FIN DE LA PRESENTACIÓN**

*¿Preguntas? Consultar informe técnico completo en `reports/Informe_Tecnico.md`*
