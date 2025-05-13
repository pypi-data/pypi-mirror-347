# Valdar

**Valdar** is a Mobileye radar data validation and analysis tool designed to process and assess radar logs for quality metrics

---

## 📦 Installation

Install from [PyPI](https://pypi.org/project/valdar):

```bash
pip install valdar
```
___

## 🚀 Usage

```python
from valdar import RadarAnalyzer

analyzer = RadarAnalyzer("/path/to/pext_dir")  # must include 'bml_LowLevelCRF_frame' pext
status = analyzer.evaluate()

# Access results
print("LRR status:", status.lrr_status)
print("NR status:", status.nr_status)
print("LRR validity", status.valid_lrr)
print("NR validity", status.valid_nr)
```

___

## Requirements
- Python 3.7+

___

## Output Structure

The `RadarStatus` object returned by `RadarAnalyzer.evaluate()` contains a structured summary of radar health metrics:

```python
{
  "valid_lrr": bool | None,               # True if LRR data passes all checks,
                                          # False if any check fails,
                                          # None if data is missing or not applicable

  "valid_nr": bool | None,                # Same as above, but for NR data

  "lrr_status": {
    "drop_rate": float,                  # Ratio of dropped LRR frames (0.0 to 1.0)
    "valid_time_sync_rate": float,       # Proportion of LRR frames with synchronized timestamps
    "valid_calibration_rate": float,     # Proportion of LRR frames marked as calibrated
    "high_latency_rate": float,          # Proportion of LRR frames with latency > 0.2 seconds
  },

  "nr_status": {
    "drop_rate": float,                  # Ratio of dropped NR frames across all relevant sensors
    "valid_time_sync_rate": float,       # Proportion of NR frames with all timestamps synchronized
    "valid_calibration_rate": float,     # Proportion of NR frames where all sensors are calibrated
    "high_latency_rate": float,          # Proportion of NR frames with latency > 0.2 seconds on any sensor
  }
}
```
Each field can be None if the corresponding data column is missing in the input.
Top-level valid_lrr and valid_nr fields summarize whether the data is considered "valid" based on configurable thresholds:
- drop_rate < 0.05
- valid_time_sync_rate > 0.95
- valid_calibration_rate > 0.95
- high_latency_rate < 0.05
Note: For NR metrics, a failure is counted if any of the four NR sensors fails the corresponding check for a frame.
