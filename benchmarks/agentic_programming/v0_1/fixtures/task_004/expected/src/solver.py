class DataAnalyzer:
    def analyze(self, data, method="mean"):
        if method == "mean":
            return sum(data) / len(data)
        elif method == "sum":
            return sum(data)
        elif method == "median":
            sorted_data = sorted(data)
            n = len(sorted_data)
            if n % 2 == 1:
                return sorted_data[n // 2]
            else:
                mid = n // 2
                return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            raise ValueError(f"Unknown method: {method}")
