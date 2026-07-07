---
name: doubao-seedream-image
description: Generate, edit, download, stream, and batch-create images with Volcano Ark Doubao Seedream 5.0 Lite / 4.5 / 4.0. Use when Codex needs to call Seedream, create character reference portraits or face/role images for Seedance videos, generate text-to-image, image-to-image, multi-reference fusion, text/image-to-image sets, storyboards, storybook/comic panels, web-search-enhanced current images, b64/url images, no-watermark assets, or troubleshoot Seedream image generation API calls and official parameter limits. For long-video, multi-role, storyboard, or multi-reference workflows, isolate visual QA in fresh disposable subagents that inspect image files and return text-only conclusions; do not view high-resolution images in the main thread.
---

# Doubao Seedream Image

Use this skill for Doubao Seedream image generation through Volcano Ark. It is especially useful before Seedance video work: create character portraits or role sheets with Seedream first, then pass the saved image into the Seedance skill as a reference image.

For long-video, multi-role, storyboard, or multi-reference workflows, avoid polluting the main thread with image base64. Do not call image-viewing tools on high-resolution outputs in the main thread. For each visual QA pass, start a fresh disposable subagent, give it only the local image path(s), intended use, and a checklist, then accept only a short text verdict. Do not reuse that subagent for later checks.

## Tool

Run the bundled CLI:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py --help
```

The CLI reads the same Ark key fallback file used by Seedance: `C:\Users\isund\.codex\seedance.env`.

## Configuration

Supported variables, in priority order:

- `SEEDREAM_API_KEY`, `ARK_API_KEY`, `SEEDANCE_API_KEY`
- `SEEDREAM_BASE_URL`, `SEEDANCE_BASE_URL`, default `https://ark.cn-beijing.volces.com/api/v3`
- `SEEDREAM_MODEL`, default `doubao-seedream-5-0-260128`
- `SEEDREAM_IMAGE_PATH`, default `/images/generations`

Use a Volcano Ark API key for Seedream and Seedance. Ark key source:

```text
https://ark.volcengine.com/region:cn-beijing/apiKey?apikey=%7B%7D
```

Do not use the Volcano Speech/OpenSpeech key for Seedream. Seed Audio uses a separate Speech key from:

```text
https://console.volcengine.com/speech/new/setting/apikeys?projectName=default
```

Never print full API keys. Use `--dry-run --show-config` to inspect masked configuration.

## Common Commands

Text-to-image:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py generate --prompt "一位年轻女性科幻飞船工程师的角色设定照，正面半身，银灰色制服，清晰五官，电影质感" --size 2K --ratio 3:4 --output-dir C:\Users\isund\Documents\Codex\2026-07-05\ban\outputs
```

Create a character reference for Seedance:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py character --name "林岚" --description "28岁女性宇航员，短黑发，冷静坚定，银白色舱外服，东亚面孔" --ratio 3:4 --output-dir C:\Users\isund\Documents\Codex\2026-07-05\ban\outputs
```

Image-to-image or multi-reference generation:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py generate --prompt "保持图1的人物脸部和姿态，将服装替换为图2的蓝色外套" --image C:\path\person.png --image C:\path\clothes.png --size 2K
```

Generate an image set:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py set --prompt "参考图1，生成4张同一角色的表情设定图：平静、惊讶、微笑、警觉" --image C:\path\character.png --max-images 4
```

Generate a storyboard from scenes:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py storyboard --prefix "电影级科幻写实风，统一角色和冷色调光影" --scene "宇航员在空间站维修飞船" --scene "突然遇到陨石带袭击" --scene "宇航员紧急躲避" --scene "惊险逃回飞船" --max-images 4
```

Use web search for current facts:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py generate --prompt "制作一张上海未来5日天气预报图，现代扁平化插画风格" --size 2048x2048 --web-search
```

Use streaming output:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py set --prompt "参考图1，生成四张同一角色的动作设定图" --image C:\path\character.png --max-images 4 --stream
```

Use exact raw JSON payload:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py generate --payload-json C:\path\payload.json --output-dir C:\Users\isund\Documents\Codex\2026-07-05\ban\outputs
```

Dry-run without spending tokens:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py generate --prompt "测试" --dry-run --show-config
```

## Workflow

1. Use `character` when the output will be a reusable Seedance character reference. Prefer front-facing or three-quarter portraits, stable lighting, clear face, consistent outfit, and no text/watermark.
2. Use `generate` for text-to-image, single-image editing, multi-reference fusion, web search, raw payloads, or exact one-off calls.
3. Use `set` for official `sequential_image_generation=auto` image sets from text, one image, or multiple reference images.
4. Use `storyboard` for comics, storybooks, visual panels, or multi-scene film/story planning.
5. Save outputs immediately. Official docs say returned image URLs are retained for 24 hours.
6. For long-video, multi-role, storyboard, or multi-reference workflows, verify images through fresh disposable subagents:
   - Pass only image path(s), intended role/scene, and checklist.
   - Require text-only output: `可用/需重做`, matching details, defects, missing elements, and regeneration prompt advice.
   - Do not request images, screenshots, markdown image embeds, base64, or full transcripts from the subagent.
   - Use a new subagent for every QA pass; do not reuse visual-QA subagents.
7. For Seedance, pass the saved local image path into `doubao-seedance-video` as `--image <path> --image-role reference_image` or `first_frame`.
8. When exact API behavior or examples are needed, read `references/api-quickref.md`; read `references/official-seedream-4-5-doc.md` for the full official pasted document.

## Notes

- Seedream 5.0 Lite model IDs: `doubao-seedream-5-0-260128`; alias `doubao-seedream-5-0-lite-260128`.
- Seedream 4.5 model ID: `doubao-seedream-4-5-251128`.
- Seedream 4.0 model ID: `doubao-seedream-4-0-250828`.
- Supported input image formats include jpeg, png, webp, bmp, tiff, gif, heic, and heif.
- Maximum reference images: 14. Reference images plus generated images must be no more than 15 for group generation.
- Supported response formats: `url`, `b64_json`.
- Seedream 5.0 Lite output formats: `png`, `jpeg`; 4.5/4.0 default to `jpeg`.
- Seedream 5.0 Lite supports `2K`, `3K`, `4K`; 4.5 supports `2K`, `4K`; 4.0 supports `1K`, `2K`, `4K`.
- Use `--web-search` only with Seedream 5.0 Lite and only for prompts that need current factual visual content such as weather or recent products.
- Prompt advice from official docs: keep prompts concise and coherent, usually within about 300 Chinese characters or 600 English words; state subject, action, environment, then style/color/light/composition.
