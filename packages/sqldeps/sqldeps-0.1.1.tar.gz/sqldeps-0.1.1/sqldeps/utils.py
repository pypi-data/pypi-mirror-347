"""Utility functions for SQLDeps.

This module provides helper functions for finding SQL files, merging SQL profiles,
and performing schema validation and comparison.
"""

from pathlib import Path

import pandas as pd

from sqldeps.models import SQLProfile


def find_sql_files(
    folder_path: str | Path,
    recursive: bool = False,
    valid_extensions: set[str] | None = None,
) -> list[Path]:
    """Find SQL files in a folder.

    Args:
        folder_path: Path to the folder
        recursive: Whether to search recursively
        valid_extensions: Set of valid file extensions (default: {'sql'})

    Returns:
        List of file paths

    Raises:
        FileNotFoundError: If folder doesn't exist
        NotADirectoryError: If path is not a directory
        ValueError: If no SQL files are found
    """
    folder_path = Path(folder_path)

    # Validate folder
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    if not folder_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {folder_path}")

    # Default extensions if not provided
    valid_extensions = valid_extensions or {"sql"}
    valid_extensions = {ext.lower().lstrip(".") for ext in valid_extensions}

    # Find matching files
    pattern = "**/*" if recursive else "*"
    sql_files = [
        f
        for f in folder_path.glob(pattern)
        if f.is_file() and f.suffix.lower().lstrip(".") in valid_extensions
    ]

    if not sql_files:
        raise ValueError(f"No SQL files found in {folder_path}")

    return sql_files


def merge_profiles(analyses: list[SQLProfile]) -> SQLProfile:
    """Merges multiple SQLProfile objects into a single one.

    Args:
        analyses: List of SQLProfile objects to merge

    Returns:
        A new SQLProfile with merged dependencies and outputs
    """
    merged_dependencies = {}
    merged_outputs = {}

    for analysis in analyses:
        # Merge dependencies
        for table, columns in analysis.dependencies.items():
            if "*" in columns:
                merged_dependencies[table] = {"*"}
            else:
                merged_dependencies.setdefault(table, set()).update(columns)

        # Merge outputs
        for table, columns in analysis.outputs.items():
            if "*" in columns:
                merged_outputs[table] = {"*"}
            else:
                merged_outputs.setdefault(table, set()).update(columns)

    return SQLProfile(
        dependencies={
            table: list(columns) for table, columns in merged_dependencies.items()
        },
        outputs={table: list(columns) for table, columns in merged_outputs.items()},
    )


