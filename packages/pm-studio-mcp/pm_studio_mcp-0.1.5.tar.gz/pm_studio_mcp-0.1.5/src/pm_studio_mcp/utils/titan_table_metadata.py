"""
Titan Table Metadata Definition File
"""

import re
import difflib
import importlib
from typing import Dict, List, Tuple, Optional
from pm_studio_mcp.utils.titan_tables.table_metadata import TABLE_METADATA
from pm_studio_mcp.utils.matching_utils import normalize_string, word_match, find_best_match, find_all_matches

def find_table_by_template_name(template_name):
    """
    Find tables that contain a SQL template with the given name

    Args:
        template_name (str): Template name or keyword to search for

    Returns:
        list: List of (table_name, template_name, template_description) tuples for matching templates
              Returns empty list if no matches found
    """
    results = []
    
    # Search through all tables in TABLE_METADATA
    for table_name, metadata in TABLE_METADATA.items():
        # Skip tables that don't have SQL templates
        if 'sql_templates' not in metadata:
            continue
            
        # Search through templates in this table
        for template in metadata['sql_templates']:
            if 'name' not in template or 'description' not in template:
                continue
            
            # Use the generic matching utilities for better matches
            name_matches = {}
            name_matches[template['name']] = template  # Create a temp dict for matching
            
            # Check for matches in both name and description
            name_match = find_best_match(template_name, name_matches, match_type='word', threshold=0.6)
            
            # If no name match, try matching against description
            if name_match[0] is None:
                desc_matches = {}
                desc_matches[template['description']] = template
                desc_match = find_best_match(template_name, desc_matches, match_type='word', threshold=0.6)
                
                if desc_match[0] is not None:
                    results.append((table_name, template['name'], template['description']))
            else:
                results.append((table_name, template['name'], template['description']))
    
    return results

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
    # Convert TABLE_METADATA to a format suitable for matching functions
    metadata_dict = {key: value for key, value in TABLE_METADATA.items()}
    
    # Find the best match using our generic matching utility
    best_match = find_best_match(table_name, metadata_dict, match_type='auto', threshold=0.6)
    
    if best_match[0] is not None:
        return best_match[1]  # Return the metadata for the matched table
    
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
