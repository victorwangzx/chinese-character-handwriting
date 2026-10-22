# Chinese Character Handwriting · v3.0.0

A reusable Agent Skill for learning to write Chinese characters, one stroke at a time. Uses **regular script (kaishu)** and **tian zi ge** practice grids.

- Exactly one cumulative diagram per stroke: 3 strokes → 3 images; 12 strokes → 12 images.
- 50% gray character strokes, pale green grids, red start dots and direction arrows.
- Ask the parent or learner whether they need a printable version. When requested, provide high-resolution images and an A4 PDF.
- 4,096 × 4,096 PNG steps at 300 DPI; 6,000-pixel-wide overview; 50 mm grids in the A4 PDF.
- Offline SVG generation with Python 3.9+; optional Node.js 22+/sharp for PNG and ReportLab plus a licensed Chinese TTF font for PDF.
- Original code and documentation: MIT. Third-party glyph data and derived glyph graphics: Arphic Public License. See LICENSE and THIRD_PARTY_NOTICES.md.

**Skill identifier / suggested GitHub repository name:** `chinese-character-handwriting`.

Install the entire folder in your agent's supported skills directory. Do not copy only SKILL.md. Example request: “Use $chinese-character-handwriting to show me how to write 财.” The agent asks whether you need printing unless you already specified a choice. This is a stroke-order teaching aid, not a certified penmanship model.

### Quick start (English)

Run from the Skill folder. Output must go outside it. Install optional dependencies only if you need the corresponding exports and have approved installation in your environment.

```sh
# No external dependencies for SVG:
python3 scripts/render.py 财 --out ../lesson-output/svg
# Optional PNG dependency, installed separately:
npm install --omit=dev
node scripts/export_png.mjs --input ../lesson-output/svg --out ../lesson-output/png
# Optional PDF dependency, installed in a virtual environment:
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-print.txt
# Replace the font path with a Chinese TTF that you may legally embed:
.venv/bin/python scripts/print_a4.py 财 --images ../lesson-output/png --font /path/to/chinese-font.ttf --out ../lesson-output/character-A4.pdf
```

On Windows, use your Python command and `.venv\Scripts\python.exe`. Existing output directories must be empty; the PDF target must not exist. Print on A4 in color at 100% / actual size. Dependencies and fonts are not bundled; no API keys, telemetry, automatic downloads, or paid APIs are required. The data does not cover every character. Verify stroke order against a reliable regional reference and visually inspect every step before teaching.

Supported package format is not a claim of runtime testing in WorkBuddy or QwenWork. This full-data ZIP is about 12.4 MB and exceeds QwenWork's documented 10 MB organization-upload limit; import through that entry is not supported as packaged.

## 中文使用指南

输入一个汉字，得到一笔一张的田字格累积图。3笔就是3张，12笔就是12张。每张用红色圆点表示当前笔画起笔，沿红线书写，在箭头处收笔；字为50%灰，田字格浅绿。

**先询问家长是否需要打印。** 未说明时，代理应先确认；选择打印则同时制作高清图和A4 PDF，已明确选择的不用重复问。此规则适用于所有汉字。

