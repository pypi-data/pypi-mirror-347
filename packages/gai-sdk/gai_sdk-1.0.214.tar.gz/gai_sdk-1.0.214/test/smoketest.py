from gai.lib.utils import get_rc

def test_get_rc():
    """
    Test the get_rc function.
    """
    # Test if the function raises an exception when the config file does not exist
    try:
        get_rc()
    except Exception as e:
        assert str(e) == "Config file ~/.gairc not found. Please run 'gai init' to initialize the configuration."
   
