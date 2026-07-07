class DataAnalyzer:
    def analyze(self, data, method="mean"):
        if method == "mean":
            return sum(data) / len(data)
        elif method == "sum":
            return sum(data)
        elif method == "median":
            raise NotImplementedError("Median not implemented")
        else:
            raise ValueError(f"Unknown method: {method}")
