"""Tests for the command-line interface."""

import os
from pathlib import Path
from typer.testing import CliRunner
import pytest
from unittest.mock import patch, MagicMock
from kwargify_core.cli import app, get_version
from kwargify_core.core.workflow import Workflow
from kwargify_core.core.block import Block
from kwargify_core.registry import WorkflowRegistry, WorkflowRegistryError
from datetime import datetime
import toml
import os


@pytest.fixture
def in_memory_registry():
    """Fixture providing an in-memory workflow registry."""
    return WorkflowRegistry(":memory:")


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


def test_version_display(runner):
    """Test that --version displays the correct version."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Kwargify CLI Version:" in result.stdout


def test_help_display(runner):
    """Test that help text is displayed correctly."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "kwargify" in result.stdout.lower()
    assert "Define, run, and manage workflows" in result.stdout


def test_no_args_shows_help(runner):
    """Test that running CLI without arguments shows help."""
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "usage:" in result.stdout.lower()
    assert "--help" in result.stdout


def test_version_function():
    """Test the version retrieval function."""
    version = get_version()
    assert isinstance(version, str)
    assert version != ""  # Should not be empty


@pytest.fixture
def workflow_with_cycle(tmp_path):
    """Create a workflow file with circular dependencies."""
    content = '''
from kwargify_core.core.workflow import Workflow
from kwargify_core.core.block import Block

class SimpleBlock(Block):
    def run(self) -> None:
        self.outputs = {"result": "success"}

def get_workflow():
    workflow = Workflow()
    workflow.name = "cycle_test"
    
    block1 = SimpleBlock(name="block1")
    block2 = SimpleBlock(name="block2")
    
    # Create a cycle
    block1.add_dependency(block2)
    block2.add_dependency(block1)
    
    workflow.add_block(block1)
    workflow.add_block(block2)
    return workflow
'''
    file_path = tmp_path / "cycle_workflow.py"
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


@pytest.fixture
def workflow_with_missing_dep(tmp_path):
    """Create a workflow file with missing dependencies."""
    content = '''
from kwargify_core.core.workflow import Workflow
from kwargify_core.core.block import Block

class SimpleBlock(Block):
    def run(self) -> None:
        self.outputs = {"result": "success"}

def get_workflow():
    workflow = Workflow()
    workflow.name = "missing_dep_test"
    
    block1 = SimpleBlock(name="block1")
    block2 = SimpleBlock(name="block2")
    
    # Add dependency but don't add block2 to workflow
    block1.add_dependency(block2)
    
    workflow.add_block(block1)
    return workflow
'''
    file_path = tmp_path / "missing_dep_workflow.py"
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


@patch("kwargify_core.cli.SQLiteLogger")
def test_run_with_resume_options(mock_logger_class, runner, valid_workflow_file):
    """Test running a workflow with resume options."""
    mock_logger_instance = mock_logger_class.return_value
    mock_logger_instance.get_run_details.return_value = {
        "run_id": "123",
        "workflow_name": "test_workflow",
        "start_time": "2025-01-01 10:00:00",
        "end_time": "2025-01-01 10:05:00",
        "status": "COMPLETED",
        "blocks": [{"block_name": "test_block", "status": "COMPLETED", "start_time": "2025-01-01 10:00:00", "end_time": "2025-01-01 10:01:00", "inputs": {}, "outputs": {}, "error_message": None, "retries_attempted": 0}]
    }

    with patch("kwargify_core.cli.load_workflow_from_py") as mock_load_workflow:
        mock_workflow = MagicMock()
        mock_workflow.name = "test_workflow"
        mock_load_workflow.return_value = mock_workflow
        mock_workflow.run.return_value = None # Mock the run method

        result = runner.invoke(app, [
            "run",
            str(valid_workflow_file),
            "--resume-id", "123",
            "--resume-after", "test_block"
        ])

        mock_load_workflow.assert_called_once_with(str(valid_workflow_file))
        mock_workflow.run.assert_called_once_with(
            workflow_version_id=None,
            resume_from_run_id="123",
            resume_after_block_name="test_block"
        )

    assert result.exit_code == 0
    assert "Loading workflow from:" in result.stdout
    assert "Starting workflow: test_workflow" in result.stdout
    assert "Attempting to resume from block: test_block" in result.stdout
    assert "Resumed Run ID: 123" in result.stdout


