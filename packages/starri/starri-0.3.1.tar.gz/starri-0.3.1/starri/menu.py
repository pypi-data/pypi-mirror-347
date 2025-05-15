from blessed import Terminal

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

        # Print the title centered
        for i, line in enumerate(title_lines):
            print(term.move_xy((width - len(line)) // 2, i) + line)

        print()
        for i, choice in enumerate(choices):
            label = choice["label"]
            if i == selected:
                print(term.reverse(f"> {label}"))
            else:
                print(f"  {label}")

        # Add this check in the `render()` function
        if height < len(choices) + len(title_lines) + 2:
            raise ValueError("Terminal height is too small for the menu.")

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
