from pathlib import Path

import altair as alt
import pandas as pd


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
RUTA_EXCEL = RAIZ_PROYECTO / "datos" / "crudo" / "data_1787673487.xlsx"
RUTA_GRAFICO = RAIZ_PROYECTO / "docs" / "graficos" / "ranking.vl.json"
HOJA = "datos"
COLUMNAS = ["País__ESTANDAR", "value"]
TITULO = (
    "¿Qué región presenta la mayor variación promedio de temperatura "
    "durante el periodo analizado?"
)


def calcular_resumen(datos):
    if datos["País__ESTANDAR"].isna().any():
        raise ValueError("La columna de región contiene valores nulos.")
    if not pd.api.types.is_numeric_dtype(datos["value"]):
        raise TypeError("La columna `value` debe contener valores numéricos.")

    resumen = (
        datos.groupby("País__ESTANDAR", as_index=False, sort=False)
        .agg(promedio=("value", "mean"), n=("value", "count"))
        .sort_values("promedio", ascending=False, kind="stable")
    )
    if resumen["promedio"].isna().any():
        raise ValueError("Hay regiones sin valores válidos de `value`.")
    return resumen


def crear_grafico(resumen, cantidad):
    orden = alt.SortField(field="promedio", order="descending")
    eje_region = alt.Y(
        "País__ESTANDAR:N",
        sort=orden,
        title="Región",
    )
    barras = alt.Chart(resumen).mark_bar(color="#4C78A8").encode(
        x=alt.X(
            "promedio:Q",
            title="Variación promedio de temperatura (°C)",
            scale=alt.Scale(domainMin=0),
        ),
        y=eje_region,
        tooltip=[
            alt.Tooltip("País__ESTANDAR:N", title="Región"),
            alt.Tooltip("promedio:Q", title="Promedio (°C)", format=".3f"),
            alt.Tooltip("n:Q", title="Tamaño de muestra (n)", format="d"),
        ],
    )
    etiquetas = alt.Chart(resumen).mark_text(
        align="left",
        dx=5,
        clip=False,
    ).encode(
        x=alt.X("promedio:Q", scale=alt.Scale(domainMin=0)),
        y=eje_region,
        text=alt.Text("promedio:Q", format=".3f"),
    )

    return (
        (barras + etiquetas)
        .properties(
            width="container",
            height=180,
            title=alt.TitleParams(
                text=TITULO,
                subtitle=[
                    f"Tamaño de muestra (n): {cantidad}",
                    "Fuente: FAOSTAT y NASA GISS",
                ],
            ),
        )
        .configure_view(stroke=None)
        .configure_axis(grid=True)
    )


def crear_html(resumen, cantidad):
    html_grafico = crear_grafico(resumen, cantidad).to_html(inline=True)
    html_grafico = html_grafico.replace(
        "<head>",
        '<head>\n  <meta name="viewport" content="width=device-width, initial-scale=1">',
        1,
    )
    tabla = resumen.rename(
        columns={
            "País__ESTANDAR": "Región",
            "promedio": "Variación promedio (°C)",
        }
    ).to_html(
        index=False,
        border=0,
        classes="datos-utilizados",
        formatters={"Variación promedio (°C)": "{:.3f}".format},
    )
    estilos = """
<style>
  body { font-family: sans-serif; margin: 2rem auto; max-width: 1100px; padding: 0 1rem; }
  h2 { margin-top: 2rem; }
  .tabla-contenedor { overflow-x: auto; }
  .datos-utilizados { border-collapse: collapse; width: 100%; }
  .datos-utilizados th, .datos-utilizados td { border: 1px solid #ccc; padding: 0.4rem; text-align: left; }
  .datos-utilizados th { background: #f2f2f2; }
</style>
"""
    contenido = (
        f"{estilos}\n"
        "<h2>Cifras utilizadas para construir el ranking</h2>\n"
        f'<p>Tamaño de muestra (n): {cantidad}. '
        "Fuente: FAOSTAT y NASA GISS.</p>\n"
        f'<div class="tabla-contenedor">{tabla}</div>\n'
    )
    return html_grafico.replace("</body>", f"{contenido}</body>")



def main():
    datos = pd.read_excel(
        RUTA_EXCEL,
        sheet_name=HOJA,
        usecols=COLUMNAS,
    )

    resumen = calcular_resumen(datos)
    cantidad = int(datos["value"].count())

    RUTA_GRAFICO.parent.mkdir(parents=True, exist_ok=True)

    grafico = crear_grafico(resumen, cantidad)
    grafico.save(str(RUTA_GRAFICO))

    print(f"Gráfico Vega-Lite guardado en {RUTA_GRAFICO}")


if __name__ == "__main__":
    main()
