import pytest
from unittest.mock import patch, mock_open, MagicMock,call
from gai.lib.config import GaiConfig
from gai.lib.tests import make_local_tmp, get_local_datadir

# mock_gai_data= {
#     "version": "1.0",
#     "gai_url": "http://localhost:8080",
#     "logging": {
#         "level": "DEBUG",
#         "format": "%(levelname)s - %(message)s"
#     },
#     "clients": {
#         "ttt": {
#             "type": "ttt",
#             "engine": "ollama",
#             "model": "llama3.1",
#             "name": "llama3.1",
#             "client_type": "ollama"
#         }
#     }
# }

@pytest.fixture
def local_datadir(request):
    """
    Create a tmp/ folder inside the directory of the test file that uses this fixture.
    """
    return get_local_datadir(request)

### GaiConfig should load from "~/.gai/gai.yml" by default

@patch("gai.lib.config.GaiConfig.from_dict", return_value={})   # No need for data, just the path will be tested for
@patch("yaml.load", return_value={})                            # No need for data, just the path will be tested for
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.config.get_app_path", return_value="~/.gai")
def test_gaiconfig_from_path_default(mock_app_path, mock_file, mock_yaml_load,mock_from_dict):
    
    # Load GaiConfig from default path
    config = GaiConfig.from_path()
    
    # Ensure only ~/.gai/gai.yml was opened
    mock_file.assert_called_once_with("~/.gai/gai.yml", 'r')
    assert len(mock_file.call_args_list) == 1

### GaiConfig should load from custom path

@patch("gai.lib.config.GaiConfig.from_dict", return_value={})   # No need for data, just the path will be tested for
@patch("yaml.load", return_value={})                            # No need for data, just the path will be tested for
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.config.get_app_path", return_value="~/.gai")
def test_gaiconfig_from_path_custom(mock_app_path, mock_file, mock_yaml_load, local_datadir):

    # Load Gaiconfig from a custom file path
    config = GaiConfig.from_path(file_path=f"{local_datadir}/gai.yml")

    # Ensure only /tmp/gai.yml was opened
    mock_file.assert_called_once_with(f"{local_datadir}/gai.yml", 'r')
    assert len(mock_file.call_args_list) == 1

# Client Config ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――    

mock_client_data= {
    "version": "1.0",
    "gai_url": "http://localhost:8080",
    "logging": {
        "level": "DEBUG",
        "format": "%(levelname)s - %(message)s"
    },
    "clients": {
        "ttt": {
            "ref": "llama3.1",
        },
        "llama3.1": {
            "type": "llama3.1",
            "engine": "ollama",
            "model": "llama3.1",
            "name": "llama3.1",
            "client_type": "ollama"
        }
    }
}

# GaiClientConfig should load from "~/.gai/gai.yml" by default

