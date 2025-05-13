import torch
import torch.nn.functional as F
from pytorch_msssim import ssim  # Make sure to install `pytorch-msssim`

class LossFunctions:
    def __init__(self):
        pass

    def make_bandpass_weights(self, H, boost_range=(25, 450), boost_factor=1, base_weight=0.1):
        weights = torch.full((H,), base_weight)
        start, end = boost_range
        weights[start:end] = boost_factor
        return weights.view(1, 1, H, 1)

    def logCoshLoss(self, y_hat, y, use_freq_weights=False):
        B, C, H, W = y.shape
        device = y.device

        diff = y_hat - y
        log_cosh = torch.log(torch.cosh(diff + 1e-12))

        if use_freq_weights:
            freq_weights = self.make_bandpass_weights(H).to(device)
            log_cosh = log_cosh * freq_weights

        return log_cosh.mean()

    def PIPEXLoss(self, y_hat, y, rho, iota):
        return rho * self.logCoshLoss(y_hat, y, use_freq_weights=True) + \
               iota * (1.0 - ssim(y_hat, y, data_range=1.0, size_average=True))
