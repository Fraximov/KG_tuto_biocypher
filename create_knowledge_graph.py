#!/usr/bin/env python3
"""
BioCypherWorkshop Tutorial Knowledge Graph - A beginner-friendly BioCypher project for learning how to build and extend a small knowledge graph from multiple data sources.

This script creates a knowledge graph using BioCypher and the ProteinInteractionAdapter.
"""

import logging

from biocypher import (
    BioCypher,
    FileDownload,
)
from biocypher_tutorial_kg.adapters.protein_interaction_adapter import ProteinInteractionAdapter


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#-------------------- DATASET URLS --------------------#
PROTEIN_INTERACTION_DATASET = (
    "https://zenodo.org/records/16902349/files/synthetic_protein_interactions.tsv"
)

#--------------------------------------------------------
#-------------------- MAIN FUNCTION ---------------------
#--------------------------------------------------------
def main():
    """Main function to create the knowledge graph."""
    logger.info("Starting BioCypherWorkshop Tutorial Knowledge Graph knowledge graph creation")
    
    # Initialize BioCypher
    bc = BioCypher(
        biocypher_config_path="config/biocypher_config.yaml",
        schema_config_path="config/schema_config.yaml"
    )

    # Step 1: Download protein interaction resource.
    #
    # Why this matters:
    #   You explicitly fetch the data this adapter will consume.
    #   Each resource is named and its purpose is clear.
    #
    # Hint:
    #   Use FileDownload to specify the dataset, then bc.download() to fetch.
    #   Extract the first (and only) file from the returned list.
    # ---------- YOUR CODE STARTS HERE ----------
    protein_interaction_file = bc.download(
        FileDownload(
            name="synthetic_protein_interactions",
            url_s=PROTEIN_INTERACTION_DATASET,
        )
    )[0]
    logger.info("Downloaded protein interactions: %s", protein_interaction_file)
    # ---------- YOUR CODE ENDS HERE ----------

    # Step 2: Create the ProteinInteractionAdapter.
    #
    # Why this matters:
    #   You instantiate the adapter with the exact resource it will consume.
    #   No ambiguity about which file goes to which adapter.
    #
    # Hint:
    #   Pass the downloaded file path directly to the adapter.
    # ---------- YOUR CODE STARTS HERE ----------
    protein_interaction_adapter = ProteinInteractionAdapter(
        data_source=protein_interaction_file
    )
    # ---------- YOUR CODE ENDS HERE ----------

    # Step 3: Collect all adapters.
    #
    # Why this matters:
    #   A single list makes it easy to add more adapters later.
    #   Each new adapter simply gets another line here.
    #
    # Hint:
    #   Add more adapter instances as you expand the KG.
    # ---------- YOUR CODE STARTS HERE ----------
    adapters = [
        protein_interaction_adapter,
        # Add more adapters here as you expand the KG
    ]
    # ---------- YOUR CODE ENDS HERE ----------

    # Step 4: Feed all adapters into BioCypher.
    #
    # Why this matters:
    #   One loop processes all adapters uniformly.
    #
    # Hint:
    #   Iterate and call write_nodes/write_edges for each.
    # ---------- YOUR CODE STARTS HERE ----------
    logger.info("Creating knowledge graph...")
    for adapter in adapters:
        bc.write_nodes(adapter.get_nodes())
        bc.write_edges(adapter.get_edges())
    # ---------- YOUR CODE ENDS HERE ----------
    
    logger.info("Knowledge graph creation completed successfully!")

    # Write import call
    bc.write_import_call()

    # Print summary
    # bc.summary() 


if __name__ == "__main__":
    main()
