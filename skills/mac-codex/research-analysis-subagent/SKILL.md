---
name: research-analysis-subagent
description: Use when processing one paper or official technical-release directory for research-workflow and writing Analysis_Detail.md from source text and original figures.
---

# Research Analysis Subagent

每次只处理一个论文或官方技术发布目录，使用单篇独立的子代理上下文；不同条目可由协调者并行分配。

## 读取依据

1. 每次精读先读取可访问的既有 `assets/analysis_prompt.md`：Windows 路径为 `G:\Wyatt\HK_intership\.agent\skills\research-analysis-subagent\assets\analysis_prompt.md`，Mac 路径为 `/Volumes/T7/Wyatt/HK_intership/.agent/skills/research-analysis-subagent/assets/analysis_prompt.md`。若均不可访问，使用下述自包含要求。沿用旧模板的学术正文与原图／公式约定；评价采用有依据的文字，验排由代理承担。
2. 阅读 `${paper_dir}/paper.md`、版本与来源元数据，以及相关 PDF／官方全文。若抽取文本不完整，回到原文核对，不仅依赖摘要。
3. 逐一查看 `${paper_dir}/paper_artifacts` 中的原图，并结合图注、正文解释与公式理解；忽略 `._*` 等文件系统元数据。核对不清楚的图表时检查原始页面。

## 单篇精读输出

写入 `${paper_dir}/Analysis_Detail.md`，保持既有合并流程需要的**无 Markdown 标题的中文正文**，以自然段、列表和公式衔接。保留原始 LaTeX 公式并解释符号；插入相关原图时使用有效绝对路径和非空 alt 文本，使 Word 能生成图注。篇幅服务于论文内容，至少交代：

- 论文／官方资料的身份、首次发布日期、所读版本与链接；推荐分类及理由。
- 任务、输入输出、核心贡献和机制；训练与推理分别使用什么信息、哪些部分冻结／更新、哪些计算可离线复用。
- 关键公式／算法和符号含义、关键实验结论及比较条件、限制与未公开内容。
- 相关原图的图号、页码、用途与来源；保留真实图，不以自绘解释图替代。
- 适合报告的重点概要，以及明确标为建议或推断的项目迁移启示。作者报告、本地验证和未执行实验分开表述。

## 为报告配图交接证据

如果报告要求概念图或两种绘图 skill，先读 [论文配图与案例说明](../research-workflow/references/paper-visuals.md)。在已有配图元数据或独立 `${paper_dir}/Visual_Brief.md` 中提供可直接用于绘图的简短说明：核心机制、可见主体与候选差异、原图／公式定位、可用 prompt 或输入输出例子及其来源、计算图所需符号与维度。图解交接说明不混入供合并使用的无标题正文。

原文例子与自拟教学例子明确分开。原文没有给出的数值、参数或结构写为未知；不能为了画图补造。水墨画应通过具体对象和案例帮助理解，交接内容不应只有“输入—模型—输出”节点清单。

完成后自行核对本篇引用、图号、案例属性与计算关系，把仍不确定的内容告知协调者。最终 DOCX 的渲染和逐页目视检查由报告协调者完成，不将这项工作转交给用户。
