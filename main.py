
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import webbrowser

from pdf_converter import convert_pdf


def pdf_verarbeiten(pfad):
    if not pfad.lower().endswith(".pdf"):
        messagebox.showerror(
            "Fehler",
            "Bitte eine PDF-Datei auswählen."
        )
        return

    try:
        status.config(text="PDF wird verarbeitet ...")
        fenster.update_idletasks()

        html_path = convert_pdf(pfad)

        status.config(text="HTML erfolgreich erstellt!")
        webbrowser.open(html_path.as_uri())

    except Exception as e:
        status.config(text="Fehler bei der Verarbeitung")
        messagebox.showerror("Fehler", str(e))


def datei_drop(event):
    dateien = fenster.tk.splitlist(event.data)

    if dateien:
        pdf_verarbeiten(dateien[0])


fenster = TkinterDnD.Tk()
fenster.title("ADR PDF Converter")
fenster.geometry("700x500")
fenster.resizable(False, False)

hinweis = tk.Label(
    fenster,
    text="ℹ Nach dem Ablegen wird automatisch eine HTML-Seite erstellt und im Browser geöffnet.",
    font=("Arial", 10),
    fg="#596579",
    wraplength=440,
    justify="center"
)
hinweis.pack(pady=10)

titel = tk.Label(
    fenster,
    text="ADR PDF Converter",
    font=("Arial", 20, "bold")
)
titel.pack(pady=25)

# pdf_icon = tk.PhotoImage(file="pdf_icon.png")
# pdf_icon.png
from PIL import Image, ImageTk
from pathlib import Path

bild_pfad = Path(__file__).resolve().parent / "pdf_icon.png"

bild = Image.open(bild_pfad)
bild = bild.resize((100, 100), Image.Resampling.LANCZOS)

pdf_icon = ImageTk.PhotoImage(bild, master=fenster)

drop_zone = tk.Label(
    fenster,
    image=pdf_icon,
    text="PDF hier hineinziehen",
    compound="top",
    bg="#000000",
    font=("Arial", 15),
    width=440,
    height=280
)

# Wichtig: Bildreferenz behalten
drop_zone.image = pdf_icon

drop_zone.pack(padx=25, pady=10)

drop_zone.drop_target_register(DND_FILES)
drop_zone.dnd_bind("<<Drop>>", datei_drop)


drop_zone.pack(fill="both",
               expand="true",
               padx=20,
               pady=20)

drop_zone.drop_target_register(DND_FILES)
drop_zone.dnd_bind("<<Drop>>", datei_drop)

status = tk.Label(
    fenster,
    text="Warte auf PDF ...",
    font=("Arial", 11)
)
status.pack(pady=20)

test_label = tk.Label(fenster, image=pdf_icon)
test_label.image = pdf_icon
test_label.pack()

fenster.mainloop()

# from pydoc import text
# import re
# import pymupdf
# import html
# from pathlib import Path
# from urllib.parse import quote_plus
#
# pdf = pymupdf.open("/Users/mikael/Downloads/job_261109.pdf")
#
# for seite in pdf:
#     text = seite.get_text("text")
#
#     for line in text.splitlines():
#         elements = re.split(r"\s{2,}", line.strip())
#
#         print(len(elements))
#         print(elements)
# pdf.close()
#
# pdf_path = "/Users/mikael/Downloads/job_261109.pdf"
# output_path = Path("index.html")
#
# header = None
# rows = []
# with pymupdf.open(pdf_path) as pdf:
#     for seite in pdf:
#         for line in seite.get_text("text").splitlines():
#             elements = re.split(r"\s{2,}", line.strip())
#
#             # Nur Datensätze mit einer 7-stelligen Nummer
#             if header is None:
#                 header = elements
#             elif len(elements) > 4:
#                 rows.append(elements)
#
# table_rows = ""
#
# for elements in rows:
#     nummer = html.escape(elements[0])
#     name = html.escape(elements[1]) if len(elements) > 1 else ""
#     plz = html.escape(elements[2])
#     titel = html.escape(header[0] + header[1])
#
#     search_url = (
#         f"https://search.ch/tel/"
#         f"?all={quote_plus(elements[1])}"
#         f"&wo={quote_plus(elements[2])}"
#     )
#
#     table_rows += f"""
#         <tr>
#             <td>
#                 <button class="nummer" onclick="kopieren(this)">
#                     {nummer}
#                 </button>
#             </td>
#             <td>{name}</td>
#             <td>{plz}</td>
#             <td>
#                 <a href="{html.escape(search_url, quote=True)}"
#                    target="_blank"
#                    rel="noopener noreferrer">
#                     🔍 Suchen
#                 </a>
#             </td>
#         </tr>
#         """
#
# html_content = f"""
# <!DOCTYPE html>
# <html lang="de">
# <head>
#     <meta charset="UTF-8">
#     <title>{titel}</title>
#     <style>
#         body {{
#             font-family: Arial, sans-serif;
#             margin: 30px;
#             background: #f5f6f8;
#         }}
#
#
#
#         table {{
#             width: fit-content;
#             border-collapse: collapse;
#             background: white;
#         }}
#
#         th, td {{
#             padding: 12px;
#             border-bottom: 1px solid #ddd;
#             text-align: left;
#         }}
#
#         th {{
#             background: #253858;
#             color: white;
#         }}
#
#         tr.kopiert {{
#             background-color: #c8f7c5 !important;
#         }}
#
#         .nummer {{
#             cursor: pointer;
#             border: none;
#             background: #e1efff;
#             color: #1459a0;
#             padding: 8px 12px;
#             border-radius: 6px;
#             font-weight: bold;
#         }}
#
#         .nummer:hover {{
#             background: #b9dbff;
#         }}
#     </style>
# </head>
# <body>
#
# <h2>ADR-Regionen</h2>
# <p>Klicke auf eine Nummer, um sie zu kopieren.</p>
#
# <table>
#     <thead>
#         <tr>
#             <th>Nummer</th>
#             <th>Name</th>
#             <th>PLZ</th>
#             <th>Telefon suche</th>
#         </tr>
#     </thead>
#     <tbody>
#         {table_rows}
#     </tbody>
# </table>
#
# <script>
# async function kopieren(button) {{
#     const nummer = button.innerText.trim();
#
#     try {{
#         await navigator.clipboard.writeText(nummer);
#
#         // Gesamte Tabellenzeile markieren
#         const zeile = button.closest("tr");
#         zeile.classList.add("kopiert");
#
#         // Button kurz ändern
#         button.innerText = "✓ Kopiert!";
#
#         setTimeout(() => {{
#             button.innerText = nummer;
#         }}, 1000);
#
#     }} catch (error) {{
#         alert("Kopieren fehlgeschlagen!");
#     }}
# }}
# </script>
#
# </body>
# </html>
# """
#
# output_path.write_text(html_content, encoding="utf-8")
#
# print(f"HTML erstellt: {output_path.resolve()}")
# print(f"{len(rows)} Datensätze gefunden")
