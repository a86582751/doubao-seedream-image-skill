# Seedream 5.0 Lite API Quick Reference

## Endpoint

- `POST https://ark.cn-beijing.volces.com/api/v3/images/generations`
- Authorization: `Bearer <ARK API key>`

## Model

- Primary: `doubao-seedream-5-0-260128`
- Alias: `doubao-seedream-5-0-lite-260128`
- Seedream 4.5: `doubao-seedream-4-5-251128`
- Seedream 4.0: `doubao-seedream-4-0-250828`

## Capability Matrix

All three documented models support text-to-image, text-to-image sets, single/multi-image reference generation, single/multi-image-to-image sets, and streaming output.

- Seedream 5.0 Lite: supports web search, 2K/3K/4K, png/jpeg output, standard prompt optimization.
- Seedream 4.5: no web search in the official matrix, 2K/4K, jpeg output, standard prompt optimization.
- Seedream 4.0: no web search in the official matrix, 1K/2K/4K, jpeg output, standard or fast prompt optimization.

## Basic Payload

```json
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "image prompt",
  "size": "2K",
  "output_format": "png",
  "response_format": "url",
  "watermark": false
}
```

## Image Reference Payload

`image` may be one URL/string or an array of URLs/strings.

```json
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "保持图1人物脸部特征，替换为图2服装",
  "image": ["https://...", "data:image/png;base64,..."],
  "size": "2K",
  "output_format": "png",
  "response_format": "url",
  "watermark": false
}
```

For multi-reference fusion, set `sequential_image_generation` to `disabled` when one final image is expected.

```json
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "将图1的服装换为图2的服装",
  "image": ["https://...", "https://..."],
  "sequential_image_generation": "disabled",
  "size": "2K",
  "output_format": "png",
  "response_format": "url",
  "watermark": false
}
```

## Image Set Generation

```json
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "参考图1，生成4张同一角色的表情设定图",
  "image": "https://...",
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
- Single-image-to-set: prompt says "参考图1..." and `image` is one URL/data URI.
- Multi-reference-to-set: `image` is an array and `max_images` controls output count.

## Useful Parameters

- `prompt`: required text instruction.
- `image`: optional reference image URL, Base64 data URI, or array of those.
- `size`: `2K`, `3K`, `4K`, or explicit `WIDTHxHEIGHT`.
- `response_format`: `url` or `b64_json`.
- `output_format`: `png` or `jpeg`.
- `watermark`: `false` for clean production/reference assets.
- `stream`: boolean. The local CLI uses non-streaming by default.
- `sequential_image_generation`: `disabled` or `auto`.
- `sequential_image_generation_options.max_images`: number of generated images for image sets.
- `optimize_prompt_options.mode`: optional, e.g. `standard` or `fast` where supported.
- `tools`: `[{"type": "web_search"}]` for Seedream 5.0 Lite current-information image generation.

## Web Search

Seedream 5.0 Lite can call web search with:

```json
{
  "tools": [{"type": "web_search"}]
}
```

The model decides whether to actually search. Check `usage.tool_usage.web_search`; `0` means no search was used.

## Streaming

Set `stream` to `true` for streaming image generation. Events include:

- `image_generation.partial_succeeded`: one finished image with URL.
- `image_generation.partial_image`: one partial image with `b64_json`.
- `image_generation.partial_failed`: partial failure with error.
- `image_generation.completed`: final completion and usage.

The local CLI can parse stream events and save returned URL or Base64 images.

## Prompt Advice

- Use concise coherent natural language.
- Include subject, action, environment.
- Add style, color, lighting, composition only when needed.
- Official docs recommend prompts stay within about 300 Chinese characters or 600 English words; long prompts may dilute attention.

## Recommended Seedream 5.0 Lite Sizes

- 2K: `1:1` 2048x2048, `3:4` 1728x2304, `4:3` 2304x1728, `16:9` 2848x1600, `9:16` 1600x2848, `3:2` 2496x1664, `2:3` 1664x2496, `21:9` 3136x1344.
- 3K: `1:1` 3072x3072, `3:4` 2592x3456, `4:3` 3456x2592, `16:9` 4096x2304, `9:16` 2304x4096, `3:2` 3744x2496, `2:3` 2496x3744, `21:9` 4704x2016.
- 4K: `1:1` 4096x4096, `3:4` 3520x4704, `4:3` 4704x3520, `16:9` 5504x3040, `9:16` 3040x5504, `3:2` 4992x3328, `2:3` 3328x4992, `21:9` 6240x2656.

Seedream 4.5 supports 2K and 4K from the same size table. Seedream 4.0 supports 1K, 2K, and 4K.

Two sizing modes are supported and should not be mixed:

- Preset mode: `size` is `1K`, `2K`, `3K`, or `4K`, with aspect ratio described in the prompt or selected by CLI `--ratio`.
- Explicit mode: `size` is `WIDTHxHEIGHT`.

## Limits

- Input image formats: jpeg, png, webp, bmp, tiff, gif, heic, heif.
- Image input size: under 30 MB each.
- Maximum reference images: 14.
- Reference images plus generated images: no more than 15 for group generation.
- Single image pixel product: no more than `6000x6000=36000000`.
- Returned image URLs are retained for 24 hours. Download immediately.

## Storybook / Comic Workflow

Official storybook guidance can be adapted locally:

1. Use a planning model to produce JSON with `title`, `summary`, `scenes`, and `scenes_detail`.
2. Use `scenes_detail` as image prompts.
3. Convert the scene array into one long prompt.
4. Append a cover request and instruction to remove image text when needed.
5. Generate a set of related images with `sequential_image_generation=auto`.

The local `storyboard` command implements the image-generation part of this flow.
