import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sys

sys.path.append('../../Cleaner/Holoclean/')
import Cleaner.Holoclean as holoclean
from Cleaner.Holoclean.detect import NullDetector, ViolationDetector, ErrorsLoaderDetector
from Cleaner.Holoclean.repair.featurize import *


# 1. Setup a HoloClean session.
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
    timeout=3*60000,
    feature_norm=False,
    weight_norm=False,
    print_fw=True
).session

# 2. Load training data and denial constraints.
hc.load_data('rayyan', r'..\..\Data\4_rayyan\dirty.csv')

hc.load_dcs(r'..\..\Data\4_rayyan\dc_rules_holoclean.txt')
hc.ds.set_constraints(hc.get_dcs())

# 3. Detect erroneous cells.
error_loader = ErrorsLoaderDetector(
        db_engine=hc.ds.engine,
        schema_name='public',
        table_name='dk_cells'
)
hc.detect_errors([error_loader])

# 4. Repair errors utilizing the defined features.
hc.setup_domain()
featurizers = [
    OccurAttrFeaturizer(),
    FreqFeaturizer(),
    ConstraintFeaturizer(),
]

hc.repair_errors(featurizers)

# 5. Evaluate the correctness of the results.
hc.evaluate(fpath=r'..\..\Data\4_rayyan\rayyan_clean_holoclean.csv',
            tid_col='tid',
            attr_col='attribute',
            val_col='correct_val')
