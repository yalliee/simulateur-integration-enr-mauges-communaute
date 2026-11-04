import os
import re

def extraire_donnees_maquette(
    fichier_entree="maquette_Imran.backup.html",
    fichier_html_sortie="maquette_Imran_clean.html",
    fichier_data_js="data.js"
):
    if not os.path.exists(fichier_entree):
        print(f"Erreur : Le fichier '{fichier_entree}' est introuvable.")
        return

    with open(fichier_entree, "r", encoding="utf-8") as f:
        content = f.read()

    # Capture des objets JavaScript META, GEO et BIN avec leur contenu JSON
    pattern_meta = r'(const\s+META\s*=\s*\{.*?\};?\n)'
    pattern_geo = r'(const\s+GEO\s*=\s*\{.*?\};?\n)'
    pattern_bin = r'(const\s+BIN\s*=\s*\{.*?\};?\n)'

    match_meta = re.search(pattern_meta, content, re.DOTALL)
    match_geo = re.search(pattern_geo, content, re.DOTALL)
    match_bin = re.search(pattern_bin, content, re.DOTALL)

    if not (match_meta and match_geo and match_bin):
        print("Erreur lors de la détection des structures META, GEO ou BIN dans le fichier HTML.")
        return

    # 1. Écriture du fichier externe data.js
    with open(fichier_data_js, "w", encoding="utf-8") as f_js:
        f_js.write("// Données brutes extraites de la maquette ENR Mauges\n")
        f_js.write(match_meta.group(1))
        f_js.write(match_geo.group(1))
        f_js.write(match_bin.group(1))

    # 2. Nettoyage du fichier HTML
    clean_content = content
    clean_content = clean_content.replace(match_meta.group(1), "")
    clean_content = clean_content.replace(match_geo.group(1), "")
    clean_content = clean_content.replace(match_bin.group(1), "")

    # 3. Inclusion du fichier JS externe avant le script du moteur
    # Détection du bloc d'ouverture de script du moteur
    script_target = "<script>\nconst MOTEUR ="
    script_replacement = f'<script src="{fichier_data_js}"></script>\n<script>\nconst MOTEUR ='
    
    if script_target in clean_content:
        clean_content = clean_content.replace(script_target, script_replacement)
    else:
        # Solution de secours si l'indentation diffère légèrement
        clean_content = re.sub(
            r'(<script>\s*const\s+MOTEUR)',
            f'<script src="{fichier_data_js}"></script>\n\\1',
            clean_content
        )

    # 4. Sauvegarde de la maquette HTML allégée
    with open(fichier_html_sortie, "w", encoding="utf-8") as f_out:
        f_out.write(clean_content)

    # Rapport d'exécution
    taille_originale = os.path.getsize(fichier_entree) / 1024
    taille_html = os.path.getsize(fichier_html_sortie) / 1024
    taille_js = os.path.getsize(fichier_data_js) / 1024

    print("=== Extraction réussie ===")
    print(f"• Fichier d'origine  : {taille_originale:.1f} Ko")
    print(f"• Nouveau HTML léger : {taille_html:.1f} Ko ({fichier_html_sortie})")
    print(f"• Données séparées   : {taille_js:.1f} Ko ({fichier_data_js})")

if __name__ == "__main__":
    extraire_donnees_maquette()