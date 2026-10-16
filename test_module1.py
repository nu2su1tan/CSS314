# МОИ СОБСТВЕННЫЕ тесты для заданий 1-7 (не официальные от препода!)
# Если у тебя есть официальный tests/test_module1.py - используй его, а этот не копируй.
import numpy as np
import pytest
from numba import cuda

from lab_kernels import module1_execution_model as m1

pytestmark = pytest.mark.skipif(not cuda.is_available(), reason="нет GPU")


@pytest.mark.parametrize("N", [1, 255, 256, 1024, 1000003])
def test_task1(N):
    a = np.random.rand(N).astype(np.float32)
    b = np.random.rand(N).astype(np.float32)
    d_out = cuda.device_array(N, dtype=np.float32)
    m1.vector_add_1d[(N + 255) // 256, 256](cuda.to_device(a), cuda.to_device(b), d_out)
    np.testing.assert_allclose(d_out.copy_to_host(), a + b, atol=1e-5)


def test_task2():
    N = 10_000_000
    x = np.random.rand(N).astype(np.float32)
    d_out = cuda.device_array(N, dtype=np.float32)
    m1.vector_scale_grid_stride[64, 256](cuda.to_device(x), np.float32(2.5), d_out)
    np.testing.assert_allclose(d_out.copy_to_host(), x * 2.5, atol=1e-5)


def test_task3():
    M, N = 513, 1021
    A = np.random.rand(M, N).astype(np.float32)
    B = np.random.rand(M, N).astype(np.float32)
    d_C = cuda.device_array((M, N), dtype=np.float32)
    grid = ((N + 15) // 16, (M + 15) // 16)
    m1.matrix_add_2d[grid, (16, 16)](cuda.to_device(A), cuda.to_device(B), d_C)
    np.testing.assert_allclose(d_C.copy_to_host(), A + B, atol=1e-5)


def test_task4():
    M, N = 300, 517
    A = np.random.rand(M, N).astype(np.float32)
    d_B = cuda.device_array((N, M), dtype=np.float32)
    grid = ((N + 15) // 16, (M + 15) // 16)
    m1.matrix_transpose_naive[grid, (16, 16)](cuda.to_device(A), d_B)
    np.testing.assert_allclose(d_B.copy_to_host(), A.T, atol=1e-5)


def test_task5():
    D, H, W = 33, 47, 65
    d_vol = cuda.device_array((D, H, W), dtype=np.int32)
    grid = ((W + 7) // 8, (H + 7) // 8, (D + 7) // 8)
    m1.volume_init_3d[grid, (8, 8, 8)](d_vol, D, H, W)
    z, y, x = np.meshgrid(np.arange(D), np.arange(H), np.arange(W), indexing="ij")
    np.testing.assert_equal(d_vol.copy_to_host(), (z * 10000 + y * 100 + x).astype(np.int32))


def test_task6():
    H, W = 480, 640
    img = np.random.rand(H, W, 3).astype(np.float32)
    d_gray = cuda.device_array((H, W), dtype=np.float32)
    grid = ((W + 15) // 16, (H + 15) // 16)
    m1.rgb_to_grayscale[grid, (16, 16)](cuda.to_device(img), d_gray)
    ref = 0.299 * img[..., 0] + 0.587 * img[..., 1] + 0.114 * img[..., 2]
    np.testing.assert_allclose(d_gray.copy_to_host(), ref, atol=1e-4)


def test_task7():
    N = 100000
    a, b, t = (np.random.rand(N).astype(np.float32) for _ in range(3))
    d_out = cuda.device_array(N, dtype=np.float32)
    m1.vector_lerp[(N + 255) // 256, 256](
        cuda.to_device(a), cuda.to_device(b), cuda.to_device(t), d_out)
    np.testing.assert_allclose(d_out.copy_to_host(), (1 - t) * a + t * b, atol=1e-5)
