#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ENV_FILES = [
    Path.home() / ".codex" / "seedream.env",
    Path.home() / ".codex" / "seedance.env",
]
DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DEFAULT_MODEL = "doubao-seedream-5-0-260128"
DEFAULT_IMAGE_PATH = "/images/generations"
MODEL_ALIASES = {
    "5": "doubao-seedream-5-0-260128",
    "5.0": "doubao-seedream-5-0-260128",
    "5-lite": "doubao-seedream-5-0-lite-260128",
    "5.0-lite": "doubao-seedream-5-0-lite-260128",
    "lite": "doubao-seedream-5-0-lite-260128",
    "4.5": "doubao-seedream-4-5-251128",
    "4": "doubao-seedream-4-0-250828",
    "4.0": "doubao-seedream-4-0-250828",
}
MODEL_PROFILES = {
    "doubao-seedream-5-0-260128": {
        "family": "5.0-lite",
        "label": "Doubao Seedream 5.0 Lite",
        "sizes": ["2K", "3K", "4K"],
        "formats": ["png", "jpeg"],
        "optimize_modes": ["standard"],
        "web_search": True,
    },
    "doubao-seedream-5-0-lite-260128": {
        "family": "5.0-lite",
        "label": "Doubao Seedream 5.0 Lite",
        "sizes": ["2K", "3K", "4K"],
        "formats": ["png", "jpeg"],
        "optimize_modes": ["standard"],
        "web_search": True,
    },
    "doubao-seedream-4-5-251128": {
        "family": "4.5",
        "label": "Doubao Seedream 4.5",
        "sizes": ["2K", "4K"],
        "formats": ["jpeg"],
        "optimize_modes": ["standard"],
        "web_search": False,
    },
    "doubao-seedream-4-0-250828": {
        "family": "4.0",
        "label": "Doubao Seedream 4.0",
        "sizes": ["1K", "2K", "4K"],
        "formats": ["jpeg"],
        "optimize_modes": ["standard", "fast"],
        "web_search": False,
    },
}
SIZE_PRESETS = {
    ("1K", "1:1"): "1024x1024",
    ("1K", "3:4"): "864x1152",
    ("1K", "4:3"): "1152x864",
    ("1K", "16:9"): "1312x736",
    ("1K", "9:16"): "736x1312",
    ("1K", "3:2"): "1248x832",
    ("1K", "2:3"): "832x1248",
    ("1K", "21:9"): "1568x672",
    ("2K", "1:1"): "2048x2048",
    ("2K", "3:4"): "1728x2304",
    ("2K", "4:3"): "2304x1728",
    ("2K", "16:9"): "2848x1600",
    ("2K", "9:16"): "1600x2848",
    ("2K", "3:2"): "2496x1664",
    ("2K", "2:3"): "1664x2496",
    ("2K", "21:9"): "3136x1344",
    ("3K", "1:1"): "3072x3072",
    ("3K", "3:4"): "2592x3456",
    ("3K", "4:3"): "3456x2592",
    ("3K", "16:9"): "4096x2304",
    ("3K", "9:16"): "2304x4096",
    ("3K", "3:2"): "3744x2496",
    ("3K", "2:3"): "2496x3744",
    ("3K", "21:9"): "4704x2016",
    ("4K", "1:1"): "4096x4096",
    ("4K", "3:4"): "3520x4704",
    ("4K", "4:3"): "4704x3520",
    ("4K", "16:9"): "5504x3040",
    ("4K", "9:16"): "3040x5504",
    ("4K", "3:2"): "4992x3328",
    ("4K", "2:3"): "3328x4992",
    ("4K", "21:9"): "6240x2656",
}


def load_env_files(paths: list[Path] = ENV_FILES) -> dict[str, str]:
    values: dict[str, str] = {}
    for path in paths:
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in values:
                values[key] = value
    return values


ENV_FALLBACK = load_env_files()


def env(name: str, default: str = "", *fallbacks: str) -> str:
    for key in (name, *fallbacks):
        value = os.environ.get(key)
        if value:
            return value
    for key in (name, *fallbacks):
        value = ENV_FALLBACK.get(key)
        if value:
            return value
    return default


def env_bool(name: str, default: bool, *fallbacks: str) -> bool:
    value = env(name, str(default).lower(), *fallbacks).strip().lower()
    return value in {"1", "true", "yes", "y", "on"}


