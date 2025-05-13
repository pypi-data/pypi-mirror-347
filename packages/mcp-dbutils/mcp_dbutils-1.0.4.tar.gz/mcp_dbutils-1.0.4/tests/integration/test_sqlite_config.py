"""Test SQLite configuration functionality"""
from pathlib import Path

import pytest
import yaml

from mcp_dbutils.sqlite.config import SQLiteConfig, parse_jdbc_url


def test_parse_jdbc_url():
    """Test JDBC URL parsing"""
    # Test basic URL
    url = "jdbc:sqlite:/path/to/test.db"
    params = parse_jdbc_url(url)
    assert params["path"] == "/path/to/test.db"
    assert params["parameters"] == {}

    # Test URL with file: prefix
    url = "jdbc:sqlite:file:/path/to/test.db"
    params = parse_jdbc_url(url)
    assert params["path"] == "/path/to/test.db"
    assert params["parameters"] == {}

    # Test URL with parameters
    url = "jdbc:sqlite:/path/to/test.db?mode=ro&cache=shared"
    params = parse_jdbc_url(url)
    assert params["path"] == "/path/to/test.db"
    assert params["parameters"] == {"mode": "ro", "cache": "shared"}

    # Test invalid format
    with pytest.raises(ValueError, match="Invalid SQLite JDBC URL format"):
        parse_jdbc_url("sqlite:/path/to/test.db")

    # Test missing path
    with pytest.raises(ValueError, match="SQLite file path must be specified"):
        parse_jdbc_url("jdbc:sqlite:")

def test_from_jdbc_url():
    """Test SQLiteConfig creation from JDBC URL"""
    url = "jdbc:sqlite:/path/to/test.db"
    config = SQLiteConfig.from_jdbc_url(url)
    
    assert str(Path(config.path)) == str(Path("/path/to/test.db"))
    assert config.password is None
    assert config.uri is True
    assert config.type == "sqlite"

    # Test with password
    config = SQLiteConfig.from_jdbc_url(url, password="test_pass")
    assert config.password == "test_pass"
    assert config.uri is True

def test_from_yaml_with_jdbc_url(tmp_path):
    """Test SQLiteConfig creation from YAML with JDBC URL"""
    config_data = {
        "connections": {
            "test_db": {
                "type": "sqlite",
                "jdbc_url": "jdbc:sqlite:/path/to/test.db",
                "password": "test_pass"
            }
        }
    }

    config_file = tmp_path / "config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)

    config = SQLiteConfig.from_yaml(str(config_file), "test_db")
    assert str(Path(config.path)) == str(Path("/path/to/test.db"))
    assert config.password == "test_pass"
    assert config.uri is True
    assert config.type == "sqlite"

def test_required_fields_validation(tmp_path):
    """Test validation of required configuration fields"""
    # Missing type
    config_data = {
        "connections": {
            "test_db": {
                "jdbc_url": "jdbc:sqlite:/path/to/test.db"
            }
        }
    }
    
    config_file = tmp_path / "config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)

    with pytest.raises(ValueError, match="missing required 'type' field"):
        SQLiteConfig.from_yaml(str(config_file), "test_db")

    # Wrong type
    config_data["connections"]["test_db"]["type"] = "postgres"
    
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)

    with pytest.raises(ValueError, match="Configuration is not SQLite type"):
        SQLiteConfig.from_yaml(str(config_file), "test_db")

    # Standard config (non-JDBC) missing path
    config_data["connections"]["test_db"] = {
        "type": "sqlite"
    }
    
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)

    with pytest.raises(ValueError, match="must include 'path' field"):
        SQLiteConfig.from_yaml(str(config_file), "test_db")
