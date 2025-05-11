"""
Text animation effects for the fate library.
"""

import time
import sys
import random
from typing import Optional

from fate.utils import create_effect, animate_text, FateString

@create_effect
def typewriter(text: str, speed: int = 10, end: str = '') -> str:
    """
    Animates text with a typewriter effect, printing one character at a time.
    
    Args:
        text: The text to animate
        speed: Characters per second (higher is faster)
        end: String to append after the animation (default is empty string)
    
    Returns:
        The fully rendered text after animation
    """
    delay = 1.0 / speed  # Convert speed to delay in seconds
    
    def render_frame(content, step):
        return content[:step]
    
    # Run the animation without printing the final text
    animate_text(text, render_frame, delay, print_final=False)
    
    # Return the full text plus any end character
    return text + end


@create_effect
def blink(text: str, count: int = 3, speed: int = 2) -> str:
    """
    Makes text blink by alternating visibility.
    
    Args:
        text: The text to animate
        count: Number of blink cycles
        speed: Blinks per second
    
    Returns:
        The text after animation
    """
    delay = 1.0 / (2 * speed)  # Two states per blink (visible/invisible)
    
    try:
        for i in range(count * 2):
            if i % 2 == 0:
                sys.stdout.write('\r' + ' ' * len(text))
            else:
                sys.stdout.write('\r' + text)
            
            sys.stdout.flush()
            time.sleep(delay)
        
        # Ensure text is visible at the end
        sys.stdout.write('\r' + text + '\n')
        return text
    except KeyboardInterrupt:
        sys.stdout.write('\r' + text + '\n')
        return text


@create_effect
def fade_in(text: str, speed: int = 5) -> str:
    """
    Fades in text gradually by revealing characters from left to right.
    
    Args:
        text: The text to animate
        speed: Characters per second to reveal
    
    Returns:
        The text after animation
    """
    delay = 1.0 / speed
    
    def render_frame(content, step):
        return content[:step]
    
    animate_text(text, render_frame, delay, print_final=False)
    return text


@create_effect
def wave(text: str, cycles: int = 2, speed: int = 10) -> str:
    """
    Animates text with a wave-like motion.
    
    Args:
        text: The text to animate
        cycles: Number of wave cycles to complete
        speed: Animation speed (frames per second)
    
    Returns:
        The text after animation
    """
    delay = 1.0 / speed
    positions = list(range(len(text)))
    wave_chars = "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁"
    wave_length = len(wave_chars)
    
    try:
        for i in range(cycles * wave_length):
            result = ""
            for j, char in enumerate(text):
                wave_pos = (i - j) % wave_length
                wave_char = wave_chars[wave_pos]
                result += char + wave_char
            
            sys.stdout.write('\r' + result)
            sys.stdout.flush()
            time.sleep(delay)
        
        sys.stdout.write('\r' + text + ' ' * len(text) + '\n')
        return text
    except KeyboardInterrupt:
        sys.stdout.write('\r' + text + '\n')
        return text


@create_effect
def glitch(text: str, intensity: int = 3, duration: float = 1.0) -> str:
    """
    Creates a glitch effect where characters are temporarily replaced with random characters.
    
    Args:
        text: The text to glitch
        intensity: How many characters to glitch at once
        duration: Duration of the effect in seconds
    
    Returns:
        The original text after the glitch effect
    """
    glitch_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/`~"
    delay = 0.05
    steps = int(duration / delay)
    
    try:
        for _ in range(steps):
            result = list(text)
            
            # Replace random characters
            for _ in range(intensity):
                if len(text) > 0:
                    idx = random.randint(0, len(text) - 1)
                    result[idx] = random.choice(glitch_chars)
            
            sys.stdout.write('\r' + ''.join(result))
            sys.stdout.flush()
            time.sleep(delay)
        
        # Show the original text at the end
        sys.stdout.write('\r' + text + '\n')
        return text
    except KeyboardInterrupt:
        sys.stdout.write('\r' + text + '\n')
        return text


@create_effect
def shake(text: str, intensity: int = 2, duration: float = 1.0) -> str:
    """
    Creates a shaking text effect by offsetting the text position.
    
    Args:
        text: The text to shake
        intensity: Maximum offset in characters
        duration: Duration of the effect in seconds
    
    Returns:
        The original text after the shake effect
    """
    delay = 0.05
    steps = int(duration / delay)
    
    try:
        for _ in range(steps):
            offset = random.randint(-intensity, intensity)
            if offset >= 0:
                result = ' ' * offset + text
            else:
                result = text[-offset:]
            
            sys.stdout.write('\r' + result)
            sys.stdout.flush()
            time.sleep(delay)
        
        # Show the original text at the end
        sys.stdout.write('\r' + text + '\n')
        return text
    except KeyboardInterrupt:
        sys.stdout.write('\r' + text + '\n')
        return text


@create_effect
def rainbow(text: str, speed: int = 5, cycles: int = 2) -> str:
    """
    Cycles through rainbow colors for text.
    
    Args:
        text: The text to colorize
        speed: Color transitions per second
        cycles: Number of full color cycles
    
    Returns:
        The text with final color applied
    """
    from fate.styles import _apply_ansi
    
    # Rainbow color codes (foreground colors)
    colors = [
        '\033[31m',  # Red
        '\033[33m',  # Yellow
        '\033[32m',  # Green
        '\033[36m',  # Cyan
        '\033[34m',  # Blue
        '\033[35m',  # Magenta
    ]
    reset = '\033[0m'
    delay = 1.0 / speed
    
    try:
        for i in range(cycles * len(colors)):
            color_code = colors[i % len(colors)]
            sys.stdout.write('\r' + color_code + text + reset)
            sys.stdout.flush()
            time.sleep(delay)
        
        # End with normal text
        sys.stdout.write('\r' + text + '\n')
        return text
    except KeyboardInterrupt:
        sys.stdout.write('\r' + text + '\n')
        return text
