# TDistributionClassifier

**Author:** Abdul Mofique Siddiqui  
**License:** MIT  
**Install via pip:**
```bash
pip install TDistributionClassifier
```

**Import it in your Python code:**
```python
from TDistributionClassifier import TDistributionClassifier
```

---

## Overview

`TDistributionClassifier` is a machine learning classifier designed to model classes using Student's t-distribution. This classifier is robust to outliers and performs effectively when data contains noise or extreme values. It is a versatile tool capable of handling both binary and multiclass classification tasks for both **univariate** (1D) and **multivariate** (multi-dimensional) data.

---

## Installation

Install the package via pip:
```bash
pip install tdistributionclassifier
```

---

## How It Works

- **Univariate Mode**: For 1D features, each class is modeled using a univariate t-distribution.
- **Multivariate Mode**: For multi-dimensional features, each class is modeled using a multivariate t-distribution.
- Uses **log-probabilities** and the **log-sum-exp trick** for numerical stability.
- Automatically detects the input dimensionality and selects the appropriate mode.

---

## Getting Started

### 1. Import the package
```python
from TDistributionClassifier import TDistributionClassifier
```

### 2. Initialize the classifier
```python
clf = TDistributionClassifier()
```

### 3. Fit the model
```python
clf.fit(X_train, y_train)
```
- `X_train`: numpy array of shape `(n_samples,)` or `(n_samples, n_features)`
- `y_train`: class labels

### 4. Predict class probabilities
```python
probs = clf.predict_proba(X_test)
```
- Returns a numpy array of shape `(n_samples, n_classes)` with class probabilities.

### 5. Predict class labels
```python
labels = clf.predict(X_test)
```
- Returns predicted class labels

---

## API Reference

### `TDistributionClassifier()`
Initializes the classifier. No arguments required.

---

### `.fit(X, y)`
Fits the model to the training data.

- **Parameters**:
  - `X`: numpy array of training features. Shape: `(n_samples,)` or `(n_samples, n_features)`
  - `y`: class labels. Shape: `(n_samples,)`

---

### `.predict_proba(X)`
Returns predicted class probabilities.

- **Input**:
  - `X`: Features. Shape: `(n_samples,)` or `(n_samples, n_features)`
- **Output**:
  - `probs`: array of shape `(n_samples, n_classes)` with class probabilities

---

### `.predict(X)`
Returns predicted class labels based on highest probability.

- **Input**:
  - `X`: Features. Shape: `(n_samples,)` or `(n_samples, n_features)`
- **Output**:
  - `labels`: array of shape `(n_samples,)` with class labels

---

## Example Usage

### Example 1: Binary Classification

```python
from TDistributionClassifier import TDistributionClassifier
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

# Load data and binarize target
data = load_diabetes()
X = data.data
y = (data.target > 100).astype(int)  # Binary classification

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Initialize and train
clf = TDistributionClassifier()
clf.fit(X_train, y_train)

# Predict
probs = clf.predict_proba(X_test)
preds = clf.predict(X_test)
```

### Example 2: Multiclass Classification

```python
from TDistributionClassifier import TDistributionClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Load the Iris dataset (3 classes)
data = load_iris()
X = data.data
y = data.target  # Multiclass labels (3 classes)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Initialize and train
clf = TDistributionClassifier()
clf.fit(X_train, y_train)

# Predict
probs = clf.predict_proba(X_test)
labels = clf.predict(X_test)
```

---

## Internals

- **PDF Estimation**: Uses `scipy.stats.t` (univariate) or `scipy.stats.multivariate_t` (multivariate).
- **Regularization**: Adds small noise (`1e-6 * I`) to covariance matrices to ensure invertibility.
- **Numerical Stability**: Log-probabilities with log-sum-exp used for probability normalization.

---

## Notes

- Supports both **binary** and **multiclass classification**.
- Multivariate mode is triggered when input has `>1` features.
- The Student's t-distribution's heavy tails make it more resilient to extreme values compared to traditional Gaussian-based models.
- If data is not linearly separable, consider applying feature transformation or dimensionality reduction before use.

---

## Author

**Abdul Mofique Siddiqui**

---

## License

This project is licensed under the **MIT License**.