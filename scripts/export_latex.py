#!/usr/bin/env python3
"""
Convertit ARTICLE_MNRAS_DRAFT.md → article_mnras.tex (prêt pour soumission MNRAS).

Usage:
    python scripts/export_latex.py

Prérequis:
    pip install pypandoc   (ou: apt install pandoc)

Sortie:
    docs/promotion-internationale/article_mnras.tex
    docs/promotion-internationale/article_mnras.pdf   (si pdflatex disponible)

Workflow de mise à jour:
    1. Éditer ARTICLE_MNRAS_DRAFT.md
    2. Relancer ce script
    3. Vérifier article_mnras.tex
    4. Compiler: pdflatex article_mnras.tex (×2) puis bibtex article_mnras
"""

import re
import os
import subprocess
import sys

SRC  = 'docs/promotion-internationale/ARTICLE_MNRAS_DRAFT.md'
BIB  = 'docs/promotion-internationale/refs_mnras.bib'
OUT  = 'docs/promotion-internationale/article_mnras.tex'
OUTD = 'docs/promotion-internationale'

# ─────────────────────────────────────────────────────────────────
# Lire le markdown source
# ─────────────────────────────────────────────────────────────────
with open(SRC, encoding='utf-8') as f:
    md = f.read()

# Supprimer les blocs de métadonnées (en-tête, checklist, notes éditoriales)
# Garder uniquement du titre jusqu'à la fin des Références
start = md.find('# Temporal distortion')
end   = md.find('\n---\n\n## Submission Checklist')
if start == -1:
    sys.exit('❌ Titre de l\'article introuvable dans le markdown.')
if end == -1:
    end = len(md)
md_body = md[start:end].strip()

# ─────────────────────────────────────────────────────────────────
# Extraire le titre, auteur, abstract, keywords
# ─────────────────────────────────────────────────────────────────
def extract_between(text, start_marker, end_marker):
    s = text.find(start_marker)
    e = text.find(end_marker, s + len(start_marker))
    if s == -1 or e == -1:
        return ''
    return text[s + len(start_marker):e].strip()

title    = 'Temporal distortion as a unified explanation for dark matter and dark energy: validation against ten independent cosmological data sets'
author   = 'Pierre-Olivier Despr\\`{e}s Asselin'
email    = 'pierreolivierdespres@gmail.com'
abstract = extract_between(md_body, '## ABSTRACT\n\n', '\n\n**Key words:**')
keywords = extract_between(md_body, '**Key words:** ', '\n\n---')

# ─────────────────────────────────────────────────────────────────
# Extraire le corps (Introduction → Références)
# ─────────────────────────────────────────────────────────────────
body_start = md_body.find('\n## 1 INTRODUCTION')
body_end   = md_body.find('\n## REFERENCES')
body_md    = md_body[body_start:body_end].strip() if body_end != -1 else md_body[body_start:].strip()

