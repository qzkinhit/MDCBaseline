import pandas as pd
import numpy as np
import signal
import copy
import time
import sys
import os
import raha
import argparse
import shutil
import logging
from collections import Counter
from datetime import datetime
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import warnings
from tqdm import tqdm
from rich.progress import track
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from Cleaner.Scared.scared import handler, check_string, SCAREd

warnings.filterwarnings("ignore")
import re
if __name__ == "__main__":
    time_limit = 24*3600
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(time_limit)
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--clean_path', type=str, default=None)
        parser.add_argument('--dirty_path', type=str, default=None)
        parser.add_argument('--rule_path', type=str, default=None)
        parser.add_argument('--task_name', type=str, default=None)
        parser.add_argument('--onlyed', type=int, default=None)
        parser.add_argument('--perfected', type=int, default=None)
        args = parser.parse_args()
        dirty_path = args.dirty_path
        clean_path = args.clean_path
        task_name = args.task_name
        rule_path = args.rule_path
        ONLYED = args.onlyed
        PERFECTED = args.perfected

        # dirty_path = "./data_with_rules/1_hospitals/noise/1_hospitals-inner_outer_error-10.csv"
        # rule_path = "./data_with_rules/5_tax/dc_rules-validate-fd-horizon.txt"
        # clean_path = "./data_with_rules/1_hospitals/clean.csv"
        # task_name = "hospital1"
        # ONLYED = 0
        # PERFECTED = 0

        detection_dictionary = {}
        if not PERFECTED:
            stra_path = "./data_with_rules/" + task_name[:-1] + "/noise/raha-baran-results-" + 'scared'+task_name+check_string(dirty_path)
            if os.path.exists(stra_path):
                shutil.rmtree(stra_path)
            stra_path = "./DATASET/data_with_rules/" + task_name[:-1] + "/noise/raha-baran-results-" + 'scared'+task_name+check_string(dirty_path)
            if os.path.exists(stra_path):
                shutil.rmtree(stra_path)
            stra_path = "./data_with_rules/5_tax/tax_50k/raha-baran-results-" + 'scared'+task_name+check_string(dirty_path)
            if os.path.exists(stra_path):
                shutil.rmtree(stra_path)
            stra_path = "./data_with_rules/5_tax/tax_50k/raha-baran-results-" + 'scared'+task_name+check_string(dirty_path)
            if os.path.exists(stra_path):
                shutil.rmtree(stra_path)
            dataset_dictionary = {
                "name": 'scared'+task_name+check_string(dirty_path),
                "path": dirty_path,
                "clean_path": clean_path
            }
            start_time = time.time()
            app = raha.Detection()
            detection_dictionary = app.run(dataset_dictionary)
        else:
            clean_df = pd.read_csv(clean_path).astype(str)
            dirty_df = pd.read_csv(dirty_path).astype(str)
            clean_df = clean_df.fillna("nan")
            dirty_df = dirty_df.fillna("nan")
            for i in range(len(clean_df)):
                for j in range(len(clean_df.columns)):
                    if dirty_df.iloc[i, j] != clean_df.iloc[i, j]:
                        detection_dictionary[(i, j)] = 'dummy'

        start_time = time.time()
        logging.basicConfig(level=logging.DEBUG)
        scared_cleaner = SCAREd(dirty_path, clean_path)
        scared_cleaner.run()
    except TimeoutError as e:
        print("Time exceeded:", e, task_name, dirty_path)
        out_file = open("./aggre_results/timeout_log.txt", "a")
        now = datetime.now()
        out_file.write(now.strftime("%Y-%m-%d %H:%M:%S"))
        out_file.write(" Scared.py: ")
        out_file.write(f" {task_name}")
        out_file.write(f" {dirty_path}\n")
        out_file.close()
