# Variación de la temperatura media en América Latina y el Caribe (1961–2025)

Análisis descriptivo de 195 observaciones anuales para El Caribe, América Central y América del Sur, a partir de datos de FAOSTAT basados en la metodología NASA GISS.

La página de presentación con los gráficos incrustados está disponible en [`index.html`](index.html). Para probarla localmente, inicia un servidor HTTP en la raíz del proyecto y abre `http://localhost:8000/`.

## Metodología

1. **Carga:** se cargó la hoja `datos` de [`datos/crudo/data_1787673487.xlsx`](datos/crudo/data_1787673487.xlsx).
2. **Exploración de variables:** se revisaron las variables de región, año y variación de temperatura, además de los tipos de datos y la unidad.
3. **Inventario:** se documentaron dimensiones, cobertura y valores nulos. El conjunto contiene 195 registros: 65 años por cada una de las tres regiones.
4. **Análisis:** se utilizaron Python y resúmenes descriptivos para comparar la evolución anual y los promedios regionales.
5. **Visualización:** se generaron gráficos con Altair y se guardaron como páginas HTML autocontenidas en [`docs/graficos/`](docs/graficos/).

## Evolución temporal

Las series fluctúan de un año a otro y, en general, presentan valores mayores en las décadas recientes que al inicio del registro. En las tres regiones, el valor observado en 2024 es el máximo de la serie; en 2025 disminuye respecto de 2024, aunque permanece positivo.

Gráfico interactivo: [`docs/graficos/cambio_tiempo.html`](docs/graficos/cambio_tiempo.html).

## Ranking regional

El Caribe presenta la mayor variación promedio de temperatura (**0,539 °C**), seguido de América del Sur (**0,532 °C**) y América Central (**0,470 °C**). Cada promedio corresponde a 65 observaciones anuales.

Gráfico interactivo: [`docs/graficos/ranking.html`](docs/graficos/ranking.html).

## Limitaciones

- El análisis es descriptivo.
- No permite establecer causalidad.
- Los datos están agregados a nivel regional.

## Créditos

CEPALSTAT · FAOSTAT · FAO · NASA GISS · GitHub Codespaces · GitHub Copilot

> El código utilizado en este proyecto fue desarrollado con apoyo de un agente de inteligencia artificial.