# EVIL: EValuation using ILlicit instructions

This repository contains the evaluation scripts for **EVIL**, the benchmark introduced in our paper:

> **[Large Language Models' Complicit Responses to Illicit Instructions across Socio-Legal Contexts](https://arxiv.org/abs/2511.20736)**
>
> Xing Wang\*, Huiyuan Xie\*, Yiyan Wang, Chaojun Xiao, Huimin Chen†, Holli Sargeant, Felix Steffek, Jie Shao, Zhiyuan Liu, and Maosong Sun.
>
> \* Equal contributions. † Corresponding author.
>
> arXiv:2511.20736, 2025.

EVIL evaluates **complicit facilitation**: whether large language models provide guidance or support that enables illicit user instructions. The benchmark is grounded in real-world court judgments and legal frameworks from China and the United States.

**[Paper](https://arxiv.org/abs/2511.20736)** | **[Dataset on Hugging Face](https://huggingface.co/datasets/TsinghuaNLP/EVIL)** | **[Evaluation guide](evaluation_script/README.md)** | **[License](LICENSE)**

## Dataset

The EVIL dataset is available on Hugging Face: [TsinghuaNLP/EVIL](https://huggingface.co/datasets/TsinghuaNLP/EVIL)

| Legal context | Language | Samples |
| --- | --- | ---: |
| China | Chinese (`zh`) | 2,842 |
| United States | English (`en`) | 2,905 |
| **Total** | | **5,747** |

Each dataset record includes `uniqid`, `instruction`, `region`, `language`, `legal_issues`, `intent`, `sub_vs_obj`, and `fac_vs_jus`. See the [dataset card](https://huggingface.co/datasets/TsinghuaNLP/EVIL/blob/main/README.md) for field descriptions.

## Evaluation Scripts

The scripts evaluate model responses along three dimensions:

- **Safety:** whether the response refuses to facilitate illicit activity.
- **Responsibility:** whether the response warns about consequences and offers lawful, constructive alternatives.
- **Credibility:** whether the response identifies a criminal charge consistent with the reference legal issues.

```text
evaluation_script/
├── README.md
├── .env.example
├── env.py
├── evaluate.py
├── openai_client.py
├── prompts.py
├── requirements.txt
├── prompts_cn/
│   ├── safety.txt
│   ├── responsibility.txt
│   └── credibility.txt
└── prompts_us/
    ├── safety.txt
    ├── responsibility.txt
    └── credibility.txt
```

### Quick Start

Use Python 3.11 or newer:

```bash
git clone https://github.com/thunlp/EVIL.git
cd EVIL
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r evaluation_script/requirements.txt
cp evaluation_script/.env.example evaluation_script/.env
```

Set `OPENAI_API_KEY` in `evaluation_script/.env`. If needed, set `OPENAI_API_BASE` to your compatible API endpoint; otherwise, leave it empty. Real evaluations send the instructions, model responses, and reference legal issues to the configured API and incur API usage costs.

To evaluate a model, generate its responses to the benchmark instructions, preserve the top-level `legal_issues` field, and save one JSON object per line in `evaluation_script/model_responses/my-model.jsonl`:

```json
{"uniqid":"<dataset record ID>","instruction":"<dataset instruction>","response":"<model response>","legal_issues":["<reference legal issue>"]}
```

Keep Chinese and US examples in separate input files or directories so that each run uses the matching regional prompts. Then run:

```bash
cd evaluation_script
python evaluate.py \
  --model_name my-model \
  --data_path ./model_responses \
  --save_path ./evaluation_results \
  --evaluator_model gpt-4o-2024-05-13 \
  --region prompts_cn
```

Use `--region prompts_us` for US legal scenarios. Results are saved to `evaluation_results/my-model_evaluation.json`, and aggregate scores are printed to the terminal.

Set `--evaluator_model` to choose the evaluator for all three dimensions. The default is `gpt-4o`; our experiments used `gpt-4o-2024-05-13`, as shown above. See the [evaluation guide](evaluation_script/README.md) for detailed usage and the model versions used in the paper.

## License and Acceptable Use

**Source code.** The EVIL evaluation code is licensed under **ResearchRAIL (RESEARCH-ONLY RAIL-S)** for academic and research use. See [LICENSE](LICENSE) for the complete terms from the [RAIL License Generator](https://www.licenses.ai/rail-license-generator), or download the [official generated copy](https://api.generator.licenses.ai/api/v1/license/ddd904d2-cc66-446c-8852-c956b1151a86/generate?media_type=text/plain&git_sha=e8502289197accc4ddd023f0fc234ca26062a9f1).

**Dataset.** The EVIL dataset is provided for AI safety research under the RAIL acceptable use policy described in its [dataset card](https://huggingface.co/datasets/TsinghuaNLP/EVIL/blob/main/README.md). By accessing or using the dataset, you agree to that policy and applicable laws.

- The dataset must not be used to train, fine-tune, or deploy models for malicious purposes, facilitate unlawful activities, or bypass safety safeguards.
- Redistribution and derivative use must preserve the dataset's license notice and comply with the same terms.
- The dataset is intended for research purposes only. Developing systems that provide actual legal advice requires proper oversight and safety measures.

## Citation

If you use EVIL or these evaluation scripts in your research, please cite:

```bibtex
@misc{wang2025complicitresponses,
  title = {Large Language Models' Complicit Responses to Illicit Instructions across Socio-Legal Contexts},
  author = {Xing Wang and Huiyuan Xie and Yiyan Wang and Chaojun Xiao and Huimin Chen and Holli Sargeant and Felix Steffek and Jie Shao and Zhiyuan Liu and Maosong Sun},
  year = {2025},
  eprint = {2511.20736},
  archivePrefix = {arXiv},
  primaryClass = {cs.CY},
  url = {https://arxiv.org/abs/2511.20736}
}
```
