# Bitácora de decisiones

Registro de las decisiones de limpieza, preparación y modelado de la base *Mice Protein Expression*. Cada entrada
indica qué se hizo, por qué, a cuántos registros afectó y en qué sección del notebook se sustenta. Las decisiones
que dependen de estimar valores a partir de los datos no se aplican en la base depurada, sino dentro del `Pipeline`
de los modelos, después de una partición agrupada por ratón.

## Actividad 1 · Análisis exploratorio (`notebooks/01_eda.ipynb`)

| # | Decisión | Registros afectados | Justificación | Sección | Dónde se aplica |
|---|---|---|---|---|---|
| 1 | Eliminar la columna `pS6_N` | 1 columna | Sus valores son idénticos a los de `ARC_N` en las 1.080 filas, lo que indica una duplicación en la base original. `ARC_N` se conserva, aunque sin una interpretación biológica confiable. | 1.4, 3.6 | Base depurada (6.4) |
| 2 | Eliminar las réplicas con más de la mitad de las proteínas sin medir | 3 filas (`3426_13`, `3426_14`, `3426_15`; 129 celdas vacías) | Las otras 12 réplicas del ratón tienen esas proteínas medidas, de modo que el faltante es una falla técnica; imputar 43 de 77 proteínas equivaldría a fabricar la observación. El ratón se conserva con 12 réplicas. | 3.2, 3.6 | Base depurada (6.2) |
| 3 | Reemplazar por faltante el valor de expresión negativo | 1 celda (`RRP1_N`, réplica 365_14, −0,062) | Una cantidad de proteína no puede ser negativa, por lo que se trata de un error de registro; no se corrige con supuestos como el cambio de signo, y se conserva el resto de la réplica. | 4.6, 4.7 | Base depurada (6.3) |
| 4 | Conservar las 8 proteínas con ausencia en bloque e imputarlas con k vecinos más cercanos | 8 proteínas en 35 ratones | La ausencia abarca las 15 réplicas de cada ratón y no se asocia con la clase (proteínas no medidas, no ausencia biológica). La mediana concentraría hasta una cuarta parte de los valores de `BCL2_N` en un solo punto; KNN usa ratones con perfil similar (Troyanskaya et al., 2001). | 3.1 – 3.6 | `Pipeline`, ajustado solo con entrenamiento (Kuhn & Johnson, 2019) |
| 5 | Conservar los atípicos de subgrupo | 757 celdas | Son atípicos frente a la base completa, pero normales dentro de su clase; reflejan diferencias reales entre grupos experimentales. | 4.1, 4.5, 4.7 | Sin cambios |
| 6 | Conservar los ratones excepcionales | 507 celdas (42 pares ratón-proteína, 20 ratones) | El valor extremo se repite en la mayoría de las réplicas del ratón, es reproducible y conserva la relación entre proteínas (sección 4.4); eliminar ratones reduciría clases de 7 a 10 individuos. | 4.3 – 4.5, 4.7 | Sin cambios |
| 7 | Conservar las réplicas aisladas | 1.267 celdas | La regla de 1,5·IQR marca valores incluso sin errores (Hoaglin et al., 1986), y más en distribuciones asimétricas; no hay evidencia de error. | 4.5, 4.7 | Sin cambios |
| 8 | No eliminar proteínas colineales en la base depurada | Grupos con ρ > 0,9 (p. ej., `DYRK1A_N`/`ITSN1_N`, ρ = 0,93) | La colinealidad no es perfecta y su tratamiento depende del objetivo del modelo (Dormann et al., 2013; James et al., 2023). | 5.1, 5.2, 5.5 | Actividades 2 y 3 |
| 9 | No transformar ni escalar en la base depurada | 77 proteínas | La transformación logarítmica no mejora todas las proteínas por igual (sección 2.2), y el escalado debe ajustarse solo con el conjunto de entrenamiento. | 2.1, 2.2 | `Pipeline` |
| 10 | Conservar `raton` y `replica` y partir los datos por ratón | 72 ratones | Las réplicas de un mismo ratón no son independientes (razón entre/dentro > 1 en 66 de 77 proteínas); una partición por filas sobreestimaría el desempeño (Roberts et al., 2017). | 1.5 – 1.8, 2.3 | Actividades 2 y 3 |

