import re
from blessed import Terminal

def starri(title, choices):
    term = Terminal()
    selected = 0

    def visible_length(text):
        # Remove ANSI escape sequences to calculate the visible length
        return len(re.sub(r'\x1b\[[0-9;]*m', '', text))

    def render():
        print(term.clear)
        height, width = term.height, term.width
        title_lines = title.splitlines()

        # Print the title centered
        for i, line in enumerate(title_lines):
            visible_width = visible_length(line)  # Calculate visible width
            x = (width - visible_width) // 2  # Calculate horizontal center
            y = i  # Vertical position for each line of the title
            print(term.move_xy(x, y) + line)

        # Print the options centered
        for i, choice in enumerate(choices):
            label = choice["label"]
            label_with_cursor = f"> {label}" if i == selected else f"  {label}"
            x = (width - len(label_with_cursor)) // 2  # Calculate horizontal center
            y = len(title_lines) + 2 + i  # Position below the title
            print(term.move_xy(x, y) + (term.reverse(label_with_cursor) if i == selected else label_with_cursor))

    with term.cbreak(), term.hidden_cursor():
        render()
        while True:
            key = term.inkey()
            if key.name == "KEY_UP":
                selected = (selected - 1) % len(choices)
            elif key.name == "KEY_DOWN":
                selected = (selected + 1) % len(choices)
            elif key.name == "KEY_ENTER" or key == "\n":
                print(term.clear)
                choices[selected]["onselect"]()
                break
            render()