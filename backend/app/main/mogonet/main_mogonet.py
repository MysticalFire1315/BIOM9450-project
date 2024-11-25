import copy
import logging
from typing import List

from app.main.mogonet.feat_importance import cal_feat_imp, summarize_imp_feat
from app.main.mogonet.models import init_model_dict
from app.main.mogonet.train_test import prepare_trte_data, train_test

logger = logging.getLogger("mogonet")


# Main entry point for the program
def main(
    data_folder: str,
    view_list: List[int],
    num_epoch_pretrain: int,
    num_epoch: int,
    lr_e_pretrain: float,
    lr_e: float,
    lr_c: float,
    num_class: int,
):
    # Step 1: Train and test the model
    logger.info("Step 1: Training and Testing the Model...")
    performance = train_test(
        data_folder,
        view_list,
        num_class,
        lr_e_pretrain,
        lr_e,
        lr_c,
        num_epoch_pretrain,
        num_epoch,
    )

    # Step 2: Compute feature importance
    logger.info("Step 2: Generating Feature Importance...")
    num_view = len(view_list)
    dim_hvcdn = pow(num_class, num_view)
    dim_he_list = [200, 200, 100] if "ROSMAP" in data_folder else [400, 400, 200]

    # Prepare the data and initialize the model
    logger.debug("Prep data and initialize model")
    data_tr_list, data_trte_list, trte_idx, labels_trte = prepare_trte_data(
        data_folder, view_list
    )
    dim_list = [x.shape[1] for x in data_tr_list]
    model_dict = init_model_dict(num_view, num_class, dim_list, dim_he_list, dim_hvcdn)

    # Calculate and summarize feature importance
    logger.debug("Start calculating and summarizing")
    featimp_list = cal_feat_imp(data_folder, model_dict, view_list, num_class)
    featimp_list_list = [copy.deepcopy(featimp_list)]
    feat_summary = summarize_imp_feat(featimp_list_list, data_folder=data_folder)

    logger.info("Feature importance generation completed!")

    return performance, feat_summary
