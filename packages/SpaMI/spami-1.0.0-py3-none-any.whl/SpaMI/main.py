import os.path
import torch
import numpy as np
from tqdm import tqdm
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
from .model import SpaMI
from .utils import fix_seed
from .preprocess import permutation


def train(omics1_data, omics2_data, result_path, out_dim=64, use_device="cpu", 
          learning_rate=0.001, epochs=1000, dropout_rate=0.15, weight_decay=0.0, random_seed=2024, 
          omics1_factor=[1, 10], omics2_factor=[1, 10], cosine_factor=5):
    
    fix_seed(random_seed)
    
    if torch.cuda.is_available():
        device = torch.device(use_device)
    else:
        device = torch.device("cpu")
        
    factors = [omics1_factor[0], omics2_factor[0], omics1_factor[1], omics2_factor[1], cosine_factor]

    # omics1 data
    omics1_feat = torch.FloatTensor(omics1_data['feat']).to(device)
    omics1_feat_shuffle = None
    omics1_label_CSL = torch.FloatTensor(omics1_data['label_CSL']).to(device)
    omics1_graph_neigh = torch.FloatTensor(omics1_data['graph_neigh'] + np.eye(omics1_data['adj'].shape[0])).to(device)
    omics1_input_dim = omics1_data['feat'].shape[1]
    omics1_adj = torch.FloatTensor(omics1_data['adj'] + np.eye(omics1_data['adj'].shape[0])).to(device)

    # omics2 data
    omics2_feat = torch.FloatTensor(omics2_data['feat']).to(device)
    omics2_feat_shuffle = None
    omics2_label_CSL = torch.FloatTensor(omics2_data['label_CSL']).to(device)
    omics2_graph_neigh = torch.FloatTensor(omics2_data['graph_neigh'] + np.eye(omics2_data['adj'].shape[0])).to(device)
    omics2_input_dim = omics2_data['feat'].shape[1]
    omics2_adj = torch.FloatTensor(omics2_data['adj'] + np.eye(omics2_data['adj'].shape[0])).to(device)


    # model
    model = SpaMI(omics1_input_dim, omics2_input_dim, out_dim, dropout_rate,
                  omics1_feat, omics1_adj, omics1_graph_neigh, omics1_label_CSL,
                  omics2_feat, omics2_adj, omics2_graph_neigh, omics2_label_CSL)
    model = model.to(device)

    # optimizer
    optimizer = torch.optim.Adam(model.parameters(), learning_rate, weight_decay=weight_decay)

    model.train()

    loss_rec = nn.MSELoss()
    loss_CSL = nn.BCEWithLogitsLoss()

    train_losses = []

    # train
    for epoch in tqdm(range(epochs)):
        model.train()

        omics1_feat_shuffle = permutation(omics1_feat)
        omics2_feat_shuffle = permutation(omics2_feat)

        (omics1_emb, omics1_rec, omics1_ret, omics1_ret_a,
         omics2_emb, omics2_rec, omics2_ret, omics2_ret_a,
         combine_emb, omics_weight) = model(omics1_feat_shuffle, omics2_feat_shuffle)

        # contrastive learning loss
        loss_omics1_csl1 = loss_CSL(omics1_ret, omics1_label_CSL)
        loss_omics1_csl2 = loss_CSL(omics1_ret_a, omics1_label_CSL)
        loss_omics1_CSL = loss_omics1_csl1 + loss_omics1_csl2

        loss_omics2_csl1 = loss_CSL(omics2_ret, omics2_label_CSL)
        loss_omics2_csl2 = loss_CSL(omics2_ret_a, omics2_label_CSL)
        loss_omics2_CSL = loss_omics2_csl1 + loss_omics2_csl2

        # reconstruction loss
        loss_omics1_rec = loss_rec(omics1_feat, omics1_rec)
        loss_omics2_rec = loss_rec(omics2_feat, omics2_rec)

        # cosine similarity loss
        cosine_sim = F.cosine_similarity(omics1_emb, omics2_emb, dim=1)
        loss_cosine = 1 - cosine_sim.mean()

        loss = (factors[0] * loss_omics1_CSL + factors[1] * loss_omics2_CSL +
                factors[2] * loss_omics1_rec + factors[3] * loss_omics2_rec + factors[4] * loss_cosine)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train_losses.append(loss.item())

    print('Model training completed!')
    
    with torch.no_grad():
        model.eval()
        omics1_emb, omics1_rec, _, _, omics2_emb, omics2_rec, _, _, combine_emb, _ = model(omics1_feat_shuffle, omics2_feat_shuffle)

        rec_omics1 = omics1_rec.clone().detach().cpu().numpy()
        rec_omics2 = omics2_rec.clone().detach().cpu().numpy()
        emb_omics1 = omics1_emb.clone().detach().cpu().numpy()
        emb_omics2 = omics2_emb.clone().detach().cpu().numpy()
        emb_combine = combine_emb.clone().detach().cpu().numpy()
        
        embedding_path = os.path.join(result_path, "embedding.npy")
        np.save(embedding_path, emb_combine)
    print(f'Result embedding has been saved in the {embedding_path} file')
    
    return emb_combine
