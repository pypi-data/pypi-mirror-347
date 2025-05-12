"""
Metadata for EdgeWindowsUsage table
"""

# Description of the table structure and purpose
DESCRIPTION = \
"""
EdgeWindowsUsage tracks usage patterns of Edge browser on Windows devices.
The table contains the following information:
- date_str/datetime: The date when the data was collected
- device_id: Anonymized identifier for the device
- country: Two-letter country code where the device is located
- os_version: Windows version running on the device
- app_version: Edge browser version
- session_count: Number of browser sessions in the time period
- usage_minutes: Total minutes of browser usage in the time period
- feature_used: The most used feature during the time period

This table is useful for understanding user engagement, feature adoption, and regional variations in browser usage patterns.
"""

# Sample data showing the table structure
SAMPLE = \
"""
Sample data for EdgeWindowsUsage:

date_str    datetime            device_id   country os_version  app_version  session_count    usage_minutes   feature_used
2025-04-20  2025-04-20T00:00:00 device123   US      Windows 11  114.0.1823   5                78              collections
2025-04-20  2025-04-20T00:00:00 device456   IN      Windows 10  113.0.1774   3                45              vertical_tabs
2025-04-20  2025-04-20T00:00:00 device789   DE      Windows 11  114.0.1823   8                120             sidebar
"""

# Description of filterable columns and mappings (for template use)
# ----------------------------------------------------------------
# The filter columns definition provides metadata for template-based queries.
# Each filter can include:
#   - description: Brief explanation of the filter
#   - mapping: For categorical variables, provides mapping from codes to display values
#   - default_value: Used when a filter is not explicitly provided
#
# Required vs Optional filters:
#   - Filters listed in a template's "required_filters" must be provided by the user
#   - Other filters in the template are optional and will use defaults if not provided
#
FILTER_COLUMNS = \
{
    "date_range": {
        "description": "Date range for data analysis",
        "start_date": "Start date in YYYY-MM-DD format", 
        "end_date": "End date in YYYY-MM-DD format"
    },
    "country": {
        "description": "Two-letter country code for filtering data by location",
        "values": ["US", "CA", "MX", "GB", "FR", "DE", "IN", "JP", "CN", "AU", "BR", "RU"],
        "default_value": "US"
    },
    "os_version": {
        "description": "Windows operating system version",
        "mapping": {
            "Windows 10": "Windows 10",
            "Windows 11": "Windows 11"
        },
        "default_value": "Windows 11"
    },
    "feature": {
        "description": "Edge browser features being tracked for usage",
        "values": [
            "collections", 
            "vertical_tabs", 
            "sidebar", 
            "pdf_viewer", 
            "web_capture", 
            "shopping", 
            "password_manager"
        ],
        "default_value": "all"
    },
    "min_usage": {
        "description": "Minimum minutes of usage to include in results",
        "default_value": "0"
    },
    "min_sessions": {
        "description": "Minimum number of sessions to include in results",
        "default_value": "1"
    }
}

# SQL Templates with placeholders for customizable filters
# ----------------------------------------------------------------
# Each template includes:
#   - name: A unique identifier for the template
#   - description: Brief explanation of the query purpose
#   - template: The SQL query with placeholders in the format {filter_name}
#   - required_filters: List of filters that must be provided by the user (will cause error if missing)
#   - optional_filters: List of filters that are optional and will use defaults if available
#
# Placeholder format: {filter_name}
# Example: WHERE `datetime` >= toDateTime('{start_date} 00:00:00')
#
# The system will:
#   1. Check that all required filters are provided by the user
#   2. For optional filters, use default values from FILTER_COLUMNS if available
#   3. Replace all placeholders with their corresponding values
#
SQL_TEMPLATES = [
    {
        "name": "usage_by_feature", 
        "description": "Analyze usage patterns across different features with filtering options",
        "required_filters": ["start_date", "end_date"],
        "optional_filters": ["country_value", "os_version_value", "min_usage_value"],
        "template": """
SELECT 
    feature_used,
    COUNT(DISTINCT device_id) as user_count,
    AVG(session_count) as avg_sessions,
    AVG(usage_minutes) as avg_usage_minutes,
    os_version
FROM 
    EdgeWindowsUsage
WHERE 
    datetime >= toDateTime('{start_date} 00:00:00')
    AND datetime < toDateTime('{end_date} 00:00:00')
    AND country = '{country_value}'
    AND (os_version = '{os_version_value}' OR '{os_version_value}' = 'all')
    AND usage_minutes >= {min_usage_value}
GROUP BY 
    feature_used,
    os_version
ORDER BY 
    user_count DESC
LIMIT 1000;
"""
    },
    {
        "name": "country_comparison",
        "description": "Compare usage metrics across different countries",
        "required_filters": ["start_date", "end_date"],
        "optional_filters": ["feature_value", "os_version_value", "min_sessions_value"],
        "template": """
SELECT 
    country,
    COUNT(DISTINCT device_id) as user_count,
    AVG(usage_minutes) as avg_usage_minutes,
    SUM(session_count) as total_sessions
FROM 
    EdgeWindowsUsage
WHERE 
    datetime >= toDateTime('{start_date} 00:00:00')
    AND datetime < toDateTime('{end_date} 00:00:00')
    AND (feature_used = '{feature_value}' OR '{feature_value}' = 'all')
    AND (os_version = '{os_version_value}' OR '{os_version_value}' = 'all')
    AND session_count >= {min_sessions_value}
GROUP BY 
    country
ORDER BY 
    user_count DESC
LIMIT 50;
"""
    },
    {
        "name": "App Version Analysis",
        "description": "Analyze feature usage across different app versions",
        "required_filters": ["start_date", "end_date"],
        "optional_filters": ["country_value", "os_version_value", "feature_value"],
        "template": """
SELECT 
    app_version,
    feature_used,
    COUNT(DISTINCT device_id) as user_count,
    AVG(usage_minutes) as avg_usage_minutes,
    AVG(session_count) as avg_sessions
FROM 
    EdgeWindowsUsage
WHERE 
    datetime >= toDateTime('{start_date} 00:00:00')
    AND datetime < toDateTime('{end_date} 00:00:00')
    AND (country = '{country_value}' OR '{country_value}' = 'all')
    AND (os_version = '{os_version_value}' OR '{os_version_value}' = 'all')
    AND (feature_used = '{feature_value}' OR '{feature_value}' = 'all')
GROUP BY 
    app_version,
    feature_used
ORDER BY 
    app_version DESC,
    user_count DESC
LIMIT 1000;
"""
    },
    {
        "name": "Daily Usage Trend",
        "description": "Track daily usage patterns over time",
        "required_filters": ["start_date", "end_date"],
        "optional_filters": ["country_value", "feature_value"],
        "template": """
SELECT 
    date_str,
    COUNT(DISTINCT device_id) as daily_active_users,
    AVG(usage_minutes) as avg_usage_minutes,
    SUM(session_count) as total_sessions
FROM 
    EdgeWindowsUsage
WHERE 
    datetime >= toDateTime('{start_date} 00:00:00')
    AND datetime < toDateTime('{end_date} 00:00:00')
    AND (country = '{country_value}' OR '{country_value}' = 'all')
    AND (feature_used = '{feature_value}' OR '{feature_value}' = 'all')
GROUP BY 
    date_str
ORDER BY 
    date_str ASC
LIMIT 1000;
"""
    }
]