def mask_secret(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "*" * len(value)
    return value[:4] + "*" * max(4, len(value) - 8) + value[-4:]


def endpoint(base_url: str, path: str) -> str:
    return urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def http_json(method: str, url: str, api_key: str, payload: Any | None = None, timeout: int = 240) -> Any:
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Authorization": f"Bearer {api_key}"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    request = Request(url, data=body, headers=headers, method=method)
    try:
        with urlopen(request, timeout=timeout) as response:
            data = response.read()
            if not data:
                return {}
            return json.loads(data.decode("utf-8"))
    except HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} {exc.reason}: {body_text}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error calling {url}: {exc.reason}") from exc


def http_stream(method: str, url: str, api_key: str, payload: Any, timeout: int = 300) -> list[Any]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(url, data=body, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, method=method)
    events: list[Any] = []
    try:
        with urlopen(request, timeout=timeout) as response:
            buffer: list[str] = []
            for raw_line in response:
                line = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")
                if not line:
                    if buffer:
                        events.append(parse_sse_event(buffer))
                        buffer = []
                    continue
                buffer.append(line)
            if buffer:
                events.append(parse_sse_event(buffer))
    except HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} {exc.reason}: {body_text}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error calling {url}: {exc.reason}") from exc
    return [event for event in events if event is not None]


def parse_sse_event(lines: list[str]) -> Any | None:
    data_lines: list[str] = []
    event_type = ""
    for line in lines:
        if line.startswith("event:"):
            event_type = line.split(":", 1)[1].strip()
        elif line.startswith("data:"):
            data_lines.append(line.split(":", 1)[1].strip())
    if not data_lines:
        return {"type": event_type} if event_type else None
    data_text = "\n".join(data_lines)
    if data_text == "[DONE]":
        return {"type": "done"}
    try:
        data = json.loads(data_text)
    except json.JSONDecodeError:
        data = {"data": data_text}
    if event_type and isinstance(data, dict) and "type" not in data:
        data["type"] = event_type
    return data


def image_to_data_uri(path_text: str) -> str:
    if re.match(r"^(https?://|data:)", path_text, flags=re.I):
        return path_text
    path = Path(path_text)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {path}")
    mime_type = mimetypes.guess_type(path.name)[0] or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def normalize_model(value: str) -> str:
    key = (value or "").strip()
    if not key:
        return ""
    return MODEL_ALIASES.get(key.lower(), key)


def model_profile(model: str) -> dict[str, Any]:
    return MODEL_PROFILES.get(model, MODEL_PROFILES[DEFAULT_MODEL])


def read_text_or_literal(value: str) -> str:
    try:
        path = Path(value)
        if path.exists():
            return path.read_text(encoding="utf-8-sig")
    except (OSError, ValueError):
        pass
    return value


def safe_name(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text)[:80] or "seedream"


def first_string(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, list):
        for item in value:
            found = first_string(item)
            if found:
                return found
    if isinstance(value, dict):
        for key in ("url", "b64_json", "image_url", "data", "output", "outputs"):
            found = first_string(value.get(key))
            if found:
                return found
    return None


def extract_images(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict) and data.get("type") in {"image_generation.partial_succeeded", "image_generation.partial_image"}:
        url = first_string(data.get("url") or data.get("image_url"))
        b64 = first_string(data.get("b64_json"))
        if url or b64:
            return [{"url": url, "b64_json": b64, "size": data.get("size"), "raw": data}]
    candidates = []
    if isinstance(data, dict):
        for value in (data.get("data"), data.get("images"), data.get("output"), data.get("outputs")):
            if isinstance(value, list):
                candidates = value
                break
        if not candidates and isinstance(data.get("data"), dict):
            inner = data["data"]
            for value in (inner.get("data"), inner.get("images"), inner.get("output"), inner.get("outputs")):
                if isinstance(value, list):
                    candidates = value
                    break
    result: list[dict[str, Any]] = []
    for item in candidates:
        if isinstance(item, dict):
            url = first_string(item.get("url") or item.get("image_url"))
            b64 = first_string(item.get("b64_json"))
            result.append({"url": url, "b64_json": b64, "size": item.get("size"), "raw": item})
        elif isinstance(item, str):
            result.append({"url": item, "b64_json": None, "size": None, "raw": item})
    if not result:
        found = first_string(data)
        if found:
            if found.startswith("data:") or len(found) > 2000:
                result.append({"url": None, "b64_json": found, "size": None, "raw": data})
            else:
                result.append({"url": found, "b64_json": None, "size": None, "raw": data})
    return result


