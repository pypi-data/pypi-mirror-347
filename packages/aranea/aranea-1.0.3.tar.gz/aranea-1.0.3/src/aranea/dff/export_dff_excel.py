"""
Module to export pandas dataframes created by build_tabular_diff_representation as formatted excel 
files.
The Excel output is organized into sections:
- Added Networks: Networks that exist in the newer graph but not in the older one
- Removed Networks: Networks that exist in the older graph but not in the newer one
- Changed Networks: Networks present in both graphs but with differences in structure
Each section contains detailed information about network components, with visual indicators:
- Green background: Components added in the newer graph
- Red background: Components removed in the newer graph
- Grey background: Components present in both graphs
"""

import logging
import os
from typing import Any

import pandas as pd
from xlsxwriter.format import Format
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from aranea.dff.build_tabular_diff_representation import (
    DiffClassification, build_tabular_diff_representation)
from aranea.dff.get_graph_diff import GraphDiffResult
from aranea.models.graph_model import Graph

logger: logging.Logger = logging.getLogger(__name__)


def export_dff_excel(
    diff_result: GraphDiffResult,
    graph_1: Graph,
    graph_2: Graph,
    output_dir: str,
    output_file_name: str,
) -> None:
    """
    Exports the given diff result as excel file if 'to_excel' is set.
    The name and path of the file are the same as the graph output.

    :param diff_result: The result of get_graph_diff() containing the differences between two graphs
    :type diff_result: GraphDiffResult
    :param graph_1: The graph which is viewed as newer in diff_result.
    :type graph_1: Graph
    :param graph_2: The graph which is viewed as older in diff_result.
    :type graph_2: Graph
    :output_dir: Where the excel file should be saved
    :output_dir: str
    :param output_file_name: The name of the output file.
    :type output_file_name: str

    :rtype: None
    """
    logger.debug("---Starting the generation of dff tabular output ---")

    diff_dataframe = build_tabular_diff_representation(diff_result, graph_1, graph_2)
    if diff_dataframe is None:
        logger.warning("No differences found between the two graphs.")
        logger.warning("No output produced!")
        return

    excel_file_path: str = os.path.join(output_dir, output_file_name + ".xlsx")

    with pd.ExcelWriter(excel_file_path, engine="xlsxwriter") as writer:
        # Get the workbook and worksheet objects
        workbook: Workbook = writer.book  # type: ignore
        worksheet: Worksheet = workbook.add_worksheet("Graph Differences")
        writer.sheets["Graph Differences"] = worksheet

        # Define formats
        formats = {
            "section_header": workbook.add_format({"bold": True, "font_size": 18, "border": 0}),
            "header": workbook.add_format(
                {"bold": True, "bg_color": "#83CCEB", "align": "top", "border": 1}  # Light blue
            ),
            "subheader": workbook.add_format(
                {"bold": True, "bg_color": "#44B3E1", "align": "center", "border": 1}  # blue
            ),
            "added": workbook.add_format(
                {"bg_color": "#92D050", "border": 1, "align": "top"}  # Light green
            ),
            "removed": workbook.add_format(
                {"bg_color": "#FF8989", "border": 1, "align": "top"}  # Light salmon
            ),
            "both_graphs": workbook.add_format(
                {"bg_color": "#D9D9D9", "border": 1, "align": "top"}  # Light grey
            ),
            "regular": workbook.add_format({"border": 1, "align": "top"}),
        }

        # Write key legend in max column of dataframe + 2
        max_col = len(diff_dataframe.columns)
        legend_col = max_col + 1
        worksheet.write(0, legend_col, "Key", formats["header"])
        worksheet.write(1, legend_col, "ECU new in graph 1", formats["added"])
        worksheet.write(2, legend_col, "ECU removed in graph 1", formats["removed"])
        worksheet.write(3, legend_col, "ECU present in both graphs", formats["both_graphs"])

        # Separate diff sections based on network diff class
        added_networks = diff_dataframe[
            diff_dataframe["nw_diff_class"] == DiffClassification.ADDED.value
        ].copy()
        removed_networks = diff_dataframe[
            diff_dataframe["nw_diff_class"] == DiffClassification.REMOVED.value
        ].copy()
        changed_networks = diff_dataframe[
            diff_dataframe["nw_diff_class"] == DiffClassification.CHANGED.value
        ].copy()

        current_row = 0

        if not added_networks.empty:
            current_row = write_excel_section(
                worksheet, "Added Networks", added_networks, formats, current_row
            )
        if not removed_networks.empty:
            current_row = write_excel_section(
                worksheet, "Removed Networks", removed_networks, formats, current_row
            )
        if not changed_networks.empty:
            current_row = write_excel_section(
                worksheet, "Changed Networks", changed_networks, formats, current_row
            )

        # Auto adjust column widths for the diff table based on its contents
        for idx, col in enumerate(diff_dataframe.columns):
            # Initialize max_length with column header length
            max_length = len(str(col))
            # Check each cell in the column
            for cell in diff_dataframe[col]:
                cell: Any = cell
                cell_str = str(cell)
                max_length = max(len(cell_str), max_length)
            worksheet.set_column(idx, idx, max_length)

    # ExcelWriter context automatically saves the file.
    logger.debug("Excel file saved to %s", excel_file_path)


