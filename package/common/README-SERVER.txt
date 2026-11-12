ReCoF Server
============

A dedicated server for Cry of Fear co-op, for players on ReCoF (https://github.com/caixax/ReCoF). It runs on Windows and on Linux, with Metamod-R and AMX Mod X for plugins. Source: https://github.com/caixax/ReCoF-Server

This package has the server and its plugins, but none of Cry of Fear's files: you need your own copy of the game (it is free on Steam).


1. Put the server together
--------------------------

a) Make a folder for the server and copy into it the cryoffear folder of your Cry of Fear install (on Steam: Library, right click Cry of Fear, Manage, Browse local files). On Linux, copy it over from a PC with the game, for example with SFTP.

b) Extract this package into the same folder and let it replace files. It adds cryoffear/cl_dlls/hl.dll (Windows) or hl.so (Linux), the server's own server.cfg and mapcycle.txt, and cryoffear/addons with Metamod-R and AMX Mod X.

c) Add Steam's server files, which every GoldSrc server needs:
   Windows: steamclient.dll, tier0_s.dll and vstdlib_s.dll, next to hlds.exe. On a PC with Steam, copy them from your Steam folder (C:\Program Files (x86)\Steam). On a server without Steam, install SteamCMD (https://developer.valvesoftware.com/wiki/SteamCMD) and the Half-Life dedicated server with it (steamcmd +login anonymous +app_update 90 -beta steam_legacy +quit), and copy the three files from that server's folder.
   Linux: steamclient.so, next to hlds_linux. Install SteamCMD (https://developer.valvesoftware.com/wiki/SteamCMD), run it once (./steamcmd.sh +quit), then copy its linux32/steamclient.so here.

d) Linux only: the server is 32-bit. On a 64-bit Debian or Ubuntu install its libraries once:
   sudo dpkg --add-architecture i386 && sudo apt update && sudo apt install lib32gcc-s1 lib32stdc++6
   The server runs on Debian 11, Ubuntu 20.04 and newer.


2. Set it up and start it
-------------------------

Edit cryoffear/server.cfg: the server's name, a password, an rcon password, the difficulty.

Start it with start_server.bat (Windows) or ./start_server.sh (Linux). They start it with -insecure: no VAC, which Cry of Fear has nothing for; Steam still checks the players who join. Both start the co-op campaign (cof_campaign_01) for up to 4 players on port 27015; change MAP, PLAYERS and PORT at the top of the script. cof_manhunt_campaign starts the Manhunt campaign.

Open UDP port 27015 (or yours) in the firewall and, at home, forward it in the router.

If the console says "Could not establish connection to Steam servers", look at the "Server IP address" line above it: on a machine with more than one network adapter (WSL, Hyper-V, a VPN) the server can pick one with no internet. Set IP in the start script to the machine's own address (Windows: ipconfig, the adapter with a default gateway; Linux: ip addr).


3. Players
----------

Players need ReCoF (0.2.3 or later): the server turns away the original game unless server.cfg sets rc_require_recof 0. To join, open the console in the game and type: connect <server address>:27015


4. Plugins
----------

AMX Mod X is in cryoffear/addons/amxmodx. Plugins go in plugins/ and are listed in configs/plugins.ini; admins in configs/users.ini. To compile a plugin, use the compiler in scripting/ (amxxpc). Include <cof> for Cry of Fear's weapon, ammo, item and monster names and notes on what differs from Half-Life (scripting/include/cof.inc): most Half-Life plugins work, plugins for Counter-Strike and other games do not.


5. Server settings ReCoF adds
-----------------------------

rc_require_recof 1   only ReCoF players can join
sv_pause_empty 1     with nobody in the game the map waits
sv_restart_empty 1   when the last player leaves, the map loads again


Licenses
--------

ReHLDS (the engine, hlds, filesystem): MIT. Metamod-R: GPL v3. AMX Mod X: GPL v3 with the Half-Life engine exception. The source of every part is public: https://github.com/caixax/ReCoF-Server, https://github.com/caixax/ReCoF-Metamod, https://github.com/caixax/ReCoF-AMXX, https://github.com/caixax/ReCoF (the game DLL). Cry of Fear is by Team Psykskallar and is not part of this package.
