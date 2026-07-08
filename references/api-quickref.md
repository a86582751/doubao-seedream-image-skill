# Seedream Image API Quick Reference

## Endpoint

- `POST https://ark.cn-beijing.volces.com/api/v3/images/generations`
- Authorization: `Bearer <ARK API key>`

Returned image URLs are valid for 24 hours. Download immediately.

## Models

- Seedream 5.0 Pro: `doubao-seedream-5-0-pro-260628`
- Seedream 5.0 Lite: `doubao-seedream-5-0-260128`
- Seedream 5.0 Lite alias: `doubao-seedream-5-0-lite-260128`
- Seedream 4.5: `doubao-seedream-4-5-251128`
- Seedream 4.0: `doubao-seedream-4-0-250828`

## Capability Matrix

| Capability | 5.0 Pro | 5.0 Lite | 4.5 | 4.0 |
|---|---:|---:|---:|---:|
| Text-to-single-image | yes | yes | yes | yes |
| Single-image-to-single-image | yes | yes | yes | yes |
| Multi-reference-to-single-image | yes, 2-10 refs | yes, 2-14 refs | yes, 2-14 refs | yes, 2-14 refs |
| Text/image-to-image-set | no | yes | yes | yes |
| `sequential_image_generation` | no | yes | yes | yes |
| Streaming | no | yes | yes | yes |
| Web search tool | no | yes | no | no |
| `output_format` | png/jpeg | png/jpeg | no, jpeg default | no, jpeg default |
| Prompt optimization mode | standard | standard | standard | standard/fast |

Do not pass unsupported parameters. Seedream 5.0 Pro rejects `sequential_image_generation`, `sequential_image_generation_options`, `stream`, and `tools`.

## Basic Single-Image Payload

```json
{
  "model": "doubao-seedream-5-0-pro-260628",
  "prompt": "一张高端腕表产品海报，黑色陶瓷表壳，微距摄影，深色背景，侧逆光，画面干净",
  "size": "2K",
  "output_format": "png",
  "response_format": "url",
  "watermark": false
}
```

## Image Reference Payload

`image` may be one URL/data URI string or an array of URL/data URI strings.

```json
{
  "model": "doubao-seedream-5-0-pro-260628",
  "prompt": "保持图一人物的脸部特征和姿态，让图一人物穿上图二的蓝色外套，背景为简洁摄影棚。",
  "image": ["https://...", "data:image/png;base64,..."],
  "size": "2K",
  "output_format": "png",
  "response_format": "url",
  "watermark": false
}
```

Use Pro for one final image. Use Lite/4.5/4.0 when the final output should be a related set.

## Image Set Payload

Only Seedream 5.0 Lite, 4.5, and 4.0 support this.

```json
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "生成一组共4张同一角色表情设定图：平静、惊讶、微笑、警觉。保持角色脸部、服装和线性插画风格一致。",
  "size": "2K",
  "sequential_image_generation": "auto",
  "sequential_image_generation_options": {
    "max_images": 4
  },
  "output_format": "png",
  "response_format": "url",
  "watermark": false
}
```

Official set-generation patterns:

- Text-to-image set: prompt describes multiple scenes; `sequential_image_generation=auto`.
- Single-image-to-set: prompt says `参考图一...` and `image` is one URL/data URI.
- Multi-reference-to-set: `image` is an array and `max_images` controls output count.
- Reference image count plus generated image count must be no more than 15.

## Useful Parameters

- `model`: required model ID or endpoint ID.
- `prompt`: required text instruction. Official guidance recommends no more than about 300 Chinese characters or 600 English words.
- `image`: optional reference image URL, Base64 data URI, or array of those.
- `size`: preset (`1K`, `2K`, `3K`, `4K`) or explicit `WIDTHxHEIGHT`; do not mix both modes.
- `response_format`: `url` or `b64_json`.
- `output_format`: `png` or `jpeg`, only for 5.0 Pro/Lite.
- `watermark`: `false` for clean production/reference assets.
- `stream`: boolean, only for Lite/4.5/4.0.
- `sequential_image_generation`: `disabled` or `auto`, only for Lite/4.5/4.0.
- `sequential_image_generation_options.max_images`: 1-15, only when `sequential_image_generation=auto`.
- `optimize_prompt_options.mode`: `standard`; 4.0 also supports `fast`.
- `tools`: `[{"type": "web_search"}]`, only for Seedream 5.0 Lite.

## Size Rules

Preset mode:

- 5.0 Pro: `1K`, `2K`.
- 5.0 Lite: `2K`, `3K`, `4K`.
- 4.5: `2K`, `4K`.
- 4.0: `1K`, `2K`, `4K`.

Explicit mode:

- 5.0 Pro: pixel product between `1280x720` and `2048x2048`; aspect ratio [1/16, 16]; width and height must be multiples of 16.
- 5.0 Lite and 4.5: pixel product between `2560x1440` and `4096x4096`; aspect ratio [1/16, 16].
- 4.0: pixel product between `1280x720` and `4096x4096`; aspect ratio [1/16, 16].

Reference image input rules:

- Formats: jpeg, png, webp, bmp, tiff, gif, heic, heif.
- Each image must be under 30 MB.
- Aspect ratio must be [1/16, 16].
- Width and height must each be greater than 14 px.
- Pixel product must be no more than `6000x6000=36000000`.

## Web Search

Seedream 5.0 Lite can call web search with:

```json
{
  "tools": [{"type": "web_search"}]
}
```

The model decides whether to actually search. Check `usage.tool_usage.web_search`; `0` means no search was used.

## Streaming

Only Seedream 5.0 Lite, 4.5, and 4.0 support `stream: true`.

Stream events can include:

- `image_generation.partial_succeeded`: one finished image with URL.
- `image_generation.partial_image`: one partial image with `b64_json`.
- `image_generation.partial_failed`: partial failure with error.
- `image_generation.completed`: final completion and usage.

## Prompt Advice

Read `prompt-guide.md` before generation if the user's request is loose. Key rules:

- Use concise coherent natural language.
- State subject, action, environment, and use case.
- Add style, color, lighting, and composition only when they matter.
- Put exact visible text in double quotes.
- For editing, name the target object, the desired operation, and what must stay unchanged.
- For multiple input images, refer to `图一`, `图二`, `图三`, and assign each image a role.
- For image sets, request `一组`, `一套`, `系列`, or a concrete count and ask for consistent character/style/color/camera language.
