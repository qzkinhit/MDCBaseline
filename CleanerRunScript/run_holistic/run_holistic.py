# run_holistic.py
import os
import sys
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

from Cleaner.Holistic_BigDansing.holistic import Holistic
import multiprocessing
import time
from datetime import datetime

def run_holistic(task_name, PERFECTED, ONLYED, rule_path, dirty_path, clean_path, output_path):
    hl = Holistic(task_name, PERFECTED, ONLYED, output_path)
    hl.run(rule_path, dirty_path, clean_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--clean_path', type=str, default="../../Data/1_hospital/clean.csv")
    parser.add_argument('--dirty_path', type=str, default="../../Data/1_hospital/noise/1_hospital-inner_outer_error-30.csv")
    parser.add_argument('--rule_path', type=str, default="../../Data/1_hospital/dc_rules_dc_holoclean.txt")
    parser.add_argument('--task_name', type=str, default="holistic_hospital3")
    parser.add_argument('--onlyed', type=int, default=0)
    parser.add_argument('--perfected', type=int, default=0)
    parser.add_argument('--output_path', type=str, default="../../results/hospital/")
    args = parser.parse_args()

    dirty_path = args.dirty_path
    clean_path = args.clean_path
    rule_path = args.rule_path
    task_name = args.task_name
    ONLYED = args.onlyed
    PERFECTED = args.perfected
    output_path = args.output_path

    time_limit = 24 * 3600  # 24h

    process = multiprocessing.Process(target=run_holistic, args=(task_name, PERFECTED, ONLYED, rule_path, dirty_path, clean_path, output_path))
    process.start()
    process.join(time_limit)
    if process.is_alive():
        process.terminate()
        process.join()
        print("Time exceeded:", task_name, dirty_path)
        with open("./aggre_results/timeout_log.txt", "a") as out_file:
            now = datetime.now()
            out_file.write(now.strftime("%Y-%m-%d %H:%M:%S"))
            out_file.write(f'Timeout: Holistic.py: {task_name} {dirty_path}\n')
