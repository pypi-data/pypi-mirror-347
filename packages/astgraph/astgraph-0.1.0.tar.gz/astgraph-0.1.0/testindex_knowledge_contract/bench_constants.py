"""
Benchmark Constants for Knowledge v1

FROZEN FOR KNOWLEDGE V1 RELEASE - DO NOT MODIFY THESE VALUES
Any changes will invalidate the benchmark results.
"""

# Django repository settings - FROZEN
DJANGO_URL = "https://github.com/django/django.git"
DJANGO_TAG = "4.2.11"  # Stable LTS release
DJANGO_SHA = "61a986f53d805e4d359ab61af60a2dcd55befe25"  # Locked SHA that matches our patch

# Benchmark settings - FROZEN
LATENCY_KPI_P95 = 30  # seconds
NUM_BENCHMARK_RUNS = 10

# Vector cost settings - FROZEN
VECTOR_COST_KPI = 15  # USD per million vectors
VECTOR_DIMENSION = 768  # Default dimension for embedding vectors

# Paths - FROZEN
PATCH_FILE = "patches/django_1k.diff" 