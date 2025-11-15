from __future__ import annotations
import threading
import time
from typing import Dict, Iterable, List, Mapping, Tuple


_LabelKey = Tuple[Tuple[str, str], ...]


def _label_key(labels: Mapping[str, str] | None) -> _LabelKey:
    if not labels:
        return tuple()
    return tuple(sorted((str(k), str(v)) for k, v in labels.items()))


class Counter:
    def __init__(self, name: str, help: str = "", label_names: Iterable[str] | None = None) -> None:
        self.name = name
        self.help = help
        self.label_names = tuple(label_names or ())
        self._values: Dict[_LabelKey, float] = {}
        self._lock = threading.Lock()

    def inc(self, amount: float = 1.0, **labels: str) -> None:
        key = _label_key(labels)
        with self._lock:
            self._values[key] = self._values.get(key, 0.0) + amount

    def samples(self) -> Iterable[Tuple[_LabelKey, float]]:
        with self._lock:
            return list(self._values.items())


class Histogram:
    def __init__(self, name: str, help: str = "", buckets: Iterable[float] | None = None, label_names: Iterable[str] | None = None) -> None:
        self.name = name
        self.help = help
        self.label_names = tuple(label_names or ())
        self.buckets = sorted(buckets or [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5])
        self._counts: Dict[_LabelKey, List[int]] = {}
        self._sum: Dict[_LabelKey, float] = {}
        self._lock = threading.Lock()

    def observe(self, value: float, **labels: str) -> None:
        key = _label_key(labels)
        with self._lock:
            if key not in self._counts:
                self._counts[key] = [0] * (len(self.buckets) + 1)  # +1 for +Inf
                self._sum[key] = 0.0
            idx = 0
            while idx < len(self.buckets) and value > self.buckets[idx]:
                idx += 1
            self._counts[key][idx] += 1
            self._sum[key] += value

    def samples(self) -> Iterable[Tuple[_LabelKey, List[int], float]]:
        with self._lock:
            return [(k, v.copy(), self._sum[k]) for k, v in self._counts.items()]


class Registry:
    def __init__(self) -> None:
        self.counters: Dict[str, Counter] = {}
        self.histograms: Dict[str, Histogram] = {}

    def counter(self, name: str, help: str = "", label_names: Iterable[str] | None = None) -> Counter:
        if name not in self.counters:
            self.counters[name] = Counter(name, help, label_names)
        return self.counters[name]

    def histogram(self, name: str, help: str = "", buckets: Iterable[float] | None = None, label_names: Iterable[str] | None = None) -> Histogram:
        if name not in self.histograms:
            self.histograms[name] = Histogram(name, help, buckets, label_names)
        return self.histograms[name]

    def render_prometheus(self) -> str:
        lines: List[str] = []
        for c in self.counters.values():
            if c.help:
                lines.append(f"# HELP {c.name} {c.help}")
            lines.append(f"# TYPE {c.name} counter")
            for labels, value in c.samples():
                label_txt = "" if not labels else "{" + ",".join(f"{k}=\"{v}\"" for k, v in labels) + "}"
                lines.append(f"{c.name}{label_txt} {value}")
        for h in self.histograms.values():
            if h.help:
                lines.append(f"# HELP {h.name} {h.help}")
            lines.append(f"# TYPE {h.name} histogram")
            for labels, counts, s in h.samples():
                base_labels = dict(labels)
                acc = 0
                for b, cnt in zip([*h.buckets, float('inf')], counts):
                    acc += cnt
                    le = "+Inf" if b == float('inf') else ("%g" % b)
                    ltxt = {**base_labels, "le": str(le)}
                    label_txt = "{" + ",".join(f"{k}=\"{v}\"" for k, v in ltxt.items()) + "}"
                    lines.append(f"{h.name}_bucket{label_txt} {acc}")
                # sum and count
                label_txt = "{" + ",".join(f"{k}=\"{v}\"" for k, v in base_labels.items()) + "}"
                lines.append(f"{h.name}_sum{label_txt} {s}")
                lines.append(f"{h.name}_count{label_txt} {acc}")
        return "\n".join(lines) + "\n"


_default_registry = Registry()
http_requests_total = _default_registry.counter(
    "http_requests_total",
    help="Total HTTP requests",
    label_names=("service", "method", "path", "status"),
)
http_request_duration_seconds = _default_registry.histogram(
    "http_request_duration_seconds",
    help="HTTP request duration in seconds",
    label_names=("service", "method", "path", "status"),
)


def registry() -> Registry:
    return _default_registry