from blessed import Terminal
import os

def starri(title, choices):
    term = Terminal()
    selected = 0

    def render():
        print(term.clear)
        height, width = term.height, term.width
        title_lines = title.splitlines()
        max_title_width = max(len(line) for line in title_lines)

        # Ensure the title fits within the terminal
        if max_title_width > width:
            raise ValueError("Terminal width is too small for the title.")

        # Calculate vertical offset for centering
        total_content_height = len(title_lines) + len(choices)
        if total_content_height > height:
            raise ValueError("Terminal height is too small for the menu.")
        vertical_offset = (height - total_content_height) // 2

        # Print the title centered
        for i, line in enumerate(title_lines):
            print(term.move_xy((width - len(line)) // 2, vertical_offset + i) + line)

        # Print the options centered
        for i, choice in enumerate(choices):
            label = choice["label"]
            y = vertical_offset + len(title_lines) + i 
            if i == selected:
                print(term.move_xy((width - len(label) - 2) // 2, y) + term.reverse(f"> {label}"))
            else:
                print(term.move_xy((width - len(label) - 2) // 2, y) + f"  {label}")

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
