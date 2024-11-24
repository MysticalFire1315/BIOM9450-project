# utils.py
import os
import numpy as np
import torch
import torch.nn.functional as F

# Check if CUDA (GPU) is available for computations
cuda = torch.cuda.is_available()

# Calculate sample weights to balance classes in the dataset
def cal_sample_weight(labels, num_class, use_sample_weight=True):
    # If sample weighting is disabled, assign equal weights to all samples
    if not use_sample_weight:
        return np.ones(len(labels)) / len(labels)

    # Initialize a counter for each class
    count = np.zeros(num_class)
    for i in range(num_class):
        count[i] = np.sum(labels == i)  # Count the number of samples for each class

    # Assign weights inversely proportional to class frequency
    sample_weight = np.zeros(labels.shape)
    for i in range(num_class):
        sample_weight[np.where(labels == i)[0]] = count[i] / np.sum(count)

    return sample_weight

# Convert class labels into one-hot encoded tensors
def one_hot_tensor(y, num_dim):
    # Initialize a tensor with zeros of shape (num_samples, num_classes)
    y_onehot = torch.zeros(y.shape[0], num_dim)
    # Set 1 in the position corresponding to the class label
    y_onehot.scatter_(1, y.view(-1, 1), 1)
    return y_onehot

# Compute pairwise cosine distance between two tensors
def cosine_distance_torch(x1, x2=None, eps=1e-8):
    # If the second tensor is not provided, use the first tensor for both
    x2 = x1 if x2 is None else x2
    # Compute the L2 norm (Euclidean norm) for each vector
    w1 = x1.norm(p=2, dim=1, keepdim=True)
    w2 = w1 if x2 is x1 else x2.norm(p=2, dim=1, keepdim=True)
    # Compute cosine similarity and return 1 - similarity (cosine distance)
    return 1 - torch.mm(x1, x2.t()) / (w1 * w2.t()).clamp(min=eps)

# Convert a dense tensor to a sparse tensor
def to_sparse(x):
    # Determine the type of the input tensor
    x_typename = torch.typename(x).split('.')[-1]
    sparse_tensortype = getattr(torch.sparse, x_typename)
    # Identify non-zero elements in the tensor
    indices = torch.nonzero(x)
    if len(indices.shape) == 0:
        return sparse_tensortype(*x.shape)
    indices = indices.t()  # Transpose the indices
    # Extract the values of the non-zero elements
    values = x[tuple(indices[i] for i in range(indices.shape[0]))]
    # Create a sparse tensor using the indices and values
    sparse_tensor = torch.sparse_coo_tensor(indices, values, x.size())
    if x.is_cuda:
        sparse_tensor = sparse_tensor.to(x.device)  # Move to the same device as input
    sparse_tensor = sparse_tensor.to(x.dtype)  # Match the data type
    return sparse_tensor

# Calculate a parameter for adjacency matrix construction based on edge density
def cal_adj_mat_parameter(edge_per_node, data, metric="cosine"):
    # Compute pairwise distances between all samples
    dist = cosine_distance_torch(data, data)
    # Select a threshold parameter corresponding to the desired edge density
    parameter = torch.sort(dist.view(-1)).values[edge_per_node * data.shape[0]]
    return parameter.cpu().item()  # Return the parameter as a CPU scalar

# Construct a binary adjacency graph from pairwise distance tensor
def graph_from_dist_tensor(dist, parameter, self_dist=True):
    # Check if the input is a square distance matrix
    if self_dist:
        assert dist.shape[0] == dist.shape[1], "Input is not pairwise dist matrix"
    # Create binary connections based on the distance threshold
    g = (dist <= parameter).float()
    if self_dist:
        # Remove self-loops by zeroing the diagonal
        diag_idx = np.diag_indices(g.shape[0])
        g[diag_idx[0], diag_idx[1]] = 0
    return g

# Generate a sparse adjacency matrix for graph construction
def gen_adj_mat_tensor(data, parameter, metric="cosine"):
    # Compute pairwise distances between samples
    dist = cosine_distance_torch(data, data)
    # Create a binary adjacency graph based on the distance threshold
    g = graph_from_dist_tensor(dist, parameter, self_dist=True)
    # Weight the edges using (1 - distance)
    adj = (1 - dist) * g
    # Ensure symmetry by adding transposed edges
    adj_T = adj.transpose(0, 1)
    I = torch.eye(adj.shape[0])  # Identity matrix
    if cuda:
        I = I.cuda()
    adj = adj + adj_T * (adj_T > adj).float() - adj * (adj_T > adj).float()
    # Normalize the adjacency matrix and convert to sparse format
    adj = F.normalize(adj + I, p=1)
    return to_sparse(adj)

# Generate a sparse adjacency matrix for test data (train-to-test connections)
def gen_test_adj_mat_tensor(data, trte_idx, parameter, metric="cosine"):
    # Initialize an adjacency matrix for the full dataset
    adj = torch.zeros((data.shape[0], data.shape[0])).cuda() if cuda else torch.zeros((data.shape[0], data.shape[0]))
    num_tr = len(trte_idx["tr"])  # Number of training samples
    # Compute train-to-test distances
    dist_tr2te = cosine_distance_torch(data[trte_idx["tr"]], data[trte_idx["te"]])
    g_tr2te = graph_from_dist_tensor(dist_tr2te, parameter, self_dist=False)
    adj[:num_tr, num_tr:] = (1 - dist_tr2te) * g_tr2te

    # Compute test-to-train distances
    dist_te2tr = cosine_distance_torch(data[trte_idx["te"]], data[trte_idx["tr"]])
    g_te2tr = graph_from_dist_tensor(dist_te2tr, parameter, self_dist=False)
    adj[num_tr:, :num_tr] = (1 - dist_te2tr) * g_te2tr

    # Ensure symmetry in the adjacency matrix
    adj_T = adj.transpose(0, 1)
    I = torch.eye(adj.shape[0])  # Identity matrix
    if cuda:
        I = I.cuda()
    adj = adj + adj_T * (adj_T > adj).float() - adj * (adj_T > adj).float()
    # Normalize and convert to sparse format
    adj = F.normalize(adj + I, p=1)
    return to_sparse(adj)

# Save model parameters to files in the specified folder
def save_model_dict(folder, model_dict):
    if not os.path.exists(folder):  # Create the folder if it doesn't exist
        os.makedirs(folder)
    for module in model_dict:
        # Save each model's parameters to a file
        torch.save(model_dict[module].state_dict(), os.path.join(folder, module + ".pth"))

# Load model parameters from files into the provided model dictionary
def load_model_dict(folder, model_dict):
    for module in model_dict:
        # Construct the file path for the module's parameters
        path = os.path.join(folder, "models", "1", f"{module}.pth")
        if os.path.exists(path):
            # Load parameters into the model
            model_dict[module].load_state_dict(torch.load(path, map_location="cuda" if cuda else "cpu"))
        else:
            print(f"WARNING: {module} not loaded, file missing.")  # Warn if file is missing
    return model_dict
