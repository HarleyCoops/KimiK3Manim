"""Verifiers v1/RLM environment wiring for M2M2 generated-code repair."""

from __future__ import annotations

import inspect
import json
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

from .scoring import ScoreResult, extract_generated_code_payload, score_completion, term_score


PACKAGE_ROOT = Path(__file__).resolve().parent
RLM_TASK_TYPE = "m2m2_rlm_repair"
RLM_QUESTION = "Inspect the external M2M2 run bundle and repair the Manim code. Submit GeneratedCode only."
RLM_WORKDIR = "/workspace"
RLM_BUNDLE_DIR = f"{RLM_WORKDIR}/run_bundle"
RLM_TASK_PATH = f"{RLM_WORKDIR}/m2m2_task.json"
RLM_SUBMISSION_PATH = f"{RLM_WORKDIR}/submission/generated_code.json"
RLM_HELPER_METRICS_PATH = f"{RLM_WORKDIR}/submission/metrics.json"

RLM_INSTRUCTION = """Inspect the external M2M2 run bundle and repair the Manim code.

The run bundle is available on the filesystem at /workspace/run_bundle. Treat it as
read-only evidence. Do not paste the bundle into the prompt or rewrite upstream
planning artifacts. Produce a better GeneratedCode artifact for generated_scene.py.

The Python REPL has these helpers preloaded:

list_artifacts()
load_artifact("scene_spec")
load_artifact("storyboard")
read_generated_scene()
search_trace("layout")
validate_candidate(code)
score_candidate(scene_name, code)
submit_generated_code(scene_name, code)

Work on candidate code in the REPL, use the trace and artifacts as evidence, then
finish by calling submit_generated_code(scene_name, improved_code). The output is
the repaired GeneratedCode only.
"""

SITECUSTOMIZE_SOURCE = """try:
    from m2m2_rlm_helpers import install_builtins

    install_builtins()
except Exception as exc:
    print(f"m2m2 RLM helper preload failed: {exc}")
"""

