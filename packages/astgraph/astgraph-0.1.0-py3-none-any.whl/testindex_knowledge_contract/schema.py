"""
Knowledge v1 Schema Contract

Defines the core schema constants used by the Knowledge v1 system.
"""

# Node labels
IMPL_LABEL = "Implementation"
GAP_LABEL = "CoverageGap"
TEST_LABEL = "Test"
MODULE_LABEL = "Module"

# Property names
PROP_ID = "id"
PROP_PATH = "path"
PROP_START = "line_start"
PROP_END = "line_end"
PROP_COVER = "coverage"  # float 0-100
PROP_NAME = "name"
PROP_FILE_PATH = "file_path"
PROP_LINE_NUMBER = "line_number"
PROP_DESCRIPTION = "description"

# Relationship types
REL_TESTS = "TESTS"
REL_CALLS = "CALLS"
REL_IMPORTS = "IMPORTS"
REL_CONTAINS = "CONTAINS"
REL_DEFINES = "DEFINES"

# Schema versioning
SCHEMA_VERSION = "v1" 