def write_excel_section(
    worksheet: Worksheet,
    section_title: str,
    df: pd.DataFrame,
    formats: dict[str, Format],
    start_row: int,
) -> int:
    """
    Write a section of the Excel file with proper formatting beginning at the given start_row.
    The section consists of a header, subheader, and the data from the DataFrame.
    Formats is expected to contain formats for the following keys:
    - "section_header": Format for the section header
    - "header": Format for the column headers
    - "subheader": Format for the subheader
    - "added": Format for added components
    - "removed": Format for removed components
    - "both_graphs": Format for components present in both graphs
    - "regular": Format for regular components
    Returns the row after the last row written in the section.

    :param worksheet: The Worksheet to write a section to
    :type worksheet: Worksheet
    :param section_title: Title of the section, gets inserted above the data of the Dataframe
    :type section_title: str
    :param df: The DataFrame containing the data to write
    :type df: pandas.DataFrame
    :param formats: Dictionary containing XLSX formatting objects
    :type formats: dict[str, Format]
    :param start_row: The row to start writing the section at
    :type start_row: int

    :return: The row after the last row written in the section
    :rtype: int
    """
    num_cols = len(df.columns)
    # Write section header spanning all columns
    worksheet.merge_range(
        start_row, 0, start_row, num_cols - 1, section_title, formats["section_header"]
    )
    start_row += 1

    # Write subheader
    worksheet.merge_range(
        start_row, 2, start_row, num_cols - 1, "connected components", formats["subheader"]
    )
    start_row += 1

    # Write column headers from the DataFrame
    headers = df.columns.tolist()
    for col, header in enumerate(headers):
        worksheet.write(start_row, col, header, formats["header"])
    start_row += 1

    # Group the DataFrame by the "label" column for merging purposes
    grouped_df = df.groupby("label", dropna=False)  # type: ignore

    current_row = start_row
    for label, group in grouped_df:
        group = group.reset_index(drop=True)
        num_rows = len(group)

        # Write the "label" column in merged cells if there are multiple rows for the same label
        if pd.notna(label):
            if num_rows > 1:
                worksheet.merge_range(
                    current_row, 0, current_row + num_rows - 1, 0, label, formats["regular"]
                )
            else:
                worksheet.write(current_row, 0, label, formats["regular"])

        # Handle the "network type" column (assumed to be the second column)
        network_type = group["network type"].iat[0]  # type: ignore
        if pd.notna(network_type):  # type: ignore
            if num_rows > 1:
                worksheet.merge_range(
                    current_row, 1, current_row + num_rows - 1, 1, network_type, formats["regular"]
                )
            else:
                worksheet.write(current_row, 1, network_type, formats["regular"])

        # Write the rest of the columns (starting from index 2) for each row in the group
        for idx, (_, row) in enumerate(group.iterrows()):  # type: ignore
            # Determine formatting based on the comp_diff_class column if available
            row_format = formats["regular"]
            if pd.notna(row.get("comp_diff_class")):  # type: ignore
                if row["comp_diff_class"] == DiffClassification.ADDED.value:
                    row_format = formats["added"]
                elif row["comp_diff_class"] == DiffClassification.REMOVED.value:
                    row_format = formats["removed"]
            else:
                row_format = formats["both_graphs"]

            for col, field in enumerate(df.columns[2:]):
                value = row[field]  # type: ignore
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value)  # type: ignore
                worksheet.write(current_row + idx, col + 2, value, row_format)
        current_row += num_rows

    # Leave a blank row after the section
    current_row += 1

    return current_row
