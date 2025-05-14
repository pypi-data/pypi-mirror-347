import platform

def detect_platform():
    """
    Detect the current operating system platform, return 'windows', 'linux', 'macos' or 'unknown'
    
    Returns:
        str: The name of the current platform (lowercase)
    """
    system = platform.system().lower()
    
    if system == 'windows':
        return 'windows'
    elif system == 'linux':
        return 'linux'
    elif system == 'darwin':  # macOS returns 'Darwin' in platform.system()
        return 'macos'
    else:
        return 'unknown'

# Simple test
if __name__ == "__main__":
    print(f"Current platform (using platform module): {detect_platform()}")