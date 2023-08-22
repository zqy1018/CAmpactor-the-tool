# Commands for Reproducing the Experimental Results

Here we only describe the commands that are only related with *CAmpactor*. 

## Experiments for RQ1

```bash
for benchmark in ` ls cnf_benchmarks `
do
    # using SamplingCA to initialize
    ./SamplingCA/SamplingCA -input_cnf_path cnf_benchmarks/${benchmark} -output_testcase_path ./SamplingCA/${benchmark}_PCA.out
    # using CAmpactor to optimize
    ./CAmpactor -i cnf_benchmarks/${benchmark} --init_PCA_path SamplingCA/${benchmark}_PCA.out -o ${benchmark}_PCA.out
    rm ./SamplingCA/${benchmark}_PCA.out
done
```

## Experiments for RQ2

```bash
for benchmark in ` ls cnf_benchmarks `
do
    ./SamplingCA/SamplingCA -input_cnf_path cnf_benchmarks/${benchmark} -output_testcase_path ./SamplingCA/${benchmark}_PCA.out
    # Alt-1
    ./CAmpactor -i cnf_benchmarks/${benchmark} --init_PCA_path SamplingCA/${benchmark}_PCA.out -o ${benchmark}_alt-1_PCA.out --delta -1
    # Alt-2
    ./CAmpactor -i cnf_benchmarks/${benchmark} --init_PCA_path SamplingCA/${benchmark}_PCA.out -o ${benchmark}_alt-2_PCA.out --use_cell_tabu
    # Alt-3
    ./CAmpactor -i cnf_benchmarks/${benchmark} --init_PCA_path SamplingCA/${benchmark}_PCA.out -o ${benchmark}_alt-3_PCA.out --psi 0.0
    rm ./SamplingCA/${benchmark}_PCA.out
done
```

## Experiments for RQ3

```bash
for benchmark in ` ls cnf_benchmarks `
do
    ./SamplingCA/SamplingCA -input_cnf_path cnf_benchmarks/${benchmark} -output_testcase_path ./SamplingCA/${benchmark}_PCA.out
    # varying gamma
    for gamma in 100 1000 10000 100000
    do
        ./CAmpactor -i cnf_benchmarks/${benchmark} --init_PCA_path SamplingCA/${benchmark}_PCA.out -o ${benchmark}_gamma_${gamma}_PCA.out --gamma ${gamma}
    done
    # varying delta
    for delta in 5 10 15 20 25 30
    do
        ./CAmpactor -i cnf_benchmarks/${benchmark} --init_PCA_path SamplingCA/${benchmark}_PCA.out -o ${benchmark}_delta_${delta}_PCA.out --delta ${delta}
    done
    # varying psi
    for psi in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
    do
        ./CAmpactor -i cnf_benchmarks/${benchmark} --init_PCA_path SamplingCA/${benchmark}_PCA.out -o ${benchmark}_psi_${psi}_PCA.out --psi ${psi}
    done
    rm ./SamplingCA/${benchmark}_PCA.out
done
```

## Experiments for RQ4

Make sure the main competitors are compiled before reproducing this part of experiments. 

```bash
for benchmark in ` ls cnf_benchmarks `
do
    cd main_competitors/
    # using AutoCCAG to initialize
    python3 simple_run.py -s A -i ../cnf_benchmarks/${benchmark} -o ./${benchmark}_by_AutoCCAG_PCA.out
    # using FastCA to initialize
    python3 simple_run.py -s F -i ../cnf_benchmarks/${benchmark} -o ./${benchmark}_by_FastCA_PCA.out
    # using TCA to initialize
    python3 simple_run.py -s T -i ../cnf_benchmarks/${benchmark} -o ./${benchmark}_by_TCA_PCA.out
    cd ..
    # alt-A
    ./CAmpactor -i cnf_benchmarks/${benchmark} --init_PCA_path main_competitors/${benchmark}_by_AutoCCAG_PCA.out -o ${benchmark}_alt-A_PCA.out
    # alt-F
    ./CAmpactor -i cnf_benchmarks/${benchmark} --init_PCA_path main_competitors/${benchmark}_by_FastCA_PCA.out -o ${benchmark}_alt-F_PCA.out
    # alt-T
    ./CAmpactor -i cnf_benchmarks/${benchmark} --init_PCA_path main_competitors/${benchmark}_by_TCA_PCA.out -o ${benchmark}_alt-T_PCA.out
    rm main_competitors/${benchmark}_by_AutoCCAG_PCA.out main_competitors/${benchmark}_by_FastCA_PCA.out main_competitors/${benchmark}_by_TCA_PCA.out
done
```
