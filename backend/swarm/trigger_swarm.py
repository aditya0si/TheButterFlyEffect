"""
Trigger Swarm Ingestion Runner.
Executes the full 500-book biomedical ingestion swarm across all 25-30 subagents upon the 'GO' command.
"""

import asyncio
import sys
import time
from .ingestion_pool import IngestionSwarmPool
from .corpus_catalog import get_total_book_count

def cli_progress_bar(domain: str, current: int, total: int):
    percent = (current / total) * 100
    bar_length = 30
    filled = int(bar_length * current // total)
    bar = "=" * filled + "-" * (bar_length - filled)
    sys.stdout.write(f"\r[Subagent Swarm] [{bar}] {percent:.1f}% ({current}/{total} vols) | Current: {domain[:32]}...")
    sys.stdout.flush()

async def main():
    print("=" * 75)
    print("  ANTIGRAVITY BIOMEDICAL CONSTELLATION - AGENT SWARM INGESTION ENGINE")
    print(f"  Target Corpus: {get_total_book_count()} Medical Books & Treatises")
    print("  Worker Subagents: 25 Parallel Instances (Gemini 3.5 High)")
    print("  Embedded Storage: Local SQLite Graph Store + LanceDB Vector Index")
    print("=" * 75)
    
    start_time = time.time()
    pool = IngestionSwarmPool(db_path="biomed_graph.db", worker_count=25)
    
    result = await pool.run_full_swarm_ingestion(progress_callback=cli_progress_bar)
    
    elapsed = time.time() - start_time
    print(f"\n\n[SUCCESS] Ingestion completed in {elapsed:.2f} seconds.")
    print(f" -> Total Volumes Ingested: {result['total_books_ingested']}")
    print(f" -> Graph Nodes Indexed:    {result['nodes_indexed']}")
    print(f" -> Graph Edges Indexed:    {result['edges_indexed']}")
    print(f" -> 3D Constellation Cache: {result['export_file']}")
    print("=" * 75)

if __name__ == "__main__":
    asyncio.run(main())
