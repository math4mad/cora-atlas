# arXiv 首发操作单 — unified-agents (v2.1-arxiv)

**账号状态**: 注册讫 (主人 09-22 报)。首射关卡 = **endorsement**（cs.AI/cs.CL 新账号需担保或走自动核验）。

## 包内容
- `main.tex` — draft-v2 英文净化版（ctex 与中文摘要块已剥, 直引改英译, 修 `\n` 幽灵控制符）
- `fig1-three-panels.png` — 三屏图
- 本机 tectonic 编译验讫 ✅ (arXiv 端用 pdflatex 亦应通过: 仅标准宏包)
- 新增 P-B1 status 段: **exp18 融合首证 (26/40 离弦鼓包 + 子代 NLL 优于双亲)** —— v2 纸面唯一后补, 与 LEDGER C39 同账

## 提交步骤 (主人操作, 5 分钟)
1. https://arxiv.org/submit → **Subject class**: cs.AI (primary), cross-list cs.CL, cs.SY
2. **Authors**: ⚠️ arXiv 政策作者须为自然人 —— 填 `Yiwei [姓氏]` 一人;
   Lola/Qwen 入 Acknowledgments: "Prose and probes developed with an LLM conversational
   partner (Qwen2.5 + an agent harness); all errors are the human author's."
   （2026 年 arXiv 要求 AI 辅助披露, 此句即合规; 勿把模型列 author）
3. **Abstract**: 粘 main.tex 摘要 (去 \emph 等记号即可, 无生僻宏)
4. **Upload**: 拖 `unified-agents-arxiv.tar.gz` (本目录打包: main.tex + fig1)
5. 若弹 endorsement 请求 → 填机构邮箱走自动核验, 或指定一位 cs.AI 挂名研究员发信担保
6. 许可: 建议 **CC BY 4.0** (园子对外姿态) 或 arXiv 非独占默认

## 双轨待命
- 博客英文版 `medium-en.md` / 知乎版 `social-zhihu.md` 在册 —— arXiv 编号一出即可发 (09-20 评审钦定双轨)
- Zenodo DOI 包在 `zenodo/` (无需推荐人, 可先射, 两轨不互斥)

## 未了
- exp18 J3 第二族: Kaggle 对 Llama/Gemma 类需**网页端点一次协议** (挂载探针核 `mount-probe-second-family` 在验哪些真落了盘)。主人若愿在 Kaggle 网页接受 Llama 3.2 社区许可, J3 即可全数开火。
