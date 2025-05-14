from typing import NamedTuple

import numpy as np
import sklearn.decomposition as skd

from scipy.sparse import issparse
from scipy.sparse.linalg import svds


class MCA(NamedTuple):
	embedding: np.ndarray
	coord_system: np.ndarray
	stdev: np.ndarray


def fit_mca(Y, n, center=True):
	"""
	计算给定数据矩阵 Y 的 MCA（多重对应分析）。
	Y : array-like, shape (n_samples, n_features)
		输入数据矩阵。
	n : int 成分数量。
	-------
	mca :MCA 使用 MCA 命名元组存储的 MCA 结果。
	"""
	
	# 计算行和列的总和
	row_sums = Y.sum(axis=1, keepdims=True)
	col_sums = Y.sum(axis=0, keepdims=True)
	grand_sum = Y.sum()
	
	# 计算观测频率/概率矩阵
	observed = Y / grand_sum
	
	# 检查总和以避免除零错误
	if grand_sum == 0:
		raise ValueError("总体总和为零，无法进行 MCA 分析")
	
	# 计算期望频率/概率矩阵
	row_freq = row_sums / grand_sum
	col_freq = col_sums / grand_sum
	expected = np.outer(row_freq, col_freq)
	
	# 计算过度矩阵 S，即标准化残差矩阵
	with np.errstate(divide='ignore', invalid='ignore'):
		Z = np.where(
				expected != 0, (observed - expected) / np.sqrt(expected), 0
		)
	
	# 使用 TruncatedSVD 进行分解
	svd = skd.TruncatedSVD(n_components=n, algorithm='arpack')  # 或 algorithm='randomized'
	U = svd.fit_transform(Z)
	Sigma = svd.singular_values_
	Vt = svd.components_  # TruncatedSVD 返回 V^T，所以需要转置
	
	# 计算细胞坐标和基因坐标
	cell_coords = U
	# 置基点为 V
	# coord_system = Vt
	coord_system = (Vt.T * Sigma).T
	
	# 返回结果，embedding 设置为细胞坐标
	return MCA(cell_coords, coord_system, Sigma)


class PCA(NamedTuple):
	embedding: np.ndarray
	coord_system: np.ndarray
	offset: np.ndarray


def fit_pca(Y, n, center=True):
	"""
	Calculate the PCA of a given data matrix Y.

	Parameters
	----------
	Y : array-like, shape (n_samples, n_features)
		The input data matrix.
	n : int
		The number of principal components to return.
	center : bool, default=True
		If True, the data will be centered before computing the covariance matrix.

	Returns
	-------
	pca : sklearn.decomposition.PCA
		The PCA object.
	"""
	if center:
		pca = skd.PCA(n_components=n)
		emb = pca.fit_transform(Y)
		coord_system = pca.components_
		mean = pca.mean_
	else:
		svd = skd.TruncatedSVD(n_components=n, algorithm="arpack")
		emb = svd.fit_transform(Y)
		coord_system = svd.components_
		mean = np.zeros(Y.shape[1])
	return PCA(emb, coord_system, mean)


def ridge_regression(Y, X, ridge_penalty=0, weights=None):
	"""
	Calculate the ridge regression of a given data matrix Y.

	Parameters
	----------
	Y : array-like, shape (n_samples, n_features)
		The input data matrix.
	X : array-like, shape (n_samples, n_coef)
		The input data matrix.
	ridge_penalty : float, default=0
		The ridge penalty.
	weights : array-like, shape (n_features,)
		The weights to apply to each feature.

	Returns
	-------
	ridge: array-like, shape (n_coef, n_features)
	"""
	n_coef = X.shape[1]
	n_samples = X.shape[0]
	n_feat = Y.shape[1]
	assert Y.shape[0] == n_samples
	if weights is None:
		weights = np.ones(n_samples)
	assert len(weights) == n_samples
	
	if np.ndim(ridge_penalty) == 0 or len(ridge_penalty) == 1:
		ridge_penalty = np.eye(n_coef) * ridge_penalty
	elif np.ndim(ridge_penalty) == 1:
		assert len(ridge_penalty) == n_coef
		ridge_penalty = np.diag(ridge_penalty)
	elif np.ndim(ridge_penalty) == 1:
		assert ridge_penalty.shape == (n_coef, n_coef)
		pass
	else:
		raise ValueError("ridge_penalty must be a scalar, 1d array, or 2d array")
	
	ridge_penalty_sq = np.sqrt(np.sum(weights)) * (ridge_penalty.T @ ridge_penalty)
	weights_sqrt = np.sqrt(weights)
	X_ext = np.vstack([multiply_along_axis(X, weights_sqrt, 0), ridge_penalty_sq])
	Y_ext = np.vstack([multiply_along_axis(Y, weights_sqrt, 0), np.zeros((n_coef, n_feat))])
	
	ridge = np.linalg.lstsq(X_ext, Y_ext, rcond=None)[0]
	return ridge


def multiply_along_axis(A, B, axis):
	# Copied from https://stackoverflow.com/a/71750176/604854
	return np.swapaxes(np.swapaxes(A, axis, -1) * B, -1, axis)