@patch("kwargify_core.cli.SQLiteLogger")
@patch("kwargify_core.cli.load_workflow_from_py")
def test_run_resume_id_without_after(mock_load_workflow, mock_logger_class, runner, valid_workflow_file):
    """Test that providing resume-id without resume-after automatically resumes after the last successful block."""
    mock_logger_instance = mock_logger_class.return_value
    mock_logger_instance.get_run_details.return_value = {
        "run_id": "123",
        "workflow_name": "test_workflow",
        "start_time": "2025-01-01 10:00:00",
        "end_time": "2025-01-01 10:05:00",
        "status": "FAILED", # Simulate a failed run that can be resumed
        "blocks": [
            {"block_name": "block1", "status": "COMPLETED", "start_time": "2025-01-01 10:00:00", "end_time": "2025-01-01 10:01:00", "inputs": {}, "outputs": {}, "error_message": None, "retries_attempted": 0},
            {"block_name": "block2", "status": "FAILED", "start_time": "2025-01-01 10:02:00", "end_time": "2025-01-01 10:03:00", "inputs": {}, "outputs": {}, "error_message": "Error", "retries_attempted": 0}
        ]
    }

    mock_workflow = MagicMock()
    mock_workflow.name = "test_workflow"
    mock_load_workflow.return_value = mock_workflow
    mock_workflow.run.return_value = None # Mock the run method

    result = runner.invoke(app, [
        "run",
        str(valid_workflow_file),
        "--resume-id", "123"
    ])

    mock_logger_instance.get_run_details.assert_called_once_with("123")
    mock_load_workflow.assert_called_once_with(str(valid_workflow_file))
    mock_workflow.run.assert_called_once_with(
        workflow_version_id=None,
        resume_from_run_id="123",
        resume_after_block_name="block1" # Should resume after the last completed block
    )

    assert result.exit_code == 0
    assert "Loading workflow from:" in result.stdout
    assert "Starting workflow: test_workflow" in result.stdout
    assert "Auto-resuming after last successful block: block1" in result.stdout
    assert "Resumed Run ID: 123" in result.stdout
    assert "Workflow completed successfully" in result.stdout # Assuming the mocked run completes successfully


def test_run_resume_after_without_id(runner, valid_workflow_file):
    """Test that providing resume-after without resume-id fails."""
    result = runner.invoke(app, [
        "run",
        str(valid_workflow_file),
        "--resume-after", "block1"
    ])
    assert result.exit_code == 1
    assert "--resume-after requires --resume-id" in result.stdout


def test_validate_valid_workflow(runner, valid_workflow_file):
    """Test validating a valid workflow."""
    result = runner.invoke(app, ["validate", str(valid_workflow_file)])
    assert result.exit_code == 0
    assert "Workflow validation successful!" in result.stdout
    assert "test_workflow" in result.stdout


def test_validate_workflow_with_cycle(runner, workflow_with_cycle):
    """Test validating a workflow with circular dependencies."""
    result = runner.invoke(app, ["validate", str(workflow_with_cycle)])
    assert result.exit_code == 1
    assert "Validation Error" in result.stdout
    assert "Circular dependency" in result.stdout


def test_validate_workflow_with_missing_dep(runner, workflow_with_missing_dep):
    """Test validating a workflow with missing dependencies."""
    result = runner.invoke(app, ["validate", str(workflow_with_missing_dep)])
    assert result.exit_code == 1
    assert "Validation Error" in result.stdout
    assert "Missing dependencies" in result.stdout


def test_validate_nonexistent_file(runner):
    """Test validating a non-existent workflow file."""
    result = runner.invoke(app, ["validate", "nonexistent.py"])
    assert result.exit_code == 2  # Typer's error code for invalid arguments
    assert "does not exist" in result.stdout.lower()


