"""
Metadata for EdgeMacECSRetentionV1 table
"""

# Description of the table
DESCRIPTION = \
"""
EdgeMacECSRetentionV1 represents the retention data for Edge Mac.
The table contains information about user retention across different time periods, regions, and channels.
Retention rate can be calculated as: retainedUser / activeUser
"""

# Sample data showing the table structure
SAMPLE = \
"""
Sample data for EdgeMacECSRetentionV1:

date_str	datetime	metrics_date_str	metrics_datetime	a14Region	accountType	dataConsent	app_build_number	channel_ingressed_name	ext_location_country	ext_os_ver	isNewUser	offset	activeUser	retainedUser
2025-04-20	2025-04-20T00:00:00	2025-04-06	2025-04-06T00:00:00	Middle East & Africa	All	0	135.0.3179.54	stable	TR	15.1.0	0	14	5	4
2025-04-20	2025-04-20T00:00:00	2025-04-06	2025-04-06T00:00:00	Middle East & Africa	All	0	135.0.3179.54	stable	TR	15.1.0	1	14	3	1
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
    "account_type": {
        "description": "Type of user account",
        "mapping": {
            "All": "All account types",
            "MSA": "Microsoft account",
            "AAD": "Azure Active Directory"
        },
        "default_value": "All"
    },
    "channel": {
        "description": "Distribution channel identifier",
        "mapping": {
            "stable": "Stable",
            "beta": "Beta",
            "dev": "Dev",
            "canary": "Canary"
        },
        "default_value": "stable"
    },
    "region": {
        "description": "Geographic region identifiers",
        "values": [
            "United States of America",
            "Canada",
            "Latin (Central & South) America",
            "United Kingdom",
            "Western Europe",
            "Central and Eastern Europe",
            "Middle East & Africa",
            "Asia Pacific",
            "Greater China",
            "Japan",
            "Korea",
            "India",
            "ANZ"
        ],
        "default_value": "United States of America"
    },
    "user_type": {
        "description": "Type of user based on experience",
        "mapping": {
            "0": "Existing user",
            "1": "New user",
            "all": "All users"
        },
        "default_value": "all"
    },
    "offset": {
        "description": "Number of days for retention calculation",
        "values": {
            "1": "Day 1 retention",
            "7": "Day 7 retention",
            "14": "Day 14 retention",
            "28": "Day 28 retention"
        },
        "default_value": "7"
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
# Example: WHERE `metrics_datetime` >= toDateTime('{start_date} 00:00:00')
#
# The system will:
#   1. Check that all required filters are provided by the user
#   2. For optional filters, use default values from FILTER_COLUMNS if available
#   3. Replace all placeholders with their corresponding values
#
SQL_TEMPLATES = [
    {
        "name": "retention_by_date",
        "description": "Calculate retention rate over time for a specific retention window",
        "required_filters": ["start_date", "end_date"],
        "optional_filters": ["channel_value", "offset_value"],
        "template": """
SELECT 
    toStartOfDay(toDateTime(`metrics_datetime`)) AS `cohort_date`,
    SUM(retainedUser)/SUM(activeUser) AS `retention_rate`,
    SUM(activeUser) AS `cohort_size`
FROM EdgeMacECSRetentionV1
WHERE `metrics_datetime` >= toDateTime('{start_date} 00:00:00')
  AND `metrics_datetime` < toDateTime('{end_date} 00:00:00')
  AND channel_ingressed_name = '{channel_value}'
  AND offset = '{offset_value}'
GROUP BY toStartOfDay(toDateTime(`metrics_datetime`))
ORDER BY `cohort_date` DESC
LIMIT 1000;
"""
    },
    {
        "name": "new_user_retention_by_region",
        "description": "Compare retention rates for new users across different regions",
        "required_filters": ["start_date", "end_date"],
        "optional_filters": ["channel_value", "offset_value"],
        "template": """
SELECT 
    a14Region AS `region`,
    SUM(retainedUser)/SUM(activeUser) AS `retention_rate`,
    SUM(activeUser) AS `cohort_size`
FROM EdgeMacECSRetentionV1
WHERE `metrics_datetime` >= toDateTime('{start_date} 00:00:00')
  AND `metrics_datetime` < toDateTime('{end_date} 00:00:00')
  AND channel_ingressed_name = '{channel_value}'
  AND offset = '{offset_value}'
  AND isNewUser = 1
GROUP BY a14Region
HAVING `cohort_size` >= 100
ORDER BY `retention_rate` DESC
LIMIT 1000;
"""
    }
]
