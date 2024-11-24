# feat_importance.py
import os
import copy
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import f1_score
from app.main.mogonet.utils import load_model_dict
from app.main.mogonet.models import init_model_dict
from app.main.mogonet.train_test import prepare_trte_data, gen_trte_adj_mat, test_epoch
import logging

# Set device to CPU explicitly
device = torch.device("cpu")
logger = logging.getLogger("mogonet")

def cal_feat_imp(data_folder, model_folder, view_list, num_class):
    num_view = len(view_list)
    dim_hvcdn = pow(num_class, num_view)
    adj_parameter = 2 if 'ROSMAP' in data_folder else 10
    dim_he_list = [200, 200, 100] if 'ROSMAP' in data_folder else [400, 400, 200]

    logger.debug("prepare_trte_data")
    data_tr_list, data_trte_list, trte_idx, labels_trte = prepare_trte_data(data_folder, view_list)
    adj_tr_list, adj_te_list = gen_trte_adj_mat(data_tr_list, data_trte_list, trte_idx, adj_parameter)

    logger.debug("featname_list")
    featname_list = []
    for v in view_list:
        df = pd.read_csv(os.path.join(data_folder, f"{v}_featname.csv"), header=None)
        featname_list.append(df.values.flatten())

    dim_list = [x.shape[1] for x in data_tr_list]
    model_dict = init_model_dict(num_view, num_class, dim_list, dim_he_list, dim_hvcdn)

    # Load model parameters onto CPU
    logger.debug("load model")
    model_dict = load_model_dict(data_folder, model_dict)
    te_prob = test_epoch(data_trte_list, adj_te_list, trte_idx["te"], model_dict)

    f1 = f1_score(labels_trte[trte_idx["te"]], te_prob.argmax(1), average='macro' if num_class > 2 else None)

    logger.debug(f"loop feat {len(featname_list)}")
    feat_imp_list = []
    for i in range(len(featname_list)):
        feat_imp = {"feat_name": featname_list[i], "imp": np.zeros(dim_list[i])}
        logger.debug(f"{i}")
        for j in range(dim_list[i]):
            feat_tr = data_tr_list[i][:, j].clone()
            feat_trte = data_trte_list[i][:, j].clone()
            data_tr_list[i][:, j] = 0
            data_trte_list[i][:, j] = 0
            adj_tr_list, adj_te_list = gen_trte_adj_mat(data_tr_list, data_trte_list, trte_idx, adj_parameter)
            te_prob = test_epoch(data_trte_list, adj_te_list, trte_idx["te"], model_dict)
            f1_tmp = f1_score(labels_trte[trte_idx["te"]], te_prob.argmax(1), average='macro' if num_class > 2 else None)
            feat_imp_score = (f1 - f1_tmp) * dim_list[i]
            if np.isscalar(feat_imp_score):
                feat_imp['imp'][j] = feat_imp_score
            else:
                feat_imp['imp'][j] = feat_imp_score[0]  # Take the first element if it's a list or array

            data_tr_list[i][:, j] = feat_tr.clone()
            data_trte_list[i][:, j] = feat_trte.clone()
        feat_imp_list.append(pd.DataFrame(data=feat_imp))

    return feat_imp_list

def summarize_imp_feat(featimp_list_list, data_folder):
    """
    Summarizes feature importance from multiple runs, saves the top features to a CSV file,
    and prints a confirmation message.

    Parameters:
        featimp_list_list: List of feature importance dataframes from multiple runs.
        data_folder: The dataset folder name ('ROSMAP' or 'BRCA').
        topn: Number of top features to save (default is 30).
    """
    # Number of repeated runs and views
    num_rep = len(featimp_list_list)
    num_view = len(featimp_list_list[0])

    # Initialize a list to store temporary dataframes with 'omics' columns
    df_tmp_list = []
    for v in range(num_view):
        # Copy dataframe and add 'omics' column indicating the view
        df_tmp = copy.deepcopy(featimp_list_list[0][v])
        df_tmp['omics'] = v
        df_tmp_list.append(df_tmp)

    # Concatenate the initial set of dataframes to create the full feature importance dataframe
    df_featimp = pd.concat(df_tmp_list, ignore_index=True)

    # Loop through subsequent repeats and views to add to df_featimp
    for r in range(1, num_rep):
        for v in range(num_view):
            df_tmp = copy.deepcopy(featimp_list_list[r][v])
            df_tmp['omics'] = v  # Add 'omics' column indicating the view
            df_featimp = pd.concat([df_featimp, df_tmp], ignore_index=True)

    # Group by 'feat_name' and 'omics', summing the 'imp' values
    df_featimp_top = df_featimp.groupby(['feat_name', 'omics'])['imp'].sum().reset_index()

    # Sort by 'imp' in descending order and take the top features
    df_featimp_top = df_featimp_top.sort_values(by='imp', ascending=False)

    return df_featimp_top
