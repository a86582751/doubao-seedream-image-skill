# Seedream Prompt Guide

This guide condenses the official Seedream prompt guidance into agent-operational rules. Use it before paid generation when a user provides a visual idea. Treat creative freedom as mandatory: preserve the user's intent, wording, genre, aesthetic, and ambiguity unless the user asks for changes, the request violates applicable policy, or the API rejects and a minimal retry adjustment is necessary.

## Core Pattern

Write prompts as concise, coherent natural language:

```text
主体 + 行为/变化 + 环境 + 用途/类型 + 风格 + 色彩 + 光影 + 构图 + 准确文字 + 保持不变/避免项
```

Prefer one readable paragraph. Do not pile up unrelated style keywords. Keep Chinese prompts near 300 characters when possible, or English prompts near 600 words.

Do not add unsolicited constraints. In particular, do not add age qualifiers, "adult", realism, modesty, safety disclaimers, identity labels, or moralizing qualifiers unless the user requested them or the API rejection requires the smallest possible retry edit.

## Text-To-Image

Use when there are no reference images.

Template:

```text
生成[用途/类型]。[主体]正在/位于[行为和环境]。[关键细节]。[风格]，[色彩]，[光影]，[构图]。如有文字，写为“精确文字”。
```

For dense educational, chart, formula, UI, or infographic images, include precise domain terms and required layout.

## Image Editing

Use when modifying an input image.

Template:

```text
对参考图进行图像编辑。编辑对象：[明确对象/位置/标记颜色]。操作：[增加/删除/替换/修改]为[目标状态]。保持不变：[动作、表情、姿态、背景、布局、风格等]。
```

Avoid vague pronouns. If the target is ambiguous, use marked images with arrows, boxes, line frames, or colored scribbles and refer to them directly, such as `红色涂抹位置` or `红框内标题`.

## Reference Image Generation

Use when extracting identity, style, product shape, material, outfit, layout, or sketch structure from image inputs.

Template:

```text
参考图中的[需要保留的特征]，生成[新画面/用途]。[新场景细节]。保持[角色/风格/材质/布局/方向]一致。
```

For design sketches, floor plans, wireframes, and UI prototypes:

- Use a clear original image.
- Say whether to follow text labels in the image.
- State the target fidelity, such as high-fidelity UI or realistic interior rendering.
- State which layout, furniture positions, orientation, or structure must match.

## Multi-Image Input

Name images by ordinal and assign roles.

Examples:

- `将图一的人物替换为图二的主体。`
- `让图一人物穿上图二的服装，保持图一人物脸部和姿态。`
- `参考图二的风格，对图一进行风格转换。`
- `参考图三的线性简约风格，设计一套图标。`

## Multi-Image Output

Use with Seedream 5.0 Lite, 4.5, or 4.0 only. Do not use with Seedream 5.0 Pro.

Template:

```text
生成一组共[N]张内容关联的图片，保持角色、视觉风格、色彩和镜头语言统一。分别对应：1.[场景]；2.[场景]；...
```

Words like `一组`, `一套`, `系列`, or a concrete image count help trigger set generation. Use `sequential_image_generation=auto` and set `max_images` when using the API/CLI.

## Visible Text

Put exact rendered text in quotes:

```text
标题为“Seedream 5.0”，副标题为“Prompt Guide”。
```

If text is not needed, say `不要生成文字`.

## Common Task Prompts

Logo:

```text
设计一个[行业/品牌] logo，主体是[图形]，logo 上写有品牌名“[文字]”，[风格]，[配色]，适合[用途]。
```

Product:

```text
生成一张[产品]的[电商主图/海报/包装设计]，[产品特征]，[材质]，[环境]，[光影]，[构图]。
```

Character reference:

```text
生成清晰可复用的人物设定照。角色：[身份/类型]，[面部/发型/服装/气质]，正面或三分之二半身构图，背景简洁，柔和光线，不要文字，不要水印。
```

Storyboard:

```text
生成一组共[N]张影视分镜，统一角色、服装、场景风格和光影。场景1：[描述]。场景2：[描述]。场景3：[描述]。
```

UI from sketch:

```text
这是一个[平台/产品]的手绘原型图，请根据图中文字示意，将其渲染成高保真的 UI 界面，保持参考图布局一致，并补充合理示例内容。
```
