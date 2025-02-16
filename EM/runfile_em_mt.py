import argparse
import json
import pathlib
import glob
import sys
import os
from os.path import exists

import numpy as np
np.float_ = np.float64
import multiprocessing
multiprocessing.set_start_method("fork")
from grim import grim
import math
import string, copy

def run(
    plan_b,
    config_file,
    count_by_prob=None,
    pop=None,
    em_mr=False,
    iteration=1,
    num_subjects=None,
    project_dir_graph="",
):
    project_dir = ""
    with open(config_file) as f:
        json_conf = json.load(f)
    output_dir = json_conf.get("output_dir", "data")
    graph_files_path = json_conf.get("graph_files_path")
    if graph_files_path[-1] != "/":
        graph_files_path += "/"
    config = {
        "planb": json_conf.get("planb", True),
        "pops": json_conf.get("populations"),
        "priority": json_conf.get("priority"),
        "epsilon": json_conf.get("epsilon", 1e-3),
        "number_of_results": json_conf.get("number_of_results", 1000),
        "number_of_pop_results": json_conf.get("number_of_pop_results", 100),
        "output_MUUG": json_conf.get("output_MUUG", False),
        "output_haplotypes": json_conf.get("output_haplotypes", True),
        "node_file": project_dir_graph + graph_files_path + json_conf.get("node_csv_file"),
        "top_links_file": project_dir_graph + graph_files_path + json_conf.get("top_links_csv_file"),
        "edges_file": project_dir_graph + graph_files_path + json_conf.get("edges_csv_file"),
        "imputation_input_file": json_conf.get("imputation_in_file"),
        "imputation_out_umug_freq_file": output_dir + json_conf.get("imputation_out_umug_freq_filename", "None"),
        "imputation_out_umug_pops_file": output_dir + json_conf.get("imputation_out_umug_pops_filename", "None"),
        "imputation_out_hap_freq_file": output_dir + json_conf.get("imputation_out_hap_freq_filename"),
        "imputation_out_hap_pops_file": output_dir + json_conf.get("imputation_out_hap_pops_filename", "None"),
        "imputation_out_miss_file": output_dir + json_conf.get("imputation_out_miss_filename", "miss.txt"),
        "imputation_out_problem_file": output_dir + json_conf.get("imputation_out_problem_filename", "problem.txt"),
        "factor_missing_data": json_conf.get("factor_missing_data", 0.01),
        "loci_map": json_conf.get("loci_map", {"A": 1, "B": 3, "C": 2, "DQB1": 4, "DRB1": 5}),
        "matrix_planb": json_conf.get("Plan_B_Matrix", [
                [[1, 2, 3, 4, 5]],
                [[1, 2, 3], [4, 5]],
                [[1], [2, 3], [4, 5]],
                [[1, 2, 3], [4], [5]],
                [[1], [2, 3], [4], [5]],
                [[1], [2], [3], [4], [5]],
            ]),
        "pops_count_file": project_dir + json_conf.get("pops_count_file", ""),
        "use_pops_count_file": json_conf.get("pops_count_file", False),
        "number_of_options_threshold": json_conf.get("number_of_options_threshold", 100000),
        "max_haplotypes_number_in_phase": json_conf.get("max_haplotypes_number_in_phase", 100),
        "bin_imputation_input_file": project_dir + json_conf.get("bin_imputation_in_file", "None"),
        "num_thread": json_conf.get("num_threads", 1),
        "nodes_for_plan_A": json_conf.get("Plan_A_Matrix", []),
        "save_mode": json_conf.get("save_space_mode", False),
        "UNK_priors": json_conf.get("UNK_priors", "MR"),
    }
    all_loci_set = set()
    for _, val in config["loci_map"].items():
        all_loci_set.add(str(val))
    config["full_loci"] = "".join(sorted(all_loci_set))
    config["imputation_out_hap_pops_file"] = config["imputation_out_hap_pops_file"] + str(iteration) + ".txt"

    if pop:
        config["pops"] = pop

    print("****************************************************************************************************")
    print("Performing imputation based on:")
    print("\tPopulation: {}".format(config["pops"]))
    print("\tPriority: {}".format(config["priority"]))
    print("\tEpsilon: {}".format(config["epsilon"]))
    print("\tPlan B: {}".format(config["planb"]))
    print("\tNumber of Results: {}".format(config["number_of_results"]))
    print("\tNumber of Population Results: {}".format(config["number_of_pop_results"]))
    print("\tNodes File: {}".format(config["node_file"]))
    print("\tTop Links File: {}".format(config["edges_file"]))
    print("\tInput File: {}".format(config["imputation_input_file"]))
    print("\tOutput UMUG Format: {}".format(config["output_MUUG"]))
    print("\tOutput UMUG Freq Filename: {}".format(config["imputation_out_umug_freq_file"]))
    print("\tOutput UMUG Pops Filename: {}".format(config["imputation_out_umug_pops_file"]))
    print("\tOutput Haplotype Format: {}".format(config["output_haplotypes"]))
    print("\tOutput HAP Freq Filename: {}".format(config["imputation_out_hap_freq_file"]))
    print("\tOutput HAP Pops Filename: {}".format(config["imputation_out_hap_pops_file"]))
    print("\tOutput Miss Filename: {}".format(config["imputation_out_miss_file"]))
    print("\tOutput Problem Filename: {}".format(config["imputation_out_problem_file"]))
    print("\tFactor Missing Data: {}".format(config["factor_missing_data"]))
    print("\tLoci Map: {}".format(config["loci_map"]))
    print("\tPlan B Matrix: {}".format(config["matrix_planb"]))
    print("\tPops Count File: {}".format(config["pops_count_file"]))
    print("\tUse Pops Count File: {}".format(config["use_pops_count_file"]))
    print("\tNumber of Options Threshold: {}".format(config["number_of_options_threshold"]))
    print("\tMax Number of haplotypes in phase: {}".format(config["max_haplotypes_number_in_phase"]))
    if config["nodes_for_plan_A"]:
        print("\tNodes in plan A: {}".format(config["nodes_for_plan_A"]))
    print("\tSave space mode: {}".format(config["save_mode"]))
    print("****************************************************************************************************")

    # Create graph instance
    graph = grim.graph_instance(config)
    imputation_list = []
    pathlib.Path(output_dir).mkdir(parents=False, exist_ok=True)

    input_file = config["imputation_input_file"]
    in_dir = os.path.dirname(input_file)
    if in_dir == "":
        in_dir = "."
    in_file_basename = os.path.basename(input_file)

    if not num_subjects:
        num_subjects = os.popen("wc -l " + input_file).read()
        num_subjects = int(num_subjects.strip().split(" ")[0]) + 1
    print(num_subjects)

    # Create output directory for split files
    output_ct = "output_ct"
    os.makedirs(output_ct, exist_ok=True)
    # Use output_ct directory directly rather than combining with in_dir
    split_prefix = os.path.join(output_ct, in_file_basename[0:2])
    split_cmd = (
        "split -l "
        + str(int(math.ceil(num_subjects / config["num_thread"])))
        + " "
        + input_file
        + " "
        + split_prefix
    )
    print(f"Split Command: {split_cmd}")
    os.system(split_cmd)

    alpha = string.ascii_lowercase
    threads_list = []
    config_list = []
    for i in range(config["num_thread"]):
        imputation = grim.impute_instance(config, graph, count_by_prob=count_by_prob)
        imputation_list.append(imputation)
        # Construct the split file name using the split_prefix
        in_file = split_prefix + alpha[int(i / 26)] + alpha[int(i % 26)]
        print(in_file)
        output_file = os.path.join(output_ct, os.path.basename(in_file) + "_out")
        config_list.append(copy.deepcopy(config))
        config_list[i]["imputation_input_file"] = in_file
        config_list[i]["imputation_out_hap_freq_file"] = output_file

    for i in range(config["num_thread"]):
        t = multiprocessing.Process(
            target=imputation_list[i].impute_file,
            args=(config_list[i], plan_b, em_mr, True),
        )
        threads_list.append(t)
    for t in threads_list:
        t.start()
    for t in threads_list:
        t.join()
    for t in threads_list:
        t.terminate()

    with open(config["imputation_out_hap_freq_file"], "w") as f_out:
        for i in range(config["num_thread"]):
            with open(config_list[i]["imputation_out_hap_freq_file"]) as f_t_out:
                for line in f_t_out:
                    f_out.write(line)
                f_t_out.close()
                os.remove(config_list[i]["imputation_out_hap_freq_file"])

    print("Starting cleanup of temporary split files.")
    temp_file_prefix = in_file_basename[0:2]
    temp_files_pattern = os.path.join(output_ct, temp_file_prefix + "*")
    temp_files = glob.glob(temp_files_pattern)
    if temp_files:
        for temp_file in temp_files:
            print(f"Removing temporary file: {temp_file}")
            try:
                os.remove(temp_file)
            except Exception as e:
                print(f"Error removing file {temp_file}: {e}")
        print("All temporary files removed.")
    else:
        print("No temporary files found with pattern:", temp_files_pattern)
    try:
        os.rmdir(output_ct)
        print(f"Temporary directory '{output_ct}' removed.")
    except Exception as e:
        print(f"Error removing directory '{output_ct}': {e}")
