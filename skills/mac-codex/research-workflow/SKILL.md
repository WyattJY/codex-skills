---
name: research-workflow
description: Use when the user asks for a literature survey, a categorized model or paper research report, batch paper downloads, PDF-to-Markdown extraction, or a figure-rich Word research report.
---

# Research Workflow

将一手文献整理成有分类、有依据、可读且可继续编辑的中文调研报告。用户已有报告、参考图或修订意见时，先读取这些材料，沿用已明确的范围与视觉方向。

## 调研范围与分类

- 明确主题、时间区间、检索截止日期和用途。对“今年到现在”按执行时日期检索；分别记录首次发布日与本次阅读版本，不把旧论文的更新日期当作今年首发。
- 按论文解决的问题、机制或训练／推理特点分类，并解释分类依据。同一模型系列的不同版本说明关系；论文、官方技术发布、预览 API 和补充案例分别标识。
- 优先使用论文全文、作者仓库、官方模型卡和官方发布。搜索摘要用于发现候选，不能代替全文精读。说明检索覆盖范围，不以固定篇数或某次报告目录限制后续调研。

## 原文、精读与合并

1. 为每个条目保留原始 PDF／官方网页材料、提取文本、原图及来源信息。记录标题、版本、日期、URL、图号／页码／章节；提取失败时保留真实状态。
2. 使用 `research-analysis-subagent`，为每篇分配独立子代理上下文进行精读。可将独立论文并行分配，但每次精读只处理一个目录；合并者负责术语、分类和跨篇比较的一致性。
3. 单篇概要解释：解决什么问题、核心改动、训练与部署分别做什么、关键结果及比较条件、适用范围和局限。只写有依据的参数、数据与结构；官方未公开的内部实现不补造。
4. 区分作者报告结果、本次实际复现和面向用户项目的迁移建议。跨论文表格保留数据集、指标、候选池、模型规模与版本等影响比较的条件；条件不同时，不拼成统一名次。
5. 合并为“范围与结论—分类导读—逐篇概要—横向比较—应用建议—参考来源”。篇幅由内容决定，不强行每篇固定两页。

## 图文调研报告

制作包含概念解释或双绘图 skill 的报告时，**先读 [论文配图与案例说明](references/paper-visuals.md)**，再设计和批量绘制。

- 保留相关原论文图，标明真实出处；自绘图用于帮助解释，不能替代原文证据。
- 按用户要求逐篇配套 `paint-with-code` 场景概念图与 wdkns 的 `tensor-formula-viz` 计算图。两图分别解释“具体例子为什么这样变化”和“机制如何计算”；不要重复同一张流程图。
- 水墨概念图以可辨认对象、案例、候选差异或证据对照为主体。参考原论文结构是为了准确表达机制，不是把所有论文套成方框箭头模板。
- 用户已给出认可的参考图时，实际查看图像；可取得原绘图源时先检查并复用适用部分。原文案例、意译、节选和自拟示意须明确区分。

## Word 交付

使用 `jiangyu-word-report-style` 作为必要样式层，并结合可用的 `documents:documents` 渲染与验排能力。Pandoc可作转换工具，不能仅依赖其默认Word样式。

- 在用户项目目录保存 `.docx`、可用时的 PDF 预览、参考材料及可编辑绘图源。图注包含来源和解释性质，正文说明图要读什么。
- 先检查独立图像，再渲染最终 DOCX，逐页查看最新结果中的中文、图表、图注和分页。若图片文字过小，调整版面或拆页，避免为固定页数缩小整张图。
- 由代理完成可执行的验排，不把“请用户检查公式和图片”当作交付步骤。渲染不可用时说明实际限制，不声称已目视检查。
- 交付当前版本的明确链接并保留用户需要的旧版；未经请求不发布到外部服务。

## 运行环境与既有脚本

先识别实际操作系统和可用运行时，不把 Windows 盘符当作所有机器的前提。

**Windows：**既有脚本与资产的源目录为 `G:\Wyatt\HK_intership\.agent\skills\research-workflow`。存在时保留原流程：

1. `powershell -ExecutionPolicy Bypass -File "G:\Wyatt\HK_intership\.agent\tools\verify-research-runtime.ps1"`
2. 下载：`scripts\run.py`；PDF 转换：`scripts\pdf_to_markdown.py`。
3. 单篇精读后合并：`scripts\merge_moe_report.py`。

脚本相对路径均基于上述 Windows 源目录；运行前读取实际参数，不猜测命令接口。旧 `merge_moe_report.py` 默认只合并第二章，依赖章节标题与论文条目列表；先确认大纲适配，按需使用 `--all-chapters`。通用分类报告也可采用本机合并方式，核对实际纳入的条目，避免遗漏章节。

**macOS：**现有完整脚本可在 `/Volumes/T7/Wyatt/HK_intership/.agent/skills/research-workflow` 查找；存在时先读该目录说明与实际参数。T7 上有源文件不代表其 Windows venv、盘符或 PowerShell 运行时可在 Mac 使用。

**跨平台执行：**使用当前可访问的来源与转换工具；桌面文档任务先用 `load_workspace_dependencies` 获取可用运行时。既有运行时不可用时，可从 PDF／HTML 提取文本并保留原图、页码与来源，使用本机工具合并和导出。明确记录实际使用的转换方式；未运行 Docling、Windows 脚本或实验时，不声称它们已成功执行。
