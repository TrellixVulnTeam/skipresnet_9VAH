import collections
from typing import Callable

import torch.nn as nn
from timm.models.layers import ScaledStdConv2dSame

from ..modules import Multiply


class NFHead(nn.Sequential):
    '''
    Head class for Normalizer-Free ResNets (NFNets).
    https://arxiv.org/abs/2102.06171
    '''

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        activation: Callable[..., nn.Module],
        gamma: float,
        **kwargs,
    ) -> None:
        super().__init__(collections.OrderedDict((n, m) for n, m in [
            ('conv', ScaledStdConv2dSame(
                in_channels, out_channels, kernel_size=1,
                padding='same', stride=1, eps=1e-5)),
            ('act', activation(inplace=True)),
            ('gamma', Multiply(gamma, inplace=True)),
        ] if m is not None))