def merge_schemas(
    df_extracted_schema: pd.DataFrame, df_db_schema: pd.DataFrame
) -> pd.DataFrame:
    """Matches extracted SQL dependencies with the actual database schema.

    Handles both exact schema matches and schema-agnostic matches.
    Expands wildcards ('*') to match all columns from the relevant table(s).
    Handles tables with no columns (None).

    Args:
        df_extracted_schema: Extracted table-column dependencies
        df_db_schema: Actual database schema information

    Returns:
        Merged schema with an `exact_match` flag indicating whether
        the schema name matched exactly
    """
    # Create copy to avoid modifying input
    df_extracted = df_extracted_schema.copy()
    df_extracted["exact_match"] = pd.Series(dtype="boolean")

    # Initialize empty DataFrame with correct dtypes
    df_no_columns = pd.DataFrame(
        {
            "schema": pd.Series(dtype="object"),
            "table": pd.Series(dtype="object"),
            "column": pd.Series(dtype="object"),
            "data_type": pd.Series(dtype="object"),
            "exact_match": pd.Series(dtype="boolean"),
        }
    )

    # Handle tables with no columns (None)
    if (no_columns_mask := df_extracted["column"].isna()).any():
        no_columns_deps = df_extracted.loc[no_columns_mask, ["schema", "table"]]
        df_extracted = df_extracted.loc[~no_columns_mask]

        # Exact schema match
        exact_matches = (
            no_columns_deps.dropna(subset=["schema"])
            .merge(df_db_schema[["schema", "table"]], on=["schema", "table"])
            .assign(column=None, data_type=None, exact_match=True)
        )

        # Schema-agnostic match
        schema_agnostic = no_columns_deps[no_columns_deps["schema"].isna()]
        matching_schemas = df_db_schema.merge(schema_agnostic[["table"]], on="table")[
            ["schema", "table"]
        ]
        schema_agnostic_matches = matching_schemas.assign(
            column=None, data_type=None, exact_match=False
        )

        # Combine results
        df_no_columns = pd.concat(
            [exact_matches, schema_agnostic_matches], ignore_index=True
        )

    # Expand wildcards (*) to include all relevant columns
    if (wildcard_mask := df_extracted["column"] == "*").any():
        regular_deps = df_extracted[~wildcard_mask]
        wildcard_deps = df_extracted[wildcard_mask]
        expanded_wildcard_deps = []

        for _, row in wildcard_deps.iterrows():
            mask = df_db_schema["table"] == row["table"]
            if pd.notna(row["schema"]):
                mask &= df_db_schema["schema"] == row["schema"]
                wildcard_schema = df_db_schema[mask][
                    ["schema", "table", "column"]
                ].assign(exact_match=True)
            else:
                wildcard_schema = df_db_schema[mask][
                    ["schema", "table", "column"]
                ].assign(exact_match=False)
            expanded_wildcard_deps.append(wildcard_schema)

        df_extracted = pd.concat(
            [regular_deps, *expanded_wildcard_deps], ignore_index=True
        )

    # Exact schema matches
    exact_matches = (
        df_extracted[df_extracted["schema"].notna()]
        .merge(df_db_schema, how="inner")
        .fillna({"exact_match": True})
    )

    # Schema-agnostic matches (ignoring schema column)
    schemaless_matches = (
        df_extracted[df_extracted["schema"].isna()]
        .drop(columns="schema")
        .merge(df_db_schema, how="inner")
        .fillna({"exact_match": False})
    )

    # Combine all results & remove duplicates with priority to exact matches
    df_merged_schemas = (
        pd.concat([exact_matches, schemaless_matches, df_no_columns], ignore_index=True)
        .reindex(columns=["schema", "table", "column", "data_type", "exact_match"])
        # Sort values to give priority to exact matches
        .sort_values(
            by=["schema", "table", "column", "data_type", "exact_match"],
            ascending=[True, True, True, True, False],
            na_position="last",
        )
        # Drop duplicates (keep exact matches)
        .drop_duplicates(subset=["schema", "table", "column", "data_type"])
        .reset_index(drop=True)
    )

    return df_merged_schemas


def schema_diff(
    df_extracted_schema: pd.DataFrame, df_db_schema: pd.DataFrame, copy: bool = True
) -> pd.DataFrame:
    """Checks if extracted schema entries exist in the database schema.

    Args:
        df_extracted_schema: Extracted table-column dependencies
        df_db_schema: Actual database schema information
        copy: Whether to create a copy of the input DataFrame

    Returns:
        The extracted schema with an added `match_db` flag
    """
    # Copy dataframe to avoid in-place update
    if copy:
        df_extracted_schema = df_extracted_schema.copy()

    # Create sets for quick lookup
    db_exact_matches = set(
        zip(
            df_db_schema["schema"],
            df_db_schema["table"],
            df_db_schema["column"],
            strict=False,
        )
    )
    db_table_matches = set(
        zip(df_db_schema["schema"], df_db_schema["table"], strict=False)
    )
    db_schema_agnostic = set(
        zip(df_db_schema["table"], df_db_schema["column"], strict=False)
    )
    db_table_agnostic = set(df_db_schema["table"])

    def check_existence(row: pd.Series) -> bool:
        """Helper function to determine if a row exists in the DB schema."""
        if pd.notna(row["schema"]):
            if row["column"] == "*":
                return (row["schema"], row["table"]) in db_table_matches
            return (row["schema"], row["table"], row["column"]) in db_exact_matches
        else:
            if row["column"] == "*":
                return row["table"] in db_table_agnostic
            return (row["table"], row["column"]) in db_schema_agnostic

    # Apply vectorized check
    df_extracted_schema["match_db"] = df_extracted_schema.apply(check_existence, axis=1)

    return df_extracted_schema
