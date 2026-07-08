---
name: doubao-seedream-image
description: Generate, edit, download, stream, and batch-create images with Volcano Ark Doubao Seedream 5.0 Pro / 5.0 Lite / 4.5 / 4.0. Use when Codex needs to call Seedream, create character reference portraits or face/role images for Seedance videos, generate text-to-image, image-to-image, multi-reference fusion, text/image-to-image sets, storyboards, storybook/comic panels, web-search-enhanced current images, b64/url images, no-watermark assets, optimize prompts from rough visual requirements, or troubleshoot Seedream image generation API calls and official parameter limits. For long-video, multi-role, storyboard, or multi-reference workflows, isolate visual QA in fresh disposable subagents that inspect image files and return text-only conclusions; do not view high-resolution images in the main thread.
---

# Doubao Seedream Image

Use this skill for Doubao Seedream image generation through Volcano Ark. It supports Seedream 5.0 Pro, 5.0 Lite, 4.5, and 4.0. It is especially useful before Seedance video work: create character portraits or role sheets with Seedream first, then pass the saved image into the Seedance skill as a reference image.

For long-video, multi-role, storyboard, or multi-reference workflows, avoid polluting the main thread with image base64. Do not call image-viewing tools on high-resolution outputs in the main thread. For each visual QA pass, start a fresh disposable subagent, give it only the local image path(s), intended use, and a checklist, then accept only a short text verdict. Do not reuse that subagent for later checks.

## Tool

Run the bundled CLI:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py --help
```

The CLI reads the same Ark key fallback file used by Seedance: `C:\Users\isund\.codex\seedance.env`.

## Model Choice

- Use Seedream 5.0 Pro (`doubao-seedream-5-0-pro-260628`, CLI alias `pro`) for the highest-quality single-image generation or editing. It supports text-to-image, single-image-to-image, and multi-reference single-image generation with 1-10 reference images. It does not support image sets, `sequential_image_generation`, web search, or streaming.
- Use Seedream 5.0 Lite (`doubao-seedream-5-0-260128` or `doubao-seedream-5-0-lite-260128`, CLI alias `lite`) for image sets, storyboards, web-search-enhanced current visuals, streaming, 2K/3K/4K output, and png/jpeg.
- Use Seedream 4.5 (`doubao-seedream-4-5-251128`) when 2K/4K image sets or editing are needed and jpeg output is acceptable. Do not pass `output_format`, web search, or `fast` prompt optimization.
- Use Seedream 4.0 (`doubao-seedream-4-0-250828`) when 1K output or `fast` prompt optimization is needed. It supports image sets and streaming but not web search or custom output format.

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
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py generate --prompt "一位科幻飞船工程师的角色设定照，正面半身，银灰色制服，清晰五官，电影质感" --size 2K --ratio 3:4 --output-dir C:\Users\isund\Documents\Codex\2026-07-05\ban\outputs
```

Seedream 5.0 Pro single image:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py generate --model pro --prompt "一张高端腕表产品海报，黑色陶瓷表壳，微距摄影，深色背景，侧逆光，画面干净" --size 2K --ratio 1:1 --output-format png
```

Create a character reference for Seedance:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py character --name "林岚" --description "女性宇航员，短黑发，冷静坚定，银白色舱外服，东亚面孔" --ratio 3:4 --output-dir C:\Users\isund\Documents\Codex\2026-07-05\ban\outputs
```

Image-to-image or multi-reference generation:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py generate --prompt "保持图1的人物脸部和姿态，将服装替换为图2的蓝色外套" --image C:\path\person.png --image C:\path\clothes.png --size 2K
```

Generate an image set:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py set --prompt "参考图1，生成4张同一角色的表情设定图：平静、惊讶、微笑、警觉" --image C:\path\character.png --max-images 4
```

Optimize a rough prompt locally before generation:

