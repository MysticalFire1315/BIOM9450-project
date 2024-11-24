# 模型组件

import torch.nn as nn
import torch
import torch.nn.functional as F

# Xavier初始化方法，用于给定的线性层参数初始化权重
def xavier_init(m):
    # 判断是否为线性层，如果是则应用Xavier初始化
    if type(m) == nn.Linear:
        nn.init.xavier_normal_(m.weight)  # 使用Xavier正态分布初始化权重
        if m.bias is not None:
            m.bias.data.fill_(0.0)  # 将偏置设置为0

# 图卷积层定义
class GraphConvolution(nn.Module):
    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        # 定义权重参数
        self.weight = nn.Parameter(torch.FloatTensor(in_features, out_features))
        # 若启用偏置，则定义偏置参数
        if bias:
            self.bias = nn.Parameter(torch.FloatTensor(out_features))
        # 对权重应用Xavier初始化
        nn.init.xavier_normal_(self.weight.data)
        # 将偏置初始化为0
        if self.bias is not None:
            self.bias.data.fill_(0.0)

    # 前向传播计算
    def forward(self, x, adj):
        # 计算输入与权重的乘积
        support = torch.mm(x, self.weight)
        # 使用稀疏矩阵乘法与邻接矩阵相乘，得到图卷积输出
        output = torch.sparse.mm(adj, support)
        # 若存在偏置，则将偏置加到输出上
        if self.bias is not None:
            return output + self.bias
        else:
            return output

# 基于图卷积网络（GCN）的编码器模块
class GCN_E(nn.Module):
    def __init__(self, in_dim, hgcn_dim, dropout):
        super().__init__()
        # 定义三层图卷积层
        self.gc1 = GraphConvolution(in_dim, hgcn_dim[0])
        self.gc2 = GraphConvolution(hgcn_dim[0], hgcn_dim[1])
        self.gc3 = GraphConvolution(hgcn_dim[1], hgcn_dim[2])
        # 定义dropout概率
        self.dropout = dropout

    def forward(self, x, adj):
        # 第一层卷积，并应用LeakyReLU激活和dropout
        x = self.gc1(x, adj)
        x = F.leaky_relu(x, 0.25)
        x = F.dropout(x, self.dropout, training=self.training)
        # 第二层卷积，并应用LeakyReLU激活和dropout
        x = self.gc2(x, adj)
        x = F.leaky_relu(x, 0.25)
        x = F.dropout(x, self.dropout, training=self.training)
        # 第三层卷积，并应用LeakyReLU激活
        x = self.gc3(x, adj)
        x = F.leaky_relu(x, 0.25)
        
        return x

# 基于线性层的分类器模块
class Classifier_1(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        # 定义线性层并应用Xavier初始化
        self.clf = nn.Sequential(nn.Linear(in_dim, out_dim))
        self.clf.apply(xavier_init)

    def forward(self, x):
        # 计算分类输出
        x = self.clf(x)
        return x

# VCDN模块（用于多视角数据的多类分类）
class VCDN(nn.Module):
    def __init__(self, num_view, num_cls, hvcdn_dim):
        super().__init__()
        self.num_cls = num_cls
        # 定义两层网络：第一层为线性层+LeakyReLU，第二层为线性层
        self.model = nn.Sequential(
            nn.Linear(pow(num_cls, num_view), hvcdn_dim),
            nn.LeakyReLU(0.25),
            nn.Linear(hvcdn_dim, num_cls)
        )
        self.model.apply(xavier_init)
        
    def forward(self, in_list):
        # 多视角数据的输入处理，将每个视角数据应用Sigmoid函数
        num_view = len(in_list)
        for i in range(num_view):
            in_list[i] = torch.sigmoid(in_list[i])
        # 逐层组合各视角特征，并通过VCDN模型进行分类
        x = torch.reshape(torch.matmul(in_list[0].unsqueeze(-1), in_list[1].unsqueeze(1)), (-1, pow(self.num_cls, 2), 1))
        for i in range(2, num_view):
            x = torch.reshape(torch.matmul(x, in_list[i].unsqueeze(1)), (-1, pow(self.num_cls, i + 1), 1))
        # 展平特征，准备进行分类
        vcdn_feat = torch.reshape(x, (-1, pow(self.num_cls, num_view)))
        output = self.model(vcdn_feat)

        return output

# 初始化模型字典函数
def init_model_dict(num_view, num_class, dim_list, dim_he_list, dim_hc, gcn_dopout=0.5):
    model_dict = {}
    # 根据视角数量初始化编码器与分类器模型
    for i in range(num_view):
        model_dict["E{:}".format(i + 1)] = GCN_E(dim_list[i], dim_he_list, gcn_dopout)
        model_dict["C{:}".format(i + 1)] = Classifier_1(dim_he_list[-1], num_class)
    # 若有2个或以上视角，初始化VCDN分类器
    if num_view >= 2:
        model_dict["C"] = VCDN(num_view, num_class, dim_hc)
    return model_dict

# 初始化优化器字典函数
def init_optim(num_view, model_dict, lr_e=1e-4, lr_c=1e-4):
    optim_dict = {}
    # 为每个视角的编码器与分类器创建优化器
    for i in range(num_view):
        optim_dict["C{:}".format(i + 1)] = torch.optim.Adam(
                list(model_dict["E{:}".format(i + 1)].parameters()) + list(model_dict["C{:}".format(i + 1)].parameters()), 
                lr=lr_e)
    # 若有2个或以上视角，为VCDN分类器创建优化器
    if num_view >= 2:
        optim_dict["C"] = torch.optim.Adam(model_dict["C"].parameters(), lr=lr_c)
    return optim_dict
