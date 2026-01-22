import textwrap


def format_clinical_output(result: dict) -> str:
    """
    Converts raw pipeline output into a clean, readable report.
    """

    episode_id = result.get("episode_id", "N/A")
    decision = result.get("final_decision", "")
    confidence = result.get("confidence", 0.0)
    disagreement = result.get("disagreement", False)

    header = (
        "=" * 80 + "\n"
        "🧠 CLINICAL DECISION SUPPORT REPORT\n"
        "=" * 80
    )

    meta = (
        f"\n📌 Episode ID      : {episode_id}\n"
        f"📊 Confidence     : {round(confidence * 100)}%\n"
        f"⚠️  Disagreement  : {'Yes' if disagreement else 'No'}\n"
        "-" * 80
    )

    body = textwrap.dedent(decision).strip()

    footer = (
        "\n" + "-" * 80 +
        "\n⚠️  DISCLAIMER\n"
        "This output is for decision-support only and does not constitute a\n"
        "medical diagnosis. Clinical judgment and appropriate investigations\n"
        "are required before any definitive conclusions.\n"
        "=" * 80
    )

    return f"{header}\n{meta}\n\n{body}\n{footer}"
