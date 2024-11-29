# train_test.py
import logging
import os

import numpy as np
import torch
import torch.nn.functional as F
from sklearn.metrics import accuracy_score, f1_score, precision_score, roc_auc_score

from app.main.mogonet.models import init_model_dict, init_optim
from app.main.mogonet.utils import (
    cal_adj_mat_parameter,
    cal_sample_weight,
    gen_adj_mat_tensor,
    gen_test_adj_mat_tensor,
    one_hot_tensor,
)

# Set device to CPU explicitly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

logger = logging.getLogger("mogonet")


def prepare_trte_data(data_folder, view_list):
    # Load training and testing data for each view
    num_view = len(view_list)
    labels_tr = np.loadtxt(
        os.path.join(data_folder, "labels_tr.csv"), delimiter=","
    ).astype(int)
    labels_te = np.loadtxt(
        os.path.join(data_folder, "labels_te.csv"), delimiter=","
    ).astype(int)
    data_tr_list = []
    data_te_list = []

    # Load features for each view
    for i in view_list:
        data_tr_list.append(
            np.loadtxt(os.path.join(data_folder, f"{i}_tr.csv"), delimiter=",")
        )
        data_te_list.append(
            np.loadtxt(os.path.join(data_folder, f"{i}_te.csv"), delimiter=",")
        )

    num_tr = data_tr_list[0].shape[0]
    num_te = data_te_list[0].shape[0]
    data_mat_list = [
        np.concatenate((data_tr_list[i], data_te_list[i]), axis=0)
        for i in range(num_view)
    ]

    # Convert data to PyTorch FloatTensor format on CPU
    data_tensor_list = [torch.FloatTensor(data).to(device) for data in data_mat_list]

    idx_dict = {"tr": list(range(num_tr)), "te": list(range(num_tr, num_tr + num_te))}
    data_train_list = [data[idx_dict["tr"]].clone() for data in data_tensor_list]
    data_all_list = [
        torch.cat((data[idx_dict["tr"]].clone(), data[idx_dict["te"]].clone()), 0)
        for data in data_tensor_list
    ]

    labels = np.concatenate((labels_tr, labels_te))

    return data_train_list, data_all_list, idx_dict, labels


def gen_trte_adj_mat(data_tr_list, data_trte_list, trte_idx, adj_parameter):
    adj_train_list = []
    adj_test_list = []
    adj_metric = "cosine"

    for i in range(len(data_tr_list)):
        adj_param_adaptive = cal_adj_mat_parameter(
            adj_parameter, data_tr_list[i], adj_metric
        )
        adj_train_list.append(
            gen_adj_mat_tensor(data_tr_list[i], adj_param_adaptive, adj_metric)
        )
        adj_test_list.append(
            gen_test_adj_mat_tensor(
                data_trte_list[i], trte_idx, adj_param_adaptive, adj_metric
            )
        )

    return adj_train_list, adj_test_list


def train_epoch(
    data_list,
    adj_list,
    label,
    one_hot_label,
    sample_weight,
    model_dict,
    optim_dict,
    train_VCDN=True,
):
    # 单个训练周期的训练过程
    loss_dict = {}  # 用于存储每个模型的损失值
    criterion = torch.nn.CrossEntropyLoss(
        reduction="none"
    )  # 损失函数：不自动求平均值，以便对样本权重进行加权

    # 将所有模型设为训练模式
    for model_key in model_dict:
        model_dict[model_key].train()

    num_view = len(data_list)  # 视图数量
    # 针对每个视图进行训练
    for i in range(num_view):
        # 优化器梯度置零，防止梯度累积
        optim_dict["C{:}".format(i + 1)].zero_grad()

        # 对应视图的模型前向传播，生成预测
        ci = model_dict["C{:}".format(i + 1)](
            model_dict["E{:}".format(i + 1)](data_list[i], adj_list[i])
        )

        # 计算损失：交叉熵损失乘以样本权重后求平均
        ci_loss = torch.mean(torch.mul(criterion(ci, label), sample_weight))

        # 反向传播更新模型参数
        ci_loss.backward()
        optim_dict["C{:}".format(i + 1)].step()

        # 将损失值保存到字典中
        loss_dict["C{:}".format(i + 1)] = ci_loss.detach().cpu().numpy().item()

    # 如果启用 VCDN 训练且视图数量大于等于 2
    if train_VCDN and num_view >= 2:
        optim_dict["C"].zero_grad()  # 清空 VCDN 的梯度
        ci_list = [
            model_dict["C{:}".format(i + 1)](
                model_dict["E{:}".format(i + 1)](data_list[i], adj_list[i])
            )
            for i in range(num_view)
        ]
        c = model_dict["C"](ci_list)  # VCDN 聚合各视图的输出

        # 计算 VCDN 损失并反向传播更新参数
        c_loss = torch.mean(torch.mul(criterion(c, label), sample_weight))
        c_loss.backward()
        optim_dict["C"].step()

        # 保存 VCDN 损失值
        loss_dict["C"] = c_loss.detach().cpu().numpy().item()

    return loss_dict  # 返回各视图和 VCDN 模型的损失值


def test_epoch(data_list, adj_list, te_idx, model_dict):
    # 进行测试（评估）过程
    for model_key in model_dict:
        model_dict[model_key].eval()  # 将所有模型设为评估模式

    # 各视图的模型输出列表
    ci_list = [
        model_dict["C{:}".format(i + 1)](
            model_dict["E{:}".format(i + 1)](data_list[i], adj_list[i])
        )
        for i in range(len(data_list))
    ]

    # 如果有多个视图，则使用 VCDN 聚合预测结果
    if len(data_list) >= 2:
        c = model_dict["C"](ci_list)
    else:
        c = ci_list[0]

    # 获取测试集的预测概率并转换为 NumPy 格式
    c = c[te_idx, :]  # 选择测试样本的索引
    prob = F.softmax(c, dim=1).data.cpu().numpy()  # 使用 softmax 得到每个类别的概率

    return prob  # 返回预测概率