def test_run_file_based_workflow(runner, valid_workflow_file):
    """Test running a workflow directly from file."""
    result = runner.invoke(app, ["run", str(valid_workflow_file)])
    assert result.exit_code == 0
    assert "Loading workflow from:" in result.stdout
    assert "Starting workflow: test_workflow" in result.stdout
    assert "Workflow completed successfully" in result.stdout


@patch("kwargify_core.cli.WorkflowRegistry")
def test_run_registered_workflow(mock_registry, runner, valid_workflow_file, in_memory_registry):
    mock_registry.return_value = in_memory_registry
    """Test running a workflow by name from registry."""
    # First register the workflow
    runner.invoke(app, ["register", str(valid_workflow_file)])
    
    # Then run it by name
    result = runner.invoke(app, ["run", "--name", "test_workflow"])
    assert result.exit_code == 0
    assert "Loading registered workflow:" in result.stdout
    assert "Version: 1" in result.stdout
    assert "Workflow completed successfully" in result.stdout


@patch("kwargify_core.cli.WorkflowRegistry")
def test_run_specific_version(mock_registry, runner, valid_workflow_file, complex_workflow_file, in_memory_registry):
    mock_registry.return_value = in_memory_registry
    """Test running a specific version of a registered workflow."""
    # Register two versions
    runner.invoke(app, ["register", str(valid_workflow_file)])
    runner.invoke(app, ["register", str(complex_workflow_file)])
    
    # Run version 1 specifically
    result = runner.invoke(app, ["run", "--name", "test_workflow", "--version", "1"])
    assert result.exit_code == 0
    assert "Version: 1" in result.stdout
    assert "Workflow completed successfully" in result.stdout


def test_run_nonexistent_workflow(runner):
    """Test running a non-existent registered workflow."""
    result = runner.invoke(app, ["run", "--name", "nonexistent"])
    assert result.exit_code == 1
    assert "Error loading workflow:" in result.stdout


def test_run_invalid_version(runner, valid_workflow_file):
    """Test running a non-existent version of a workflow."""
    # Register workflow
    runner.invoke(app, ["register", str(valid_workflow_file)])
    
    # Try to run non-existent version
    result = runner.invoke(app, ["run", "--name", "test_workflow", "--version", "999"])
    assert result.exit_code == 1
    assert "Error loading workflow:" in result.stdout


def test_run_missing_source_file(runner, valid_workflow_file, tmp_path):
    """Test running a registered workflow whose source file was moved/deleted."""
    # Register workflow
    runner.invoke(app, ["register", str(valid_workflow_file)])
    
    # Move the source file to simulate deletion/move
    new_path = tmp_path / "moved_workflow.py"
    valid_workflow_file.rename(new_path)
    
    # Try to run the workflow
    result = runner.invoke(app, ["run", "--name", "test_workflow"])
    assert result.exit_code == 1
    assert "Source file" in result.stdout
    assert "not found" in result.stdout


def test_run_mutually_exclusive_args(runner, valid_workflow_file):
    """Test that file path and name cannot be used together."""
    result = runner.invoke(app, [
        "run",
        str(valid_workflow_file),
        "--name", "test_workflow"
    ])
    assert result.exit_code == 1
    assert "Cannot provide both" in result.stdout


@patch("kwargify_core.cli.WorkflowRegistry")
def test_register_workflow(mock_registry, runner, valid_workflow_file, in_memory_registry):
    mock_registry.return_value = in_memory_registry
    """Test registering a valid workflow."""
    result = runner.invoke(app, ["register", str(valid_workflow_file)])
    assert result.exit_code == 0
    assert "Workflow registered successfully!" in result.stdout
    assert "test_workflow" in result.stdout


@patch("kwargify_core.cli.WorkflowRegistry")
def test_register_with_description(mock_registry, runner, valid_workflow_file, in_memory_registry):
    mock_registry.return_value = in_memory_registry
    """Test registering a workflow with description."""
    result = runner.invoke(app, [
        "register",
        str(valid_workflow_file),
        "--description",
        "Test description"
    ])
    assert result.exit_code == 0
    assert "Workflow registered successfully!" in result.stdout


