"""
Advanced animation utilities for the fate library.
"""

import sys
import time
import random
from typing import List, Callable, Optional, Union

from fate.utils import create_effect

@create_effect
def typing_with_errors(text: str, error_rate: float = 0.1, backspace_delay: float = 0.1, 
                       typing_speed: int = 10) -> str:
    """
    Realistic typing animation that includes random errors and backspacing.
    
    Args:
        text: Text to be displayed
        error_rate: Probability of making a typo (0-1)
        backspace_delay: Delay between backspace operations
        typing_speed: Characters per second
    
    Returns:
        The text after animation
    """
    delay = 1.0 / typing_speed
    
    # Possible typo characters (neighbors on QWERTY keyboard)
    keyboard_map = {
        'a': 'qwsz', 'b': 'vghn', 'c': 'xdfv', 'd': 'serfcx', 'e': 'wsdr',
        'f': 'drtgvc', 'g': 'ftyhbv', 'h': 'gyujnb', 'i': 'ujko', 'j': 'huikmn',
        'k': 'jiolm', 'l': 'kop;', 'm': 'njk,', 'n': 'bhjm', 'o': 'iklp',
        'p': 'ol;[', 'q': 'wa', 'r': 'edft', 's': 'awedxz', 't': 'rfgy',
        'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu',
        'z': 'asx'
    }
    
    current = ""
    errors = 0
    
    try:
        for i, char in enumerate(text):
            # Randomly decide whether to make a typo
            if random.random() < error_rate and char.lower() in keyboard_map:
                # Choose a typo character from nearby keys
                typo_char = random.choice(keyboard_map.get(char.lower(), char))
                if char.isupper():
                    typo_char = typo_char.upper()
                
                current += typo_char
                sys.stdout.write('\r' + current)
                sys.stdout.flush()
                time.sleep(delay)
                
                # Backspace the typo
                current = current[:-1]
                sys.stdout.write('\r' + current + ' ')
                sys.stdout.flush()
                time.sleep(backspace_delay)
                
                # Continue with the correct character
                current += char
            else:
                current += char
            
            sys.stdout.write('\r' + current)
            sys.stdout.flush()
            time.sleep(delay)
        
        sys.stdout.write('\n')
        return text
    except KeyboardInterrupt:
        sys.stdout.write('\r' + text + '\n')
        return text


@create_effect
def matrix_effect(text: str, speed: int = 5, char_set: Optional[str] = None) -> str:
    """
    Creates a matrix-like effect where characters fall into place.
    
    Args:
        text: Text to display
        speed: Animation speed
        char_set: Optional set of characters to use for the effect
    
    Returns:
        The text after animation
    """
    if char_set is None:
        char_set = "01"
    
    delay = 1.0 / speed
    width = len(text)
    
    # Create random initial positions for each character
    positions = [random.randint(0, 5) for _ in range(width)]
    max_height = max(positions) + 1
    
    try:
        # Animate characters falling into place
        for step in range(max_height + len(text)):
            result = ""
            
            for i in range(width):
                char_pos = step - positions[i]
                
                if char_pos < 0:
                    # Character hasn't started falling yet
                    result += " "
                elif char_pos < 5:
                    # Character is falling, show a random matrix character
                    result += random.choice(char_set)
                else:
                    # Character has reached its position, show the actual character
                    result += text[i]
            
            sys.stdout.write('\r' + result)
            sys.stdout.flush()
            time.sleep(delay)
        
        sys.stdout.write('\n')
        return text
    except KeyboardInterrupt:
        sys.stdout.write('\r' + text + '\n')
        return text


@create_effect
def slide_in(text: str, direction: str = "left", speed: int = 10) -> str:
    """
    Slides text into view from a specified direction.
    
    Args:
        text: Text to display
        direction: Direction to slide from ("left", "right")
        speed: Animation speed
    
    Returns:
        The text after animation
    """
    delay = 1.0 / speed
    width = len(text)
    
    try:
        if direction.lower() == "left":
            # Slide in from left
            for i in range(width + 1):
                result = text[:i]
                sys.stdout.write('\r' + result)
                sys.stdout.flush()
                time.sleep(delay)
        else:
            # Slide in from right
            for i in range(width + 1):
                result = " " * (width - i) + text[:i]
                sys.stdout.write('\r' + result)
                sys.stdout.flush()
                time.sleep(delay)
        
        sys.stdout.write('\n')
        return text
    except KeyboardInterrupt:
        sys.stdout.write('\r' + text + '\n')
        return text


@create_effect
def reveal_masked(text: str, mask_char: str = "*", speed: int = 5) -> str:
    """
    Reveals text by replacing mask characters one by one.
    
    Args:
        text: Text to reveal
        mask_char: Character used for masking
        speed: Characters per second to reveal
    
    Returns:
        The text after animation
    """
    delay = 1.0 / speed
    width = len(text)
    
    try:
        # Start with all characters masked
        current = mask_char * width
        revealed = [False] * width
        
        # Reveal characters one by one in random order
        indices = list(range(width))
        random.shuffle(indices)
        
        for idx in indices:
            # Update the current text
            current_list = list(current)
            current_list[idx] = text[idx]
            current = ''.join(current_list)
            
            # Display
            sys.stdout.write('\r' + current)
            sys.stdout.flush()
            time.sleep(delay)
        
        sys.stdout.write('\n')
        return text
    except KeyboardInterrupt:
        sys.stdout.write('\r' + text + '\n')
        return text