HELPER_SOURCE = r'''
from __future__ import annotations

import builtins
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

from m2m2_visual_repair.scoring import (
    discover_scene_classes,
    score_completion,
    validate_source,
)

BUNDLE_DIR = Path(os.environ.get("M2M2_RLM_BUNDLE_DIR", "/workspace/run_bundle"))
TASK_PATH = Path(os.environ.get("M2M2_RLM_TASK_PATH", "/workspace/m2m2_task.json"))
CANDIDATE_DIR = Path(os.environ.get("M2M2_RLM_CANDIDATE_DIR", "/workspace/candidate"))
SUBMISSION_PATH = Path(os.environ.get("M2M2_RLM_SUBMISSION_PATH", "/workspace/submission/generated_code.json"))
METRICS_PATH = Path(os.environ.get("M2M2_RLM_HELPER_METRICS_PATH", "/workspace/submission/metrics.json"))


def _read_metrics() -> dict[str, Any]:
    if not METRICS_PATH.exists():
        return {}
    try:
        data = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _write_metrics(metrics: dict[str, Any]) -> None:
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(metrics, sort_keys=True), encoding="utf-8")


def _increment_metric(name: str, amount: int = 1) -> None:
    metrics = _read_metrics()
    metrics[name] = int(metrics.get(name, 0) or 0) + amount
    _write_metrics(metrics)


def _artifact_candidates(name: str) -> list[Path]:
    if "/" in name or "\\" in name or ".." in name:
        raise ValueError("artifact name must be a simple filename or stem")
    raw = Path(name)
    if raw.suffix:
        return [BUNDLE_DIR / raw.name]
    return [
        BUNDLE_DIR / f"{name}.json",
        BUNDLE_DIR / f"{name}.jsonl",
        BUNDLE_DIR / f"{name}.py",
        BUNDLE_DIR / name,
    ]


def _artifact_path(name: str) -> Path:
    for path in _artifact_candidates(name):
        if path.exists():
            return path
    tried = ", ".join(str(path.name) for path in _artifact_candidates(name))
    raise FileNotFoundError(f"artifact not found: {name!r}; tried {tried}")


def _load_jsonl(path: Path) -> list[Any]:
    rows = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"raw": line})
    return rows


def _load_artifact_no_metric(name: str) -> Any:
    path = _artifact_path(name)
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if path.suffix == ".jsonl":
        return _load_jsonl(path)
    return path.read_text(encoding="utf-8")


def list_artifacts() -> list[str]:
    """Return artifact filenames available in the external run bundle."""

    _increment_metric("artifact_list_calls")
    if not BUNDLE_DIR.exists():
        return []
    return sorted(path.name for path in BUNDLE_DIR.iterdir() if path.is_file())


def load_artifact(name: str) -> Any:
    """Load one run-bundle artifact by stem or filename."""

    _increment_metric("artifacts_read")
    return _load_artifact_no_metric(name)


def read_generated_scene() -> str:
    """Read the canonical generated_scene.py from the run bundle."""

    _increment_metric("artifacts_read")
    return _artifact_path("generated_scene.py").read_text(encoding="utf-8")


def search_trace(term: str) -> list[Any]:
    """Return trace.jsonl entries whose JSON/text representation contains term."""

    _increment_metric("artifacts_read")
    _increment_metric("trace_search_calls")
    needle = str(term).casefold()
    try:
        rows = _load_artifact_no_metric("trace")
    except FileNotFoundError:
        return []
    matches = []
    for row in rows:
        text = json.dumps(row, sort_keys=True, default=str) if not isinstance(row, str) else row
        if needle in text.casefold():
            matches.append(row)
    return matches


def _write_candidate(code: str) -> Path:
    CANDIDATE_DIR.mkdir(parents=True, exist_ok=True)
    path = CANDIDATE_DIR / "generated_scene.py"
    path.write_text(code, encoding="utf-8")
    return path


def validate_candidate(code: str) -> dict[str, Any]:
    """Validate candidate Manim code with static checks and update the working copy."""

    _increment_metric("validation_calls")
    _write_candidate(code)
    result = validate_source(code)
    scene_classes = discover_scene_classes(code) if result.get("parsed") else []
    return {
        "parsed": bool(result.get("parsed")),
        "unsafe": bool(result.get("unsafe")),
        "errors": result.get("errors") or [],
        "scene_classes": scene_classes,
    }


def _task_payload() -> dict[str, Any]:
    if not TASK_PATH.exists():
        return {}
    try:
        data = json.loads(TASK_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _generated_payload(scene_name: str, code: str) -> dict[str, Any]:
    try:
        base = _load_artifact_no_metric("generated_code")
    except Exception:
        base = {}
    if not isinstance(base, dict):
        base = {}
    metadata = base.get("metadata") if isinstance(base.get("metadata"), dict) else {}
    return {
        "scene_name": scene_name,
        "language": "python",
        "code": code,
        "dependencies": base.get("dependencies") or ["manim"],
        "manim_version": base.get("manim_version"),
        "source_spec_id": base.get("source_spec_id"),
        "checksum": hashlib.sha256(code.encode("utf-8")).hexdigest(),
        "metadata": {
            **metadata,
            "file_path": "generated_scene.py",
            "rlm_repair": True,
        },
    }


def _tagged_generated_code(payload: dict[str, Any]) -> str:
    return "<generated_code>" + json.dumps(payload, sort_keys=True) + "</generated_code>"


def _scene_spec_alignment(scene_name: str, code: str) -> float:
    try:
        scene_spec = _load_artifact_no_metric("scene_spec")
    except Exception:
        scene_spec = {}
    if not isinstance(scene_spec, dict):
        return 0.0
    expected_scene = str(scene_spec.get("scene_name") or "")
    scene_match = 1.0 if (not expected_scene or scene_name == expected_scene) else 0.0
    class_match = 1.0 if re.search(rf"class\s+{re.escape(scene_name)}\b", code) else 0.0
    terms: list[str] = []
    for item in scene_spec.get("objects") or []:
        if isinstance(item, dict):
            terms.extend(str(item.get(key) or "") for key in ("id", "type"))
    for item in scene_spec.get("animations") or []:
        if isinstance(item, dict):
            terms.extend(str(item.get(key) or "") for key in ("action", "target"))
    terms.extend(str(item) for item in scene_spec.get("code_requirements") or [])
    normalized_terms = []
    seen = set()
    for term in terms:
        for token in re.findall(r"[A-Za-z][A-Za-z0-9_ -]{2,}", term):
            key = " ".join(token.casefold().split())
            if key and key not in seen:
                seen.add(key)
                normalized_terms.append(token)
            if len(normalized_terms) >= 24:
                break
        if len(normalized_terms) >= 24:
            break
    if normalized_terms:
        haystack = " ".join(code.casefold().split())
        term_hits = sum(1 for term in normalized_terms if " ".join(term.casefold().split()) in haystack)
        term_score = term_hits / len(normalized_terms)
    else:
        term_score = 1.0
    return round(0.25 * scene_match + 0.25 * class_match + 0.50 * term_score, 6)


def score_candidate(scene_name: str, code: str) -> dict[str, Any]:
    """Score candidate code with the same static reward used by training."""

    _increment_metric("validation_calls")
    _increment_metric("scoring_calls")
    _write_candidate(code)
    payload = _generated_payload(scene_name, code)
    result = score_completion(_task_payload(), _tagged_generated_code(payload))
    return {
        "final_code_score": result.score,
        "scene_spec_alignment": _scene_spec_alignment(scene_name, code),
        "components": result.components,
        "errors": result.errors,
        "scene_classes": result.scene_classes,
    }


def submit_generated_code(scene_name: str, code: str) -> str:
    """Submit the repaired GeneratedCode artifact without modifying the run bundle."""

    _increment_metric("submission_calls")
    _write_candidate(code)
    payload = _generated_payload(scene_name, code)
    SUBMISSION_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUBMISSION_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return _tagged_generated_code(payload)


def install_builtins() -> None:
    for name in (
        "list_artifacts",
        "load_artifact",
        "read_generated_scene",
        "search_trace",
        "validate_candidate",
        "score_candidate",
        "submit_generated_code",
    ):
        setattr(builtins, name, globals()[name])
'''


