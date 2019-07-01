# Diner Mafia

a 2D RPG written in Python using the [Pygame](https://www.pygame.org/wiki/about) library for the [GameShell Game Jam (2019Q2)](https://itch.io/jam/gameshell-19q2)

![Village Preview](https://user-images.githubusercontent.com/43303199/60416017-6c919c00-9ba2-11e9-96c0-0d37d28611da.gif)

## Background

*Diner Mafia* was designed to run natively on the ClockworkPi GameShell, but you can run the game on any computer that has the latest version of Python and Pygame installed.

## ClockworkPi GameShell Installation

To install *Diner Mafia* you need to ssh into your GameShell from your desktop or laptop and clone this repository. Before doing so make sure that your desktop or laptop is on the same network as the GameShell. Outlined below are the exact steps you need to follow.

1. Open Tiny Cloud on your GameShell

2. On your desktop open your favorite terminal, and type the command under the text "For ssh and scp:" found on the Tiny Cloud page on your GameShell. It should look something like this: `ssh cpi@123.456.7.89`

3. If you established a connection with the GameShell the terminal will ask you for your GameShell's password. Type your password into the terminal to finish the connection. The password for your GameShell is "cpi" by default. Keep in mind that characters will not show up when you type the password into the terminal. Do not worry, this is normal.

4. If you logged in successfully you should see the CPI ASCII logo pop up, and your terminal should start with `cpi@clockworkpi:-$`. From here type the command `git clone https://github.com/austin0209/diner-mafia /home/cpi/games/Python/diner-mafia/` to copy the game onto your GameShell

5. Once the repository has been cloned type the command `mv /home/cpi/games/Python/diner-mafia/33_DinerMafia/ /home/cpi/launcher/Menu/GameShell`. This will create a shortcut in your GameShell's Menu. If you have not ran into any errors then you are done with the terminal. Type `exit` to end the ssh connection to your GameShell.

6. Reload the UI on your GameShell. Once that finishes, find *Diner Mafia* in your menu and click on it to play!
