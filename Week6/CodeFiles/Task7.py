"""
Comprehensive Data Analysis App
- Decorators: timing
- Exception handling: robust I/O, stats
- JSON I/O: config + report
- collections: Counter, defaultdict (internally optional), deque, namedtuple
- Multithreading: parallel stats + category counts
- Asyncio: async config load + async report save
- Visualization: matplotlib bar chart
- Exports: cleaned.csv + report.json + chart.png
"""

import os
import json
import time
import random
import threading
import asyncio
from collections import Counter, deque, namedtuple

import pandas as pd
import matplotlib.pyplot as plt
import statistics as stats


# =============== 1) Utility: timing decorator ===============
def timing(func):
    """Prints execution time of any function."""
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.time()
            print(f"[TIMING] {func.__name__} took {end - start:.4f}s")
    return wrapper


# =============== 2) Data I/O (CSV/JSON) with exceptions ===============
@timing
def load_or_create_input(csv_path="input.csv", json_path="input.json", rows=100) -> pd.DataFrame:
    """
    Try reading CSV; if missing, try JSON; if both missing,
    create sample data and save both.
    """
    try:
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            print(f"Loaded CSV: {csv_path}")
            return df

        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            print(f"Loaded JSON: {json_path}")
            return df

        # Create sample data
        categories = ["A", "B", "C", "D"]
        data = {
            "id": list(range(1, rows + 1)),
            "value": [round(random.uniform(10, 100), 2) for _ in range(rows)],
            "category": [random.choice(categories) for _ in range(rows)],
        }
        df = pd.DataFrame(data)

        # Save both formats
        df.to_csv(csv_path, index=False)
        with open(json_path, "w") as f:
            json.dump(df.to_dict(orient="records"), f, indent=4)

        print(f"Created sample data and saved to: {csv_path} & {json_path}")
        return df

    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"[ERROR] Failed to read/create input: {e}")
        return pd.DataFrame({"id": [], "value": [], "category": []})


# =============== 3) Processing helpers (collections) ===============
def compute_category_counts(series) -> dict:
    return dict(Counter(series))


def compute_stats(values) -> dict:
    out = {}
    try:
        vals = list(values)
        out["count"] = len(vals)
        out["mean"] = float(stats.mean(vals)) if vals else None
        out["median"] = float(stats.median(vals)) if vals else None
        out["stdev"] = float(stats.stdev(vals)) if len(vals) > 1 else 0.0
    except stats.StatisticsError as e:
        print(f"[WARN] Stats error: {e}")
    return out


def moving_average(values, window=5):
    """Use deque to compute simple moving average efficiently."""
    q = deque(maxlen=window)
    avgs = []
    s = 0.0
    for v in values:
        if len(q) == q.maxlen:
            s -= q[0]
        q.append(v)
        s += v
        avgs.append(s / len(q))
    return avgs


# =============== 4) Multithreading for CPU-light parallel tasks ===============
@timing
def parallel_analyze(df: pd.DataFrame) -> dict:
    results = {}
    lock = threading.Lock()

    def t_stats():
        res = compute_stats(df["value"] if "value" in df else [])
        with lock:
            results["stats"] = res

    def t_counts():
        res = compute_category_counts(df["category"] if "category" in df else [])
        with lock:
            results["category_counts"] = res

    t1 = threading.Thread(target=t_stats, daemon=True)
    t2 = threading.Thread(target=t_counts, daemon=True)
    t1.start(); t2.start()
    t1.join(); t2.join()
    return results


# =============== 5) Visualization ===============
@timing
def plot_category_counts(counts: dict, out_path="category_counts.png"):
    if not counts:
        print("[WARN] No counts to plot.")
        return None
    labels = list(counts.keys())
    values = list(counts.values())
    plt.figure(figsize=(7, 4))
    plt.bar(labels, values)  # no explicit colors/styles
    plt.title("Category Counts")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved chart: {out_path}")
    return out_path


# =============== 6) Async tasks (config + report) ===============
async def async_load_config(path="config.json"):
    """Load config; create default if missing. Simulate I/O with small await."""
    await asyncio.sleep(0.1)
    default_cfg = {"moving_average_window": 5, "top_n_categories": 10}
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default_cfg, f, indent=4)
        print(f"Created default config: {path}")
        return default_cfg
    try:
        with open(path, "r") as f:
            cfg = json.load(f)
        print(f"Loaded config: {path}")
        return cfg
    except json.JSONDecodeError:
        print("[WARN] Config invalid JSON; using defaults.")
        return default_cfg


async def async_save_report(report: dict, path="report.json"):
    """Save report asynchronously."""
    await asyncio.sleep(0.1)
    try:
        with open(path, "w") as f:
            json.dump(report, f, indent=4)
        print(f"Async saved report: {path}")
        return path
    except OSError as e:
        print(f"[ERROR] Failed to save report: {e}")
        return None


# ---- Helper to run async safely in any environment (including notebooks) ----
def run_async(coro):
    """Run an async coroutine on a dedicated thread/event loop (safe in notebooks)."""
    result = {"value": None}
    def runner():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result["value"] = loop.run_until_complete(coro)
        finally:
            loop.close()
    t = threading.Thread(target=runner, daemon=True)
    t.start(); t.join()
    return result["value"]


# =============== 7) End-to-end pipeline ===============
@timing
def run_pipeline():
    # 1) Load / create input
    df = load_or_create_input()
    if df.empty:
        print("[WARN] Input is empty; exiting early.")
        return {}

    # 2) Clean/prepare
    try:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df.dropna(subset=["value", "category"])
    except Exception as e:
        print(f"[ERROR] Cleaning failed: {e}")

    # 3) Multithreaded analysis
    results = parallel_analyze(df)

    # 4) Async config, moving average via deque
    cfg = run_async(async_load_config("config.json"))
    window = int(cfg.get("moving_average_window", 5))
    df["moving_avg"] = moving_average(df["value"].tolist(), window=window)

    # 5) Visualization
    chart_path = plot_category_counts(results.get("category_counts", {}), "category_counts.png")

    # 6) Export cleaned data
    cleaned_csv = "cleaned.csv"
    df.to_csv(cleaned_csv, index=False)
    print(f"Exported cleaned data: {cleaned_csv}")

    # 7) Build + async save report
    # (namedtuple demo: pack stats neatly before dumping)
    Summary = namedtuple("Summary", ["count", "mean", "median", "stdev"])
    s = results.get("stats", {})
    summary_tuple = Summary(s.get("count"), s.get("mean"), s.get("median"), s.get("stdev"))

    report = {
        "summary": summary_tuple._asdict(),          # namedtuple -> dict for JSON
        "category_counts": results.get("category_counts", {}),
        "chart_path": chart_path,
        "cleaned_csv": cleaned_csv,
        "rows": int(len(df)),
        "moving_average_window": window,
    }

    report_path = run_async(async_save_report(report, "report.json"))

    # Return artifact paths
    return {
        "report": report_path,
        "chart": chart_path,
        "cleaned_csv": cleaned_csv,
        "config": "config.json",
        "input_csv": "input.csv",
        "input_json": "input.json",
    }


# =============== 8) CLI entrypoint ===============
if __name__ == "__main__":
    artifacts = run_pipeline()
    print("\nArtifacts:")
    for k, v in artifacts.items():
        print(f"- {k}: {v}")
