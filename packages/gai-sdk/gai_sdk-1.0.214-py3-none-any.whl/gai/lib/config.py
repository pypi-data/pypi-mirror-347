import copy
import os
import yaml
from pydantic import Field, BaseModel
from typing import Literal, Optional, Dict, Union
from gai.lib.utils import get_app_path
from gai.lib.logging import getLogger
logger = getLogger(__name__)
from abc import ABC, abstractmethod

class LogConfig(BaseModel):
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    datefmt: str = "%Y-%m-%d %H:%M:%S"
    filename: Optional[str] = None
    filemode: str = "a"
    stream: str = "stdout"
    loggers: Optional[Dict] = None

class ConfigBase(BaseModel):
    
    @staticmethod
    def _resolve_references(raw_config: Dict) -> Dict:
        if not isinstance(raw_config,Dict):
            raise ValueError("GaiGeneratorConfig._resolve_references: raw_config must be a dictionary")
        
        resolved_config = raw_config.copy()

        for config_type in ["clients", "generators"]:
            if config_type not in raw_config:
                continue

            if raw_config.get(config_type,None):
                for k, v in raw_config[config_type].items():
                    config = copy.deepcopy(v)
                    if v.get("ref"):
                        ref = v["ref"]
                        # Make a copy of the referenced config to avoid mutating the original
                        config = copy.deepcopy(raw_config[config_type][ref])

                    # By now, config is either a copy of the referenced config or copy of the referencing config

                    if config.get("module") and config["module"].get("class_"):
                        config["module"]["class"] = config["module"].pop("class_")

                    # Save to assign the config to the resolved_config

                    resolved_config[config_type][k] = config

        return resolved_config    
    
    @classmethod
    def _get_gai_config(cls, file_path:str=None) -> Dict:
        
        # if file_path is None, use the default gai config path
        
        if not file_path:
            app_dir=get_app_path()
            file_path = os.path.join(app_dir, 'gai.yml')
        
        try:
            with open(file_path, 'r') as f:
                raw_config = yaml.load(f, Loader=yaml.FullLoader)

            # raw_config is a config that can contain references to other config in the gai config.
            # resolved_config resolves the references to the actual config and replaces them in the config.
            config = cls._resolve_references(raw_config)
            if not config.get("generators",None):
                config["generators"] = {}
               
            for k,v in config["generators"].items():
                v = copy.deepcopy(v)
                source = v["source"]
                if isinstance(source, dict):
                    
                    # Cast it to the appropriate type
                    if source["type"]=="huggingface":
                        from gai.lib.config import HuggingfaceDownloadConfig
                        v["source"] = HuggingfaceDownloadConfig(**source)
                    elif source["type"]=="civictai":
                        from gai.lib.config import CivictaiDownloadConfig
                        v["source"] = CivictaiDownloadConfig(**source)
                    else:
                        raise ValueError(f"GaiGeneratorConfig._get_gai_config: Unknown source type {v['source']['type']}")
                else:
                    raise ValueError(f"GaiGeneratorConfig._get_gai_config: source must be a dictionary, got {type(v['source'])}")

                # After all the changes are done to the copy,
                # assign the copy back to the config
                
                config["generators"][k] = v

            return config
        
        except Exception as e:
            raise ValueError(f"GaiGeneratorConfig._get_gai_config: Error loading config from file: {e}")
    
### GaiClientConfig

class GaiClientConfig(ConfigBase):
    client_type: str
    type: Optional[str] = None
    engine: Optional[str] = None
    model: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    env: Optional[Dict] = None
    extra: Optional[Dict] = None
    hyperparameters: Optional[Dict] = {}

    @classmethod
    def from_name(cls,name:str, file_path:str=None) -> "GaiClientConfig":
        return cls._get_client_config(name=name, file_path=file_path)

    @classmethod
    def from_dict(cls, client_config:dict) -> "GaiClientConfig":
        return cls._get_client_config(client_config=client_config)

    @classmethod
    def _get_client_config(
            cls,
            name: Optional[str] = None,
            client_config: Optional[dict] = None,
            file_path: Optional[str] = None    
        ) -> "GaiClientConfig":
        
        if name:
            
            # If name is provided, load the generator config from gai.yml
            
            try:
                gai_dict = cls._get_gai_config(file_path=file_path)
            except Exception as e:
                raise ValueError(f"GaiClientConfig: Error loading client config from file: {e}")

            client_config = gai_dict["clients"].get(name, None)
            if not client_config:
                raise ValueError(f"GaiClientConfig: Client Config not found. name={name}")
    
        elif client_config:
            pass
        else:
            raise ValueError("GaiClientConfig: Invalid arguments. Either 'name' or 'config' must be provided.")
        
    
        return cls(**client_config)

### GaiGeneratorConfig

class MissingGeneratorConfigError(Exception):
    """Custom Exception with a message"""
    def __init__(self, message):
        super().__init__(message)

class ModuleConfig(BaseModel):
    name: str
    class_: str = Field(alias="class")  # Use 'class' as an alias for 'class_'

    class Config:
        allow_population_by_name = True  # Allow access via both 'class' and 'class_'

