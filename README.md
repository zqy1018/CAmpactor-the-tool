# *CAmpactor*: A Novel and Effective Local Search Algorithm for Optimizing Pairwise Covering Arrays

*CAmpactor* is a novel and effective local search algorithm for compacting given PCAs into smaller-sized ones. This repository includes the implementation of *CAmpactor*, the testing instances adopted in the experiments and the experimental results. 

As is described in the paper, *CAmpactor* itself is a tool for optimizing a given pairwise covering array (PCA), but it can generate small PCAs efficiently when adopting *SamplingCA* as the initializing algorithm providing the input PCAs. Therefore, this repository contains a copy of *SamplingCA* (with tag `v1.0.0`), allowing users to run the initialization phase and the optimization phase together. 

**Note**: the *CAmpactor* in this repository is a more user-friendly version, compared with the original version (*i.e.,* the version at the time of paper submission) in [this repository](https://github.com/chuanluocs/CAmpactor). Remarkably, the core algorithmic implementation of *CAmpactor* in the `src/` directory ***is not modified***. The major differences between this version and the original version are listed as follows. 
- This repository contains a parser for the [CTWedge input language](https://github.com/fmselab/ctwedge/wiki/Grammar) and an accompanying Python3 script, allowing users to write human-readable input files for describing the system under test and to obtain human-readable CSV files for describing the PCA. See [this section](#a-more-user-friendly-approach) for more details. 
- This repository contains fewer redundant files that are not necessary for *CAmpactor* to reduce the repository size. In particular, many files related to only *SamplingCA* have been removed (*e.g.,* the testing instances and experimental results of *SamplingCA*). Users may refer to [the original repository of *SamplingCA*](https://github.com/chuanluocs/SamplingCA) for its complete version. 
- This repository contains additional instructions that may make the reproduction of experiments easier. See [experiment_reproduction.md](experiment_reproduction.md). 

## Instructions for Building *CAmpactor*

See [INSTALL.md](INSTALL.md). 

## Instructions for Running *CAmpactor*

After building *CAmpactor*, users may run it with the following command: 

```
./CAmpactor -i [INSTANCE_PATH] --init_PCA_path [INITIAL_PCA_PATH] -o [OUTPUT_PCA_PATH] <optional_parameters> <optional_flags>
```

For the required parameters, we list them as follows. Note that the optimized PCA is of the same form as the initial PCA constructed by *SamplingCA*. 

| Parameter | Type | Description | 
| - | - | - |
| `-i` | string | path of the input CNF instance |
| `--init_PCA_path` | string | path of the initial PCA generated by *SamplingCA* |
| `-o` | string | path to which the optimized PCA is saved |

For the optional parameters, we list them as follows. 

| Parameter | Type | Default Value | Description | 
| - | - | - | - |
| `--gamma` | integer | 10000 | used to control the termination criterion | 
| `--psi` | float number | 0.1 | used to control the forced patching technique | 
| `--delta` | integer | 10 | used to control the assignment-level forbidden mechanism | 
| `--seed` | integer | 1 | random seed |

Note that by setting `--delta` to -1, *CAmpactor* works without assignment-level forbidden mechanism; by setting `--psi` to 0.0, *CAmpactor* works without forced patching technique. 

For the optional flags, we list them as follows. 

| Flag | Description | 
| - | - |
| `--use_cell_tabu` | if set, the assignment-level forbidden mechanism will be replaced with cell-level tabu mechanism |
| `--nosimplcnf` | if set, the input will not be simplified with `bin/coprocessor` |

**Tip:** *CAmpactor* adopts *SamplingCA* as its initialization algorithm. As described in the repository of *SamplingCA*, *SamplingCA* employs a tool named *Coprocessor* to simplify input CNFs. Therefore, in order to conform to *SamplingCA*, by default *CAmpactor* utilizes `bin/coprocessor` to simplify input CNFs as well. The flag `--nosimplcnf` controls this behavior. For issues related with this simplification mechanism, users may find the tip in [SamplingCA/README.md](SamplingCA/README.md) useful. 

## Example Command for Running *CAmpactor*

We provide a short bash script `simple_run.sh` for users to run *CAmpactor* in an end-to-end manner. That is, by executing this bash script, users can obtain a PCA which is initially constructed by *SamplingCA* and then optimized by *CAmpactor*. 

**Note**: For running *SamplingCA* separately, users may refer to the instructions in [SamplingCA/README.md](SamplingCA/README.md). For running *CAmpactor* separately, users may refer to the instructions in the above section. 

The usage of `simple_run.sh` is as follows. 

```
bash simple_run.sh [RANDOM_SEED] [INSTANCE_PATH] [OUTPUT_PCA_NAME]
```

An example of running `simple_run.sh`: 

```
bash simple_run.sh 1 cnf_benchmarks/linux.cnf linux_PCA.out
```

The command above calls *SamplingCA* to solve the instance `cnf_benchmarks/linux.cnf` with default hyper-parameter settings, and then calls *CAmpactor* to optimize the initial PCA with default hyper-parameter settings. The result is stored in `linux_PCA.out`. Here, both *SamplingCA* and *CAmpactor* use random seed 1. Users may refer to [INSTALL.md](INSTALL.md#quick-installation-testing) to understand the console output via a simpler example. For understanding the format of the output PCA, users may check [the README file in the `examples/` directory](examples/README.md). 

## How to Use *CAmpactor*

### The Vanilla Approach

In our implementation of *CAmpactor*, the input PCA generation instance should be modeled as a Boolean formula in CNF in [Dimacs format](http://www.satcompetition.org/2011/format-benchmarks2011.html); *SamplingCA* has the same requirement. The directory named `cnf_benchmarks/` contains all 124 testing benchmarks, which can be taken as input. Users may also use [FeatureIDE](https://github.com/FeatureIDE/FeatureIDE/) to generate input files from existing configurable systems. For a simple case study on how to model a system under test as a Boolean formula as well as how to interpret the format of the output PCA, users may check the documents in the `examples/` directory. 

### A More User-friendly Approach

However, we also provide a more user-friendly way to use *CAmpactor*. That is, the user can specify the system under test using a domain-specific language accepted by [CTWedge](https://github.com/fmselab/ctwedge), and then the input in that language can be automatically encoded into a Boolean formula in CNF by a special parser provided by us. Furthermore, the output PCA can be translated into a human-readable CSV file. 

In order to adopt this approach, the user should first compile *SamplingCA* and *CAmpactor*, and then compile the parser by calling the following command: 

```
bash build_parser.sh
```

We have prepared a Python3 script file `ctw_run.py` for running the parser, *SamplingCA* and *CAmpactor* in an end-to-end manner. The usage of `ctw_run.py` is shown as follows. 

```
python3 ctw_run.py [INSTANCE_PATH] [OUTPUT_PCA_PATH]
```

An example of running `ctw_run.py`: 

```
python3 ctw_run.py CTWedge_interface/simple.ctw simple_PCA.csv
```

The command above calls *SamplingCA* and *CAmpactor* to solve the instance `CTWedge_interface/simple.ctw` (taken from [here](https://github.com/fmselab/CIT_Benchmark_Generator/blob/main/Benchmarks_CITCompetition_2023/EvaluationPhase/CTWedge/INDUSTRIAL_10.ctw)) with default hyper-parameter settings and random seed 1. The result is stored in `./simple_PCA.csv`. 

**NOTE**: for more concrete information about the parser, users may refer to [the README file in the `CTWedge_interface/` directory](CTWedge_interface/README.md). 

## Implementation of *CAmpactor*

The directory named `src/` includes the implementation of *CAmpactor*. 

## Testing Benchmarks for Evaluating *CAmpactor*

The directory named `cnf_benchmarks/` contains all 124 testing benchmarks. We also provide [Benchmark_information.csv](./Benchmark_information.csv) which shows the number of options and the number of constraints for each benchmark. 

## Implementation of Main Competitors of *CAmpactor*

As presented in the paper, the main competitors of *CAmpactor* include *SamplingCA*, as well as *AutoCCAG*, *FastCA* and *TCA* (with *SamplingCA* as the initialization algorithm). 

The implementation of *SamplingCA* is in the same directory as this document, and we make the implementations of the other three PCAG solvers involved in our experiment (*AutoCCAG*, *FastCA* and *TCA*) also publicly available. Their sources are clarified in the paper (Section 5.2). Originally these tools are encapsulated as CA generators rather than reducers. For our purpose, we did minimal modification to remove their original initialization phases and to enable them to take initial PCAs from *SamplingCA*. 

For instructions of running *SamplingCA*, users may refer to [SamplingCA/README.md](./SamplingCA/README.md). For instructions of running the other three solvers (*i.e.,* *AutoCCAG*, *FastCA* and *TCA*), users may refer to [main_competitors/README.md](./main_competitors/README.md). 

**Note**: We also evaluate the performance of other four influential PCAG algorithms, *i.e.*, *HHSA*, *CASA*, *ACTS* and *CTLog*, whose original implementations are available through following links:

- *HHSA*: http://www0.cs.ucl.ac.uk/staff/Yue.Jia/projects/cit_hyperheuristic/downloads/Comb_Linux_64.tar.gz
- *CASA*: https://cse.unl.edu/~citportal/
- *ACTS*: https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/downloadable-tools
- *CTLog*: http://hardlog.udl.cat/static/doc/ctlog/html/index.html

For the evaluation results of *HHSA*, *CASA*, *ACTS* and *CTLog*, readers can refer to [this CSV file](experimental_results/Results_of_CAmpactor_and_its_SOTA_competitors.csv).

## Experimental Results

The directory `experimental_results/` contains 7 `.csv` files for presenting the experimental results. 
- [Results_of_CAmpactor_and_its_SOTA_competitors.csv](https://github.com/chuanluocs/CAmpactor/blob/master/experimental_results/Results_of_CAmpactor_and_its_SOTA_competitors.csv): Results of *CAmpactor* (with *SamplingCA* as its initialization algorithm) and its state-of-the-art competitors on all testing instances. 
- [Results_of_CAmpactor_and_its_alternative_versions.csv](https://github.com/chuanluocs/CAmpactor/blob/master/experimental_results/Results_of_CAmpactor_and_its_alternative_versions.csv): Results of *CAmpactor* and its alternative versions on all testing instances.
- [Results_of_CAmpactor_with_different_gamma_settings.csv](https://github.com/chuanluocs/CAmpactor/blob/master/experimental_results/Results_of_CAmpactor_with_different_gamma_settings.csv): Results of *CAmpactor* with different $\gamma$ settings on all testing instances.
- [Results_of_CAmpactor_with_different_delta_settings.csv](https://github.com/chuanluocs/CAmpactor/blob/master/experimental_results/Results_of_CAmpactor_with_different_delta_settings.csv): Results of *CAmpactor* with different $\delta$ settings on all testing instances.
- [Results_of_CAmpactor_with_different_psi_settings.csv](https://github.com/chuanluocs/CAmpactor/blob/master/experimental_results/Results_of_CAmpactor_with_different_psi_settings.csv): Results of *CAmpactor* with different $\psi$ settings on all testing instances.
- [Results_of_CAmpactor_on_its_generality.csv](https://github.com/chuanluocs/CAmpactor/blob/master/experimental_results/Results_of_CAmpactor_on_its_generality.csv): Results of the generality of *CAmpactor* (with *AutoCCAG*, *FastCA* and *TCA* as its initialization algorithms) on all testing instances.
- [Results_of_two_versions_of_AutoCCAG_FastCA_TCA.csv](https://github.com/chuanluocs/CAmpactor/blob/master/experimental_results/Results_of_two_versions_of_AutoCCAG_FastCA_TCA.csv): Results of the versions of *AutoCCAG*, *FastCA* and *TCA*, which employ *SamplingCA* as their initialization algorithms, and the original versions of *AutoCCAG*, *FastCA* and *TCA*, which use their own, original initialization algorithms.

## Instructions for Reproducing the Experimental Results

See [experiment_reproduction.md](experiment_reproduction.md). 

## Main Developers

- Qiyuan Zhao (<zqy1018@hotmail.com>)
- Chuan Luo (<chuanluophd@outlook.com>)

## Reference

Qiyuan Zhao, Chuan Luo, Shaowei Cai, Wei Wu, Jinkun Lin, Hongyu Zhang, Chunming Hu. *CAmpactor: A Novel and Effective Local Search Algorithm for Optimizing Pairwise Covering Arrays.* To appear in Proceedings of ESEC/FSE 2023. 

This repository contains a pre-print of this paper `paper.pdf`. 
