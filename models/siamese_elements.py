import torch
import torch.nn as nn
import torch.nn.functional as F


class SingleSiameseCNN(nn.Module):
    def __init__(self, embedding_layer, max_len, output_size, linear_size=128, windows=[3, 4, 5]):
        super(SingleSiameseCNN, self).__init__()
        self.embedding = embedding_layer
        self.cnn_filters = [
            nn.Sequential(
                nn.Conv1d(max_len, linear_size, kernel_wide),
                nn.ReLU()
            ) for kernel_wide in windows]
        self.dense = nn.Sequential(
            nn.Linear(linear_size*len(windows), output_size),
            nn.Sigmoid()
        )

    def forward(self, sentence):
        sent_embed = self.embedding(sentence)
        output_of_cnns = [
            cnn_filter(sent_embed)
            for cnn_filter in self.cnn_filters]
        global_pooled_output = list(map(
            lambda x: torch.max(x, dim=2)[0], output_of_cnns))
        dense_input = torch.cat(global_pooled_output, dim=1)
        output = self.dense(dense_input)
        return output