"""
Text styling functions for the fate library.
"""

from typing import Callable, Any
from fate.utils import create_effect, FateString

def _apply_ansi(text: str, code: str) -> str:
    """
    Apply ANSI escape code to text and reset at the end.
    
    Args:
        text: The text to style
        code: ANSI escape code
    
    Returns:
        Styled text string
    """
    reset = '\033[0m'
    return f"{code}{text}{reset}"


# Create a class for color methods
class ColorFactory:
    """Factory class to generate color styling methods."""
    
    @staticmethod
    def _create_color_func(color_code: str) -> Callable:
        """Create a function that applies a specific color to text."""
        @create_effect
        def color_func(text: str) -> str:
            return _apply_ansi(text, color_code)
        return color_func
    
    def __init__(self):
        """Initialize the color factory with standard ANSI colors."""
        # Standard foreground colors
        self.black = self._create_color_func('\033[30m')
        self.red = self._create_color_func('\033[31m')
        self.green = self._create_color_func('\033[32m')
        self.yellow = self._create_color_func('\033[33m')
        self.blue = self._create_color_func('\033[34m')
        self.magenta = self._create_color_func('\033[35m')
        self.cyan = self._create_color_func('\033[36m')
        self.white = self._create_color_func('\033[37m')
        
        # Bright foreground colors
        self.bright_black = self._create_color_func('\033[90m')
        self.bright_red = self._create_color_func('\033[91m')
        self.bright_green = self._create_color_func('\033[92m')
        self.bright_yellow = self._create_color_func('\033[93m')
        self.bright_blue = self._create_color_func('\033[94m')
        self.bright_magenta = self._create_color_func('\033[95m')
        self.bright_cyan = self._create_color_func('\033[96m')
        self.bright_white = self._create_color_func('\033[97m')
    
    def rgb(self, r: int, g: int, b: int) -> Callable:
        """
        Create a color function using RGB values.
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
            
        Returns:
            A function that colors text with the specified RGB color
        """
        @create_effect
        def rgb_color(text: str) -> str:
            color_code = f'\033[38;2;{r};{g};{b}m'
            return _apply_ansi(text, color_code)
        return rgb_color


# Create a class for background color methods
class BackgroundColorFactory:
    """Factory class to generate background color styling methods."""
    
    @staticmethod
    def _create_bg_color_func(color_code: str) -> Callable:
        """Create a function that applies a specific background color to text."""
        @create_effect
        def bg_color_func(text: str) -> str:
            return _apply_ansi(text, color_code)
        return bg_color_func
    
    def __init__(self):
        """Initialize the background color factory with standard ANSI colors."""
        # Standard background colors
        self.black = self._create_bg_color_func('\033[40m')
        self.red = self._create_bg_color_func('\033[41m')
        self.green = self._create_bg_color_func('\033[42m')
        self.yellow = self._create_bg_color_func('\033[43m')
        self.blue = self._create_bg_color_func('\033[44m')
        self.magenta = self._create_bg_color_func('\033[45m')
        self.cyan = self._create_bg_color_func('\033[46m')
        self.white = self._create_bg_color_func('\033[47m')
        
        # Bright background colors
        self.bright_black = self._create_bg_color_func('\033[100m')
        self.bright_red = self._create_bg_color_func('\033[101m')
        self.bright_green = self._create_bg_color_func('\033[102m')
        self.bright_yellow = self._create_bg_color_func('\033[103m')
        self.bright_blue = self._create_bg_color_func('\033[104m')
        self.bright_magenta = self._create_bg_color_func('\033[105m')
        self.bright_cyan = self._create_bg_color_func('\033[106m')
        self.bright_white = self._create_bg_color_func('\033[107m')
    
    def rgb(self, r: int, g: int, b: int) -> Callable:
        """
        Create a background color function using RGB values.
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
            
        Returns:
            A function that colors text background with the specified RGB color
        """
        @create_effect
        def rgb_bg_color(text: str) -> str:
            color_code = f'\033[48;2;{r};{g};{b}m'
            return _apply_ansi(text, color_code)
        return rgb_bg_color


# Create a class for text style methods
class StyleFactory:
    """Factory class to generate text styling methods."""
    
    def __init__(self):
        """Initialize the style factory with standard ANSI text styles."""
        # Text styles
        self.bold = create_effect(lambda text: _apply_ansi(text, '\033[1m'))
        self.dim = create_effect(lambda text: _apply_ansi(text, '\033[2m'))
        self.italic = create_effect(lambda text: _apply_ansi(text, '\033[3m'))
        self.underline = create_effect(lambda text: _apply_ansi(text, '\033[4m'))
        self.blink = create_effect(lambda text: _apply_ansi(text, '\033[5m'))
        self.reverse = create_effect(lambda text: _apply_ansi(text, '\033[7m'))
        self.hidden = create_effect(lambda text: _apply_ansi(text, '\033[8m'))
        self.strikethrough = create_effect(lambda text: _apply_ansi(text, '\033[9m'))


# Instantiate the factories
color = ColorFactory()
bg_color = BackgroundColorFactory()
style = StyleFactory()
