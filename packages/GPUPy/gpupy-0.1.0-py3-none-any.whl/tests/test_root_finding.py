#test_root_finding.py
# test_root_finding.py
import pytest
import numpy as np
from src.root_finding import bisection, newton_raphson

# CPU test için örnek fonksiyonlar
def func(x):
    return x**2 - 4

def dfunc(x):
    return 2*x

# Bisection - doğru sonuç testi
def test_bisection_root_cpu():
    root = bisection(func, 0, 3, tolerance=1e-6, use_gpu=False)
    assert abs(root - 2.0) < 1e-6

# Bisection - geçersiz aralık testi
def test_bisection_invalid_interval():
    with pytest.raises(ValueError):
        bisection(func, 2, 3, use_gpu=False)  # f(2) and f(3) both > 0

# Newton-Raphson - doğru sonuç testi
def test_newton_raphson_root_cpu():
    root = newton_raphson(func, dfunc, 3.0, tol=1e-6, use_gpu=False)
    assert abs(root - 2.0) < 1e-6

# Newton-Raphson - sıfır türev hatası testi
def test_newton_raphson_zero_derivative():
    def f(x): return x**3
    def df(x): return 0*x  # türev sıfır olacak şekilde
    
    with pytest.raises(ValueError):
        newton_raphson(f, df, 1.0, use_gpu=False)

# Newton-Raphson - maksimum iterasyon hatası testi
def test_newton_raphson_no_convergence():
    def f(x): return np.cos(x) - x
    def df(x): return -np.sin(x) - 1

    with pytest.raises(ValueError):
        newton_raphson(f, df, 10.0, max_iter=5, tol=1e-12, use_gpu=False)

# GPU uyumlu örnek fonksiyonlar
def gpu_func(x):
    return x**2 - 4

def gpu_dfunc(x):
    return 2*x

# GPU Bisection - doğru sonuç testi
def test_bisection_root_gpu():
    root = bisection(gpu_func, 0, 3, tolerance=1e-6, use_gpu=True)
    assert abs(root - 2.0) < 1e-6

# GPU Bisection - geçersiz aralık testi
def test_bisection_invalid_interval_gpu():
    with pytest.raises(ValueError):
        bisection(gpu_func, 2, 3, use_gpu=True)  # f(2) and f(3) > 0

# GPU Newton-Raphson - doğru sonuç testi
def test_newton_raphson_root_gpu():
    root = newton_raphson(gpu_func, gpu_dfunc, 3.0, tol=1e-6, use_gpu=True)
    assert abs(root - 2.0) < 1e-6

# GPU Newton-Raphson - türev sıfır hatası testi
def test_newton_raphson_zero_derivative_gpu():
    def f(x): return x**3
    def df(x): return cp.zeros_like(x)  # GPU üzerinde sıfır türev
    
    with pytest.raises(ValueError):
        newton_raphson(f, df, 1.0, use_gpu=True)

# GPU Newton-Raphson - maksimum iterasyon hatası testi
def test_newton_raphson_no_convergence_gpu():
    def f(x): return cp.cos(x) - x
    def df(x): return -cp.sin(x) - 1
    
    with pytest.raises(ValueError):
        newton_raphson(f, df, 10.0, max_iter=5, tol=1e-12, use_gpu=True)