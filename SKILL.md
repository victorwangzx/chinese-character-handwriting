---
name: chinese-character-handwriting
description: Create stroke-by-stroke Chinese character handwriting diagrams in regular script (kaishu), with cumulative strokes, red start dots and direction arrows on tian zi ge grids. Use for parents, teachers, and learners requesting Chinese stroke order, handwriting worksheets, high-resolution images, or optional printable A4 PDFs. Ask about printing when unspecified. Not for cursive calligraphy.
license: See LICENSE and THIRD_PARTY_NOTICES.md
metadata:
  version: "3.0.1"
  author: "Victor使用Codex制作"
---

# Chinese Character Handwriting

楷书田字格逐笔教学

运行环境：Python 3.9+；可选Node.js 22+/sharp用于PNG，ReportLab和合法中文TTF用于A4 PDF。无需API密钥。

## 确认用途

用户提供单字后，若尚未说明打印需求，先问：“是否需要可打印的 A4 PDF？可以选择仅查看教学图，或同时提供打印版。”这条规则适用于所有汉字。可以同时核验笔顺，不擅自替用户选择。用户已明确要求打印或已明确不要打印时遵从选择，不重复询问。

## 固定教学规则

N 笔生成恰好 N 张累积图：第 k 张保留前 k 笔，未来笔画不出现。不把空白格、完整范字或总览计入 N。当前新增笔画叠加红色实心起笔点、沿笔势的红线和末端箭头；其他已写笔画不带标记。折钩沿转折走向，不能用起终点直线代替。

字形采用不透明 50% 黑 #808080；红色 #d92f2f；浅绿田字格 #a6ceb0，内线 #c1dfc6。所有步骤固定视口、尺度与位置，不逐笔居中。除用户要求外不更改这些已确定的教学样式。

## 核验再制作

默认大陆简体规范；繁体或地区要求依用户指定。先查教育部门规范或可靠字典，记录字形、笔画数、次序和折钩名称及来源。对照内置路径和 medians 的方向，特别检查折、钩和交叉处。来源冲突须解决，不能猜补。

内置9574条 Make Me a Hanzi 数据来自 Arphic 楷书衍生字形，未逐字人工审定，不能直接称为专业硬笔书法范字；无核验的硬笔范字时称“楷书笔顺演示”。缺字或无有效方向数据时说明不支持，不用生成式图片或整字字体切割补造。

## 执行

首次运行必须阅读 [README.md](README.md) 的安装、命令、依赖、打印字体和许可说明。以 Skill 实际位置为根目录，所有输出写到用户任务目录，不写入 Skill。执行前取得环境要求的安装许可；脚本不联网、不自动安装包。不要依赖作者机器路径或某个应用的专有运行时。

1. `python3 scripts/render.py 财 --out /task/svg` 生成 N 张SVG、总览、许可和manifest。
2. 需要图片时：`node scripts/export_png.mjs --input /task/svg --out /task/png`，从矢量生成4096×4096独立PNG、6000像素宽总览，300DPI。
3. 用户选择打印时，在高清PNG基础上运行 `scripts/print_a4.py`（完整命令见README），生成A4 PDF，每格50mm，每页最多8步，多页编号连续。长字自动分页，仍是N张独立步骤图。中文字体用用户环境中实际可用且可合法嵌入的TTF；不默认下载或重新分发字体。

## 验收和边界

SVG核心无外部依赖；PNG和PDF依赖独立列明。部分机器不具备可选依赖时，解释需要安装的内容并按用户选择处理，不把SVG改后缀冒充PNG/PDF。无可用中文字体时保留PDF待完成，不偷偷更换成缺字字体。

运行 `python3 scripts/check_release.py` 检查数据与发布结构；运行 `python3 -m unittest discover -s tests` 检查核心行为。任务中另检查N张、编号、前k笔路径、方向标记、未来笔画为零和固定布局。打印版核验实际PNG像素、PDF A4尺寸、页数与中文字体嵌入。必须渲染查看全部步骤、总览和全部PDF页，检查方向、裁切、重叠、行首标点和可读性。自动生成成功不等于教学内容已审定。

过程笔记记录用户是否打印、规范核验、版本和QA；不要混入家长打开的图片目录。对外分发图形须保留随附许可；manifest保留在过程或源目录。完整数据未经修改，转换后的图形按Arphic条件提供，并保留转换日期说明。原创代码/文字MIT，不把第三方数据改为MIT。
