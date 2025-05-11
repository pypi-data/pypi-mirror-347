"""
Titan Table Metadata Definition File
"""

import re
import difflib
import importlib
from pm_studio_mcp.utils.titan_tables.table_metadata import TABLE_METADATA

def get_table_metadata(table_name):
    """
    Get metadata information for a specified table

    Args:
        table_name (str): Table name or keyword

    Returns:
        dict: Dictionary containing table metadata, including:
              - sample: Sample data showing the table structure
              - description: Table structure description
              - sample_query: Example query (for legacy tables)
              - filter_columns: Filter configurations (for template-based tables)
              - sql_templates: SQL templates with placeholders (for template-based tables)
              Returns None if table doesn't exist
    """
    # If exact match found
    if table_name in TABLE_METADATA:
        return TABLE_METADATA[table_name]

    # If no exact match, try keyword matching
    for key in TABLE_METADATA.keys():
        if re.search(table_name, key, re.IGNORECASE):
            return TABLE_METADATA[key]

    # If still no match, try fuzzy matching
    # First, normalize input for matching (convert words to lowercase)
    normalized_input = table_name.lower().replace('_', ' ').replace('-', ' ')

    # Prepare normalized versions of the table names for matching
    table_matches = {}
    for key in TABLE_METADATA.keys():
        normalized_key = key.lower().replace('_', ' ').replace('-', ' ')

        # Calculate similarity score
        # Method 1: Check if all input words are in the table name
        input_words = set(normalized_input.split())
        key_words = set(normalized_key.split())

        # Check if each input word has a close match in any key word
        match_count = 0
        for input_word in input_words:
            for key_word in key_words:
                # Use sequence matcher to find similarity
                similarity = difflib.SequenceMatcher(None, input_word, key_word).ratio()
                if similarity > 0.7 or input_word in key_word or key_word in input_word:
                    match_count += 1
                    break

        # Calculate a score based on how many input words matched
        if input_words and match_count / len(input_words) > 0.5:
            score = match_count / len(input_words)
            table_matches[key] = score

    # Return the best match if one exists
    if table_matches:
        best_match = max(table_matches.items(), key=lambda x: x[1])[0]
        return TABLE_METADATA[best_match]

    return None

def get_table_metadata_extended(table_name):
    """
    Get extended metadata information for a specified table, including SQL templates and filter configurations

    Args:
        table_name (str): Table name or keyword

    Returns:
        dict: Dictionary containing extended table metadata including SQL_TEMPLATES and FILTER_COLUMNS if available
              Returns None if table doesn't exist or has no extended metadata
    """
    # First, find the matching table using standard method
    standard_metadata = get_table_metadata(table_name)

    if not standard_metadata:
        return None

    # Find the actual table name that was matched
    actual_table_name = None
    for key in TABLE_METADATA.keys():
        if TABLE_METADATA[key] == standard_metadata:
            actual_table_name = key
            break

    if not actual_table_name:
        return None

    # Initialize result dictionary
    extended_metadata = {}

    # Check if extended metadata is available in TABLE_METADATA
    table_meta = TABLE_METADATA[actual_table_name]
    if 'sql_templates' in table_meta:
        extended_metadata['sql_templates'] = table_meta['sql_templates']

    if 'filter_columns' in table_meta:
        extended_metadata['filter_columns'] = table_meta['filter_columns']

    # If we already have the extended metadata from TABLE_METADATA, return it
    if extended_metadata:
        return extended_metadata

    # If not found in TABLE_METADATA, try to import the module directly
    try:
        # First try to preserve the original table name case (for tables like EdgeWindowsUsage)
        module_name = actual_table_name

        # Then try different module name formats (removing duplicates)
        module_names_to_try = [
            actual_table_name,          # Original case: EdgeWindowsUsage
            actual_table_name.lower(),  # Lowercase: edgewindowsusage
        ]

        # Try importing each module name until one succeeds
        module = None
        print(f"Attempting to import module for table '{actual_table_name}'...")
        for name in module_names_to_try:
            try:
                module_path = f"utils.titan_tables.{name}"
                print(f"Trying to import {module_path}...")
                module = importlib.import_module(module_path)
                print(f"Successfully imported {module_path}")
                break  # Exit the loop if import succeeds
            except ImportError as e:
                print(f"Failed to import {module_path}: {e}")
                continue
            except Exception as e:
                print(f"Unexpected error importing {module_path}: {e}")
                continue

        # If all import attempts failed, raise ImportError
        if module is None:
            print(f"All import attempts failed for table {actual_table_name}")
            raise ImportError(f"Could not import module for table {actual_table_name}")

        # Check for SQL templates
        if hasattr(module, 'SQL_TEMPLATES'):
            extended_metadata['sql_templates'] = module.SQL_TEMPLATES

        # Check for filter columns
        if hasattr(module, 'FILTER_COLUMNS'):
            extended_metadata['filter_columns'] = module.FILTER_COLUMNS

        return extended_metadata if extended_metadata else None

    except (ImportError, AttributeError):
        # Either the module couldn't be imported or it doesn't have the extended attributes
        return None
