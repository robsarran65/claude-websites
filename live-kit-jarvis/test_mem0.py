from dotenv import load_dotenv
from mem0 import MemoryClient
import json
import logging

load_dotenv()
user_name = "Robert"
mem0 = MemoryClient()
logging.basicConfig(level=logging.INFO)


def add_memory():
    """Add conversation messages to Mem0 for Robert."""
    try:
        messages_formatted = [
            {"role": "user", "content": "I really like Led Zeppelin."},
            {"role": "assistant", "content": "That is a good choice."},
            {"role": "user", "content": "I think so too."},
            {"role": "assistant", "content": "What is your favorite song by them?"},
        ]
        mem0.add(messages_formatted, user_id="Robert")
        logging.info("Memory added successfully for user Robert")
    except Exception as e:
        logging.error(f"Error adding memory: {e}")
        raise


def _search_and_format(query):
    """Search Mem0 for the current user and normalize the results to a JSON string."""
    results = mem0.search(query, filters={"user_id": user_name})

    # Handle different response structures
    if isinstance(results, str):
        results = json.loads(results)
    if isinstance(results, dict) and "results" in results:
        results = results["results"]

    memories = []
    for result in results:
        if isinstance(result, dict):
            memories.append(
                {
                    "memory": result.get("memory") or result.get("text") or str(result),
                    "updated_at": result.get("updated_at") or result.get("created_at"),
                }
            )
        else:
            memories.append({"memory": str(result), "updated_at": None})

    return json.dumps(memories, indent=2), len(memories)


def get_memory_by_query():
    """Search for memories by query for the current user."""
    try:
        query = f"What are {user_name}'s preferences?"
        memories_str, count = _search_and_format(query)
        logging.info(f"Found {count} memories")
        print(f"Memories: {memories_str}")
        return memories_str
    except Exception as e:
        logging.error(f"Error retrieving memory: {e}")
        raise


def delete_memory(memory_id):
    """Delete a memory by ID."""
    try:
        mem0.delete(memory_id)
        logging.info(f"Memory {memory_id} deleted successfully")
    except Exception as e:
        logging.error(f"Error deleting memory: {e}")
        raise


def update_memory(memory_id, new_content):
    """Update an existing memory."""
    try:
        mem0.update(memory_id, new_content)
        logging.info(f"Memory {memory_id} updated successfully")
    except Exception as e:
        logging.error(f"Error updating memory: {e}")
        raise


def list_all_memories():
    """Retrieve all memories by searching for a broad query."""
    try:
        # Use a broad search query to retrieve all memories
        memories_str, count = _search_and_format("Tell me everything you know")
        logging.info(f"Retrieved {count} total memories")
        print(f"All Memories: {memories_str}")
        return memories_str
    except Exception as e:
        logging.error(f"Error listing memories: {e}")
        raise


if __name__ == "__main__":
    """Main execution entry point for testing Mem0 operations."""
    logging.info("Starting Mem0 memory management demo...")

    try:
        # Add a memory
        logging.info("--- Adding Memory ---")
        add_memory()

        # Search for memories
        logging.info("--- Searching Memories ---")
        get_memory_by_query()

        # List all memories
        logging.info("--- Listing All Memories ---")
        list_all_memories()

    except Exception as e:
        logging.error(f"Demo failed: {e}")
        exit(1)

    logging.info("Demo completed successfully!")
    exit(0)