@patch("kwargify_core.cli.WorkflowRegistry")
def test_register_nonexistent_file(mock_registry, runner, in_memory_registry):
    mock_registry.return_value = in_memory_registry
    """Test registering a non-existent workflow file."""
    result = runner.invoke(app, ["register", "nonexistent.py"])
    assert result.exit_code == 2  # Typer's error code for invalid arguments
    assert "does not exist" in result.stdout.lower()


@patch("kwargify_core.cli.WorkflowRegistry")
def test_list_workflows_empty(mock_registry, runner, in_memory_registry):
    mock_registry.return_value = in_memory_registry
    """Test listing workflows when none are registered."""
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Registered Workflows" in result.stdout


@patch("kwargify_core.cli.WorkflowRegistry")
def test_list_workflows(mock_registry, runner, valid_workflow_file, in_memory_registry):
    mock_registry.return_value = in_memory_registry
    """Test listing workflows after registration."""
    # First register a workflow
    runner.invoke(app, ["register", str(valid_workflow_file)])
    
    # Then list workflows
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "test_workflow" in result.stdout
    assert "Version" in result.stdout


@patch("kwargify_core.cli.WorkflowRegistry")
def test_list_workflow_versions(mock_registry, runner, valid_workflow_file, in_memory_registry):
    mock_registry.return_value = in_memory_registry
    """Test listing versions of a specific workflow."""
    # First register the workflow
    runner.invoke(app, ["register", str(valid_workflow_file)])
    
    # Then list its versions
    result = runner.invoke(app, ["list", "--name", "test_workflow"])
    assert result.exit_code == 0
    assert "Versions of Workflow: test_workflow" in result.stdout
    assert "Version" in result.stdout


@patch("kwargify_core.cli.WorkflowRegistry")
def test_list_nonexistent_workflow(mock_registry, runner, in_memory_registry):
    mock_registry.return_value = in_memory_registry
    """Test listing versions of a non-existent workflow."""
    result = runner.invoke(app, ["list", "--name", "nonexistent"])
    assert result.exit_code == 1
    assert "Error" in result.stdout


def test_show_workflow_summary(runner, valid_workflow_file):
    """Test showing workflow summary."""
    result = runner.invoke(app, ["show", str(valid_workflow_file)])
    assert result.exit_code == 0
    assert "Workflow Summary" in result.stdout
    assert "test_workflow" in result.stdout
    assert "test_block" in result.stdout
    assert "Total Blocks: 1" in result.stdout
    assert "Execution Order" in result.stdout


def test_show_workflow_diagram(runner, valid_workflow_file):
    """Test showing workflow Mermaid diagram."""
    result = runner.invoke(app, ["show", "--diagram", str(valid_workflow_file)])
    assert result.exit_code == 0
    assert "```mermaid" in result.stdout
    assert "graph TD" in result.stdout
    assert "test_block" in result.stdout


@pytest.fixture
def complex_workflow_file(tmp_path):
    """Create a workflow file with multiple blocks and dependencies."""
    content = '''
from kwargify_core.core.workflow import Workflow
from kwargify_core.core.block import Block

class SimpleBlock(Block):
    def run(self) -> None:
        self.outputs = {"result": "success"}

def get_workflow():
    workflow = Workflow()
    workflow.name = "complex_workflow"
    
    block1 = SimpleBlock(name="block1", config={"param": "value1"})
    block2 = SimpleBlock(name="block2", config={"param": "value2"})
    block3 = SimpleBlock(name="block3")
    
    block3.add_dependency(block1)
    block3.add_dependency(block2)
    
    block3.input_map = {
        "input1": (block1, "result"),
        "input2": (block2, "result")
    }
    
    workflow.add_block(block1)
    workflow.add_block(block2)
    workflow.add_block(block3)
    return workflow
'''
    file_path = tmp_path / "complex_workflow.py"
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


