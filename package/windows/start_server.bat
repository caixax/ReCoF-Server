@echo off
rem ReCoF Server for Cry of Fear. Change the map, the number of players and the port here.
rem cof_campaign_01 starts the co-op campaign, cof_manhunt_campaign the Manhunt one.
cd /d "%~dp0"
set MAP=cof_campaign_01
set PLAYERS=4
set PORT=27015
rem The address to use, only if the PC has more than one network adapter (WSL, Hyper-V, a VPN) and the server picks the wrong one
set IP=

if not exist cryoffear\maps\%MAP%.bsp (
	echo The Cry of Fear game files are missing: copy the cryoffear folder of your game here. See README-SERVER.txt.
	pause
	exit /b 1
)
rem a partial copy loads the maps but stops the server when a player draws a weapon whose model is missing
if not exist cryoffear\police\models\weapons\p345\p_p345.mdl goto partial
if not exist cryoffear\gfx.wad goto partial
goto files_ok
:partial
echo The cryoffear folder here is incomplete: copy the whole cryoffear folder of your game, every file and folder in it.
pause
exit /b 1
:files_ok
if not exist steamclient.dll (
	echo steamclient.dll, tier0_s.dll and vstdlib_s.dll are missing. See README-SERVER.txt.
	pause
	exit /b 1
)

set IPARG=
if not "%IP%"=="" set IPARG=+ip %IP%

rem -insecure: no VAC, which Cry of Fear has nothing for; Steam still checks who joins
.\hlds.exe -console -game cryoffear -insecure %IPARG% -port %PORT% +maxplayers %PLAYERS% -dll addons/metamod/dlls/metamod.dll +map %MAP% %*
