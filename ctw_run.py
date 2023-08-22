#!/usr/bin/env python3

import os, sys

def read_param_list(expected_param_list_name):
    res = []
    with open(expected_param_list_name, "r") as f:
        for l in f.readlines():
            line = l.strip()
            if line:
                res.append(line)
    return res

def read_cnf_info(annotated_cnf):
    param2var = dict()
    var2param = dict()

    with open(annotated_cnf) as f:
        for l in f.readlines():
            line = l.strip()
            if line:
                if line.startswith("c "):
                    tokens = line.split(" ")
                    param2var[tokens[1]] = tokens[3]
                    var2param[int(tokens[3])] = tokens[1]

    return (param2var, var2param)

def read_our_output(filepath):
    testcases = []

    with open(filepath) as f:
        for l in f.readlines():
            line = l.strip()
            if line:
                tc = []
                for c in line:
                    if c == '0':
                        tc.append(0)
                    elif c == '1':
                        tc.append(1)

                testcases.append(tc)

    return testcases

def our_output_to_required_output(our_testcases, var2param, params):
    res = []

    for tc in our_testcases:
        realtc = dict()
        for i, x in enumerate(tc):

            p = var2param[i + 1]
            if p == "@top" or p.startswith("@tmp"):
                continue

            if "@" in p:
                if x:
                    pa, v = p.split("@")
                    realtc[pa] = v
            else:
                if x:
                    realtc[p] = "true"
                else:
                    realtc[p] = "false"
        
        realtc_ordered = []
        for paname in params:
            realtc_ordered.append(realtc[paname])

        res.append(realtc_ordered)
    
    return res

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 ctw_run.py [INPUT_CTW_FILE] [OUTPUT_CSV_FILE]")
        exit(0) 

    parser_name = "./ctw_parser"
    instance_path = sys.argv[1]
    output_path = sys.argv[2]
    mainscript_name = "bash simple_run.sh"
    expected_cnf_name = "____tmp.cnf"
    expected_param_list_name = "____tmp.params"
    tmp_output_path = "____tmp_PCA.out"

    call_parser_cmd = " ".join([parser_name, instance_path, expected_cnf_name, expected_param_list_name, "> /dev/null 2>&1"])
    os.system(call_parser_cmd)

    params = read_param_list(expected_param_list_name)
    
    real_cmd = " ".join([mainscript_name, "1", expected_cnf_name, tmp_output_path, "> /dev/null 2>&1"])
    os.system(real_cmd)

    param2var, var2param = read_cnf_info(expected_cnf_name)
    our_testcases = read_our_output(tmp_output_path)
    testcases_to_be_put = our_output_to_required_output(our_testcases, var2param, params)

    with open(output_path, "w") as f:
        f.write(",".join(params) + "\n")
        for tc in testcases_to_be_put:
            f.write(",".join(tc) + "\n")

    clean_cmd = " ".join(["rm", expected_cnf_name, expected_param_list_name, tmp_output_path])
    os.system(clean_cmd)