class DownloadConfig(BaseModel):
    type: str
    local_dir: str

class HuggingfaceDownloadConfig(DownloadConfig):
    type: Literal["huggingface"]
    repo_id: str
    revision: str
    file: Optional[str]=None

class CivitaiDownloadConfig(DownloadConfig):
    type: Literal["civitai"]
    url: str
    download: str

class GaiAliasConfig(DownloadConfig):
    """
    GaiAliasConfig is a configuration class for aliasing generators with just a reference to the generator name.
    """
    ref: str

class GaiGeneratorConfig(ConfigBase, ABC):
    type: str
    engine: str
    model: str
    name: str
    hyperparameters: Optional[Dict] = {}
    extra: Optional[Dict] = None
    module: ModuleConfig
    source: Optional[Union[HuggingfaceDownloadConfig, CivitaiDownloadConfig]] = None
    class Config:
        extra = "allow"

    @classmethod
    def from_name(cls,name:str, file_path:str=None) -> "GaiGeneratorConfig":
        return cls._get_generator_config(name=name, file_path=file_path)

    @classmethod
    def from_dict(cls, generator_config:dict) -> "GaiGeneratorConfig":
        return cls._get_generator_config(generator_config=generator_config)

    @classmethod
    def get_builtin_config_path(cls, this_file) -> str:
        """
        This method is for server subclass to locate the server config file
        """
        from pathlib import Path
        cfg_file = Path(this_file).resolve().parent / "gai.yml"
        file_path = str(cfg_file)
        return file_path
    
    @classmethod
    
    def _list_generator_configs(cls, file_path: Optional[str]=None) -> Dict[str, "GaiGeneratorConfig"]:
        """
        List all generator configs in either the local or global gai.yml file.
        """
        try:
            gai_dict = cls._get_gai_config(file_path=file_path)
        except Exception as e:
            raise ValueError(f"GaiGeneratorConfig: Error loading generator config from file: {e}")

        generators = gai_dict.get("generators", {})
        generator_configs = {}
        
        for name, config in generators.items():
            generator_configs[name] = cls.from_dict(config)
        
        return generator_configs
    
    @classmethod
        
    def _get_generator_config(
            cls,
            name: Optional[str] = None,
            generator_config: Optional[dict] = None,
            file_path: Optional[str] = None    
        ) -> "GaiGeneratorConfig":
        
        """
        This method is used to load a single generator entry from gai.yml or from a config dictionary.
        """

        if not name and not generator_config:
            raise ValueError("GaiGeneratorConfig: Invalid arguments. Either 'name' or 'config' must be provided.")

        if name:
            
            # If name is provided, load the generator config from gai.yml
            
            try:
                gai_dict = cls._get_gai_config(file_path=file_path)
            except Exception as e:
                raise ValueError(f"GaiGeneratorConfig: Error loading generator config from file: {e}")

            if not gai_dict.get("generators",None):
                return None

            generator_config = gai_dict["generators"].get(name, None)
            
        
        if not generator_config:
            return None

        # Final Processing
                
        if generator_config.get("module",None):
            
            # Sometimes "class" maybe stored as class_ after exporting because class is a reserved word in python
            # So we need to convert class_ to class before converting to GaiGeneratorConfig
            
            if generator_config["module"].get("class_",None):
                generator_config["module"]["class"] = generator_config["module"].pop("class_")
            
        return cls(**generator_config)

    @classmethod
    def update_gai_config(cls, local_config_path:str, global_config_path:str=None) -> "GaiConfig":
        """
        This method is called whenever a generator config is read.
        graft the current generator config into gai config["generators"]
        """
        import copy
        if not global_config_path:
            app_path = get_app_path()
            global_config_path = os.path.join(app_path, 'gai.yml')
        
        global_gai_config = GaiConfig.from_path(global_config_path)

        local_gai_config = GaiConfig.from_path(cls.get_builtin_config_path(local_config_path))
        
        # Copy the local generator config to the global gai config if it doesn't exist
        if not global_gai_config.generators:
            global_gai_config.generators = {}
        for k,v in local_gai_config.generators.items():
            v=copy.deepcopy(v)
            if not global_gai_config.generators.get(k,None):
                global_gai_config.generators[k] = v
                
        # Save the global gai config to the file
        with open(global_config_path, "w") as f:
            y = global_gai_config.to_yaml()
            f.write(y)
        return global_gai_config


### GaiToolConfig

class MissingToolConfigError(Exception):
    """Custom Exception with a message"""
    def __init__(self, message):
        super().__init__(message)


