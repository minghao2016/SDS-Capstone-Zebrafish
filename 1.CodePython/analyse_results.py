import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score


"""
Return a list of result file pathes in the output folder

output_path: output folder name
"""
def get_result_file_pathes(output_path):
    results = os.listdir(output_path)
    results = [output_path + '/' + result for result in results]
    return results


"""
Return the result dataframe containing precision scores calculated.

input_path: raw result file's path
"""
def process_row_data(input_path):
    results = pd.read_csv(input_path)
    results.columns = results.columns.str.strip()
    
    base=os.path.basename(input_path)
    sample_index = os.path.splitext(base)[0][2:]
    print(sample_index)
    results['sample_index'] = sample_index
    
    results['type0_num'] = (results['ww'] + results['wm'])
    results['type1_num'] = (results['mm'] + results['mw'])

    results['type0_precision'] = results['ww'] / (results['ww'] + results['mw'])
    results['type0_recall'] = results['ww'] / (results['ww'] + results['wm'])
    results['type1_precision'] = results['mm'] / (results['mm'] + results['wm'])
    results['type1_recall'] = results['mm'] / (results['mm'] + results['mw'])
    results = results.fillna(0)
    
    results['type0_f1'] = ( 2 * results['type0_precision'] * results['type0_recall'] )/ (results['type0_precision'] + results['type0_recall'])
    results['type1_f1'] = ( 2 * results['type1_precision'] * results['type1_recall'] )/ (results['type1_precision'] + results['type1_recall'])
    results = results.fillna(0)
    
    results['precision'] = ((results['type0_precision'] * results['type0_num']) + (results['type1_precision'] * results['type1_num']))/ (results['type0_num'] + results['type1_num'])
    results['recall'] = ((results['type0_recall'] * results['type0_num']) + (results['type1_recall'] * results['type1_num']))/ (results['type0_num'] + results['type1_num'])
    results['f1'] = ((results['type0_f1'] * results['type0_num']) + (results['type1_f1'] * results['type1_num']))/ (results['type0_num'] + results['type1_num'])
    results = results.fillna(0)
    
    return results

input_folder = str(input("Please enter raw results' folder name: "))
output_path = str(input("Please enter result file path: "))

# get result file names
result_files = get_result_file_pathes(os.path.join(os.getcwd(), input_folder))

results = []
for result_file in result_files:
    name = result_file.split('/')[-1]
    if (name == '.DS_Store'): continue
    print('processing: ' + name)
    
    # process raw result and append the dataframe to the results list
    results.append(process_row_data(result_file))


aggregated_result = pd.concat(results)
print('aggregated result shape:', aggregated_result.shape)

aggregated_result.to_csv(output_path)