本项目符合 [Agent Skills开放格式](https://agentskills.io/specification)，可作为独立Skill目录使用；未声称获得平台认证。格式兼容不保证每个宿主都能执行Python、Node或安装依赖。

## 安装Skill

解压后将整个 `chinese-character-handwriting` 目录复制到宿主支持的技能目录。不要只复制SKILL.md，数据和许可也需要保留。

- GitHub Copilot项目级：`.github/skills/chinese-character-handwriting/`（也支持`.agents/skills/`）；个人级可用`~/.agents/skills/`。以[GitHub当前文档](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)为准。
- Codex：放入当前环境已配置的技能目录，或通过该环境的Skill安装器导入；不同宿主版本的入口可能不同。
- 也可不使用代理，按下方命令直接生成。

调用例子：`使用 $chinese-character-handwriting 教孩子写“财”。` 代理会先确认是否需要A4打印版，然后核验并制作。

## 从零准备运行环境

SVG基础功能只需Python 3.9+标准库，内置数据无需再次下载，无API、账号、付费服务。运行时不联网；约9574条字形并不代表完整覆盖所有汉字。

可选高清PNG：Node.js 22+、npm及sharp 0.35.5。可选A4 PDF：Python、ReportLab 4.x、可合法嵌入的中文TrueType字体。可用你已安装的阿里巴巴普惠体或其他适合的中文TTF；字体未随包附送。路径必须替换为使用者自己机器上的真实路径，不要照抄作者个人目录。PDF不读取系统字体名称猜测替代。

以下安装操作由使用者手动执行或批准后执行，不是自动步骤。Python、Node、sharp、ReportLab均可免费获取；商业使用遵循各自开源许可。sharp及其预编译组件有独立第三方许可，发布打包了运行库的产品时须继续检查；字体商业使用及嵌入权限需由字体供应方确认。

在Skill目录执行：

```sh
# 仅SVG无需安装以下任何依赖。
# 如需要PNG，安装到本Skill目录：
npm install --omit=dev
# 如需要PDF，建议使用项目虚拟环境：
python3 -m venv .venv
# macOS / Linux
.venv/bin/python -m pip install -r requirements-print.txt
# Windows用 .venv\Scripts\python.exe 替代 .venv/bin/python
```

本发布包不附带node_modules、虚拟环境、字体或API密钥。安装需要网络；依赖准备好后生成可离线进行。若离线且没有可选依赖，仍可生成SVG，不声称PNG/PDF完成。

## 生成文件

下例从Skill目录运行，`../lesson-output/`是Skill目录外的示例输出位置。换成自己的任务目录即可；命令中的“财”可以换成任意已覆盖的单个汉字。Windows可把python3换为本机python命令。输出目录必须为空，PDF目标须不存在，避免覆盖既有作品。

```sh
# 1. SVG步骤图、总览、来源manifest及完整许可
python3 scripts/render.py 财 --out ../lesson-output/svg
# 2. 高清PNG：步骤4096×4096，300 DPI；总览宽6000
node scripts/export_png.mjs --input ../lesson-output/svg --out ../lesson-output/png
# 3. 仅在选择打印时生成A4 PDF
# 将 /path/to/chinese-font.ttf 替换为自己的中文TrueType字体路径
.venv/bin/python scripts/print_a4.py 财 --images ../lesson-output/png --font /path/to/chinese-font.ttf --out ../lesson-output/财-A4.pdf
```

PDF每格50毫米，每页最多8步，9笔以上自动续页。字体会嵌入PDF；清晰度来自原矢量重渲染，不是修改旧图的DPI标签。打印选择A4、彩色、实际大小100%，关闭照片软件的自动裁切。浅绿色格线在不同打印机和纸张上可能略有差异。

SVG/PNG目录含N张`step-*.svg/png`、1张`overview.svg/png`、`licenses/`和`manifest.json`。总览不计入N。交给家长的目录只保留所需图片、PDF与许可说明；manifest作为来源记录另存。图形派生作品仍需按Arphic条件保留许可。

## 自动与人工边界

自动：按内置顺序累积、绘制方向标记、固定几何与配色、检查输出计数、导出高清PNG、分页排版PDF。

人工/代理核验：确认简繁与地区规范；查验目标字笔顺及折钩；检查每笔箭头；确认字体授权；逐页视觉检查。数据及中线并非逐字审定，不能把生成成功当作教材级准确性保证。缺字不猜造，不把Arphic衍生楷书称为专业硬笔书法家范字。

## 验证与维护

```sh
python3 scripts/check_release.py
python3 -m unittest discover -s tests
```

以上核心检查不需pip依赖，包含数据SHA256、连续步骤、样式、无未来笔画、缺字及非空目录保护。PNG/PDF端到端另按上述命令运行并渲染查看；GitHub Actions配置提供三平台核心检查。CI尚未在GitHub实际运行时不能宣称已通过。

## 许可证与贡献

原创代码和说明：MIT，见[LICENSE](LICENSE)。第三方字形数据：Arphic Public License，见[第三方说明](THIRD_PARTY_NOTICES.md)；不是整包统一MIT。数据含原许可与固定提交哈希，随包分发。`dictionary.txt`未打包，不涉及其LGPL内容。

可反馈具体汉字、期望笔顺的权威链接、出现问题的步骤和运行环境；提交改动前运行核心检查。请勿提交孩子个人信息、node_modules、字体文件或本机绝对路径。无遥测、无上传、无自动下载。维护者：Victor使用Codex制作。

## 修订记录

- v3.0.0（2026-10-22）：公开名称改为Chinese Character Handwriting，技术标识改为`chinese-character-handwriting`，增加英文简介、安装速览与平台边界。技术调用名更改，采用主版本升级；教学图配色、笔顺与打印规则保持。

- v2.0.0（2026-10-22）：首次公开版；为保证许可完整，自定义--data暂仅接受内置数据路径（接口收紧，因此升级主版本）。公开发布结构、MIT及第三方许可分离、可移植PNG导出、输入保护、来源记录、核心测试及CI；将所有汉字的打印需求确认写入通用流程。
- v1.1.0：高清及A4打印能力。
- v1.0.1：字形改为50%灰。
- v1.0.0：逐笔累积、方向标记和浅绿田字格。

作者：Victor使用Codex制作。
