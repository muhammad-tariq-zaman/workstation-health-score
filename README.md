# workstation-health-score

Turn four everyday workstation metrics into one 0-100 health score per host, so the machines needing attention sort themselves to the top.

## How to run

```sh
python3 main.py hosts.csv
```

## Example output

```
WS-01: 100/100 HEALTHY
WS-02: 55/100 ACTION
1 host(s) needing action.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
