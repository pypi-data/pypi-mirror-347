# Fated - Text Effects Library for Python

![Version](https://img.shields.io/pypi/v/fated)
![Python Version](https://img.shields.io/pypi/pyversions/fated)
![License](https://img.shields.io/github/license/fredised/fated)

Fated is a Python library that adds visual effects to text output including typewriter animation and other text styling options. It provides a simple API for creating rich, animated terminal text with no external dependencies.

Make your terminal applications more engaging with smooth animations, colorful text, and eye-catching effects!

## Features

- **Text Animation Effects**: Typewriter, blink, fade-in, wave, glitch, shake, matrix, and more
- **Text Styling**: Colors, background colors, bold, italic, underline, and other text styles
- **Chainable Effects**: Combine multiple effects together seamlessly
- **Simple API**: Intuitive interface that works with standard print function
- **Alternative Syntax**: Use the + operator with shortcut objects for even cleaner code
- **Interactive Components**: Progress bars, menus, typing prompts, and loading animations
- **No Dependencies**: Uses only Python standard library modules
- **Cross-Platform**: Works on Windows, macOS, and Linux terminals that support ANSI escape codes

## Installation

Install directly from PyPI using pip:

```bash
pip install fated
```

For the latest version with bug fixes:

```bash
pip install fated==0.2.2
```

Alternative installation methods:

1. Clone the repository and include the `fate` folder in your project:

```bash
git clone https://github.com/fredised/fated.git
```

2. Or simply copy the `fate` directory to your project.

## Getting Started

1. Install the library:
   ```bash
   pip install fated
   ```

2. Create a new Python file (e.g., `demo.py`):
   ```python
   from fate import typewriter, color, style
   
   # Try a simple typewriter effect
   print(typewriter("Hello, World!"))
   
   # Add some color
   print(color.green("Success!"))
   
   # Combine effects
   print(style.bold(color.blue("Important information")))
   ```

3. Run your script:
   ```bash
   python demo.py
   ```

4. Explore other effects in the documentation below!

## Compatibility

Fated works best in terminals that support ANSI escape codes:
- Modern versions of Windows Terminal, PowerShell, and cmd.exe
- macOS Terminal, iTerm2
- Linux terminals (GNOME Terminal, Konsole, xterm, etc.)
- VS Code integrated terminal
- Jupyter notebooks (results may vary)

## Usage

### Traditional Syntax

```python
from fate import typewriter, color, style

# Simple typewriter effect
print(typewriter("Hello, World!"))

# Colored text
print(color.red("This text is red"))
print(color.blue("This text is blue"))
print(color.rgb(255, 128, 0)("Custom orange text"))

# Text styling
print(style.bold("Bold text"))
print(style.italic("Italic text"))
print(style.underline("Underlined text"))

# Background colors
print(color.bg.yellow("Text with yellow background"))
print(color.bg.rgb(0, 128, 128)("Custom teal background"))

# Chain multiple effects
print(style.bold(color.green(typewriter("Bold green typewriter text"))))

# Predefined combinations
from fate import error, warning, success, info
print(error("Error message"))
print(warning("Warning message"))
print(success("Success message"))
print(info("Information message"))
```

### Shortcut Syntax (New!)

```python
from fate.shortcuts import fateTypeWriter, fateRed, fateBold, fateBgYellow

# Use the + operator
print(fateTypeWriter + "Hello, World!")

# Colored text
print(fateRed + "This text is red")

# Text styling
print(fateBold + "Bold text")

# Background colors
print(fateBgYellow + "Text with yellow background")

# Combine shortcuts (in order from right to left)
print(fateBold + fateRed + "Bold red text")

# Custom parameters
print(fateTypeWriter(speed=20) + "Fast typing!")
print(fateGlitch(intensity=5, duration=2.0) + "Intense glitching effect")

# Predefined combinations
from fate.shortcuts import fateError, fateSuccess, fateWarning, fateInfo
print(fateError + "Error message")
print(fateWarning + "Warning message")
print(fateSuccess + "Success message") 
print(fateInfo + "Information message")
```

### Practical Applications

```python
from fate import typewriter, color, style
import time

# Create an interactive CLI application with styled output
def interactive_cli():
    print(style.bold(color.blue("Welcome to My App!")))
    time.sleep(0.5)
    
    print(typewriter("Loading settings..."))
    time.sleep(1)
    print(color.green("✓ Settings loaded successfully"))
    
    user_input = input(color.yellow("Enter your name: "))
    print(typewriter(f"Hello, {style.bold(user_input)}! Nice to meet you."))

# Password input with masked animation
from fate import reveal_masked
password = input("Enter password: ")
print("Verifying: ", end="")
print(reveal_masked("*" * len(password)))
print(color.green("✓ Access granted"))
```

## Examples

The repository includes example files:

- `examples.py` - Comprehensive demonstration of all effects with traditional syntax
- `shortcut_example.py` - Basic demonstration of the new shortcut syntax
- `shortcut_demo.py` - Interactive demonstration of various shortcut combinations
- `interactive_example.py` - Showcases the interactive components (menus, progress bars, etc.)
- `test_fix.py` - Test script for verifying the typewriter effect fix

Run the examples to see the library in action:

```bash
# Full demonstration with traditional syntax
python examples.py

# Demonstration of the shortcut syntax
python shortcut_example.py

# Interactive demonstration with various combinations
python shortcut_demo.py

# Interactive components demonstration
python interactive_example.py
```

## Available Effects

### Text Animation Effects

- `typewriter` - Types text character by character
- `blink` - Makes text blink
- `fade_in` - Gradually reveals text
- `wave` - Creates a wave-like animation
- `glitch` - Creates a glitchy, distorted effect
- `shake` - Shakes the text
- `rainbow` - Cycles through rainbow colors
- `typing_with_errors` - Realistic typing with random errors
- `matrix_effect` - Matrix-like falling character effect
- `slide_in` - Slides text in from left or right
- `reveal_masked` - Reveals masked text character by character

### Colors

- Standard colors: `red`, `green`, `blue`, `yellow`, `magenta`, `cyan`, `white`, `black`
- Bright variants: `bright_red`, `bright_green`, `bright_blue`, etc.
- Custom colors: `color.rgb(r, g, b)` - Create custom colors using RGB values (0-255)

### Background Colors

Available through the `color.bg` namespace:
- Standard backgrounds: `bg.red`, `bg.green`, `bg.blue`, etc.
- Bright variants: `bg.bright_red`, `bg.bright_green`, etc.
- Custom backgrounds: `color.bg.rgb(r, g, b)` - Create custom background colors

### Text Styles

- `bold` - Bold text
- `italic` - Italic text (not supported in all terminals)
- `underline` - Underlined text
- `dim` - Dimmed text
- `reverse` - Reversed colors (swaps foreground and background)
- `strike` - Strikethrough text (not supported in all terminals)

### Predefined Combinations

- `error` - Red text with typewriter effect (for error messages)
- `warning` - Yellow text with blink effect (for warnings)
- `success` - Green text with fade-in effect (for success messages)
- `info` - Blue text with glitch effect (for information messages)

### Interactive Components

- `progress_bar` - Display an animated progress bar
- `typing_prompt` - Show a typewriter-animated prompt and get user input
- `menu` - Display an interactive menu with styled options
- `loading_animation` - Show a simple loading animation
- `countdown` - Display a countdown timer

## Advanced Usage

### Interactive Components

The library includes interactive components for building command-line interfaces:

```python
from fate import color, style
from fate import progress_bar, typing_prompt, menu, loading_animation, countdown

# Display an animated progress bar
progress_bar(
    total=20,                # Total number of steps
    prefix="Processing:",    # Text before the bar
    suffix="Complete",       # Text after the bar
    color_func=color.green,  # Color function to apply
    delay=0.1                # Delay between updates
)

# Display a typewriter-animated prompt and get user input
name = typing_prompt(
    prompt="What is your name? ",
    typing_speed=15,
    prompt_color=color.yellow
)
print(f"Hello, {style.bold(name)}!")

# Display an interactive menu
options = ["Option 1", "Option 2", "Option 3", "Exit"]
choice = menu(
    title="Select an Option",
    options=options,
    title_style=style.bold,
    option_style=color.cyan,
    animate=True
)
print(f"You selected: {options[choice]}")

# Show a loading animation
loading_animation(
    message="Connecting to server",
    duration=3.0,
    color_func=color.green
)

# Display a countdown timer
countdown(
    seconds=5,
    prefix="Starting in",
    suffix="seconds", 
    color_func=color.yellow
)
```

### Custom Animation Parameters

Most effects accept parameters to customize their behavior:

```python
# Customize typewriter effect
print(typewriter("Slow typing...", speed=5))  # Slower typing (5 chars/sec)
print(typewriter("Fast typing!", speed=30))   # Faster typing (30 chars/sec)

# Customize blink effect
print(blink("More blinks", count=5, speed=3))  # 5 blinks at 3 blinks/sec

# Customize glitch effect
print(glitch("Intense glitching", intensity=5, duration=2.0))  # More characters affected

# Customize wave effect
print(wave("Long wave effect", cycles=4, speed=15))  # 4 cycles at 15 frames/sec
```

### Creating Custom Effects

You can create your own custom effects by combining existing effects or writing new animation functions:

```python
from fate import create_effect, animate_text
import random
import time

@create_effect
def jumble(text, iterations=5, speed=10):
    """
    Custom effect that jumbles characters randomly before settling.
    
    Args:
        text: The text to animate
        iterations: Number of random jumbles
        speed: Speed of animation
    
    Returns:
        The original text after animation
    """
    def render_frame(content, step):
        if step >= iterations:
            return content
        
        jumbled = list(content)
        # Jumble some characters
        for i in range(min(step + 1, len(jumbled))):
            idx = random.randint(0, len(jumbled) - 1)
            if jumbled[idx].isalpha():
                jumbled[idx] = chr(random.randint(65, 90) if jumbled[idx].isupper() else random.randint(97, 122))
        
        return ''.join(jumbled)
    
    return animate_text(text, render_func=render_frame, delay=1/speed)

# Use your custom effect
print(jumble("Custom jumble effect"))
```

## Troubleshooting

### Colors or effects not displaying correctly?

1. Make sure your terminal supports ANSI escape codes
2. On Windows, try using Windows Terminal or PowerShell instead of old cmd.exe
3. Check if your terminal settings have ANSI color support enabled
4. If running in a custom environment, ensure it interprets escape sequences correctly

### Performance issues with long animations?

For very long texts or slow terminals, you can:
1. Increase the animation speed parameter
2. Break text into smaller chunks
3. Use simpler effects for large text blocks

### Text appearing twice or animation issues?

If you encounter any issues with text appearing twice during animations or other visual glitches:
1. Make sure you're using the latest version (0.2.2 or later)
2. Try setting `print_final=False` if available in the effect function
3. Ensure you're not printing the result multiple times

## Contributing

Contributions are welcome! Here's how you can help:

1. Report bugs or request features by opening an issue
2. Improve documentation
3. Add new effects or styles
4. Fix bugs or optimize existing code
5. Add tests or examples

### Development Setup

```bash
# Clone the repository
git clone https://github.com/fredised/fated.git
cd fated

# Install development dependencies
pip install -e .
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by various text animation libraries and demos
- Thanks to all contributors who have helped improve this library

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/fredised">Fred</a>
</p>
