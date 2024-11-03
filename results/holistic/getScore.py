import pandas as pd
from util.getScore import calculate_all_metrics

# holistic
clean = pd.read_csv('../Data/1_hospital/clean_index.csv')
dirty = pd.read_csv('../Data/1_hospital/dirty_index.csv')
cleaned = pd.read_csv('../results/holistic/Repaired_res/hospital/hospital_dirty/repaired_hospital_dirty1.csv')
calculate_all_metrics(clean, dirty, cleaned,
                    ['ProviderNumber', 'HospitalName', 'Address1', 'Address2', 'Address3', 'City', 'State', 'ZipCode', 'CountyName', 'PhoneNumber', 'HospitalType', 'HospitalOwner', 'EmergencyService', 'Condition', 'MeasureCode', 'MeasureName', 'Score', 'Sample', 'Stateavg'],
                    '../results/holistic/Score/hospital', 'dirty')