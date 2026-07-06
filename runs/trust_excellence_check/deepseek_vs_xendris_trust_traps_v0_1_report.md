# DeepSeek Base vs Xendris+DeepSeek - Trust Traps v0.1

## Purpose

Measure benchmark-local resistance to trust traps under the fixed Trust Traps
v0.1 dataset and configured Xendris gates.

## Configuration

| Field | Value |
|---|---|
| Execution mode | `dry-run` |
| Provider | `mock` |
| Model | `deepseek-chat` |
| Temperature | `0.0` |
| Max tokens | `1024` |
| Dataset hash | `61759a015286a2daab1d91e664cb3f1e4df85aecb45dec5b8c2329e854f5b76f` |
| Xendris version | `0.2.0` |

## No Universal Superiority Warning

This benchmark does not imply universal model superiority. It only measures a
closed benchmark-local behavior under Trust Traps v0.1 and this configuration.

## Results

| Metric | Value |
|---|---:|
| Total samples | 100 |
| DeepSeek average score | 0.1 |
| Xendris average score | 0.985 |
| Average delta | 0.885 |
| Xendris wins | 90 |
| DeepSeek wins | 0 |
| Ties | 10 |
| Cost per valid DeepSeek answer | 8e-06 |
| Cost per valid Xendris answer | 7.7e-05 |
| DeepSeek average latency ms | 100.0 |
| Xendris average latency ms | 100.01 |

## Limitations

- Closed dataset.
- Benchmark-local interpretation only.
- Dry-run results do not measure real provider performance.
- Passing the excellence gate does not validate universal superiority.
