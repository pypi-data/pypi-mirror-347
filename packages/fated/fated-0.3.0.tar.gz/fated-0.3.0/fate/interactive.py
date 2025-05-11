"""
Interactive effects and utilities for the fate library.

This module provides components for creating interactive terminal applications
with text effects.
"""

import sys
import time
from typing import Callable, Optional, List

from fate.effects import typewriter
from fate.styles import StyleFactory, ColorFactory
from fate import style, color

# Instantiate style and color factories
style_factory = StyleFactory()
color_factory = ColorFactory()


def progress_bar(
    total: int,
    filled_char: str = "█",
    empty_char: str = "░",
    width: int = 30,
    prefix: str = "",
    suffix: str = "",
    color_func: Optional[Callable] = None,
    show_percentage: bool = True,
    delay: float = 0.05
) -> None:
    """
    Displays an animated progress bar in the terminal.
    
    Args:
        total: The total number of steps in the progress
        filled_char: Character to use for filled portion
        empty_char: Character to use for empty portion
        width: Width of the progress bar in characters
        prefix: Text to display before the progress bar
        suffix: Text to display after the progress bar
        color_func: Optional color function to apply to the bar
        show_percentage: Whether to show percentage in suffix
        delay: Delay between updates in seconds
    """
    def update_progress(iteration):
        filled = int(width * iteration // total)
        bar = filled_char * filled + empty_char * (width - filled)
        
        if color_func:
            bar = color_func(bar)
            
        percentage = f" {100 * iteration // total}%" if show_percentage else ""
        progress_text = f"\r{prefix} {bar} {suffix}{percentage}"
        
        sys.stdout.write(progress_text)
        sys.stdout.flush()
    
    # Display initial empty bar
    update_progress(0)
    
    # Simulate progress
    for i in range(1, total + 1):
        time.sleep(delay)
        update_progress(i)
    
    sys.stdout.write("\n")
    sys.stdout.flush()


def typing_prompt(
    prompt: str = "",
    typing_speed: int = 10,
    prompt_color: Optional[Callable] = None,
    input_color: Optional[Callable] = None
) -> str:
    """
    Displays a typewriter-animated prompt and waits for user input.
    
    Args:
        prompt: The prompt text to animate
        typing_speed: Characters per second for typewriter effect
        prompt_color: Optional color function for the prompt
        input_color: Optional color function for the input text
        
    Returns:
        The user input
    """
    # Apply color to prompt if specified
    display_prompt = prompt
    if prompt_color:
        display_prompt = prompt_color(prompt)
    
    # Display the prompt with typewriter effect
    if prompt:
        typewriter(display_prompt, speed=typing_speed, end="")
    
    # Get user input with optional color
    if input_color:
        # We need to temporarily modify the input function to apply color
        original_input = input
        
        def colored_input(prompt=""):
            result = original_input(prompt)
            return input_color(result)
        
        # Replace built-in input temporarily
        __builtins__["input"] = colored_input
        user_input = input()
        # Restore original input function
        __builtins__["input"] = original_input
        
        return user_input
    else:
        return input()


def menu(
    title: str,
    options: List[str],
    title_style: Optional[Callable] = None,
    option_style: Optional[Callable] = None,
    selected_style: Optional[Callable] = style.bold,
    animate: bool = False,
    animation_speed: int = 10
) -> int:
    """
    Display an interactive menu and return the selected option index.
    
    Args:
        title: Menu title to display
        options: List of option strings
        title_style: Optional style function for the title
        option_style: Optional style function for unselected options
        selected_style: Style function for the selected option
        animate: Whether to use typewriter effect
        animation_speed: Typewriter animation speed
        
    Returns:
        The index of the selected option (0-based)
    """
    if not options:
        raise ValueError("Menu must have at least one option")
    
    # Apply styles
    display_title = title
    if title_style:
        display_title = title_style(title)
    
    display_options = []
    for option in options:
        if option_style:
            display_options.append(option_style(option))
        else:
            display_options.append(option)
    
    # Display the menu
    if animate:
        print(typewriter(display_title, speed=animation_speed))
        print(typewriter("-" * len(title), speed=animation_speed))
    else:
        print(display_title)
        print("-" * len(title))
    
    for i, option in enumerate(display_options):
        option_text = f"{i+1}. {option}"
        if animate:
            print(typewriter(option_text, speed=animation_speed))
        else:
            print(option_text)
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-{}): ".format(len(options))))
            if 1 <= choice <= len(options):
                return choice - 1  # Convert to 0-based index
            else:
                print(color.red("Invalid choice. Please try again."))
        except ValueError:
            print(color.red("Please enter a number."))


# Predefined interactive components
def loading_animation(
    message: str = "Loading",
    duration: float = 3.0,
    color_func: Optional[Callable] = color.blue,
    animation_chars: Optional[List[str]] = None
) -> None:
    """
    Display a simple loading animation in the terminal.
    
    Args:
        message: The message to display
        duration: Duration of the animation in seconds
        color_func: Optional color function to apply
        animation_chars: List of characters to use for animation
    """
    if animation_chars is None:
        animation_chars = ['|', '/', '-', '\\']
    
    start_time = time.time()
    i = 0
    
    while time.time() - start_time < duration:
        char = animation_chars[i % len(animation_chars)]
        if color_func:
            display_text = f"\r{message}... {color_func(char)}"
        else:
            display_text = f"\r{message}... {char}"
            
        sys.stdout.write(display_text)
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    
    # Clear the animation
    sys.stdout.write("\r" + " " * (len(message) + 6) + "\r")
    sys.stdout.flush()


def countdown(
    seconds: int,
    prefix: str = "Starting in",
    suffix: str = "",
    color_func: Optional[Callable] = color.yellow
) -> None:
    """
    Display a countdown timer in the terminal.
    
    Args:
        seconds: Number of seconds to count down from
        prefix: Text to display before the countdown
        suffix: Text to display after the countdown
        color_func: Optional color function to apply to the number
    """
    for i in range(seconds, 0, -1):
        if color_func:
            display_num = color_func(str(i))
        else:
            display_num = str(i)
            
        sys.stdout.write(f"\r{prefix} {display_num} {suffix}")
        sys.stdout.flush()
        time.sleep(1)
    
    # Clear the line
    sys.stdout.write("\r" + " " * (len(prefix) + len(suffix) + 5) + "\r")
    sys.stdout.flush()