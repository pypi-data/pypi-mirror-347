from blessed import Terminal

def starri(title, choices):
    term = Terminal()
    selected = 0

    def render():
        print(term.clear)
        print(title)  # Print pre-styled title (e.g., from gradify)
        print()
        for i, choice in enumerate(choices):
            label = choice["label"]
            if i == selected:
                print(term.reverse(f"> {label}"))
            else:
                print(f"  {label}")

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
