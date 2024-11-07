import sys
import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sys
# 获取当前脚本所在目录的上级目录路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')
sys.path.append('../../Cleaner/Holoclean/')
import Cleaner.Holoclean as holoclean
from Cleaner.Holoclean.detect import NullDetector, ViolationDetector
from Cleaner.Holoclean.repair.featurize import *

# 1. Set up a HoloClean session.
hc = holoclean.HoloClean(
    db_user='datacleanuser',
    db_name='holo',
    domain_thresh_1=0,
    domain_thresh_2=0,
    weak_label_thresh=0.99,
    max_domain=10000,
    cor_strength=0.6,
    nb_cor_strength=0.8,
    epochs=10,
    weight_decay=0.01,
    learning_rate=0.001,
    threads=1,
    batch_size=1,
    verbose=True,
    timeout=3 * 60000,
    feature_norm=False,
    weight_norm=False,
    print_fw=True
).session

# 2. Load training data and denial constraints.
hc.load_data('hospitalt2', r'..\..\Data\1_hospital\dirty_index.csv')

hc.load_dcs(r'..\..\Data\1_hospital\dc_rules_dc_holoclean.txt')
hc.ds.set_constraints(hc.get_dcs())

# 3. Detect erroneous cells using these two detectors.
detectors = [NullDetector(), ViolationDetector()]
hc.detect_errors(detectors)

# 4. Repair errors utilizing the defined features.
hc.setup_domain()
featurizers = [
    InitAttrFeaturizer(),
    OccurAttrFeaturizer(),
    FreqFeaturizer(),
    ConstraintFeaturizer(),
]

hc.repair_errors(featurizers)

# # 5. Evaluate the correctness of the results.
# hc.evaluate(fpath=r'.ata\4_rayyan\rayyan_clean_holoclean.csv',
#             tid_col='tid',
#             attr_col='attribute',
#             val_col='correct_val')
# 5. 评估修复效果，并导出修复后的数据到 CSV
output_csv_path = r'./1_hospital_repaired_dataset.csv'  # 你想保存的文件路径
eval_report = hc.evaluate(fpath=r'../../Data/1_hospital/hospital_clean_holoclean.csv',
            tid_col='tid',
            attr_col='attribute',
            val_col='correct_val',
            output_csv_path=output_csv_path)
# eval_report = hc.evaluate(.\..\D
#     fpath=r'D:\holoclean\Data\1_hospital\hospital_clean_holoclean.csv',
#     tid_col='tid',
#     attr_col='attribute',
#     val_col='correct_val',
#     output_csv_path=output_csv_path
# )

print(f"清洗后的数据已保存到: {output_csv_path}")