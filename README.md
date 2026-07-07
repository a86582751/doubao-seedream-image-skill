# Doubao Seedream Image Skill for Codex

A Codex skill for generating, editing, batching, and downloading images with Volcano Ark Doubao Seedream image models, including Doubao Seedream 5.0 Lite.

It is especially useful as a companion to long-form AI video workflows: for multi-character stories, roleplay adaptations, worldbuilding documents, recurring outfits, or important props, Codex can first create stable character/reference images with Seedream and then pass them to Seedance video generation.

Keywords: Codex skill, Doubao Seedream 5.0 Lite, Volcano Ark, AI image generation, character reference, role sheet, image-to-image, storyboard, story-to-video, Seedance companion.

## What It Does

- Generate text-to-image outputs with Seedream.
- Create character reference portraits and role sheets for Seedance videos.
- Generate storyboard panels or image sets from multiple scene descriptions.
- Use one or more reference images for image-to-image and multi-reference fusion.
- Support web-search-enhanced image generation when the selected model supports it.
- Run dry-run configuration checks with masked API keys.

## Repository Layout

```text
doubao-seedream-image/
  SKILL.md
  agents/openai.yaml
  references/api-quickref.md
  scripts/seedream_image.py
```

## Install In Codex

```bash
mkdir -p ~/.codex/skills
cp -R doubao-seedream-image ~/.codex/skills/
```

Restart Codex after installing a new skill.

## Configuration

The CLI reads process environment variables first, then falls back to:

```text
~/.codex/seedream.env
~/.codex/seedance.env
```

Use a Volcano Ark API key:

```text
https://ark.volcengine.com/region:cn-beijing/apiKey?apikey=%7B%7D
```

Supported variables:

```text
SEEDREAM_API_KEY=your_volcano_ark_api_key
ARK_API_KEY=your_volcano_ark_api_key
SEEDANCE_API_KEY=your_volcano_ark_api_key
SEEDREAM_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
SEEDREAM_MODEL=doubao-seedream-5-0-260128
```

Do not use the Volcano Speech/OpenSpeech key here. Speech keys are for Seed Audio only.

## Quick Start

Generate a character reference:

```bash
python doubao-seedream-image/scripts/seedream_image.py character \
  --name "Lin Lan" \
  --description "28-year-old spacecraft engineer, short black hair, silver uniform, calm expression" \
  --ratio 3:4 \
  --output-dir outputs
```

Generate a storyboard:

```bash
python doubao-seedream-image/scripts/seedream_image.py storyboard \
  --prefix "cinematic sci-fi realism, consistent character, cool lighting" \
  --scene "Engineer repairing a spacecraft corridor" \
  --scene "Emergency lights turn red" \
  --scene "Engineer runs toward the airlock" \
  --max-images 3 \
  --output-dir outputs
```

Dry-run configuration:

```bash
python doubao-seedream-image/scripts/seedream_image.py generate \
  --prompt "test" --dry-run --show-config
```

## Companion Workflow

Use this with the Seedance video skill when character or prop continuity matters:

1. Generate Seedream character/reference images.
2. Review the images for identity, outfit, props, and style.
3. Pass accepted references to Seedance as `reference_image` inputs.

## Privacy And Safety

This public package does not include API keys, private env files, generated images, local output folders, or machine-specific configuration.

## License

MIT. See [LICENSE](LICENSE).
