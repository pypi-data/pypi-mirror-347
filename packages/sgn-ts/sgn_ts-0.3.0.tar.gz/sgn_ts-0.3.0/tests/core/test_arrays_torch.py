"""Tests for array backends"""

import sys

import pytest
from unittest import mock

from sgnts.base.array_ops import TorchBackend

torch = pytest.importorskip("torch")

TorchBackend.DEVICE


class TestTorchBackendCPU:
    """Test group for TorchBackend class with CPU"""

    def test_check_torch_err(self):
        """Test the check_torch method of the GPUTorchBackend class"""
        # Patch the torch import to raise an ImportError
        original = sys.modules
        keys = ["torch", "sgnts"]
        clean = {k: v for k, v in original.items() if all(key not in k for key in keys)}
        clean.update({"torch": None})
        with mock.patch.dict("sys.modules", clear=True, values=clean):
            from sgnts.base.array_ops import TorchBackend

            assert TorchBackend.DEVICE is None
            assert TorchBackend.DTYPE is None

    def test_constants(self):
        """Test the constants of the CPUTorchBackend class"""
        assert TorchBackend.DEVICE == torch.device("cpu")
        assert TorchBackend.DTYPE == torch.float32

    def test_set_device(self):
        """Test the set device method of the TorchBackend class"""
        TorchBackend.set_device("cpu")
        assert TorchBackend.DEVICE == torch.device("cpu")

    def test_set_dtype(self):
        """Test the set dtype method of the TorchBackend class"""
        TorchBackend.set_dtype(torch.float32)
        assert TorchBackend.DTYPE == torch.float32

    def test_arange(self):
        """Test the arange method of the TorchBackend class"""
        res = TorchBackend.arange(10, start=1, step=2)
        assert torch.all(res == torch.arange(start=1, end=10, step=2))

    def test_cat(self):
        """Test the cat method of the TorchBackend class"""
        res = TorchBackend.cat(
            [
                torch.tensor([1, 2, 3]),
                torch.tensor([4, 5, 6]),
            ],
            axis=0,
        )
        assert torch.all(res == torch.tensor([1, 2, 3, 4, 5, 6]))

    def test_full(self):
        """Test the full method of the TorchBackend class"""
        res = TorchBackend.full(shape=(2, 3), fill_value=1)
        assert torch.all(res == (torch.ones((2, 3))))

    def test_matmul(self):
        """Test the matmul method of the TorchBackend class"""
        res = TorchBackend.matmul(torch.ones((3, 3)), torch.ones((3, 3)))
        assert torch.all(res == torch.ones((3, 3)) * 3)

    def test_ones(self):
        """Test the ones method of the TorchBackend class"""
        res = TorchBackend.ones(shape=(2, 3))
        assert torch.all(res == torch.ones((2, 3)))

    def test_pad(self):
        """Test the pad method of the TorchBackend class"""
        res = TorchBackend.pad(torch.tensor([1, 2, 3]), pad_samples=(1, 2))
        assert torch.all(res == torch.tensor([0, 1, 2, 3, 0, 0]))

    def test_stack(self):
        """Test the stack method of the TorchBackend class"""
        res = TorchBackend.stack(
            [
                torch.tensor([1, 2, 3]),
                torch.tensor([4, 5, 6]),
            ],
            axis=0,
        )
        assert torch.all(res == torch.tensor([[1, 2, 3], [4, 5, 6]]))

    def test_sum(self):
        """Test the sum method of the TorchBackend class"""
        res = TorchBackend.sum(torch.tensor([[1, 2, 3], [4, 5, 6]]), axis=0)
        assert torch.all(res == torch.tensor([5, 7, 9]))

    def test_zeros(self):
        """Test the zeros method of the TorchBackend class"""
        res = TorchBackend.zeros(shape=(2, 3))
        assert torch.all(res == torch.zeros((2, 3)))


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
class TestTorchBackendGPU:
    """Test group for TorchBackend class with GPU"""

    DEVICE = "cuda:0"
    DTYPE = torch.float16

    def test_set_device(self):
        """Test the set device method of the TorchBackend class"""
        TorchBackend.set_device(self.DEVICE)
        assert TorchBackend.DEVICE == self.DEVICE

    def test_set_dtype(self):
        """Test the set dtype method of the TorchBackend class"""
        TorchBackend.set_dtype(self.DTYPE)
        assert TorchBackend.DTYPE == self.DTYPE

    def test_arange(self):
        """Test the arange method of the TorchBackend class"""
        res = TorchBackend.arange(10, start=1, step=2)
        assert torch.all(
            res
            == torch.arange(
                start=1, end=10, step=2, device=self.DEVICE, dtype=self.DTYPE
            )
        )

    def test_cat(self):
        """Test the cat method of the TorchBackend class"""
        res = TorchBackend.cat(
            [
                torch.tensor([1, 2, 3], device=self.DEVICE, dtype=self.DTYPE),
                torch.tensor([4, 5, 6], device=self.DEVICE, dtype=self.DTYPE),
            ],
            axis=0,
        )
        assert torch.all(
            res
            == torch.tensor([1, 2, 3, 4, 5, 6], device=self.DEVICE, dtype=self.DTYPE)
        )

    def test_full(self):
        """Test the full method of the TorchBackend class"""
        res = TorchBackend.full(shape=(2, 3), fill_value=1)
        assert torch.all(
            res == (torch.ones((2, 3), device=self.DEVICE, dtype=self.DTYPE))
        )

    def test_matmul(self):
        """Test the matmul method of the TorchBackend class"""
        res = TorchBackend.matmul(
            torch.ones((3, 3), device=self.DEVICE, dtype=self.DTYPE),
            torch.ones((3, 3), device=self.DEVICE, dtype=self.DTYPE),
        )
        assert torch.all(
            res == torch.ones((3, 3), device=self.DEVICE, dtype=self.DTYPE) * 3
        )

    def test_ones(self):
        """Test the ones method of the TorchBackend class"""
        res = TorchBackend.ones(shape=(2, 3))
        assert torch.all(
            res == torch.ones((2, 3), device=self.DEVICE, dtype=self.DTYPE)
        )

    def test_pad(self):
        """Test the pad method of the TorchBackend class"""
        res = TorchBackend.pad(
            torch.tensor([1, 2, 3], device=self.DEVICE, dtype=self.DTYPE),
            pad_samples=(1, 2),
        )
        assert torch.all(
            res
            == torch.tensor([0, 1, 2, 3, 0, 0], device=self.DEVICE, dtype=self.DTYPE)
        )

    def test_stack(self):
        """Test the stack method of the TorchBackend class"""
        res = TorchBackend.stack(
            [
                torch.tensor([1, 2, 3], device=self.DEVICE, dtype=self.DTYPE),
                torch.tensor([4, 5, 6], device=self.DEVICE, dtype=self.DTYPE),
            ],
            axis=0,
        )
        assert torch.all(
            res
            == torch.tensor(
                [[1, 2, 3], [4, 5, 6]], device=self.DEVICE, dtype=self.DTYPE
            )
        )

    def test_sum(self):
        """Test the sum method of the TorchBackend class"""
        res = TorchBackend.sum(
            torch.tensor([[1, 2, 3], [4, 5, 6]], device=self.DEVICE, dtype=self.DTYPE),
            axis=0,
        )
        assert torch.all(
            res == torch.tensor([5, 7, 9], device=self.DEVICE, dtype=self.DTYPE)
        )

    def test_zeros(self):
        """Test the zeros method of the TorchBackend class"""
        res = TorchBackend.zeros(shape=(2, 3))
        assert torch.all(
            res == torch.zeros((2, 3), device=self.DEVICE, dtype=self.DTYPE)
        )
