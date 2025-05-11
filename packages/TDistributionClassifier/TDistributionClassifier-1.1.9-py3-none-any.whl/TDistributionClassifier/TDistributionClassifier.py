# Made by: Abdul Mofique Siddiqui 
import numpy as np
from scipy.stats import t, multivariate_t
from numpy.linalg import LinAlgError
from typing import Union


class TDistributionClassifier:
    def __init__(self):
        self.class_stats = {}
        self.mode = None  # 'univariate' or 'multivariate'
        self.classes_ = None

    def fit(self, X: Union[np.ndarray, list], y: Union[np.ndarray, list]) -> None:
        X = np.asarray(X)
        y = np.asarray(y)

        if X.ndim == 1:
            X = X.reshape(-1, 1)

        self.mode = 'univariate' if X.shape[1] == 1 else 'multivariate'
        self.classes_ = np.unique(y)

        for cls in self.classes_:
            Xc = X[y == cls]
            df = max(Xc.shape[0] - 1, 1)  # prevent df=0
            mean = np.mean(Xc, axis=0)

            if self.mode == 'univariate':
                std = np.std(Xc, ddof=1) or 1e-6  # avoid division by zero
                self.class_stats[cls] = {"mean": mean[0], "std": std, "df": df}
            else:
                cov = np.cov(Xc.T, ddof=1)
                cov += np.eye(cov.shape[0]) * 1e-6  # regularization
                self.class_stats[cls] = {"mean": mean, "cov": cov, "df": df}

    def _log_pdf_univariate(self, x: float, stats: dict) -> float:
        """Log PDF for univariate t-distribution."""
        t_score = (x - stats["mean"]) / stats["std"]
        log_pdf = t.logpdf(t_score, df=stats["df"]) - np.log(stats["std"])
        return log_pdf

    def _log_pdf_multivariate(self, x: np.ndarray, stats: dict) -> float:
        """Log PDF for multivariate t-distribution."""
        try:
            return multivariate_t.logpdf(x, loc=stats["mean"], shape=stats["cov"], df=stats["df"])
        except LinAlgError:
            return -np.inf  # fallback if matrix is non-invertible

    def predict_proba(self, X: Union[np.ndarray, list]) -> np.ndarray:
        X = np.asarray(X)
        if X.ndim == 1:
            X = X.reshape(-1, 1)

        proba_list = []
        for x in X:
            log_probs = {}
            for cls in self.classes_:
                stats = self.class_stats[cls]
                log_p = (
                    self._log_pdf_univariate(x[0], stats)
                    if self.mode == 'univariate'
                    else self._log_pdf_multivariate(x, stats)
                )
                log_probs[cls] = log_p

            # Log-sum-exp for numerical stability
            max_log = max(log_probs.values())
            exp_shifted = {cls: np.exp(log_p - max_log) for cls, log_p in log_probs.items()}
            total = sum(exp_shifted.values()) + 1e-10
            probs = [exp_shifted.get(cls, 0.0) / total for cls in self.classes_]
            proba_list.append(probs)

        return np.array(proba_list)

    def predict(self, X: Union[np.ndarray, list]) -> np.ndarray:
        probs = self.predict_proba(X)
        indices = np.argmax(probs, axis=1)
        return self.classes_[indices]
