
Debian
====================
This directory contains files used to package commapluscoind/commapluscoin-qt
for Debian-based Linux systems. If you compile commapluscoind/commapluscoin-qt yourself, there are some useful files here.

## commapluscoin: URI support ##


commapluscoin-qt.desktop  (Gnome / Open Desktop)
To install:

	sudo desktop-file-install commapluscoin-qt.desktop
	sudo update-desktop-database

If you build yourself, you will either need to modify the paths in
the .desktop file or copy or symlink your commapluscoinqt binary to `/usr/bin`
and the `../../share/pixmaps/commapluscoin128.png` to `/usr/share/pixmaps`

commapluscoin-qt.protocol (KDE)

