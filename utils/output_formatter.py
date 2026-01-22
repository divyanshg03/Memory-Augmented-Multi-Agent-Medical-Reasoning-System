import textwrap

def format_clinical_output(result: dict) -> str:
    """
    Formats FINAL synthesized clinical output.
    Prints ONCE per episode.
    """

    lines = []

    # ================= HEADER =================
    lines.append("=" * 80)
    lines.append("🧠 CLINICAL DECISION SUPPORT REPORT")
    lines.append("=" * 80)
    lines.append("")

    # ================= METADATA =================
    lines.append(f"🧍 Patient ID      : {result['patient_id']}")
    lines.append(f"📌 Episode ID      : {result['episode_id']}")
    lines.append(f"📊 Confidence     : {int(result['confidence'] * 100)}%")
    lines.append(
        f"⚠️  Disagreement  : {'Yes' if result['disagreement'] else 'No'}"
    )
    lines.append("")
    lines.append("-" * 80)
    lines.append("")

    # ================= FINAL DECISION =================
    lines.append(result["final_decision"].strip())
    lines.append("")

    # ================= DISCLAIMER =================
    lines.append("-" * 80)
    lines.append("⚠️  DISCLAIMER")
    lines.append(
        "This output is for decision-support only and does not constitute a\n"
        "medical diagnosis. Clinical judgment and appropriate investigations\n"
        "are required before any definitive conclusions."
    )

    return "\n".join(lines)
