

# Reproduction of Data Cleaning Systems

## Environment Activation
```bash
cd ~/MDCBaseline/baseline_env
source bin/activate
cd ..
./CleanerRunScript/run_horizon/run.sh
````

This repository contains the reproduction of several data cleaning systems proposed in academic papers. The goal is to replicate these systems and validate their effectiveness under controlled environments.

## Contents

1. [Horizon](#horizon)
2. [ActiveClean](#activeclean)
3. [Raha & Baran](#raha--baran)
4. [BoostClean](#boostclean)
5. [CPClean](#cpclean)
6. [Holistic](#holistic)
7. [BigDansing](#bigdansing)
8. [ScaRed](#scared)
9. [HoloClean](#holoclean)

## Reproduction Status and Details

### Horizon

* **Paper**: [Horizon: Scalable Dependency-Driven Data Cleaning](https://www.vldb.org/pvldb/vol14/p25)
* **Presenter**: Zekai
* **Status**: Completed
* **Summary**: Implements a scalable dependency-driven cleaning strategy. Focused on reproducing the FD-based method and validating its effectiveness on benchmark datasets.
* **Error Handling Signals**: Optimal FD pattern selection
* **Error Types**: Dependency violations, distribution anomalies
* **Precondition**: FD rule set
* **Downstream Feedback**: Generic
* **Task Type**: General-purpose detection
* **Evaluation Metrics**: Precision, Recall

### ActiveClean

* **Paper**: [ActiveClean: An Interactive Data Cleaning Framework for Modern Machine Learning](https://arxiv.org/pdf/1601.03797.pdf)
* **Presenter**: Siying
* **Language**: Python
* **Status**: Completed
* **Summary**: Reproduction of the interactive feedback framework and its integration with machine learning workflows.
* **Error Handling Signals**: User interaction feedback
* **Error Types**: Noise, missing values
* **Precondition**: Feedback mechanism
* **Downstream Feedback**: Convex loss models
* **Task Type**: Detection and repair for ML
* **Evaluation Metrics**: Data accuracy, ML performance improvement

### Raha & Baran

* **Papers**:

  * *Raha*: A Configuration-Free Error Detection System
  * *Baran*: Effective Error Correction via a Unified Context Representation and Transfer Learning
* **Presenter**: Zekai
* **Status**: Completed
* **Summary**: Raha focuses on rule-free error detection; Baran extends with context-driven repair using transfer learning.
* **Error Handling Signals**: Rule-based detection, contextual representation
* **Error Types**: Data errors, inconsistencies
* **Precondition**: None (Raha); Contextual rule set (Baran)
* **Downstream Feedback**: None
* **Task Type**: Error detection and repair
* **Evaluation Metrics**: Detection rate, repair accuracy

### BoostClean

* **Paper**: Automated Error Detection and Repair for Machine Learning
* **Presenter**: Siying
* **Status**: Completed
* **Summary**: Evaluates BoostClean's automatic error handling capabilities in ML data pipelines.
* **Error Handling Signals**: Statistical analysis, ML models
* **Error Types**: Noise, outliers
* **Precondition**: Error pattern library
* **Downstream Feedback**: ML model
* **Task Type**: Detection and repair
* **Evaluation Metrics**: Post-repair model performance

### CPClean

* **Paper**: Nearest Neighbor Classifiers over Incomplete Information
* **Presenter**: Siying
* **Language**: Python
* **Status**: Completed
* **Summary**: Reproduces CPClean for handling incomplete data using nearest neighbor classifiers.
* **Error Handling Signals**: Nearest-neighbor classification
* **Error Types**: Missing or incomplete data
* **Precondition**: None
* **Downstream Feedback**: Prediction models
* **Task Type**: Detection and repair
* **Evaluation Metrics**: Accuracy, imputation correctness

### Holistic

* **Paper**: Holistic Data Cleaning: Putting Violations into Context
* **Presenters**: Zekai & Siying
* **Status**: Completed
* **Summary**: Assesses context-based violation handling methods.
* **Error Handling Signals**: Contextual analysis
* **Error Types**: Violations, contextual conflicts
* **Precondition**: Contextual rule sets
* **Downstream Feedback**: None
* **Task Type**: Error detection
* **Evaluation Metrics**: Precision, Recall

### BigDansing

* **Status**: Completed

### ScaRed

* **Paper**: Don’t Be Scared: Use Scalable Automatic Repairing with Maximal Likelihood and Bounded Changes
* **Presenter**: Siying
* **Status**: Completed
* **Summary**: Focuses on probabilistic repair under change constraints.
* **Error Handling Signals**: Maximum likelihood estimation
* **Error Types**: Noise, incorrect values
* **Precondition**: Error probability model
* **Downstream Feedback**: None
* **Task Type**: Error repair
* **Evaluation Metrics**: Repair precision, constrained change magnitude

### HoloClean

* **Paper**: Holistic Data Repairs with Probabilistic Inference
* **Presenter**: Zekai
* **Status**: Completed
* **Summary**: Implements probabilistic inference-based repair on noisy and inconsistent data.
* **Error Handling Signals**: Probabilistic inference
* **Error Types**: Data errors, inconsistencies
* **Precondition**: Prior probabilities, rule set
* **Downstream Feedback**: None
* **Task Type**: Error repair
* **Evaluation Metrics**: Repair accuracy, data consistency