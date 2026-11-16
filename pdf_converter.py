
import html
import re
from pathlib import Path
from urllib.parse import urlencode

import pymupdf


def convert_pdf(pdf_path):
    pdf_path = Path(pdf_path)
    header = None
    rows = []

    with pymupdf.open(pdf_path) as pdf:
        for seite in pdf:
            for line in seite.get_text("text").splitlines():
                elements = re.split(r"\s{2,}", line.strip())

                # Nur Datensätze mit einer 7-stelligen Nummer
                if header is None:
                    header = elements
                elif len(elements) > 4:
                    rows.append(elements)

    table_rows = ""

    titel = html.escape(f"{header[1]} - {header[0]}")
    for elements in rows:
        nummer = html.escape(elements[0])
        name = html.escape(elements[1])
        plz = html.escape(elements[2])

        search_url = "https://search.ch/tel/?" + urlencode({
            "all": elements[1],
            "wo": elements[2]
        })

        table_rows += f"""
        <tr>
            <td>
                <button onclick="kopieren(this)">
                    {nummer}
                </button>
            </td>
            <td>{name}</td>
            <td>{plz}</td>
            <td>
                <a href="{html.escape(search_url, quote=True)}"
                   target="_blank" rel="noopener noreferrer">
                    Suchen
                </a>
            </td>
        </tr>
        """
    print(titel)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <title>{titel}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 30px;
                background: #f5f6f8;
            }}

            table {{
                border-collapse: collapse;
                width: 650px;
                max-width: 100%;
                background: white;
            }}

            th, td {{
                padding: 6px 10px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }}

            th {{
                background: #253858;
                color: white;
            }}

            button {{
                cursor: pointer;
                border: none;
                border-radius: 5px;
                padding: 7px;
                color: #1459a0;
                background: #e1efff;
            }}

            tr.kopiert {{
                background: #c8f7c5;
            }}
        </style>
    </head>
    <body>
        <h2>{titel}</h2>
        <table>
            <thead>
                <tr>
                    <th>Nummer</th>
                    <th>Name</th>
                    <th>PLZ</th>
                    <th>Suche</th>
                </tr>
            </thead>
            <tbody>
                __TABLE_ROWS__
            </tbody>
        </table>

        <script>
            async function kopieren(button) {{
                const nummer = button.textContent.trim();

                try {{
                    await navigator.clipboard.writeText(nummer);
                    button.closest("tr").classList.add("kopiert");
                }} catch (error) {{
                    alert("Kopieren fehlgeschlagen!");
                }}
            }}
        </script>
    </body>
    </html>
    """

    html_content = html_content.replace(
        "__TABLE_ROWS__", table_rows
    )

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    datum = header[0].replace(".", "-") if header else "unbekannt"
    output_path = output_dir / f"ADR-Regionen_{datum}.html"
    output_path.write_text(html_content, encoding="utf-8")

    return output_path.resolve()
