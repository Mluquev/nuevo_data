from pathlib import Path

import altair as alt
import pandas as pd


RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
RUTA_EXCEL = RAIZ_PROYECTO / "datos" / "crudo" / "data_1787673487.xlsx"
RUTA_GRAFICO = RAIZ_PROYECTO / "docs" / "graficos" / "cambio_tiempo.html"
HOJA = "datos"
COLUMNAS = ["Años__ESTANDAR", "value", "País__ESTANDAR"]
TITULO = (
    "¿Cómo ha evolucionado la variación de la temperatura media en las regiones "
    "de América Latina y el Caribe entre 1961 y 2025?"
)


def crear_grafico(datos):
    cantidad = len(datos)
    grafico = (
        alt.Chart(datos)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "Años__ESTANDAR:Q",
                title="Año",
                axis=alt.Axis(format="d"),
            ),
            y=alt.Y("value:Q", title="Variación de temperatura (°C)"),
            color=alt.Color(
                "País__ESTANDAR:N",
                title="Región",
                scale=alt.Scale(scheme="tableau10"),
            ),
            order=alt.Order("Años__ESTANDAR:Q"),
            tooltip=[
                alt.Tooltip("País__ESTANDAR:N", title="Región"),
                alt.Tooltip("Años__ESTANDAR:Q", title="Año", format="d"),
                alt.Tooltip("value:Q", title="Variación (°C)"),
            ],
        )
        .properties(
            width="container",
            height=450,
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
    return grafico


def crear_html(datos):
    html_grafico = crear_grafico(datos).to_html(inline=True)
    html_grafico = html_grafico.replace(
        "<head>",
        '<head>\n  <meta name="viewport" content="width=device-width, initial-scale=1">',
        1,
    )
    tabla = datos.to_html(index=False, border=0, classes="datos-utilizados")
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
        "<h2>Datos utilizados para construir el gráfico</h2>\n"
        f'<p>Tamaño de muestra (n): {len(datos)}. '
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
    datos = datos[COLUMNAS]

    if datos.isna().any().any():
        raise ValueError(
            "Las columnas requeridas contienen valores nulos; no se eliminarán "
            "ni imputarán registros."
        )
    if datos.duplicated(subset=["Años__ESTANDAR", "País__ESTANDAR"]).any():
        raise ValueError(
            "Hay más de un registro para una combinación de año y región; "
            "no se agregarán observaciones."
        )

    RUTA_GRAFICO.parent.mkdir(parents=True, exist_ok=True)
    RUTA_GRAFICO.write_text(crear_html(datos), encoding="utf-8")
    print(f"Gráfico guardado en {RUTA_GRAFICO}")


if __name__ == "__main__":
    main()
