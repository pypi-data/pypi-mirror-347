""" Just a manual test to check if the code is working
"""

import asyncio
from strata.file_manager import FileManager
from strata.backends.local_storage_backend import LocalStorageBackend
from strata.logging import trace_id_context


async def test_file_operations() -> None:
    """Test basic file operations using a local backend"""
    # Generate a unique trace ID for this test run
    trace_id = "test-123456"
    # Set the trace ID in the context
    if trace_id is not None:  # Check for non-None value
        trace_id_context.set(trace_id)  # This should be fixed if trace_id_context expects None

    # Create a FileManager instance with a LocalStorageBackend
    backend = LocalStorageBackend(config={"base_folder": "c:/tmp"})
    file_manager = FileManager()
    file_manager.register_backend(name="local", backend=backend, set_as_default=True)

    # Test the list method
    files = await file_manager.list("test_directory")
    print("Files in test_directory:", files)

    # Test the view method
    content = await file_manager.view("test_directory/test_file.txt")
    print("Content of test_file.txt:", content)

    # Test the create_file method
    new_file = await file_manager.create_file("test_directory/new_file.txt", b"Hello, World!")
    print("Created new file:", new_file)

    # Test the create_directory method
    new_directory = await file_manager.create_directory("test_directory/new_subdirectory")
    print("Created new directory:", new_directory)

    # Test the delete method
    await file_manager.delete("test_directory/new_file.txt")
    print("Deleted new_file.txt")

    # Test the move method
    moved_file = await file_manager.move("test_directory/test_file.txt", "test_directory/moved_file.txt")
    print("Moved test_file.txt to moved_file.txt:", moved_file)

    # Test the copy method
    copied_file = await file_manager.copy("test_directory/moved_file.txt", "test_directory/copied_file.txt")
    print("Copied moved_file.txt to copied_file.txt:", copied_file)


def main() -> None:
    """Main entry point for testing"""
    # Use asyncio.run to execute the async function
    asyncio.run(test_file_operations())


if __name__ == "__main__":
    main()