Resultado: base depurada de 1.077 filas × 83 columnas, 72 ratones y 1.268 celdas faltantes en proteínas
(`datos/procesados/mice_depurado.parquet`, que no se versiona y se regenera al ejecutar `01_eda.ipynb`).

## Actividad 2 · Regresión lineal y regularizada (`notebooks/02_regresion.ipynb`)

| # | Decisión | Registros afectados | Justificación | Sección |
|---|---|---|---|---|
| 11 | Variable objetivo `pERK_N`, con dos modelos: M1 (`DYRK1A_N`, `BRAF_N`, `ITSN1_N` + diseño) para explicar y M2 (75 proteínas + diseño) para predecir | 1.077 réplicas | pERK es la forma activa de ERK, implicada en plasticidad sináptica y memoria (Sweatt, 2004); sus predictores tienen correlaciones de 0,83 a 0,93 y respaldo biológico (Kelly & Rahmani, 2005) | 1 |
| 12 | Conjunto de prueba de ~20 % de los ratones con `StratifiedGroupKFold`, usado una sola vez | 14 ratones (210 filas) en prueba; 58 (867 filas) en entrenamiento | Agrupar por ratón evita que sus réplicas queden en ambos conjuntos, y estratificar por clase mantiene las 8 condiciones en prueba (Roberts et al., 2017) | 2 |
| 13 | Errores estándar agrupados por ratón en M1, con t de 57 grados de libertad | 58 ratones | Con 15 réplicas por ratón, los errores ordinarios se subestiman entre 1,9 y 4,5 veces; el efecto aparente del tratamiento era un artefacto de la pseudorreplicación (Cameron & Miller, 2015) | 3 |
| 14 | Escala log-log en M1 y M2; métricas en escala original con `TransformedTargetRegressor` | Objetivo y 78 predictores | En log-log la curtosis de los residuos baja de 231 a 26 y la distancia de Cook máxima de 7,6 a 0,94; los coeficientes dejan de depender del ratón 3484 | 4.5 – 4.7 |
| 15 | Conservar el ratón 3484 y medir su influencia con sensibilidad | 15 réplicas | Decisión de la Actividad 1; en log-log los coeficientes casi no cambian sin él, por lo que no hace falta eliminarlo | 4.4, 4.5 |
| 16 | No eliminar proteínas colineales y tratarlas con regularización | VIF entre 14 y 27 en las proteínas de M1 | La colinealidad vuelve inestables los coeficientes de MCO, pero no la predicción; Ridge, Lasso y Elastic Net la manejan sin descartar información (James et al., 2023) | 4.3, 5 |
| 17 | Preprocesamiento de M2 dentro del `Pipeline`: log → `StandardScaler` → `KNNImputer`; `OneHotEncoder(drop="if_binary")` | 75 proteínas y 3 variables de diseño | Mantiene la escala de M1, permite que KNN use distancias comparables y evita la fuga de información (Kuhn & Johnson, 2019) | 5 |
| 18 | Grillas de α: Ridge de 10⁻³ a 10³; Lasso y Elastic Net de 10⁻⁵ a 10⁻¹, con `l1_ratio` de 0,1 a 0,9 | 3 modelos | La penalización L1 anula los coeficientes con α mucho menores que Ridge; se verificó que ningún α quedara en el borde (Zou & Hastie, 2005) | 5.1 |
| 19 | Modelo final: M2 Elastic Net para predecir y M1 log-log para explicar | — | Ridge, Lasso y Elastic Net empatan en validación; Elastic Net combina ese desempeño con coeficientes estables y una selección reproducible. En prueba: R² = 0,97 y RMSE = 0,046 | 7 |
