"""
Titan Table Metadata Dictionary Definition File
"""

# Import table metadata
from pm_studio_mcp.utils.titan_tables.edgewindowsusage import (
    SAMPLE as EDGE_WINDOWS_USAGE_SAMPLE,
    DESCRIPTION as EDGE_WINDOWS_USAGE_DESC,
    FILTER_COLUMNS as EDGE_WINDOWS_USAGE_FILTER_COLUMNS,
    SQL_TEMPLATES as EDGE_WINDOWS_USAGE_SQL_TEMPLATES
)
from pm_studio_mcp.utils.titan_tables.edgemacecsretentionv1 import (
    SAMPLE as EDGE_MAC_ECS_RETENTION_SAMPLE,
    DESCRIPTION as EDGE_MAC_ECS_RETENTION_DESC,
    FILTER_COLUMNS as EDGE_MAC_ECS_RETENTION_FILTER_COLUMNS,
    SQL_TEMPLATES as EDGE_MAC_ECS_RETENTION_SQL_TEMPLATES
)
from pm_studio_mcp.utils.titan_tables.KPI_DailyUser import (
    SAMPLE as KPI_DAILY_USER_SAMPLE,
    DESCRIPTION as KPI_DAILY_USER_DESC,
    FILTER_COLUMNS as KPI_DAILY_USER_FILTER_COLUMNS,
    SQL_TEMPLATES as KPI_DAILY_USER_SQL_TEMPLATES
)

# Define table metadata dictionary
TABLE_METADATA = {
    "EdgeWindowsUsage": {
        "sample": EDGE_WINDOWS_USAGE_SAMPLE,
        "description": EDGE_WINDOWS_USAGE_DESC,
        "filter_columns": EDGE_WINDOWS_USAGE_FILTER_COLUMNS,
        "sql_templates": EDGE_WINDOWS_USAGE_SQL_TEMPLATES
    },
    "EdgeMacECSRetentionV1": {
        "sample": EDGE_MAC_ECS_RETENTION_SAMPLE,
        "description": EDGE_MAC_ECS_RETENTION_DESC,
        "filter_columns": EDGE_MAC_ECS_RETENTION_FILTER_COLUMNS,
        "sql_templates": EDGE_MAC_ECS_RETENTION_SQL_TEMPLATES
    },
    "KPI_DailyUser": {
        "sample": KPI_DAILY_USER_SAMPLE,
        "description": KPI_DAILY_USER_DESC,
        "filter_columns": KPI_DAILY_USER_FILTER_COLUMNS,
        "sql_templates": KPI_DAILY_USER_SQL_TEMPLATES
    }
}