def build_rlm_records(entries: list[dict[str, Any]], task_filter: Optional[Sequence[str]] = None) -> list[dict[str, Any]]:
    """Build Verifiers v1/RLM task rows without putting run-bundle artifacts in the prompt."""

    allowed = {item.lower() for item in task_filter or []}
    records = []
    for index, raw_task in enumerate(entries):
        task_payload = _ensure_context(raw_task)
        task_type = str(task_payload.get("task_type") or RLM_TASK_TYPE)
        if allowed and task_type.lower() not in allowed:
            continue
        task_id = str(task_payload.get("task_id") or f"m2m2_rlm_repair_{index:05d}")
        scoring_task = _scoring_task(task_payload)
        context = task_payload.get("context") if isinstance(task_payload.get("context"), dict) else {"artifacts": {}}
        records.append(
            {
                "id": task_id,
                "task_id": task_id,
                # verifiers>=0.2: top-level "task" strings are no longer valid
                # rollout inputs; keep the type inside info instead.
                "question": RLM_QUESTION,
                "instruction": RLM_INSTRUCTION,
                "answer": json.dumps(scoring_task, sort_keys=True),
                "info": {
                    "task_id": task_id,
                    "task_type": RLM_TASK_TYPE,
                    "scene_name": task_payload.get("scene_name"),
                    "acceptance_terms": task_payload.get("acceptance_terms") or [],
                    "context": context,
                },
                "program": {
                    "files": _bundle_program_files(task_payload, scoring_task),
                },
            }
        )
    return records


