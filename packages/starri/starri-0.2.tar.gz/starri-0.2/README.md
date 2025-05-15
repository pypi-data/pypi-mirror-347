# Starri

Starri is a simple Python library for creating terminal-based menus using the curses module. It supports navigation with the arrow keys and submenus for a dynamic user experience.

## Installation

You can install Starri with pip:

```pip install starri```

## Usage

Here’s how to use Starri:

```python
import starri as *

def main():
    starri(
        title = "Test Menu"
        choices = [
            {"label": "Option 1", "onselect": lambda: print("Option 1 selected")},
            {"label": "Exit", "onselect": exit}
        ]
    )
    
if __name__ == "__main__":
    main()
```