import curses

def starri(title, choices):
    def menu(stdscr):
        # Clear the screen
        stdscr.clear()

        # Set up color pairs (optional, you can customize the color scheme)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Highlight color
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default color

        # Define the starting position and initial index for the selection
        current_idx = 0

        # Get the height and width of the terminal window
        height, width = stdscr.getmaxyx()

        # Draw the title in the center
        title_lines = title.split("\n")
        for i, line in enumerate(title_lines):
            stdscr.addstr(i, (width - len(line)) // 2, line, curses.A_BOLD)

        # Function to display the choices
        def display_choices():
            for idx, choice in enumerate(choices):
                # Highlight the current choice
                if idx == current_idx:
                    stdscr.addstr(len(title_lines) + idx, (width - len(choice['label'])) // 2, choice['label'], curses.color_pair(1))
                else:
                    stdscr.addstr(len(title_lines) + idx, (width - len(choice['label'])) // 2, choice['label'], curses.color_pair(2))

        # Display the menu choices
        display_choices()

        while True:
            # Refresh the screen to update
            stdscr.refresh()

            # Get the key input from the user
            key = stdscr.getch()

            # Handle arrow key navigation
            if key == curses.KEY_DOWN:
                current_idx = (current_idx + 1) % len(choices)
            elif key == curses.KEY_UP:
                current_idx = (current_idx - 1) % len(choices)

            # Handle Enter key press to select an option
            elif key == 10:  # Enter key
                # Call the corresponding 'onselect' function for the selected choice
                result = choices[current_idx]["onselect"]()
                
                # If the onselect function returns a submenu, run it
                if callable(result):
                    # If the result is callable, it is another starri menu
                    return result(stdscr)

                if current_idx == len(choices) - 1:  # If "Exit" option is selected
                    break

            # Redraw the menu after every input
            stdscr.clear()
            for i, line in enumerate(title_lines):
                stdscr.addstr(i, (width - len(line)) // 2, line, curses.A_BOLD)
            display_choices()

    # Automatically wrap the menu with curses.wrapper
    curses.wrapper(menu)