# ─────────────────────────────────────────────────────────────────
# Conversions Markdown → LaTeX (règles ciblées MNRAS)
# ─────────────────────────────────────────────────────────────────
def md_to_latex_body(text):
    lines = text.split('\n')
    out   = []
    in_table    = False
    in_verbatim = False
    in_itemize  = False

    for line in lines:
        # Blocs de code (verbatim)
        if line.strip().startswith('```'):
            if not in_verbatim:
                out.append('\\begin{verbatim}')
                in_verbatim = True
            else:
                out.append('\\end{verbatim}')
                in_verbatim = False
            continue
        if in_verbatim:
            out.append(line)
            continue

        # Sections
        if line.startswith('## '):
            close_list(out, in_itemize); in_itemize = False
            sec = line[3:].strip()
            # Extraire numéro si présent (ex: "## 2 THEORETICAL FRAMEWORK")
            m = re.match(r'^(\d+)\s+(.*)', sec)
            label = re.sub(r'[^a-z0-9]+', '-', sec.lower()).strip('-')
            sec_title = m.group(2) if m else sec
            out.append(f'\n\\section{{{tex_escape(sec_title)}}}\\label{{sec:{label}}}')
            continue
        if line.startswith('### '):
            close_list(out, in_itemize); in_itemize = False
            sec = line[4:].strip()
            m = re.match(r'^(\d+\.\d+)\s+(.*)', sec)
            label = re.sub(r'[^a-z0-9]+', '-', sec.lower()).strip('-')
            sec_title = m.group(2) if m else sec
            out.append(f'\n\\subsection{{{tex_escape(sec_title)}}}\\label{{sec:{label}}}')
            continue

        # Tableaux markdown → tabular
        if line.strip().startswith('|'):
            if not in_table:
                cols = [c.strip() for c in line.strip().strip('|').split('|')]
                ncols = len(cols)
                col_spec = 'l' * ncols
                out.append('\\begin{table}\n\\centering\n\\begin{tabular}{' + col_spec + '}')
                out.append('\\hline')
                header = ' & '.join(tex_escape(c) for c in cols) + ' \\\\'
                out.append(header)
                out.append('\\hline')
                in_table = True
            elif re.match(r'^\|[-| :]+\|$', line.strip()):
                continue  # ligne de séparation
            else:
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                row = ' & '.join(tex_escape(c) for c in cells) + ' \\\\'
                out.append(row)
            continue
        elif in_table:
            out.append('\\hline\n\\end{tabular}\n\\end{table}')
            in_table = False

        # Listes
        if line.startswith('- ') or line.startswith('* '):
            if not in_itemize:
                out.append('\\begin{itemize}')
                in_itemize = True
            out.append('\\item ' + inline_md(line[2:]))
            continue
        elif in_itemize and line.strip() == '':
            out.append('\\end{itemize}')
            in_itemize = False

        # Ligne vide
        if line.strip() == '':
            out.append('')
            continue

        # Séparateur horizontal
        if line.strip() in ('---', '***', '___'):
            continue

        # Équations numérotées : ligne indentée avec (N) à la fin
        # ex: "    M_eff(r) = ...   (7)"
        m_eq = re.match(r'^    (.+?)\s+\((\d+)\)\s*$', line)
        if m_eq:
            eq_body = m_eq.group(1).strip()
            eq_num  = m_eq.group(2)
            # Convertir symboles grecs dans l'équation
            eq_body = inline_md(eq_body)
            # Retirer les $ ajoutés par inline_md pour les réenvelopper proprement
            eq_body = eq_body.replace('$', '')
            out.append(f'\\begin{{equation}}\\label{{eq:{eq_num}}}\n  {eq_body}\n\\end{{equation}}')
            continue

        # Paragraphe normal
        out.append(inline_md(line))

    if in_table:
        out.append('\\hline\n\\end{tabular}\n\\end{table}')
    if in_itemize:
        out.append('\\end{itemize}')

    return '\n'.join(out)


def close_list(out, in_itemize):
    if in_itemize:
        out.append('\\end{itemize}')


def tex_escape(s):
    """Échappe les caractères spéciaux LaTeX dans le texte courant."""
    s = s.replace('&',  '\\&')
    s = s.replace('%',  '\\%')
    s = s.replace('#',  '\\#')
    s = s.replace('_',  '\\_')
    s = s.replace('^',  '\\^{}')
    s = s.replace('~',  '\\textasciitilde{}')
    s = s.replace('$',  '\\$')
    # conserver ² ³ etc. comme unicode — pdflatex les accepte avec inputenc utf8
    return s