def test_show_complex_workflow(runner, complex_workflow_file):
    """Test showing summary of a complex workflow."""
    result = runner.invoke(app, ["show", str(complex_workflow_file)])
    assert result.exit_code == 0
    
    # Check workflow details
    assert "complex_workflow" in result.stdout
    assert "Total Blocks: 3" in result.stdout
    
    # Check block configuration
    assert "block1:" in result.stdout
    assert "param: value1" in result.stdout
    assert "block2:" in result.stdout
    assert "param: value2" in result.stdout
    
    # Check dependencies and input mappings
    assert "depends on: block1, block2" in result.stdout
    assert "input1 <- block1.result" in result.stdout
    assert "input2 <- block2.result" in result.stdout


def test_show_nonexistent_file(runner):
    """Test showing a non-existent workflow file."""
    result = runner.invoke(app, ["show", "nonexistent.py"])
    assert result.exit_code == 2  # Typer's error code for invalid arguments
    assert "does not exist" in result.stdout.lower()


@pytest.fixture
def valid_workflow_file(tmp_path):
    """Create a valid workflow file for testing."""
    content = '''
from kwargify_core.core.workflow import Workflow
from kwargify_core.core.block import Block

class SimpleBlock(Block):
    def run(self) -> None:
        self.outputs = {"result": "success"}

def get_workflow():
    workflow = Workflow()
    workflow.name = "test_workflow"
    block = SimpleBlock(name="test_block")
    workflow.add_block(block)
    return workflow
'''
    file_path = tmp_path / "valid_workflow.py"
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


@pytest.fixture
def invalid_workflow_file(tmp_path):
    """Create an invalid workflow file for testing."""
    content = '''
def get_workflow():
    return "not a workflow object"
'''
    file_path = tmp_path / "invalid_workflow.py"
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


def test_run_valid_workflow(runner, valid_workflow_file):
    """Test running a valid workflow."""
    result = runner.invoke(app, ["run", str(valid_workflow_file)])
    assert result.exit_code == 0
    assert "Loading workflow from:" in result.stdout
    assert "Starting workflow: test_workflow" in result.stdout
    assert "Workflow completed successfully" in result.stdout


def test_run_invalid_workflow(runner, invalid_workflow_file):
    """Test running an invalid workflow file."""
    result = runner.invoke(app, ["run", str(invalid_workflow_file)])
    assert result.exit_code == 1
    assert "Error loading workflow:" in result.stdout


def test_run_nonexistent_file(runner):
    """Test running a non-existent workflow file."""
    result = runner.invoke(app, ["run", "nonexistent.py"])
    assert result.exit_code == 2  # Typer's error code for invalid arguments
    assert "does not exist" in result.stdout.lower()


@pytest.fixture
def mock_sqlite_logger():
    """Create a mock SQLiteLogger with sample data."""
    mock = MagicMock()
    
    # Sample data for list_runs
    mock.list_runs.return_value = [
        {
            "run_id": "run1",
            "workflow_name": "test_workflow",
            "start_time": "2025-04-28 08:00:00",
            "end_time": "2025-04-28 08:05:00",
            "status": "COMPLETED"
        },
        {
            "run_id": "run2",
            "workflow_name": "test_workflow",
            "start_time": "2025-04-28 08:10:00",
            "end_time": None,
            "status": "FAILED"
        }
    ]
    
    # Sample data for get_run_details
    mock.get_run_details.return_value = {
        "run_id": "run1",
        "workflow_name": "test_workflow",
        "start_time": "2025-04-28 08:00:00",
        "end_time": "2025-04-28 08:05:00",
        "status": "COMPLETED",
        "blocks": [
            {
                "block_name": "block1",
                "start_time": "2025-04-28 08:00:00",
                "end_time": "2025-04-28 08:02:00",
                "status": "COMPLETED",
                "inputs": {"param": "value1"},
                "outputs": {"result": "success"},
                "error_message": None,
                "retries_attempted": 0
            }
        ]
    }
    
    return mock


@patch("kwargify_core.cli.SQLiteLogger")
def test_history_list_runs(mock_logger_class, runner, mock_sqlite_logger):
    """Test listing all workflow runs."""
    mock_logger_class.return_value = mock_sqlite_logger
    
    result = runner.invoke(app, ["history"])
    assert result.exit_code == 0
    assert "Recent Workflow Runs" in result.stdout
    assert "test_workflow" in result.stdout
    assert "COMPLETED" in result.stdout
    assert "FAILED" in result.stdout
    assert "run1" in result.stdout
    assert "run2" in result.stdout