def load_rlm_environment(
    train_records: list[dict[str, Any]],
    eval_records: list[dict[str, Any]] | None = None,
    *,
    sampling_args: Optional[dict[str, Any]] = None,
    system_prompt: str | None = None,
    rlm_max_turns: int = 100,
    rlm_exec_timeout: int = 300,
    rlm_max_depth: int = 0,
    summarize_at_tokens: int | tuple[int, int] | list[int] | None = None,
    local_checkout: str | Path | None = None,
    sandbox: bool | Mapping[str, object] = True,
) -> Any:
    """Load the Verifiers v1 RLM environment for filesystem-backed repair."""

    try:
        import verifiers as vf

        Env = getattr(vf, "Env")
        Taskset = getattr(vf, "Taskset")
        RLM = getattr(vf, "RLM", None)
        if RLM is None:
            rlm_module = __import__("verifiers.v1.packages.harnesses.rlm", fromlist=["RLM"])
            RLM = getattr(rlm_module, "RLM")
    except (AttributeError, ModuleNotFoundError) as exc:
        raise RuntimeError(
            "Verifiers v1/RLM is unavailable in this Python runtime. "
            "Use verifiers>=0.1.14 on Linux/WSL/Prime; the current package imports "
            "POSIX fcntl for its RLM harness."
        ) from exc

    _patch_renderer_pool_compatibility()

    metrics = [
        scene_spec_alignment,
        acceptance_terms,
        layout_static,
        safety,
        repl_turns,
        artifacts_read,
        validation_calls,
    ]
    rewards = [final_code_score]
    taskset_config = {
        "source": train_records,
        "eval_source": eval_records,
        "taskset_id": RLM_TASK_TYPE,
        "metrics": metrics,
        "rewards": rewards,
    }
    try:
        taskset = Taskset(
            source=train_records,
            eval_source=eval_records,
            taskset_id=RLM_TASK_TYPE,
            metrics=metrics,
            rewards=rewards,
        )
    except TypeError as exc:
        message = str(exc)
        if "source" not in message and "required positional" not in message:
            raise
        try:
            taskset = Taskset(config=taskset_config)
        except TypeError as config_exc:
            if "config" not in str(config_exc) and "unexpected keyword" not in str(config_exc):
                raise
            try:
                taskset = Taskset(
                    train_records,
                    eval_records,
                    RLM_TASK_TYPE,
                    metrics=metrics,
                    rewards=rewards,
                )
            except TypeError as fallback_exc:
                if "metrics" not in str(fallback_exc) and "rewards" not in str(fallback_exc):
                    raise
                taskset = Taskset(train_records, eval_records, RLM_TASK_TYPE)
                for metric in metrics:
                    if hasattr(taskset, "add_metric"):
                        taskset.add_metric(metric)
                    else:
                        taskset.metrics = [*getattr(taskset, "metrics", []), metric]
                for reward in rewards:
                    if hasattr(taskset, "add_reward"):
                        taskset.add_reward(reward)
                    else:
                        taskset.rewards = [*getattr(taskset, "rewards", []), reward]
    harness = RLM(
        rlm_max_turns=rlm_max_turns,
        rlm_exec_timeout=rlm_exec_timeout,
        rlm_max_depth=rlm_max_depth,
        summarize_at_tokens=summarize_at_tokens,
        append_to_system_prompt=system_prompt or "",
        local_checkout=local_checkout,
        sandbox=sandbox,
        sampling_args=sampling_args,
        program={
            "files": _static_program_files(),
            "env": {
                "PYTHONPATH": RLM_WORKDIR,
                "M2M2_RLM_BUNDLE_DIR": RLM_BUNDLE_DIR,
                "M2M2_RLM_TASK_PATH": RLM_TASK_PATH,
                "M2M2_RLM_CANDIDATE_DIR": f"{RLM_WORKDIR}/candidate",
                "M2M2_RLM_SUBMISSION_PATH": RLM_SUBMISSION_PATH,
                "M2M2_RLM_HELPER_METRICS_PATH": RLM_HELPER_METRICS_PATH,
            },
            "artifacts": {
                "submitted_generated_code": {
                    "path": RLM_SUBMISSION_PATH,
                    "format": "json",
                    "optional": True,
                },
                "m2m2_helper_metrics": {
                    "path": RLM_HELPER_METRICS_PATH,
                    "format": "json",
                    "optional": True,
                },
            },
        },
    )
    return Env(taskset=taskset, harness=harness)


def _patch_renderer_pool_compatibility() -> None:
    """Keep Verifiers 0.1.14 compatible with Prime's platform renderers build."""

    try:
        import verifiers.clients.renderer_client as renderer_client  # type: ignore[import-not-found]
    except Exception:
        return

    create_pool = getattr(renderer_client, "create_renderer_pool", None)
    if create_pool is None or getattr(create_pool, "_m2m2_renderer_compat", False):
        return
    try:
        parameters = inspect.signature(create_pool).parameters
    except (TypeError, ValueError):
        return
    unsupported_kwargs = {"renderer", "tool_parser"} - set(parameters)
    if not unsupported_kwargs:
        return

    def create_renderer_pool_compat(tokenizer_name_or_path: str, *args: Any, **kwargs: Any) -> Any:
        for key in unsupported_kwargs:
            kwargs.pop(key, None)
        return create_pool(tokenizer_name_or_path, *args, **kwargs)

    create_renderer_pool_compat._m2m2_renderer_compat = True  # type: ignore[attr-defined]
    renderer_client.create_renderer_pool = create_renderer_pool_compat


