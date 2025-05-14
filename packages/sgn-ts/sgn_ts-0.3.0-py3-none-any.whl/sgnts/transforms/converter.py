from dataclasses import dataclass
from functools import wraps

import numpy as np

from sgnts.base import SeriesBuffer, TSFrame, TSTransform

# Try to import torch, but don't fail if it's not available
try:
    import torch

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


@dataclass
class Converter(TSTransform):
    """Change the data type or the device of the data.

    Args:
        backend:
            str, the backend to convert the data to. Supported backends:
            ['numpy'|'torch']
        dtype:
            str, the data type to convert the data to. Supported dtypes:
            ['float32'|'float16']
        device:
            str, the device to convert the data to. Suppored devices:
            if backend = 'numpy', only supports device = 'cpu', if backend = 'torch',
            supports device = ['cpu'|'cuda'|'cuda:<GPU number>'] where <GPU number> is
            the GPU device number.
    """

    backend: str = "numpy"
    dtype: str = "float32"
    device: str = "cpu"

    def __post_init__(self):
        assert set(self.source_pad_names) == set(self.sink_pad_names)
        super().__post_init__()

        if self.backend == "numpy":
            if self.device != "cpu":
                raise ValueError("Converting to numpy only supports device as cpu")
        elif self.backend == "torch":
            if not TORCH_AVAILABLE:
                raise ImportError(
                    "PyTorch is not installed. Install it with 'pip install "
                    "sgn-ts[torch]'"
                )

            if isinstance(self.dtype, str):
                if self.dtype == "float64":
                    self.dtype = torch.float64
                elif self.dtype == "float32":
                    self.dtype = torch.float32
                elif self.dtype == "float16":
                    self.dtype = torch.float16
                else:
                    raise ValueError(
                        "Supported torch data types: float64, float32, float16"
                    )
            elif isinstance(self.dtype, torch.dtype):
                pass
            else:
                raise ValueError("Unknown dtype")
        else:
            raise ValueError("Supported backends: 'numpy' or 'torch'")

        self.pad_map = {
            p: self.sink_pad_dict["%s:snk:%s" % (self.name, p.name.split(":")[-1])]
            for p in self.source_pads
        }

    @wraps(TSTransform.new)
    def new(self, pad):
        frame = self.preparedframes[self.pad_map[pad]]
        self.preparedframes[self.pad_map[pad]] = None

        outbufs = []
        for buf in frame:
            if buf.is_gap:
                out = None
            else:
                data = buf.data
                if self.backend == "numpy":
                    if isinstance(data, np.ndarray):
                        # numpy to numpy
                        out = data.astype(self.dtype, copy=False)
                    elif isinstance(data, torch.Tensor):
                        # torch to numpy
                        out = data.detach().cpu().numpy().astype(self.dtype, copy=False)
                    else:
                        raise ValueError("Unsupported data type")
                else:
                    if not TORCH_AVAILABLE:
                        raise ImportError(
                            "PyTorch is not installed. Install it with 'pip "
                            "install sgn-ts[torch]'"
                        )

                    if isinstance(data, np.ndarray):
                        # numpy to torch
                        out = torch.from_numpy(data).to(self.dtype).to(self.device)
                    elif hasattr(torch, "Tensor") and isinstance(data, torch.Tensor):
                        # torch to torch
                        out = data.to(self.dtype).to(self.device)
                    else:
                        raise ValueError("Unsupported data type")

            outbufs.append(
                SeriesBuffer(
                    offset=buf.offset,
                    sample_rate=buf.sample_rate,
                    data=out,
                    shape=buf.shape,
                )
            )

        return TSFrame(
            buffers=outbufs,
            metadata=frame.metadata,
            EOS=frame.EOS,
        )