def inline_md(text):
    """Convertit le markdown inline en LaTeX inline."""
    # Gras → textbf
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    # Italique → textit
    text = re.sub(r'\*(.+?)\*', r'\\textit{\1}', text)
    # Code inline → texttt
    text = re.sub(r'`(.+?)`', r'\\texttt{\1}', text)
    # Liens [texte](url)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Exposants unicode courants
    text = text.replace('⁻¹', '$^{-1}$').replace('⁻²', '$^{-2}$')
    text = text.replace('⁻³', '$^{-3}$').replace('²', '$^{2}$')
    text = text.replace('³', '$^{3}$').replace('☉', r'$_\odot$')
    # Subscripts (H₀ → H$_0$, etc.)
    text = re.sub(r'([A-Za-z])₀', r'\1$_0$', text)
    text = re.sub(r'([A-Za-z])₁', r'\1$_1$', text)
    text = re.sub(r'([A-Za-z])₂', r'\1$_2$', text)
    # Signes mathématiques courants dans le texte
    text = text.replace('≈', '$\\approx$')
    text = text.replace('≤', '$\\leq$')
    text = text.replace('≥', '$\\geq$')
    text = text.replace('×', '$\\times$')
    text = text.replace('±', '$\\pm$')
    text = text.replace('→', '$\\rightarrow$')
    text = text.replace('⟩', '$\\rangle$')
    text = text.replace('⟨', '$\\langle$')
    text = text.replace('Ω', '$\\Omega$')
    text = text.replace('Λ', '$\\Lambda$')
    text = text.replace('σ', '$\\sigma$')
    text = text.replace('β', '$\\beta$')
    text = text.replace('α', '$\\alpha$')
    text = text.replace('ξ', '$\\xi$')
    text = text.replace('ψ', '$\\psi$')
    text = text.replace('ρ', '$\\rho$')
    text = text.replace('Δ', '$\\Delta$')
    text = text.replace('δ', '$\\delta$')
    text = text.replace('μ', '$\\mu$')
    text = text.replace('Φ', '$\\Phi$')
    text = text.replace('φ', '$\\phi$')
    # Guillemets
    text = text.replace('"', "``").replace('"', "''")
    return text


# ─────────────────────────────────────────────────────────────────
# Construire le fichier LaTeX complet
# ─────────────────────────────────────────────────────────────────
abstract_tex = inline_md(abstract)
keywords_tex = keywords.replace('—', '--')
body_tex     = md_to_latex_body(body_md)

latex = r"""\documentclass[a4paper,fleqn,usenatbib]{mnras}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{hyperref}

%% MNRAS style — ne pas modifier
\bibliographystyle{mnras}

\title[TMT: Temporal distortion unified dark matter \& dark energy]{""" + tex_escape(title) + r"""}

\author[P.-O.\ Despr\`{e}s Asselin]{Pierre-Olivier Despr\`{e}s Asselin$^{1}$\thanks{E-mail: pierreolivierdespres@gmail.com}\\
$^{1}$ Independent Researcher, Montr\'{e}al, Qu\'{e}bec, Canada
}

\begin{document}

\maketitle

\begin{abstract}
""" + abstract_tex + r"""
\end{abstract}

\begin{keywords}
""" + keywords_tex + r"""
\end{keywords}

""" + body_tex + r"""

\bibliography{refs_mnras}

\end{document}
"""

os.makedirs(OUTD, exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(latex)

print(f'✓ LaTeX généré : {OUT}')
print()
print('─── Pour compiler (dans docs/promotion-internationale/) ───')
print('  cd docs/promotion-internationale')
print('  pdflatex article_mnras.tex')
print('  bibtex  article_mnras')
print('  pdflatex article_mnras.tex')
print('  pdflatex article_mnras.tex')
print()
print('─── Fichiers requis dans le même dossier ───')
print('  mnras.cls   → télécharger sur https://www.ctan.org/pkg/mnras')
print('  refs_mnras.bib  → déjà présent ✓')
print()
print('─── Vérifications manuelles recommandées ───')
print('  1. Équations numérotées (1)–(10) : vérifier le rendu')
print('  2. Tableaux : ajuster largeur colonnes si besoin')
print('  3. Références croisées \\cite{} : vérifier concordance avec .bib')