async def final_code_score(task: Mapping[str, Any], state: Mapping[str, Any]) -> float:
    return _score_state(task, state).score


async def scene_spec_alignment(task: Mapping[str, Any], state: Mapping[str, Any]) -> float:
    generated = _generated_from_state(state)
    task_payload = _task_payload(task)
    if not generated:
        return 0.0
    return _alignment_score(task_payload.get("scene_spec"), str(generated.get("scene_name") or ""), str(generated.get("code") or ""))


async def acceptance_terms(task: Mapping[str, Any], state: Mapping[str, Any]) -> float:
    return _score_state(task, state).components.get("acceptance_terms", 0.0)


async def layout_static(task: Mapping[str, Any], state: Mapping[str, Any]) -> float:
    return _score_state(task, state).components.get("layout_static", 0.0)


async def safety(task: Mapping[str, Any], state: Mapping[str, Any]) -> float:
    return _score_state(task, state).components.get("safety", 0.0)


async def repl_turns(task: Mapping[str, Any], state: Mapping[str, Any]) -> float:
    _ = task
    return _artifact_number(state, "rlm_metrics", "repl_call_count")


async def artifacts_read(task: Mapping[str, Any], state: Mapping[str, Any]) -> float:
    _ = task
    return _artifact_number(state, "m2m2_helper_metrics", "artifacts_read")


async def validation_calls(task: Mapping[str, Any], state: Mapping[str, Any]) -> float:
    _ = task
    return _artifact_number(state, "m2m2_helper_metrics", "validation_calls")


def _score_state(task: Mapping[str, Any], state: Mapping[str, Any]) -> ScoreResult:
    task_payload = _task_payload(task)
    generated = _generated_from_state(state)
    if generated is not None:
        completion = "<generated_code>" + json.dumps(generated, sort_keys=True) + "</generated_code>"
    else:
        completion = _completion_text(state)
    return score_completion(task_payload, completion)


def _generated_from_state(state: Mapping[str, Any]) -> dict[str, Any] | None:
    artifacts = state.get("artifacts")
    if isinstance(artifacts, Mapping):
        submitted = artifacts.get("submitted_generated_code")
        if isinstance(submitted, dict):
            return submitted
    payload, _ = extract_generated_code_payload(_completion_text(state))
    if payload is None:
        return None
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def _completion_text(state: Mapping[str, Any]) -> str:
    completion = state.get("completion")
    if isinstance(completion, str):
        return completion
    if isinstance(completion, list):
        parts = []
        for message in completion:
            if not isinstance(message, Mapping) or message.get("role") != "assistant":
                continue
            content = message.get("content")
            if isinstance(content, str):
                parts.append(content)
        return "\n".join(parts)
    return ""


def _task_payload(task: Mapping[str, Any]) -> dict[str, Any]:
    answer = task.get("answer")
    if isinstance(answer, str):
        try:
            payload = json.loads(answer)
        except json.JSONDecodeError:
            payload = {}
        if isinstance(payload, dict):
            return payload
    return _scoring_task(dict(task))


def _artifact_number(state: Mapping[str, Any], artifact_name: str, key: str) -> float:
    artifacts = state.get("artifacts")
    if not isinstance(artifacts, Mapping):
        return 0.0
    payload = artifacts.get(artifact_name)
    if not isinstance(payload, Mapping):
        return 0.0
    return float(payload.get(key, 0.0) or 0.0)


def _alignment_score(scene_spec: Any, scene_name: str, code: str) -> float:
    if not isinstance(scene_spec, Mapping):
        return 0.0
    expected_scene = str(scene_spec.get("scene_name") or "")
    scene_match = 1.0 if (not expected_scene or scene_name == expected_scene) else 0.0
    class_match = 1.0 if f"class {scene_name}" in code else 0.0
    terms = _scene_spec_terms(scene_spec)
    terms_score = term_score(terms, code) if terms else 1.0
    return round(0.25 * scene_match + 0.25 * class_match + 0.50 * terms_score, 6)


