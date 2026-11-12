#!/bin/sh
# ReCoF Server for Cry of Fear. Change the map, the number of players and the port here, or set them when you run it:
#   MAP=cof_manhunt_campaign PORT=27016 ./start_server.sh
# cof_campaign_01 starts the co-op campaign, cof_manhunt_campaign the Manhunt one.
# IP is the address to use, only if the machine has more than one network address and the server picks the wrong one.
cd "$(dirname "$0")" || exit 1
MAP=${MAP:-cof_campaign_01}
PLAYERS=${PLAYERS:-4}
PORT=${PORT:-27015}
IP=${IP:-}

if [ ! -f "cryoffear/maps/$MAP.bsp" ]; then
	echo "The Cry of Fear game files are missing: copy the cryoffear folder of your game here. See README-SERVER.txt."
	exit 1
fi
# a partial copy loads the maps but stops the server when a player draws a weapon whose model is missing
if [ ! -f cryoffear/police/models/weapons/p345/p_p345.mdl ] || [ ! -f cryoffear/gfx.wad ]; then
	echo "The cryoffear folder here is incomplete: copy the whole cryoffear folder of your game, every file and folder in it."
	exit 1
fi
if [ ! -f steamclient.so ]; then
	echo "steamclient.so is missing. See README-SERVER.txt."
	exit 1
fi

if [ -n "$IP" ]; then
	set -- +ip "$IP" "$@"
fi

export LD_LIBRARY_PATH=".:$LD_LIBRARY_PATH"
# -insecure: no VAC, which Cry of Fear has nothing for; Steam still checks who joins
exec ./hlds_linux -game cryoffear -insecure -port "$PORT" +maxplayers "$PLAYERS" -dll addons/metamod/dlls/metamod_i386.so +map "$MAP" "$@"
