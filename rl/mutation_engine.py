"""Mutation engine: break passing Manim scenes in rubric-measurable ways.

Every mutation maps to components of the m2m2_visual_repair rubric
(scoring.py), so the resulting repair task has an honest gradient: the
mutated (broken) code scores meaningfully lower than the gold original,
and a correct repair restores exactly what the rubric measures.

Difficulties:
    easy   - single binary break (safety / parse / scene class)
    normal - layout-quality degradations the rubric's layout_static sees
    hard   - stacked combinations
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Mutation:
    name: str
    difficulty: str
    targets: tuple[str, ...]
    apply: Callable[[str], str | None]


WIDTH_GUARD_RE = re.compile(r"\.(?:scale_to_fit_width|set_width)\([^)]*\)")
FADEOUT_PLAY_RE = re.compile(r"^[ \t]*self\.play\(\s*FadeOut\([^\n]*\)\s*\)?\s*\n", re.MULTILINE)
FONT_SIZE_RE = re.compile(r"font_size\s*=\s*(\d+(?:\.\d+)?)")
BUFF_RE = re.compile(r"buff\s*=\s*[0-9.]+")
ARRANGE_RE = re.compile(r"\.arrange\(")
MANIM_IMPORT_RE = re.compile(r"^(from manim import \*.*)$", re.MULTILINE)
CONSTRUCT_RE = re.compile(r"def construct\(")


def _strip_width_guards(code: str) -> str | None:
    if not WIDTH_GUARD_RE.search(code):
        return None
    return WIDTH_GUARD_RE.sub("", code)


def _drop_fadeouts(code: str) -> str | None:
    if not FADEOUT_PLAY_RE.search(code):
        return None
    return FADEOUT_PLAY_RE.sub("", code)


def _inflate_text(code: str) -> str | None:
    def bump(match: re.Match) -> str:
        size = float(match.group(1))
        return f"font_size={min(110, int(size * 1.9))}"

    out, count = FONT_SIZE_RE.subn(bump, code)
    return out if count else None


def _dense_arrange(code: str) -> str | None:
    if BUFF_RE.search(code):
        return BUFF_RE.sub("buff=0.05", code)
    if ARRANGE_RE.search(code):
        return ARRANGE_RE.sub(".arrange(buff=0.05, ", code)
    return None


def _unsafe_import(code: str) -> str | None:
    if "import os" in code:
        return None
    if MANIM_IMPORT_RE.search(code):
        return MANIM_IMPORT_RE.sub(r"\1\nimport os", code, count=1)
    return "import os\n" + code


def _break_construct(code: str) -> str | None:
    if not CONSTRUCT_RE.search(code):
        return None
    return CONSTRUCT_RE.sub("def build_scene(", code, count=1)


def _syntax_break(code: str) -> str | None:
    idx = code.find("self.play(")
    if idx < 0:
        return None
    return code[:idx] + "self.play" + code[idx + len("self.play("):]


CROWD_BLOCK = (
    '        _crowd_1 = Text("Auxiliary caption that never leaves the frame", font_size=44)\n'
    "        self.add_fixed_in_frame_mobjects(_crowd_1)\n"
    '        _crowd_2 = Text("A second persistent overlay fighting for attention", font_size=44)\n'
    "        self.add_fixed_in_frame_mobjects(_crowd_2)\n"
    '        _crowd_3 = MathTex(r"\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2} \\;\\;\\;\\; \\text{unguarded wide formula caption}", font_size=42)\n'
    "        self.add_fixed_in_frame_mobjects(_crowd_3)\n"
    '        _crowd_4 = Text("Yet another fixed note stacked on top of everything", font_size=44)\n'
    "        self.add_fixed_in_frame_mobjects(_crowd_4)\n"
)


def _crowd_overlays(code: str) -> str | None:
    match = re.search(r"^([ \t]*)def construct\(self\):\s*$", code, re.MULTILINE)
    if not match:
        return None
    insert_at = match.end()
    return code[:insert_at] + "\n" + CROWD_BLOCK + code[insert_at:]


def _compose(*mutations: Mutation) -> Callable[[str], str | None]:
    def apply(code: str) -> str | None:
        out = code
        applied = 0
        for mutation in mutations:
            result = mutation.apply(out)
            if result is not None:
                out = result
                applied += 1
        return out if applied == len(mutations) else None

    return apply


STRIP_GUARDS = Mutation("strip_width_guards", "normal", ("layout_static", "acceptance_terms"), _strip_width_guards)
DROP_FADEOUTS = Mutation("drop_fadeouts", "normal", ("layout_static", "acceptance_terms"), _drop_fadeouts)
INFLATE_TEXT = Mutation("inflate_text", "normal", ("layout_static",), _inflate_text)
DENSE_ARRANGE = Mutation("dense_arrange", "normal", ("layout_static",), _dense_arrange)
CROWD_OVERLAYS = Mutation("crowd_overlays", "normal", ("layout_static",), _crowd_overlays)
UNSAFE_IMPORT = Mutation("unsafe_import", "easy", ("safety",), _unsafe_import)
BREAK_CONSTRUCT = Mutation("break_construct", "easy", ("static_validation",), _break_construct)
SYNTAX_BREAK = Mutation("syntax_break", "easy", ("python_parse",), _syntax_break)

EASY = [UNSAFE_IMPORT, BREAK_CONSTRUCT, SYNTAX_BREAK]
NORMAL = [CROWD_OVERLAYS, STRIP_GUARDS, DROP_FADEOUTS, INFLATE_TEXT, DENSE_ARRANGE]


def hard_combos() -> list[Mutation]:
    """Stacked mutations for hard tasks (built lazily so compose stays pure)."""

    return [
        Mutation(
            "crowd_plus_strip",
            "hard",
            ("layout_static", "acceptance_terms"),
            _compose(CROWD_OVERLAYS, STRIP_GUARDS),
        ),
        Mutation(
            "crowd_plus_inflate",
            "hard",
            ("layout_static",),
            _compose(CROWD_OVERLAYS, INFLATE_TEXT),
        ),
        Mutation(
            "crowd_plus_fadeouts",
            "hard",
            ("layout_static", "acceptance_terms"),
            _compose(CROWD_OVERLAYS, DROP_FADEOUTS),
        ),
    ]