def _scene_spec_terms(scene_spec: Mapping[str, Any]) -> list[str]:
    terms: list[str] = []
    for item in scene_spec.get("objects") or []:
        if isinstance(item, Mapping):
            terms.extend(str(item.get(key) or "") for key in ("id", "type"))
    for item in scene_spec.get("animations") or []:
        if isinstance(item, Mapping):
            terms.extend(str(item.get(key) or "") for key in ("action", "target"))
    terms.extend(str(item) for item in scene_spec.get("code_requirements") or [])
    normalized: list[str] = []
    seen: set[str] = set()
    for term in terms:
        cleaned = " ".join(term.split())
        key = cleaned.casefold()
        if len(cleaned) < 3 or key in seen:
            continue
        normalized.append(cleaned)
        seen.add(key)
        if len(normalized) >= 24:
            break
    return normalized


def _ensure_context(task: dict[str, Any]) -> dict[str, Any]:
    payload = dict(task)
    context = payload.get("context") if isinstance(payload.get("context"), dict) else {}
    artifacts = context.get("artifacts") if isinstance(context.get("artifacts"), dict) else {}
    if artifacts:
        return payload
    artifacts = {}
    if payload.get("request"):
        artifacts["request.json"] = payload["request"]
    elif payload.get("prompt"):
        artifacts["request.json"] = {
            "prompt": payload.get("prompt"),
            "target_audience": payload.get("audience"),
            "style": payload.get("style"),
            "duration_seconds": payload.get("duration_seconds"),
        }
    for key, filename in {
        "intent": "intent.json",
        "knowledge_graph": "knowledge_graph.json",
        "curriculum": "curriculum.json",
        "math_packet": "math_packet.json",
        "storyboard": "storyboard.json",
        "scene_spec": "scene_spec.json",
        "generated_code": "generated_code.json",
    }.items():
        if payload.get(key) is not None:
            artifacts[filename] = payload[key]
    generated = payload.get("generated_code") if isinstance(payload.get("generated_code"), dict) else {}
    if generated.get("code"):
        artifacts["generated_scene.py"] = generated["code"]
    evidence = payload.get("evidence") if isinstance(payload.get("evidence"), dict) else {}
    for key, filename in {
        "validation": "validation_report.json",
        "render": "render_result.json",
        "review": "review_report.json",
    }.items():
        if evidence.get(key) is not None:
            artifacts[filename] = evidence[key]
    payload["context"] = {"artifacts": artifacts}
    return payload


def _scoring_task(task: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in task.items()
        if key not in {"context", "program", "info"}
    }


def _bundle_program_files(task: Mapping[str, Any], scoring_task: Mapping[str, Any]) -> dict[str, str]:
    context = task.get("context") if isinstance(task.get("context"), Mapping) else {}
    artifacts = context.get("artifacts") if isinstance(context.get("artifacts"), Mapping) else {}
    files = {
        RLM_TASK_PATH: json.dumps(scoring_task, indent=2, sort_keys=True, ensure_ascii=True),
    }
    for filename, value in artifacts.items():
        files[f"{RLM_BUNDLE_DIR}/{filename}"] = _artifact_content(str(filename), value)
    return files


def _artifact_content(filename: str, value: Any) -> str:
    if filename.endswith(".jsonl") and isinstance(value, list):
        return "\n".join(json.dumps(row, sort_keys=True, ensure_ascii=True, default=str) for row in value) + "\n"
    if filename.endswith(".json"):
        return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True, default=str)
    return str(value)


def _static_program_files() -> dict[str, str]:
    return {
        f"{RLM_WORKDIR}/sitecustomize.py": SITECUSTOMIZE_SOURCE,
        f"{RLM_WORKDIR}/m2m2_rlm_helpers.py": HELPER_SOURCE,
        f"{RLM_WORKDIR}/m2m2_visual_repair/__init__.py": "",
        f"{RLM_WORKDIR}/m2m2_visual_repair/scoring.py": (PACKAGE_ROOT / "scoring.py").read_text(encoding="utf-8"),
    }