def download_url(url: str, output_dir: Path, label: str, index: int, output_format: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "." + output_format.lower().lstrip(".")
    url_suffix = Path(url.split("?", 1)[0]).suffix
    if url_suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        suffix = url_suffix
    path = output_dir / f"{timestamp}_{safe_name(label)}_{index:02d}{suffix}"
    request = Request(url, headers={"User-Agent": "Codex Seedream CLI"})
    with urlopen(request, timeout=240) as response, path.open("wb") as file:
        shutil.copyfileobj(response, file)
    return path


def save_b64_image(b64_text: str, output_dir: Path, label: str, index: int, output_format: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "." + output_format.lower().lstrip(".")
    data = b64_text
    if "," in data and data.lower().startswith("data:"):
        header, data = data.split(",", 1)
        match = re.search(r"data:image/([^;]+)", header, flags=re.I)
        if match:
            suffix = "." + ("jpg" if match.group(1).lower() == "jpeg" else match.group(1).lower())
    path = output_dir / f"{timestamp}_{safe_name(label)}_{index:02d}{suffix}"
    path.write_bytes(base64.b64decode(data))
    return path


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


@dataclass
class Config:
    api_key: str
    base_url: str
    model: str
    image_path: str

    @classmethod
    def from_env(cls) -> "Config":
        api_key = env("SEEDREAM_API_KEY", "", "ARK_API_KEY", "SEEDANCE_API_KEY").strip()
        if not api_key:
            raise RuntimeError("Missing API key. Set SEEDREAM_API_KEY, ARK_API_KEY, or SEEDANCE_API_KEY, or add it to ~/.codex/seedream.env or ~/.codex/seedance.env.")
        return cls(
            api_key=api_key,
            base_url=env("SEEDREAM_BASE_URL", DEFAULT_BASE_URL, "SEEDANCE_BASE_URL").strip(),
            model=env("SEEDREAM_MODEL", DEFAULT_MODEL).strip(),
            image_path=env("SEEDREAM_IMAGE_PATH", DEFAULT_IMAGE_PATH).strip(),
        )

    def masked(self) -> dict[str, Any]:
        return {
            "api_key": mask_secret(self.api_key),
            "base_url": self.base_url,
            "model": self.model,
            "image_path": self.image_path,
            "env_files": [str(path) for path in ENV_FILES if path.exists()],
        }


def resolve_size(size: str, ratio: str) -> str:
    raw = size.strip()
    if re.match(r"^\d+x\d+$", raw, flags=re.I):
        return raw.lower()
    normalized = raw.upper()
    return SIZE_PRESETS.get((normalized, ratio), normalized)


def validate_payload(payload: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    model = normalize_model(str(payload.get("model") or DEFAULT_MODEL)) or DEFAULT_MODEL
    payload["model"] = model
    profile = model_profile(model)
    size = str(payload.get("size") or "")
    if size.upper() in {"1K", "2K", "3K", "4K"} and size.upper() not in profile["sizes"]:
        warnings.append(f"{profile['label']} is not documented for size {size}. Supported presets: {', '.join(profile['sizes'])}.")
    fmt = str(payload.get("output_format") or "").lower()
    if fmt and fmt not in profile["formats"]:
        warnings.append(f"{profile['label']} is documented for output format(s): {', '.join(profile['formats'])}.")
    if payload.get("tools") and not profile.get("web_search"):
        warnings.append(f"{profile['label']} is not documented with web_search support.")
    mode = ((payload.get("optimize_prompt_options") or {}) if isinstance(payload.get("optimize_prompt_options"), dict) else {}).get("mode")
    if mode and mode not in profile["optimize_modes"]:
        warnings.append(f"{profile['label']} supports optimize prompt mode(s): {', '.join(profile['optimize_modes'])}.")
    images = payload.get("image")
    image_count = len(images) if isinstance(images, list) else (1 if images else 0)
    max_images = ((payload.get("sequential_image_generation_options") or {}) if isinstance(payload.get("sequential_image_generation_options"), dict) else {}).get("max_images") or 1
    if image_count > 14:
        warnings.append("Official docs allow at most 14 reference images.")
    if payload.get("sequential_image_generation") == "auto" and image_count + int(max_images) > 15:
        warnings.append("For group generation, reference images plus generated images must be no more than 15.")
    prompt = str(payload.get("prompt") or "")
    if len(prompt) > 300:
        warnings.append("Official prompt advice recommends keeping Chinese prompts within about 300 characters when possible.")
    return warnings


def make_payload(args: argparse.Namespace, config: Config, prompt: str) -> dict[str, Any]:
    if args.payload_json:
        payload = json.loads(read_text_or_literal(args.payload_json))
        if not isinstance(payload, dict):
            raise ValueError("--payload-json must be a JSON object.")
        payload.setdefault("model", args.model or config.model)
        return payload
    model = normalize_model(args.model) or config.model
    output_format = args.output_format
    profile = model_profile(model)
    if not getattr(args, "output_format_explicit", False) and output_format not in profile["formats"]:
        output_format = profile["formats"][0]
    payload: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "size": resolve_size(args.size, args.ratio),
        "output_format": output_format,
        "response_format": args.response_format,
        "watermark": bool(args.watermark),
        "stream": bool(args.stream),
    }
    images = [image_to_data_uri(value) for value in (args.image or [])]
    if len(images) == 1:
        payload["image"] = images[0]
    elif images:
        payload["image"] = images
    if args.sequential:
        payload["sequential_image_generation"] = args.sequential
    if args.max_images:
        payload["sequential_image_generation_options"] = {"max_images": args.max_images}
    if args.optimize_prompt_mode:
        payload["optimize_prompt_options"] = {"mode": args.optimize_prompt_mode}
    if args.web_search:
        payload["tools"] = [{"type": "web_search"}]
    if args.extra_json:
        extra = json.loads(args.extra_json)
        if not isinstance(extra, dict):
            raise ValueError("--extra-json must be a JSON object.")
        payload.update(extra)
    return payload


def run_generation(args: argparse.Namespace, prompt: str) -> int:
    config = Config.from_env()
    payload = make_payload(args, config, prompt)
    warnings = validate_payload(payload)
    if args.show_config:
        print(json.dumps(config.masked(), ensure_ascii=False, indent=2))
    if args.dry_run:
        safe_payload = json.loads(json.dumps(payload, ensure_ascii=False))
        image_value = safe_payload.get("image")
        if isinstance(image_value, str) and image_value.startswith("data:"):
            safe_payload["image"] = image_value[:44] + "...<base64 omitted>"
        elif isinstance(image_value, list):
            safe_payload["image"] = [value[:44] + "...<base64 omitted>" if isinstance(value, str) and value.startswith("data:") else value for value in image_value]
        print(json.dumps({"dry_run": True, "warnings": warnings, "payload": safe_payload}, ensure_ascii=False, indent=2))
        return 0
    if payload.get("stream"):
        events = http_stream("POST", endpoint(config.base_url, config.image_path), config.api_key, payload)
        images: list[dict[str, Any]] = []
        for event in events:
            images.extend(extract_images(event))
        data: Any = {"events": events}
    else:
        data = http_json("POST", endpoint(config.base_url, config.image_path), config.api_key, payload)
        images = extract_images(data)
    output_dir = args.output_dir
    local_paths: list[str] = []
    if not args.no_download:
        for index, image in enumerate(images, 1):
            if image.get("url"):
                local_paths.append(str(download_url(image["url"], output_dir, args.label or "seedream", index, args.output_format)))
            elif image.get("b64_json"):
                local_paths.append(str(save_b64_image(image["b64_json"], output_dir, args.label or "seedream", index, args.output_format)))
    output_dir.mkdir(parents=True, exist_ok=True)
    result = {"warnings": warnings, "images": images, "local_paths": local_paths, "response": data}
    result_path = output_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_name(args.label or 'seedream')}.json"
    write_json(result_path, result)
    result["result_json"] = str(result_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def command_generate(args: argparse.Namespace) -> int:
    if args.prompt_file:
        args.prompt = Path(args.prompt_file).read_text(encoding="utf-8-sig")
    if not args.prompt.strip():
        if not args.payload_json:
            raise ValueError("--prompt is required.")
    return run_generation(args, args.prompt)


def command_character(args: argparse.Namespace) -> int:
    details = args.description.strip()
    if not details:
        raise ValueError("--description is required.")
    name = args.name.strip() or "角色"
    style = args.style.strip()
    prompt = (
        f"为影视视频生成角色形象参考图。角色名：{name}。"
        f"角色描述：{details}。"
        "输出清晰可复用的人物设定照，面部特征稳定，五官清楚，眼神自然，正面或三分之二半身构图，"
        "服装和发型细节明确，背景简洁干净，柔和电影布光，真实摄影质感，无遮挡，"
        "不要文字，不要水印，不要Logo，不要多人。"
    )
    if style:
        prompt += f" 风格要求：{style}。"
    args.label = args.label or safe_name(name)
    return run_generation(args, prompt)


def command_set(args: argparse.Namespace) -> int:
    if args.prompt_file:
        args.prompt = Path(args.prompt_file).read_text(encoding="utf-8-sig")
    if not args.prompt.strip():
        raise ValueError("--prompt is required.")
    if not args.sequential:
        args.sequential = "auto"
    if not args.max_images:
        args.max_images = 4
    return run_generation(args, args.prompt)


def command_storyboard(args: argparse.Namespace) -> int:
    scenes: list[str]
    if args.scenes_json:
        data = json.loads(Path(args.scenes_json).read_text(encoding="utf-8-sig"))
        if isinstance(data, dict):
            value = data.get("scenes_detail") or data.get("scenes") or data.get("prompts")
        else:
            value = data
        if not isinstance(value, list):
            raise ValueError("--scenes-json must be a list or an object containing scenes_detail/scenes/prompts.")
        scenes = [str(item) for item in value]
    else:
        scenes = [item for item in (args.scene or []) if item.strip()]
    if not scenes:
        raise ValueError("Provide --scene one or more times, or --scenes-json.")
    max_images = args.max_images or len(scenes)
    prompt = f"生成一组共{max_images}张连贯图片，保持统一风格、角色一致、色彩和镜头语言连贯。"
    if args.prefix:
        prompt += args.prefix.strip() + "。"
    prompt += " ".join(f"场景{index}：{scene}" for index, scene in enumerate(scenes[:max_images], 1))
    if args.cover:
        prompt += " 最后，为这组图片创作一个封面。再检查所有图片，去除图片中的文字。"
    args.sequential = "auto"
    args.max_images = max_images
    args.label = args.label or "seedream_storyboard"
    return run_generation(args, prompt)


def add_generation_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--model", default="")
    parser.add_argument("--size", default="2K", help="2K, 3K, 4K, or WIDTHxHEIGHT.")
    parser.add_argument("--ratio", default="3:4", help="Used only when --size is 2K/3K/4K.")
    parser.add_argument("--output-format", default="png", choices=["png", "jpeg"])
    parser.add_argument("--response-format", default="url", choices=["url", "b64_json"])
    parser.add_argument("--watermark", action=argparse.BooleanOptionalAction, default=env_bool("SEEDREAM_WATERMARK", False))
    parser.add_argument("--stream", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--image", action="append", help="Reference image URL or local path. Repeatable.")
    parser.add_argument("--sequential", default="", choices=["", "disabled", "auto"], help="Use auto for image set generation.")
    parser.add_argument("--max-images", type=int, default=0)
    parser.add_argument("--optimize-prompt-mode", default="", choices=["", "standard", "fast"])
    parser.add_argument("--web-search", action="store_true")
    parser.add_argument("--payload-json", default="", help="Raw full payload JSON or path. Missing model defaults to configured model.")
    parser.add_argument("--prompt-file", default="", help="Read prompt text from a UTF-8 file.")
    parser.add_argument("--extra-json", default="")
    parser.add_argument("--label", default="")
    parser.add_argument("--output-dir", type=Path, default=Path.cwd() / "outputs")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--show-config", action="store_true")
    parser.add_argument("--no-download", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate images with Doubao Seedream 5.0 Lite on Volcano Ark.")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Generate or edit images.")
    gen.add_argument("--prompt", default="")
    add_generation_args(gen)
    gen.set_defaults(func=command_generate)

    image_set = sub.add_parser("set", help="Generate a related image set with sequential_image_generation=auto.")
    image_set.add_argument("--prompt", default="")
    add_generation_args(image_set)
    image_set.set_defaults(func=command_set)

    storyboard = sub.add_parser("storyboard", help="Generate storyboard/storybook-style image sets from scenes.")
    storyboard.add_argument("--scene", action="append", default=[], help="Scene visual prompt. Repeatable.")
    storyboard.add_argument("--scenes-json", default="", help="JSON list, or object with scenes_detail/scenes/prompts.")
    storyboard.add_argument("--prefix", default="", help="Global style/character/story prefix.")
    storyboard.add_argument("--cover", action=argparse.BooleanOptionalAction, default=False)
    add_generation_args(storyboard)
    storyboard.set_defaults(func=command_storyboard)

    character = sub.add_parser("character", help="Create a reusable character reference image for Seedance.")
    character.add_argument("--name", default="")
    character.add_argument("--description", default="")
    character.add_argument("--style", default="")
    add_generation_args(character)
    character.set_defaults(func=command_character)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.output_format_explicit = any(part == "--output-format" or part.startswith("--output-format=") for part in sys.argv[1:])
    try:
        return int(args.func(args))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
