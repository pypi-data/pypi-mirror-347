"""
Shortcut wrappers around the fate library for even easier text effects.

This module provides a simpler syntax using Python's operator overloading.
"""

from typing import Any
from fate import typewriter, blink, fade_in, wave, glitch, shake, rainbow
from fate import color, style, bg_color
from fate import error, warning, success, info
from fate.utils import FateString


class EffectShortcut:
    """
    Class that allows using operators like + to apply effects.
    
    Example:
        fateTypeWriter + "Hello, World!"
    """
    def __init__(self, effect_func):
        """Initialize with the effect function to apply."""
        self.effect_func = effect_func
    
    def __add__(self, text: str) -> str:
        """Apply the effect when using the + operator."""
        return self.effect_func(text)
    
    def __call__(self, *args, **kwargs) -> 'EffectShortcut':
        """Allow customizing parameters."""
        effect_func = self.effect_func
        
        def wrapped_effect(text):
            return effect_func(text, *args, **kwargs)
        
        return EffectShortcut(wrapped_effect)


class ColorShortcut:
    """
    Class that allows using operators like + to apply colors.
    
    Example:
        fateRed + "Error message"
    """
    def __init__(self, color_func):
        """Initialize with the color function to apply."""
        self.color_func = color_func
    
    def __add__(self, text: str) -> str:
        """Apply the color when using the + operator."""
        return self.color_func(text)


class StyleShortcut:
    """
    Class that allows using operators like + to apply styles.
    
    Example:
        fateBold + "Important text"
    """
    def __init__(self, style_func):
        """Initialize with the style function to apply."""
        self.style_func = style_func
    
    def __add__(self, text: str) -> str:
        """Apply the style when using the + operator."""
        return self.style_func(text)


# Create shortcuts for effects
fateTypeWriter = EffectShortcut(typewriter)
fateBlink = EffectShortcut(blink)
fateFadeIn = EffectShortcut(fade_in)
fateWave = EffectShortcut(wave)
fateGlitch = EffectShortcut(glitch)
fateShake = EffectShortcut(shake)
fateRainbow = EffectShortcut(rainbow)

# Create shortcuts for colors
fateRed = ColorShortcut(color.red)
fateGreen = ColorShortcut(color.green)
fateBlue = ColorShortcut(color.blue)
fateYellow = ColorShortcut(color.yellow)
fateCyan = ColorShortcut(color.cyan)
fateMagenta = ColorShortcut(color.magenta)
fateWhite = ColorShortcut(color.white)
fateBlack = ColorShortcut(color.black)

# Create shortcuts for styles
fateBold = StyleShortcut(style.bold)
fateItalic = StyleShortcut(style.italic)
fateUnderline = StyleShortcut(style.underline)
fateReverse = StyleShortcut(style.reverse)
fateBlink = StyleShortcut(style.blink)

# Create shortcuts for predefined combinations
fateError = ColorShortcut(error)
fateWarning = ColorShortcut(warning)
fateSuccess = ColorShortcut(success)
fateInfo = ColorShortcut(info)