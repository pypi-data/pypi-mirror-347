"""
Utility functions and base classes for the fate library.
"""

import sys
import time
import functools
from typing import Callable, Any, Union, Optional

class FateString(str):
    """
    A string subclass that maintains character-level styling and animation effects.
    
    This allows for chaining different effects and maintaining the overall styling
    when printing or using the string.
    """
    def __new__(cls, content: str, effect_func: Optional[Callable] = None):
        instance = super().__new__(cls, content)
        instance._content = content
        instance._effect_func = effect_func
        return instance
    
    def __str__(self) -> str:
        """Return the string content with effects applied when converting to string."""
        if self._effect_func:
            return self._effect_func(self._content)
        return self._content
    
    def __repr__(self) -> str:
        """Return a representation of the FateString for debugging."""
        return f"FateString({repr(self._content)})"
    
    def __add__(self, other: Union[str, 'FateString']) -> 'FateString':
        """Concatenate with another string or FateString, preserving effects."""
        if isinstance(other, FateString):
            # Complex concatenation of two FateStrings with different effects
            # (This is a simplified implementation)
            new_content = self._content + other._content
            
            # Create a new effect function that applies both effects
            def combined_effect(text):
                # Split the text according to the lengths of the original strings
                split_point = len(self._content)
                first_part = text[:split_point]
                second_part = text[split_point:]
                
                # Apply respective effects
                if self._effect_func:
                    first_part = self._effect_func(first_part)
                if other._effect_func:
                    second_part = other._effect_func(second_part)
                
                return first_part + second_part
            
            return FateString(new_content, combined_effect)
        else:
            # Concatenate with a regular string
            return FateString(self._content + str(other), self._effect_func)
    
    def __radd__(self, other: str) -> 'FateString':
        """Support for string + FateString operations."""
        return FateString(str(other) + self._content, self._effect_func)
    
    def __call__(self, *args, **kwargs) -> 'FateString':
        """
        Allow calling the FateString as a function to apply additional parameters.
        
        This enables syntax like: typewriter("Hello")(speed=10)
        """
        if self._effect_func and hasattr(self._effect_func, "__closure__"):
            # Create a new effect function with updated parameters
            original_func = self._effect_func.__closure__[0].cell_contents
            
            @functools.wraps(original_func)
            def updated_effect(text):
                return original_func(text, *args, **kwargs)
            
            return FateString(self._content, updated_effect)
        
        return self


def create_effect(func: Callable) -> Callable:
    """
    Decorator for creating effect functions that return FateString objects.
    
    Args:
        func: The effect function to wrap
    
    Returns:
        A wrapped function that returns a FateString with the effect applied
    """
    @functools.wraps(func)
    def wrapper(text: str, *args, **kwargs) -> FateString:
        # Create a closure that contains the original function and its arguments
        def effect_func(content: str) -> str:
            return func(content, *args, **kwargs)
        
        return FateString(text, effect_func)
    
    return wrapper


def animate_text(text: str, render_func: Callable, delay: float = 0.05) -> str:
    """
    Base function for text animations that handles rendering to the terminal.
    
    Args:
        text: The text to animate
        render_func: A function that takes (text, step) and returns what to print at each step
        delay: Time delay between animation frames in seconds
    
    Returns:
        The final text after animation completes
    """
    try:
        for step in range(len(text) + 1):
            frame = render_func(text, step)
            
            # Clear the line and print the current frame
            sys.stdout.write('\r')
            sys.stdout.write(frame)
            sys.stdout.flush()
            
            # Delay before the next frame
            if step < len(text):
                time.sleep(delay)
        
        # Add newline at the end of the animation
        sys.stdout.write('\n')
        return text
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully by completing the animation
        sys.stdout.write('\r' + text + '\n')
        return text
