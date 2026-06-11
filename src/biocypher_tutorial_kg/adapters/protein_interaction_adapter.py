"""
ProteinInteractionAdapter Adapter

This adapter handles protein interaction TSV data for BioCypher.
"""

import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


class ProteinInteractionAdapter:
    """
    Adapter for protein interaction TSV data source.

    This adapter implements the BioCypher adapter interface and is intentionally
    scaffolded as a workshop exercise.
    """
    
    def __init__(self, data_source: str | Path, **kwargs):
        """
        Initialize the adapter.

        Args:
            data_source: Path to the TSV data source
            **kwargs: Additional configuration parameters
        """
        self.data_source = data_source
        self.config = kwargs
        logger.info(
            "Initialized ProteinInteractionAdapter with data source: %s", data_source
        )
        
    def get_nodes(self):
        """
        Extract nodes from the data source.

        Yields:
            Tuples of (node_id, node_label, properties) for each node.
        """
        logger.info("Extracting nodes from data source")

        # BioCypher node tuple format:
        # (node_id, node_label, properties)


        # Step 1: Read the interaction TSV into a DataFrame.
        #
        # Why this matters:
        #   The adapter operates row-wise and needs a tabular structure
        #   before it can build BioCypher node tuples.
        #
        # Hint:
        #   Use pd.read_csv(self.data_source, sep="\t").
        # ---------- YOUR CODE STARTS HERE ----------
        df = pd.read_csv(self.data_source, sep="\t")
        # ---------- YOUR CODE ENDS HERE ----------
      
        
        # Step 2.1: Build the source-side Protein table.
        #
        # Why this matters:
        #   Each interaction row has a source protein that must become a node.
        #
        # Hint:
        #   Select source-side columns and rename to:
        #     - node_id
        #     - genesymbol
        #     - ncbi_tax_id
        #     - entity_type
        # ---------- YOUR CODE STARTS HERE ----------
        source_nodes = df[
                    ["source", "source_genesymbol", "ncbi_tax_id_source", "entity_type_source"]
        ].copy()
        source_nodes = source_nodes.rename(
            columns={
                "source": "node_id",
                "source_genesymbol": "genesymbol",
                "ncbi_tax_id_source": "ncbi_tax_id",
                "entity_type_source": "entity_type",
            }
        )
        # ---------- YOUR CODE ENDS HERE ----------
        

        # Step 2.2: Build the target-side Protein table.
        #
        # Why this matters:
        #   The target protein is also a node and must be included.
        #
        # Hint:
        #   Mirror Step 2.1 using target-side columns, then rename
        #   to the same common schema.
        # ---------- YOUR CODE STARTS HERE ----------
        target_nodes = df[
            ["target", "target_genesymbol", "ncbi_tax_id_target", "entity_type_target"]
        ].copy()
        target_nodes = target_nodes.rename(
            columns={
                "target": "node_id",
                "target_genesymbol": "genesymbol",
                "ncbi_tax_id_target": "ncbi_tax_id",
                "entity_type_target": "entity_type",
            }
        )
        # ---------- YOUR CODE ENDS HERE ----------



        # Step 2.3: Merge source-side and target-side proteins.
        #
        # Why this matters:
        #   A single unified table simplifies downstream node emission.
        #
        # Hint:
        #   Use pd.concat([source_nodes, target_nodes], ignore_index=True).
        # ---------- YOUR CODE STARTS HERE ----------
        proteins_df = pd.concat([source_nodes, target_nodes], ignore_index=True)
        # ---------- YOUR CODE ENDS HERE ----------



        # Step 2.4: Remove duplicate proteins by node_id.
        #
        # Why this matters:
        #   The same protein can appear in many interactions and should only
        #   exist once as a node.
        #
        # Hint:
        #   Use drop_duplicates(subset=["node_id"]).
        # ---------- YOUR CODE STARTS HERE ----------
        proteins_df = proteins_df.drop_duplicates(subset=["node_id"])
        # ---------- YOUR CODE ENDS HERE ----------


        # Step 3: Yield nodes in BioCypher format.
        #
        # Why this matters:
        #   BioCypher expects node tuples in this exact shape:
        #   (node_id, node_label, properties).
        #
        # Hint:
        #   Use label "uniprot_protein" and build properties with:
        #     - genesymbol
        #     - ncbi_tax_id
        #     - entity_type
        #   Cast IDs/taxonomy fields to str for consistency.
        # ---------- YOUR CODE STARTS HERE ----------
        
        # ---------- YOUR CODE ENDS HERE ----------

        
    
    def get_edges(self):
        """
        Extract edges from the data source.

        Yields:
            Tuples of (edge_id, source_id, target_id, edge_label, properties)
            for each edge.
        """
        logger.info("Extracting edges from data source")

        # BioCypher edge tuple format:
        # (edge_id, source_id, target_id, edge_label, properties)

        # Step 1: Read the interaction TSV into a DataFrame.
        #
        # Why this matters:
        #   Each row represents one interaction and is the source for
        #   one BioCypher edge tuple.
        #
        # Hint:
        #   Use pd.read_csv(self.data_source, sep="\t").
        # ---------- YOUR CODE STARTS HERE ----------

        # ---------- YOUR CODE ENDS HERE ----------

        # Step 2.1: Iterate over interaction rows.
        #
        # Why this matters:
        #   Each row in the table should produce one edge tuple.
        #
        # Hint:
        #   Use a row iterator and extract values from each row.
        # ---------- YOUR CODE STARTS HERE ----------

        # ---------- YOUR CODE ENDS HERE ----------

        # Step 2.2: Extract normalized edge identifiers.
        #
        # Why this matters:
        #   Stable and consistent identifiers make the graph easier
        #   to validate and debug.
        #
        # Hint:
        #   Build:
        #     - source_id from row["source"]
        #     - target_id from row["target"]
        #     - interaction_type from row["type"]
        #   Cast to str.
        # ---------- YOUR CODE STARTS HERE ----------

        # ---------- YOUR CODE ENDS HERE ----------

        # Step 2.3: Build a deterministic edge_id.
        #
        # Why this matters:
        #   A predictable edge_id makes tracing and dedup checks easier.
        #
        # Hint:
        #   Use f"{source_id}_{target_id}_{interaction_type}".
        # ---------- YOUR CODE STARTS HERE ----------

        # ---------- YOUR CODE ENDS HERE ----------

        # Step 2.4: Build edge properties from interaction flags.
        #
        # Why this matters:
        #   Flags carry biological meaning and should be preserved
        #   as edge-level attributes.
        #
        # Hint:
        #   Include these keys and convert values to bool:
        #     - is_directed
        #     - is_stimulation
        #     - is_inhibition
        #     - consensus_direction
        #     - consensus_stimulation
        #     - consensus_inhibition
        # ---------- YOUR CODE STARTS HERE ----------

        # ---------- YOUR CODE ENDS HERE ----------

        # Step 3: Yield edges in BioCypher format.
        #
        # Why this matters:
        #   BioCypher expects edge tuples in this exact shape:
        #   (edge_id, source_id, target_id, edge_label, properties).
        #
        # Hint:
        #   Use interaction_type as edge_label and emit one tuple per row.
        #   Optional: skip malformed rows missing source/target/type.
        # ---------- YOUR CODE STARTS HERE ----------

        # ---------- YOUR CODE ENDS HERE ----------

    
    def get_metadata(self) -> dict[str, Any]:
        """
        Get metadata about the data source.

        Returns:
            Dictionary containing metadata
        """
        return {
            "name": "ProteinInteractionAdapter",
            "data_source": str(self.data_source),
            "data_type": "tsv",
            "version": "0.1.0",
            "adapter_class": "ProteinInteractionAdapter",
        }
    
    def validate_data_source(self) -> bool:
        """
        Validate that the TSV data source is accessible and properly formatted.

        Returns:
            True if data source is valid, False otherwise
        """
        try:
            data_path = Path(self.data_source)
            if not data_path.exists() or not data_path.is_file():
                return False

            # Read one row to validate TSV format and required columns.
            df = pd.read_csv(data_path, sep="\t", nrows=1)
            required_columns = {"source", "target"}
            return required_columns.issubset(df.columns)

        except (OSError, ValueError, pd.errors.ParserError) as exc:
            logger.exception("Data source validation failed: %s", exc)
            return False
