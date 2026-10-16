from numba import cuda


# ---------- Task 1: сложение векторов ----------
@cuda.jit
def vector_add_1d(a, b, out):
    i = cuda.grid(1)
    # проверка границ, иначе вылетим за массив
    if i < out.shape[0]:
        out[i] = a[i] + b[i]


# ---------- Task 2: grid-stride loop ----------
@cuda.jit
def vector_scale_grid_stride(x, alpha, out):
    start = cuda.grid(1)
    stride = cuda.gridDim.x * cuda.blockDim.x  # всего потоков в сетке
    n = x.shape[0]
    # каждый поток берет элементы с шагом stride
    for i in range(start, n, stride):
        out[i] = x[i] * alpha


# ---------- Task 3: сложение матриц 2D ----------
@cuda.jit
def matrix_add_2d(A, B, C):
    row = cuda.blockIdx.y * cuda.blockDim.y + cuda.threadIdx.y
    col = cuda.blockIdx.x * cuda.blockDim.x + cuda.threadIdx.x
    if row < A.shape[0] and col < A.shape[1]:
        C[row, col] = A[row, col] + B[row, col]


# ---------- Task 4: наивный transpose ----------
@cuda.jit
def matrix_transpose_naive(A, B):
    col, row = cuda.grid(2)  # grid(2) отдает (x, y), не (row, col)!
    M, N = A.shape
    if row < M and col < N:
        B[col, row] = A[row, col]  # запись со страйдом, для этого задания норм


# ---------- Task 5: 3D volume ----------
@cuda.jit
def volume_init_3d(vol, D, H, W):
    x, y, z = cuda.grid(3)
    if z < D and y < H and x < W:
        vol[z, y, x] = z * 10000 + y * 100 + x


# ---------- Task 6: RGB -> grayscale ----------
@cuda.jit
def rgb_to_grayscale(img_rgb, img_gray):
    x, y = cuda.grid(2)
    H, W = img_gray.shape
    if y < H and x < W:
        r = img_rgb[y, x, 0]
        g = img_rgb[y, x, 1]
        b = img_rgb[y, x, 2]
        img_gray[y, x] = 0.299 * r + 0.587 * g + 0.114 * b


# ---------- Task 7: LERP ----------
@cuda.jit
def vector_lerp(a, b, t, out):
    i = cuda.grid(1)
    if i < out.shape[0]:
        ti = t[i]
        # (1 - t)*a + t*b через fma
        out[i] = cuda.fma(ti, b[i], (1.0 - ti) * a[i])
