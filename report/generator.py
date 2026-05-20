import json
import os
from datetime import datetime
from jinja2 import Template

def calculate_score(violations):
    """
    Calcule le score architectural (0-100)
    100 = parfait, 0 = catastrophique
    """
    if not violations:
        return 100

    deductions = {
        "CRITICAL": 20,
        "WARNING":  10
    }

    score = 100
    for v in violations:
        score -= deductions.get(v["severity"], 5)

    return max(0, score)


def get_score_color(score):
    if score >= 80:
        return "green"
    elif score >= 50:
        return "orange"
    else:
        return "red"


def generate_report(violations, project_path, output_path="report.html"):
    """
    Génère un rapport HTML à partir des violations
    """

    score       = calculate_score(violations)
    color       = get_score_color(score)
    criticals   = [v for v in violations if v["severity"] == "CRITICAL"]
    warnings    = [v for v in violations if v["severity"] == "WARNING"]
    date        = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Lire le template
    template_path = os.path.join(
        os.path.dirname(__file__),
        "template.html"
    )

    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    # Générer le HTML
    html = template.render(
        project_path = project_path,
        date         = date,
        score        = score,
        score_color  = color,
        violations   = violations,
        criticals    = criticals,
        warnings     = warnings,
        total        = len(violations)
    )

    # Sauvegarder
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"📄 Rapport généré : {output_path}")
    return output_path