@patch("kwargify_core.cli.SQLiteLogger")
def test_history_specific_run(mock_logger_class, runner, mock_sqlite_logger):
    """Test showing details of a specific workflow run."""
    mock_logger_class.return_value = mock_sqlite_logger
    
    result = runner.invoke(app, ["history", "run1"])
    assert result.exit_code == 0
    assert "Execution Details:" in result.stdout
    assert "test_workflow" in result.stdout
    assert "block1" in result.stdout
    assert "COMPLETED" in result.stdout
    assert "param: value1" in result.stdout
    assert "result: success" in result.stdout


@patch("kwargify_core.cli.SQLiteLogger")
def test_history_nonexistent_run(mock_logger_class, runner, mock_sqlite_logger):
    """Test showing details of a non-existent run."""
    mock_logger_class.return_value = mock_sqlite_logger
    mock_sqlite_logger.get_run_details.return_value = None
    
    result = runner.invoke(app, ["history", "nonexistent"])
    assert result.exit_code == 1
    assert "Run not found" in result.stdout


@patch("kwargify_core.cli.SQLiteLogger")
def test_history_empty_database(mock_logger_class, runner, mock_sqlite_logger):
    """Test listing runs when no runs exist."""
    mock_logger_class.return_value = mock_sqlite_logger
    mock_sqlite_logger.list_runs.return_value = []
    
    result = runner.invoke(app, ["history"])
    assert result.exit_code == 0
    assert "No workflow runs found" in result.stdout


@patch("kwargify_core.cli.load_config")
@patch("kwargify_core.cli.save_config")
def test_init_command_creates_config(mock_save_config, mock_load_config, runner):
    """Test that the init command creates a new configuration."""
    mock_load_config.return_value = {}  # Simulate no existing config
    
    result = runner.invoke(app, ["init"], input="my_project\nmy_data.db\n")
    
    assert result.exit_code == 0
    assert "Project 'my_project' initialized. Configuration saved to config.toml." in result.stdout
    
    mock_load_config.assert_called_once()
    mock_save_config.assert_called_once_with({
        "project": {"name": "my_project"},
        "database": {"name": "my_data.db"}
    })


@patch("kwargify_core.cli.load_config")
@patch("kwargify_core.cli.save_config")
def test_init_command_updates_existing_config(mock_save_config, mock_load_config, runner):
    """Test that the init command updates an existing configuration."""
    existing_config = {
        "other_setting": "value",
        "project": {"name": "old_project"},
        "database": {"name": "old_db.db"}
    }
    mock_load_config.return_value = existing_config  # Simulate existing config
    
    result = runner.invoke(app, ["init"], input="new_project\nnew_data.db\n")
    
    assert result.exit_code == 0
    assert "Project 'new_project' initialized. Configuration saved to config.toml." in result.stdout
    
    mock_load_config.assert_called_once()
    mock_save_config.assert_called_once_with({
        "other_setting": "value",
        "project": {"name": "new_project"},
        "database": {"name": "new_data.db"}
    })


@patch("kwargify_core.cli.load_config")
@patch("kwargify_core.cli.save_config")
def test_init_command_prompts_correctly(mock_save_config, mock_load_config, runner):
    """Test that the init command prompts the user for input."""
    mock_load_config.return_value = {}
    
    # Use a side_effect to capture prompts - Typer's CliRunner handles prompts
    # by consuming input from the 'input' argument. We just need to ensure
    # the command runs successfully with valid input.
    result = runner.invoke(app, ["init"], input="prompt_test_project\nprompt_test.db\n")
    
    assert result.exit_code == 0
    assert "Project 'prompt_test_project' initialized." in result.stdout
    mock_save_config.assert_called_once() # Ensure save was attempted


