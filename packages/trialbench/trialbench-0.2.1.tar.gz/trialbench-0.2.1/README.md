
# TrialBench: Multi-modal AI-ready Clinical Trial Datasets

[![PyPI version](https://img.shields.io/pypi/v/trialbench.svg?color=brightgreen)](https://pypi.org/project/trialbench/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 1. Installation 

```bash
pip install trialbench
```

## 2. Tasks & Phases 

| Supported Tasks               | Task Name                 | Phase Name                                                                 | 
|-------------------------------|---------------------------|---------------------------------------------------------------------------|
| Mortality Prediction          | `mortality_rate`/`mortality_rate_yn` | 1-4                                                                      |
| Adverse Event Prediction      | `serious_adverse_rate`/`serious_adverse_rate_yn` | 1-4                                                                      |
| Patient Retention Prediction  | `patient_dropout_rate`/`patient_dropout_rate_yn` | 1-4                                                                      |
| Trial Duration Prediction     | `duration`               | 1-4                                                                      |
| Trial Outcome Prediction      | `outcome`                | 1-4                                                                      |
| Trial Failure Analysis        | `failure_reason`         | 1-4                                                                      |
| Dosage Prediction             | `dose`/`dose_cls`        | All                                                                      |

### Clinical Trial Phases
```
Phase 1: Safety Evaluation
Phase 2: Efficacy Assessment
Phase 3: Large-scale Testing
Phase 4: Post-marketing Surveillance
```

## 3. Quick Start 

```python
import trialbench

# Download all datasets at once (optional)
save_path = 'data/'
trialbench.function.download_all_data(save_path)

# Load dataset
task = 'dose'
phase = 'All'

# Load dataloader.Dataloader 
train_loader, valid_loader, test_loader, num_classes, tabular_input_dim = trialbench.function.load_data(task, phase, data_format='dl')
# or Load pd.Dataframe
train_df, valid_df, test_df, num_classes, tabular_input_dim = trialbench.function.load_data(task, phase, data_format='df')
```

## 4. Data Loading 

### `load_data` Parameters
| Parameter       | Type | Description                                      |
|----------------|------|--------------------------------------------------|
| `task`         | str  | Target prediction task (e.g., 'mortality_rate_yn') |
| `phase`        | int  | Clinical trial phase (1-4)                       |
| `data_format` | str  | Data format ('dl' for Dataloader, 'df' for pd.DataFrame) |


## 5. Citation 

If you use TrialBench in your research, please cite:

```bibtex
@article{chen2024trialbench,
  title={Trialbench: Multi-modal artificial intelligence-ready clinical trial datasets},
  author={Chen, Jintai and Hu, Yaojun and Wang, Yue and Lu, Yingzhou and Cao, Xu and Lin, Miao and Xu, Hongxia and Wu, Jian and Xiao, Cao and Sun, Jimeng and others},
  journal={arXiv preprint arXiv:2407.00631},
  year={2024}
}
```