class GaiToolConfig(ConfigBase, ABC):
    type: str
    name: str
    extra: Optional[Dict] = None
    module: ModuleConfig
    class Config:
        extra = "allow"

    @classmethod
    def from_name(cls,name:str, file_path:str=None) -> "GaiToolConfig":
        return cls._get_tool_config(name=name, file_path=file_path)

    @classmethod
    def from_dict(cls, tool_config:dict) -> "GaiToolConfig":
        return cls._get_tool_config(tool_config=tool_config)

    @classmethod
    def get_builtin_config_path(cls, this_file) -> str:
        """
        This method is for server subclass to locate the server config file
        """
        from pathlib import Path
        cfg_file = Path(this_file).resolve().parent / "gai.yml"
        file_path = str(cfg_file)
        return file_path
    
    @classmethod
    def _list_tool_configs(cls, file_path: Optional[str]=None) -> Dict[str, "GaiToolConfig"]:
        """
        List all tool configs in either the local or global gai.yml file.
        """
        try:
            gai_dict = cls._get_tool_config(file_path=file_path)
        except Exception as e:
            raise ValueError(f"GaiToolConfig: Error loading tool config from file: {e}")

        tools = gai_dict.get("tools", {})
        tool_configs = {}
        
        for name, config in tools.items():
            tool_configs[name] = cls.from_dict(config)
        
        return tool_configs
    
    @classmethod
    def _get_tool_config(
            cls,
            name: Optional[str] = None,
            tool_config: Optional[dict] = None,
            file_path: Optional[str] = None    
        ) -> "GaiToolConfig":
        
        """
        This method is used to load a single tool entry from gai.yml or from a config dictionary.
        """

        if not name and not tool_config:
            raise ValueError("GaiGeneratorConfig: Invalid arguments. Either 'name' or 'config' must be provided.")

        if name:
            
            # If name is provided, load the tool config from gai.yml
            
            try:
                gai_dict = cls._get_gai_config(file_path=file_path)
            except Exception as e:
                raise ValueError(f"GaiGeneratorConfig: Error loading generator config from file: {e}")

            if not gai_dict.get("tools",None):
                return None

            tool_config = gai_dict["tools"].get(name, None)
            
        
        if not tool_config:
            return None

        # Final Processing
                
        if tool_config.get("module",None):
            
            # Sometimes "class" maybe stored as class_ after exporting because class is a reserved word in python
            # So we need to convert class_ to class before converting to GaiGeneratorConfig
            
            if tool_config["module"].get("class_",None):
                tool_config["module"]["class"] = tool_config["module"].pop("class_")
            
        return cls(**tool_config)

    @classmethod
    def update_gai_config(cls, local_config_path:str, global_config_path:str=None) -> "GaiConfig":
        """
        This method is called whenever a generator config is read.
        graft the current generator config into gai config["generators"]
        """
        import copy
        if not global_config_path:
            app_path = get_app_path()
            global_config_path = os.path.join(app_path, 'gai.yml')
        
        global_gai_config = GaiConfig.from_path(global_config_path)

        local_gai_config = GaiConfig.from_path(cls.get_builtin_config_path(local_config_path))
        
        # Copy the local generator config to the global gai config if it doesn't exist
        if not global_gai_config.tools:
            global_gai_config.tools = {}
        for k,v in local_gai_config.tools.items():
            v=copy.deepcopy(v)
            if not global_gai_config.tools.get(k,None):
                global_gai_config.tools[k] = v
                
        # Save the global gai config to the file
        with open(global_config_path, "w") as f:
            y = global_gai_config.to_yaml()
            f.write(y)
        return global_gai_config


### GaiConfig
    
class GaiConfig(ConfigBase):
    version: str
    gai_url: Optional[str] = None
    logging: Optional[LogConfig] = None
    clients: Optional[dict[str,GaiClientConfig] ] = None
    generators: Optional[dict[str,GaiGeneratorConfig] ] = None
    tools: Optional[dict[str,GaiToolConfig] ] = None
    class Config:
        extra = "ignore"
        
    @classmethod
    def from_dict(cls, config) -> "GaiConfig":
        
        if "generators" in config:
            
            # Convert class_ to class before converting to GaiConfig
            
            for k,v in config["generators"].items():
                if v.get("module",None):
                    if v["module"].get("class_",None):
                        v["module"]["class"] = v["module"].pop("class_")
        
        return cls(**config)

    @classmethod
    def from_path(cls, file_path=None) -> "GaiConfig":
        try:
            gai_dict=cls._get_gai_config(file_path=file_path)
            return GaiConfig.from_dict(gai_dict)        
        except Exception as e:
            raise ValueError(f"GaiConfig: Error loading config from file: {e}")
    
    def to_yaml(self):
        
        # Convert class_ to class before saving
        
        jsoned = self.model_dump()
        if jsoned.get("generators",None):

            # Ensure full module and source fields are preserved

            for g in jsoned["generators"].values():
                if isinstance(g.get("module"), BaseModel):
                    g["module"] = g["module"].model_dump()

                source = g.get("source")
                if isinstance(source, BaseModel):
                    g["source"] = source.model_dump()

                # Convert class_ to class for YAML output
                if g.get("module") and g["module"].get("class_"):
                    g["module"]["class"] = g["module"].pop("class_")        
        
        y=yaml.dump(jsoned, sort_keys=False,indent=4)
        return y