# Add AUC and Precision to both training and testing performance
def train_test(
    data_folder,
    view_list,
    num_class,
    lr_e_pretrain,
    lr_e,
    lr_c,
    num_epoch_pretrain,
    num_epoch,
):
    """
    Main training and testing function with AUC and Precision added
    Logs performance metrics at specific intervals:
    - Training: ACC, F1_Weighted, F1_Macro, AUC, Precision
    - Testing: ACC, F1_Weighted, F1_Macro, AUC, Precision
    """
    num_view = len(view_list)  # Number of views
    dim_hvcdn = pow(num_class, num_view)  # Dimension for VCDN hidden layer

    # Set adjacency matrix parameters and hidden dimensions based on dataset
    if "ROSMAP" in data_folder:
        adj_parameter = 2
        dim_he_list = [200, 200, 100]  # Hidden dimensions for each view
    else:
        adj_parameter = 10
        dim_he_list = [400, 400, 200]

    # Prepare training and testing data and corresponding labels
    data_tr_list, data_trte_list, trte_idx, labels_trte = prepare_trte_data(
        data_folder, view_list
    )

    # Convert training labels and sample weights to PyTorch tensors
    labels_tr_tensor = torch.LongTensor(labels_trte[trte_idx["tr"]])
    onehot_labels_tr_tensor = one_hot_tensor(labels_tr_tensor, num_class)
    sample_weight_tr = torch.FloatTensor(
        cal_sample_weight(labels_trte[trte_idx["tr"]], num_class)
    )

    if device.type == "cuda":
        labels_tr_tensor = labels_tr_tensor.cuda()
        onehot_labels_tr_tensor = onehot_labels_tr_tensor.cuda()
        sample_weight_tr = sample_weight_tr.cuda()

    # Generate adjacency matrices for training and testing data
    adj_tr_list, adj_te_list = gen_trte_adj_mat(
        data_tr_list, data_trte_list, trte_idx, adj_parameter
    )

    # Initialize model dictionary containing feature extractors, classifiers, and VCDN model
    dim_list = [x.shape[1] for x in data_tr_list]
    model_dict = init_model_dict(num_view, num_class, dim_list, dim_he_list, dim_hvcdn)

    # Load models onto GPU (if available)
    for model_key in model_dict:
        if device.type == "cuda":
            model_dict[model_key].to(device)

    logger.info("Pretraining GCNs...")
    # Pretrain GCNs optimizer
    optim_dict = init_optim(num_view, model_dict, lr_e_pretrain, lr_c)
    for epoch in range(num_epoch_pretrain):
        train_epoch(
            data_tr_list,
            adj_tr_list,
            labels_tr_tensor,
            onehot_labels_tr_tensor,
            sample_weight_tr,
            model_dict,
            optim_dict,
            train_VCDN=False,
        )

    logger.info("Training...")
    # Initialize optimizers for actual training
    optim_dict = init_optim(num_view, model_dict, lr_e, lr_c)

    performance = {
        "training": [
            ("Epoch", "ACC", "F1_Weighted", "F1_Macro", "AUC", "Precision", "Loss")
        ],
        "testing": [
            ("Epoch", "ACC", "F1_Weighted", "F1_Macro", "AUC", "Precision", "Loss")
        ],
    }

    for epoch in range(num_epoch + 1):
        # Perform training for one epoch
        loss_dict = train_epoch(
            data_tr_list,
            adj_tr_list,
            labels_tr_tensor,
            onehot_labels_tr_tensor,
            sample_weight_tr,
            model_dict,
            optim_dict,
        )
        epoch_loss = sum(loss_dict.values())  # Sum losses from all views

        for method in ["training", "testing"]:
            # Calculate performance metrics
            prob = test_epoch(
                data_tr_list if method == "training" else data_trte_list,
                adj_tr_list if method == "training" else adj_te_list,
                trte_idx[method[:2]],
                model_dict,
            )  # Get probabilities for training data
            acc = accuracy_score(labels_trte[trte_idx[method[:2]]], prob.argmax(1))
            f1_weighted = f1_score(
                labels_trte[trte_idx[method[:2]]], prob.argmax(1), average="weighted"
            )
            f1_macro = f1_score(
                labels_trte[trte_idx[method[:2]]], prob.argmax(1), average="macro"
            )
            auc = (
                roc_auc_score(
                    labels_trte[trte_idx[method[:2]]], prob, multi_class="ovr"
                )
                if num_class > 2
                else roc_auc_score(labels_trte[trte_idx[method[:2]]], prob[:, 1])
            )
            precision = precision_score(
                labels_trte[trte_idx[method[:2]]],
                prob.argmax(1),
                average="macro",
                zero_division=0,
            )

            performance[method].append(
                (epoch, acc, f1_weighted, f1_macro, auc, precision, epoch_loss)
            )

            # Log testing metrics at arbitrary intervals (for debugging)
            if method == "testing" and epoch % 50 == 0:
                logger.debug(f"Epoch {epoch}")
                logger.debug(f"ACC: {acc:.3f}")
                logger.debug(f"F1 Weighted: {f1_weighted:.3f}")
                logger.debug(f"F1 Macro: {f1_macro:.3f}")
                logger.debug(f"AUC: {auc:.3f}")
                logger.debug(f"Precision: {precision:.3f}")

    return performance
