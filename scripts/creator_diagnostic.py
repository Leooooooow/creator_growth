#!/usr/bin/env python3
"""
Creator Diagnostic Radar Chart Generator
生成达人六维能力雷达图

Usage:
    python creator_diagnostic.py --name "Kris" \
        --content 8 --visual 6 --engagement 4 \
        --operations 5 --business 2 --mindset 7 \
        --output radar.png

Dependencies: matplotlib (pip install matplotlib)
"""

import argparse
import math
import sys

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    from matplotlib.patches import FancyBboxPatch
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


# ── Dimension labels (Chinese + English) ──────────────────────
DIMENSIONS = [
    ("内容力", "Content"),
    ("视觉力", "Visual"),
    ("互动力", "Engage"),
    ("运营力", "Ops"),
    ("商业力", "Biz"),
    ("心态力", "Mind"),
]

# ── Stage thresholds ──────────────────────────────────
STAGE_THRESHOLDS = [
    (0, 15, "新手期", "#E74C3C"),
    (15, 30, "成长期", "#F39C12"),
    (30, 45, "稳定期", "#2ECC71"),
    (45, 60, "成熟期", "#3498DB"),
]


def get_stage(total_score: int) -> tuple:
    """Determine creator's growth stage based on total score."""
    for low, high, name, color in STAGE_THRESHOLDS:
        if low <= total_score < high:
            return name, color
    return "成熟期", "#3498DB"


def generate_text_radar(name: str, scores: list[int]) -> str:
    """Generate a text-based radar chart (no matplotlib needed)."""
    lines = []
    lines.append(f"\n📊 {name} 的达人能力雷达\n")
    lines.append("=" * 45)

    total = sum(scores)
    stage_name, _ = get_stage(total)

    for (cn, en), score in zip(DIMENSIONS, scores):
        bar = "█" * score + "░" * (10 - score)
        lines.append(f"  {cn:4s} ({en:7s}): {bar} {score}/10")

    lines.append("=" * 45)
    lines.append(f"  总分: {total}/60 | 阶段: {stage_name}")
    lines.append("")

    # Find top weakness and strength
    max_idx = scores.index(max(scores))
    min_idx = scores.index(min(scores))
    lines.append(f"  💪 最强: {DIMENSIONS[max_idx][0]} ({scores[max_idx]}/10)")
    lines.append(f"  🎯 优先提升: {DIMENSIONS[min_idx][0]} ({scores[min_idx]}/10)")
    lines.append("")

    return "\n".join(lines)


def generate_radar_chart(name: str, scores: list[int], output_path: str) -> str:
    """Generate a visual radar chart PNG using matplotlib."""
    if not HAS_MATPLOTLIB:
        return generate_text_radar(name, scores)

    # Setup
    N = len(DIMENSIONS)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]  # close the polygon
    values = scores + scores[:1]

    total = sum(scores)
    stage_name, stage_color = get_stage(total)

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    # Draw the radar
    ax.plot(angles, values, 'o-', linewidth=2.5, color='#e94560', markersize=8)
    ax.fill(angles, values, alpha=0.25, color='#e94560')

    # Grid styling
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], color='#888', size=9)
    ax.grid(color='#333', linewidth=0.5)

    # Dimension labels
    labels = [f"{cn}\n{en}" for cn, en in DIMENSIONS]
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=12, color='#ddd', fontweight='bold')

    # Title
    ax.set_title(
        f"{name} · 达人能力雷达",
        size=18, color='#fff', fontweight='bold', pad=30
    )

    # Stage badge
    fig.text(
        0.5, 0.02,
        f"总分 {total}/60  ·  {stage_name}",
        ha='center', va='bottom',
        fontsize=14, color=stage_color, fontweight='bold'
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    return f"Radar chart saved to {output_path}"


def main():
    parser = argparse.ArgumentParser(description="Generate creator diagnostic radar chart")
    parser.add_argument("--name", required=True, help="Creator's name")
    parser.add_argument("--content", type=int, required=True, help="Content quality (1-10)")
    parser.add_argument("--visual", type=int, required=True, help="Visual quality (1-10)")
    parser.add_argument("--engagement", type=int, required=True, help="Engagement (1-10)")
    parser.add_argument("--operations", type=int, required=True, help="Operations (1-10)")
    parser.add_argument("--business", type=int, required=True, help="Business (1-10)")
    parser.add_argument("--mindset", type=int, required=True, help="Mindset (1-10)")
    parser.add_argument("--output", default="radar.png", help="Output file path")
    parser.add_argument("--text-only", action="store_true", help="Output text only (no matplotlib)")

    args = parser.parse_args()

    scores = [args.content, args.visual, args.engagement,
              args.operations, args.business, args.mindset]

    # Validate scores
    for s, (cn, _) in zip(scores, DIMENSIONS):
        if not 1 <= s <= 10:
            print(f"Error: {cn} score must be 1-10, got {s}", file=sys.stderr)
            sys.exit(1)

    if args.text_only or not HAS_MATPLOTLIB:
        print(generate_text_radar(args.name, scores))
    else:
        result = generate_radar_chart(args.name, scores, args.output)
        print(result)
        # Also print text version
        print(generate_text_radar(args.name, scores))


if __name__ == "__main__":
    main()