@patch("yaml.load", return_value=mock_client_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.config.get_app_path", return_value="~/.gai")
def test_clientconfig_from_path_default(mock_yaml_load, mock_file, mock_app_path):
    from gai.lib.config import GaiClientConfig
    
    # Load GaiConfig from default path
    config = GaiClientConfig.from_name("ttt")
    
    # Ensure only ~/.gai/gai.yml was opened
    mock_file.assert_called_once_with("~/.gai/gai.yml", 'r')
    assert len(mock_file.call_args_list) == 1

# GaiClientConfig should load from custom file path if provided
@patch("yaml.load", return_value=mock_client_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.config.get_app_path", return_value="~/.gai")
def test_clientconfig_from_custom_path(mock_yaml_load, mock_file, mock_app_path):
    from gai.lib.config import GaiClientConfig
    
    # Load GaiConfig from default path
    config = GaiClientConfig.from_name("ttt", file_path="/tmp/gai.yml")
    
    # Ensure only ~/.gai/gai.yml was opened
    mock_file.assert_called_once_with("/tmp/gai.yml", 'r')
    assert len(mock_file.call_args_list) == 1

# GaiClientConfig should not load from any file if the config is provided
@patch("yaml.load", return_value=mock_client_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.utils.get_app_path", return_value="~/.gai")
def test_clientconfig_from_dict(mock_yaml_load, mock_file, mock_app_path):
    from gai.lib.config import GaiClientConfig
    
    # Load GaiConfig from default path
    config = GaiClientConfig.from_dict({
        "type": "ttt",
        "engine": "ollama",
        "model": "llama3.1",
        "name": "llama3.1",
        "client_type": "ollama"
    })
    
    # Ensure only ~/.gai/gai.yml was opened
    assert len(mock_file.call_args_list) == 0

# GaiClientConfig resolve "ref"
@patch("yaml.load", return_value=mock_client_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.config.get_app_path", return_value="~/.gai")
def test_clientconfig_resolve_ref(mock_yaml_load, mock_file, mock_app_path):
    from gai.lib.config import GaiClientConfig
    
    # Load actual config from mock client data
    config = GaiClientConfig.from_name("llama3.1")
    
    # Assert that the config is
    assert config.name == "llama3.1"
    
    # Load ref
    
    ref_config = GaiClientConfig.from_name("ttt")
    
    assert ref_config.name == "llama3.1"

# Generator Config ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――    

mock_generator_data= {
    "version": "1.0",
    "generators": {
        "ttt": {
            "ref": "ttt-exllamav2-dolphin",
        },
        "ttt-exllamav2-dolphin": {
            "type": "ttt",
            "engine": "exllamav2",
            "model": "dolphin",
            "name": "ttt-exllamav2-dolphin",
            "module":{
                "name": "gai.ttt.server.gai_exllamav2",
                "class": "GaiExllamav2"
            }
        }
    }
}

# GaiGeneratorConfig should load from "~/.gai/gai.yml" by default
@patch("yaml.load", return_value=mock_generator_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.config.get_app_path", return_value="~/.gai")
def test_generatorconfig_from_path_default(mock_app_path, mock_file, mock_yaml_load):
    from gai.lib.config import GaiGeneratorConfig
    
    # Load GaiConfig from default path
    config = GaiGeneratorConfig.from_name("ttt-exllamav2-dolphin")
    
    # Ensure only ~/.gai/gai.yml was opened
    mock_file.assert_called_once_with("~/.gai/gai.yml", 'r')
    assert len(mock_file.call_args_list) == 1
    
    assert config.module.name == "gai.ttt.server.gai_exllamav2"

# GaiGeneratorConfig should load from custom file path if provided
@patch("yaml.load", return_value=mock_generator_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.config.get_app_path", return_value="~/.gai")
def test_generatorconfig_from_custom_path(mock_app_path, mock_file, mock_yaml_load):
    from gai.lib.config import GaiGeneratorConfig
    
    # Load GaiConfig from default path
    config = GaiGeneratorConfig.from_name("ttt-exllamav2-dolphin", file_path="/tmp/gai.yml")
    
    # Ensure only ~/.gai/gai.yml was opened
    mock_file.assert_called_once_with("/tmp/gai.yml", 'r')
    assert len(mock_file.call_args_list) == 1
    
    assert config.module.name == "gai.ttt.server.gai_exllamav2"

# GaiGeneratortConfig should not load from any file if the config is provided
@patch("yaml.load", return_value=mock_generator_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.utils.get_app_path", return_value="~/.gai")
def test_generatorconfig_from_dict(mock_app_path, mock_file, mock_yaml_load):
    from gai.lib.config import GaiGeneratorConfig
    
    # Load GaiConfig from default path
    config = GaiGeneratorConfig.from_dict({
        "type": "ttt",
        "engine": "llamacpp",
        "model": "dolphin",
        "name": "ttt-llamacpp-dolphin",
        "module":{
            "name": "gai.ttt.server.gai_llamacpp",
            "class": "GaiLlamaCpp"
        }
    })
    
    assert config.module.name == "gai.ttt.server.gai_llamacpp"
    
    # Ensure only ~/.gai/gai.yml was opened
    assert len(mock_file.call_args_list) == 0


# GaiGeneratorConfig resolve "ref"
@patch("yaml.load", return_value=mock_generator_data)
@patch("builtins.open", new_callable=mock_open, read_data="version: 1.0\ngai_url: http://localhost")
@patch("gai.lib.config.get_app_path", return_value="~/.gai")
def test_generatorconfig_resolve_ref(mock_yaml_load, mock_file, mock_app_path):
    from gai.lib.config import GaiGeneratorConfig
    
    # Load actual config from mock client data
    config = GaiGeneratorConfig.from_name("ttt-exllamav2-dolphin")
    
    # Assert that the config is
    assert config.name == "ttt-exllamav2-dolphin"
    
    # Load ref
    
    ref_config = GaiGeneratorConfig.from_name("ttt")
    
    assert ref_config.name == "ttt-exllamav2-dolphin"
    