@patch("kwargify_core.cli.load_config")
@patch("kwargify_core.cli.save_config")
def test_init_command_handles_no_input_for_prompts(mock_save_config, mock_load_config, runner):
    """Test that the init command handles no input for mandatory prompts."""
    mock_load_config.return_value = {}
    
    # Simulate pressing Enter for the first prompt (project_name)
    result = runner.invoke(app, ["init"], input=" \n") # Provide input for both prompts
    
    # Typer should exit with a non-zero code because the option is mandatory
    assert result.exit_code != 0
    # Check for error message related to missing required option
    assert "Missing required argument" in result.stdout or "Aborted" in result.stdout # Typer might abort on empty mandatory prompt


@pytest.fixture
def create_config_file(tmp_path):
    """Fixture to create a temporary config.toml file."""
    def _creator(config_data):
        config_path = tmp_path / "config.toml"
        with open(config_path, "w") as f:
            toml.dump(config_data, f)
        # Return the path and a cleanup function
        return config_path, lambda: os.remove(config_path)
    return _creator


@patch("kwargify_core.cli.SQLiteLogger")
def test_logger_uses_configured_db(mock_logger_class, runner, valid_workflow_file, create_config_file, tmp_path):
    """Test that SQLiteLogger in CLI uses the configured database name."""
    # Create a temporary config file with a custom DB name
    config_data = {"database": {"name": "custom_test.db"}}
    config_path, cleanup = create_config_file(config_data)

    # Change the current working directory to the temporary directory
    # so that load_config finds the temporary config.toml
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # Run a command that instantiates SQLiteLogger (e.g., 'run')
        # We need to mock the actual workflow run to avoid needing a real DB
        with patch("kwargify_core.cli.load_workflow_from_py") as mock_load_workflow:
             mock_workflow = MagicMock()
             mock_workflow.name = "test_workflow"
             mock_load_workflow.return_value = mock_workflow

             # Mock the run method to prevent actual execution
             mock_workflow.run.return_value = None

             # Mock get_run_details to satisfy the resume logic in cli.py
             mock_logger_instance = mock_logger_class.return_value
             mock_logger_instance.get_run_details.return_value = {
                 "run_id": "dummy_run_id",
                 "workflow_name": "test_workflow",
                 "start_time": "2025-01-01 10:00:00",
                 "end_time": "2025-01-01 10:05:00",
                 "status": "COMPLETED",
                 "blocks": [{"block_name": "block1", "status": "COMPLETED", "start_time": "2025-01-01 10:00:00", "end_time": "2025-01-01 10:01:00", "inputs": {}, "outputs": {}, "error_message": None, "retries_attempted": 0}]
             }

             result = runner.invoke(app, ["run", str(valid_workflow_file), "--resume-id", "dummy_run_id"])

             # Assert that SQLiteLogger was instantiated with the custom DB name
             mock_logger_class.assert_called_once_with("custom_test.db")

    finally:
        # Restore the original working directory and clean up the config file
        os.chdir(original_cwd)
        cleanup()


@patch("kwargify_core.cli.SQLiteLogger")
def test_commands_with_default_db_if_no_config(mock_logger_class, runner, valid_workflow_file, tmp_path):
    """Test that CLI commands use the default DB name if no config is present."""
    # Ensure no config.toml exists in the temporary directory
    config_path = tmp_path / "config.toml"
    if config_path.exists():
        os.remove(config_path)

    # Change the current working directory to the temporary directory
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # Run a command that instantiates SQLiteLogger (e.g., 'run')
        # We need to mock the actual workflow run to avoid needing a real DB
        with patch("kwargify_core.cli.load_workflow_from_py") as mock_load_workflow:
             mock_workflow = MagicMock()
             mock_workflow.name = "test_workflow"
             mock_load_workflow.return_value = mock_workflow

             # Mock the run method to prevent actual execution
             mock_workflow.run.return_value = None

             result = runner.invoke(app, ["run", str(valid_workflow_file)])

             # Assert that SQLiteLogger was instantiated with the default DB name
             mock_logger_class.assert_called_once_with("kwargify_runs.db")

    finally:
        # Restore the original working directory
        os.chdir(original_cwd)
