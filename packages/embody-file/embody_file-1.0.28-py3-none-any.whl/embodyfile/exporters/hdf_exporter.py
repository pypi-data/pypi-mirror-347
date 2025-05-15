"""HDF exporter implementation."""

import logging
from pathlib import Path

import pandas as pd
from typing import Literal

from ..models import Data
from ..schemas import SchemaRegistry, DataType
from . import BaseExporter


class HDFExporter(BaseExporter):
    """Modern schema-based exporter for HDF format with consolidated output.

    Unlike ParquetExporter which creates separate files per schema,
    this exporter writes all data to a single HDF file with different
    groups for each schema.
    """

    # Define file extension for HDF files
    FILE_EXTENSION = "hdf5"

    def export(self, data: Data, output_path: Path) -> None:
        """Export data to a single HDF file with multiple datasets."""
        logging.info(f"Exporting data to HDF format: {output_path}")

        # Add extension if not present
        if output_path.suffix.lower() != f".{self.FILE_EXTENSION}":
            output_path = output_path.with_suffix(f".{self.FILE_EXTENSION}")

        # Create parent directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write mode for first schema, append mode for subsequent schemas
        mode: Literal["a", "w", "r+"] = "w"

        # Export each schema to the same file with different keys
        exported_schemas = []
        for schema in SchemaRegistry.get_schemas_for_export():
            # Skip schemas that don't match our filter
            if self._schema_filter and schema.data_type not in self._schema_filter:
                continue

            # Format data according to schema
            df = self.formatter.format_data(data, schema)

            if df.empty:
                logging.debug(f"No data to export for schema {schema.name}")
                continue

            # Export the formatted data to the HDF file
            self._export_dataframe_to_hdf(data, df, output_path, schema.name, mode)

            # Use append mode for subsequent schemas
            mode = "a"

            exported_schemas.append(schema.name)

        # Export device info as well
        if hasattr(data, "device_info") and data.device_info:
            from dataclasses import asdict

            info = {k: [v] for k, v in asdict(data.device_info).items()}
            pd.DataFrame(info).to_hdf(output_path, key="device_info", mode="a", complevel=4)
            exported_schemas.append("device_info")

        if exported_schemas:
            logging.info(f"Exported schemas {', '.join(exported_schemas)} to HDF file: {output_path}")
        else:
            logging.warning(f"No data exported to HDF file: {output_path}")

    def _export_dataframe(self, data: Data, df: pd.DataFrame, file_path: Path, schema_name: str) -> None:
        """Export a dataframe to HDF."""
        self._export_dataframe_to_hdf(data, df, file_path, schema_name, "w")

    def _export_dataframe_to_hdf(
        self, data: Data, df: pd.DataFrame, file_path: Path, schema_name: str, mode: Literal["a", "w", "r+"] = "a"
    ) -> None:
        """Export a dataframe to HDF with specified mode."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if "timestamp" in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("timestamp", inplace=True)
            df.sort_index(inplace=True)
        elif isinstance(df.index, pd.DatetimeIndex):
            df.sort_index(inplace=True)
        if schema_name == SchemaRegistry.SCHEMAS[DataType.ECG_PPG].name and data.ecg_ppg_sample_frequency:
            df.index.freq = pd.to_timedelta(1 / data.ecg_ppg_sample_frequency, unit="s")
        df.to_hdf(
            file_path,
            key=schema_name,
            mode=mode,
            format="table",
            complevel=4,
            complib="zlib",
        )
