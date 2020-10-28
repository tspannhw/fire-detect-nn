# Aerial Fire Dataset +

import torch
import torchvision
import torchvision.transforms as transforms
import numpy as np


class ConcatDataset(torch.utils.data.Dataset):
    def __init__(self, *datasets):
        self.datasets = datasets

    def __getitem__(self, i):
        return tuple(d[i] for d in self.datasets)

    def __len__(self):
        return min(len(d) for d in self.datasets)

def make_combo_train_loaders(
    directory="~/fire_aerial2k_dataset/",
    val_frac=0.1,
    batch_size=16,
    random_seed=4822,
    shuffle=True,
):

    transform = torchvision.transforms.Compose(
        [
            torchvision.transforms.Resize((224, 224)),
            torchvision.transforms.Normalize(
                mean=(0.4005, 0.3702, 0.3419), std=(0.2858, 0.2749, 0.2742)
            ),
            torchvision.transforms.ToTensor(),
        ]
    )

    entire_dataset = torchvision.datasets.ImageFolder(root=directory, transform=tr)

    n_all = len(entire_dataset)
    n_valid = int(np.floor(val_frac * n_all))
    indices = list(range(n_all))

    np.random.seed(random_seed)

    if shuffle:
        np.random.shuffle(indices)

    train_idxs_list, test_idxs_list = indices[n_valid:], indices[:n_valid]

    train_loader = torch.utils.data.DataLoader(
        entire_dataset,
        batch_size=batch_size,
        num_workers=4,
        shuffle=False,
        sampler=torch.utils.data.sampler.SubsetRandomSampler(train_idxs_list),
    )

    test_loader = torch.utils.data.DataLoader(
        entire_dataset,
        batch_size=batch_size,
        num_workers=4,
        shuffle=False,
        sampler=torch.utils.data.sampler.SubsetRandomSampler(test_idxs_list),
    )

    return train_loader, test_loader
