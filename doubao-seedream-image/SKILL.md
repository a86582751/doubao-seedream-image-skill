---
name: doubao-seedream-image
description: Generate, edit, download, stream, and batch-create images with Volcano Ark Doubao Seedream 5.0 Lite / 4.5 / 4.0. Use when Codex needs character reference portraits, role sheets, storyboards, image-to-image edits, multi-reference fusion, storybook/comic panels, web-search-enhanced images, or Seedance video references for multi-character, story-driven, roleplay-adaptation, continuous-video, costume, prop, or worldbuilding workflows.
---

# Doubao Seedream Image

Use this skill for Doubao Seedream image generation through Volcano Ark. It is especially useful before Seedance video work: create character portraits, role sheets, outfit references, prop references, or storyboard panels, then pass accepted images into Seedance as reference images.

For long-video, multi-role, storyboard, or multi-reference workflows, avoid polluting the main thread with image base64. For each visual QA pass, use a fresh disposable subagent that inspects only the relevant image paths and returns a short text verdict.

## Tool

Run the bundled CLI:

```powershell
python doubao-seedream-image/scripts/seedream_image.py --help
```

## Configuration

The CLI reads process environment variables first, then falls back to `~/.codex/seedream.env` and `~/.codex/seedance.env`.

Supported variables, in priority order:

- `SEEDREAM_API_KEY`, `ARK_API_KEY`, `SEEDANCE_API_KEY`
- `SEEDREAM_BASE_URL`, `SEEDANCE_BASE_URL`, default `https://ark.cn-beijing.volces.com/api/v3`
- `SEEDREAM_MODEL`, default `doubao-seedream-5-0-260128`
- `SEEDREAM_IMAGE_PATH`, default `/images/generations`

Use a Volcano Ark API key for Seedream and Seedance:

```text
https://ark.volcengine.com/region:cn-beijing/apiKey?apikey=%7B%7D
```

Do not use the Volcano Speech/OpenSpeech key for Seedream. Seed Audio uses a separate Speech key.

Never print full API keys. Use `--dry-run --show-config` to inspect masked configuration.

## Common Commands

Text-to-image:

```powershell
python doubao-seedream-image/scripts/seedream_image.py generate --prompt "A cinematic character reference portrait, clean lighting, no text" --size 2K --ratio 3:4 --output-dir ./outputs
```

Create a character reference for Seedance:

```powershell
python doubao-seedream-image/scripts/seedream_image.py character --name "Lin Lan" --description "28-year-old spacecraft engineer, short black hair, silver uniform, calm expression" --ratio 3:4 --output-dir ./outputs
```

Image-to-image or multi-reference generation:

```powershell
python doubao-seedream-image/scripts/seedream_image.py generate --prompt "Keep image 1's face and pose; replace clothing with image 2's blue jacket" --image ./person.png --image ./clothes.png --size 2K
```

Generate a storyboard:

```powershell
python doubao-seedream-image/scripts/seedream_image.py storyboard --prefix "cinematic sci-fi realism, consistent character" --scene "Engineer repairs a spacecraft corridor" --scene "Emergency lights turn red" --max-images 2
```

Dry-run:

```powershell
python doubao-seedream-image/scripts/seedream_image.py generate --prompt "test" --dry-run --show-config
```

## Workflow

1. Use `character` when the downstream Seedance task has recurring characters.
2. Use `storyboard` when a long video needs shot planning or visual anchors.
3. Use image-to-image or multi-reference fusion when outfit, prop, or identity consistency matters.
4. Review generated references before sending them into Seedance.

## References

- Read `references/api-quickref.md` for payload fields, examples, response handling, and model capability notes.
