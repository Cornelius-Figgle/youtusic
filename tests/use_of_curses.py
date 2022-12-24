import curses

def main(main_screen):
    curses.echo()
    main_screen.addstr('smth\n')
    main_screen.refresh()
    var = main_screen.getstr()
    main_screen.addstr(var)
    main_screen.refresh()
    curses.napms(1000)

curses.wrapper(main)