```powershell
python C:\Users\isund\.codex\skills\doubao-seedream-image\scripts\seedream_image.py optimize-prompt --task reference --prompt "做一张手办照片" --reference "参考图中的人物形象、服装和发型" --environment "室内桌面，后方有生日礼物包装盒" --style "真实摄影感" --composition "手办在画面左侧，圆形透明塑料底座"
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

1. **Respect creative freedom.** Preserve the user's creative intent, subject wording, style, aesthetics, and ambiguity unless the user asks for changes, the request violates applicable policy, or the API returns a rejection that requires a minimal retry adjustment. Do not add unsolicited restrictions such as age, "adult", realism, modesty, identity, safety disclaimers, or moralizing qualifiers just because the prompt is broad.
2. **Reference the prompt guide.** Before paid generation, read or apply `references/prompt-guide.md` and optimize only the expression: make the prompt clearer, more coherent, and better structured while preserving the user's creative direction.
3. If the user's request is rough, compose a Seedream-ready prompt with the Prompt Optimization Rules below or the `optimize-prompt` subcommand. Do this before calling paid generation, but keep additions minimal and intent-preserving.
4. Use `character` when the output will be a reusable Seedance character reference. Prefer front-facing or three-quarter portraits, stable lighting, clear face, consistent outfit, and no text/watermark when those qualities serve the user's goal.
5. Use `generate --model pro` for high-quality single-image text-to-image, single-image editing, or 2-10 reference-image fusion. Do not use Pro for group images, streaming, or web search.
6. Use `generate` for text-to-image, single-image editing, multi-reference fusion, web search, raw payloads, or exact one-off calls.
7. Use `set` for official `sequential_image_generation=auto` image sets from text, one image, or multiple reference images. This is only for Lite/4.5/4.0.
8. Use `storyboard` for comics, storybooks, visual panels, or multi-scene film/story planning. This is only for Lite/4.5/4.0.
9. Save outputs immediately. Official docs say returned image URLs are retained for 24 hours.
10. For long-video, multi-role, storyboard, or multi-reference workflows, verify images through fresh disposable subagents:
   - Pass only image path(s), intended role/scene, and checklist.
   - Require text-only output: `可用/需重做`, matching details, defects, missing elements, and regeneration prompt advice.
   - Do not request images, screenshots, markdown image embeds, base64, or full transcripts from the subagent.
   - Use a new subagent for every QA pass; do not reuse visual-QA subagents.
11. For Seedance, pass the saved local image path into `doubao-seedance-video` as `--image <path> --image-role reference_image` or `first_frame`.
12. When exact API behavior or examples are needed, read `references/api-quickref.md`; read `references/prompt-guide.md` for prompt tactics; read `references/official-seedream-4-5-doc.md` only when the older full pasted document is needed.

## Prompt Optimization Rules

Before generation, rewrite loose visual requests into concise natural language. Prefer a single coherent paragraph over keyword piles. The target shape is:

```text
主体 + 行为/变化 + 环境 + 用途/类型 + 风格 + 色彩 + 光影 + 构图 + 需要准确渲染的文字 + 保持不变/避免项
```

Rules from the official prompt guide:

- Preserve creative freedom: do not narrow the user's subject, age, genre, tone, pose, outfit, or style unless the user requested it or the API rejects and a minimal retry change is necessary.
- Keep prompts concise and coherent, usually within about 300 Chinese characters or 600 English words. Long prompts can dilute attention.
- For text-to-image, clearly state subject, action, environment, then add style, color, lighting, and composition only when useful.
- For logos, posters, UI, infographics, teaching diagrams, product images, wallpapers, and storyboards, explicitly state the image type and use case.
- Put exact visible text in double quotation marks, for example `标题为“Seedream 5.0”`.
- For editing, name the exact object or region and the operation: add, delete, replace, modify. State what must remain unchanged.
- For complex edits, tell the user/agent to use arrows, boxes, scribbles, or marked reference images when text alone is ambiguous.
- For reference images, explicitly say what to extract and preserve, such as `参考图中的人物形象`, `参考图二的风格`, or `衣服款式与图中一致`, then describe the new scene.
- For multi-image input, refer to images by ordinal: `图一的人物`, `图二的服装`, `图三的线性简约风格`.
- For image sets, use words like `一组`, `一套`, `系列`, or a concrete count; request consistency of character, style, color, and camera language.
- Avoid vague pronouns like `它` when several objects are present.

## Notes

- Seedream 5.0 Pro model ID: `doubao-seedream-5-0-pro-260628`; CLI aliases include `pro`, `5-pro`, `5.0-pro`.
- Seedream 5.0 Lite model IDs: `doubao-seedream-5-0-260128`; alias `doubao-seedream-5-0-lite-260128`.
- Seedream 4.5 model ID: `doubao-seedream-4-5-251128`.
- Seedream 4.0 model ID: `doubao-seedream-4-0-250828`.
- Supported input image formats include jpeg, png, webp, bmp, tiff, gif, heic, and heif.
- Maximum reference images: Pro supports 10; Lite/4.5/4.0 support 14. Reference images plus generated images must be no more than 15 for group generation.
- Supported response formats: `url`, `b64_json`.
- Seedream 5.0 Pro and Lite output formats: `png`, `jpeg`; 4.5/4.0 default to `jpeg` and do not support custom `output_format`.
- Size presets: Pro supports `1K`, `2K`; Lite supports `2K`, `3K`, `4K`; 4.5 supports `2K`, `4K`; 4.0 supports `1K`, `2K`, `4K`.
- Explicit size constraints: Pro requires total pixels between `1280x720` and `2048x2048`, aspect ratio [1/16, 16], and width/height multiples of 16. Lite/4.5 require total pixels between `2560x1440` and `4096x4096`. 4.0 requires total pixels between `1280x720` and `4096x4096`.
- Use `--web-search` only with Seedream 5.0 Lite and only for prompts that need current factual visual content such as weather or recent products.
- Use `--optimize-prompt-mode standard` for Pro/Lite/4.5. Only 4.0 supports `fast`.
- Use `--payload-json` when reproducing exact official API examples; the CLI will warn about capability mismatches but does not rewrite raw JSON.
