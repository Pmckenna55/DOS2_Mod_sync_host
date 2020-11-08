# DOS2_Mod_sync_host

A simple mod syncing tool for the game Divinity Original Sin 2.

Often differences in mods between the host and other players can be result in a crash. This can be down to players missing mods the host has, or due to unreliable automatic mod updates by steam, some players having different versions of the same mods. The out of sync mod responsible for the crash can be difficult and time consuming to detect.

DOS2_Mod_sync_host is the tool for the host.

1. Place both client csv files recived from client using client version of this tool into the 'client_csv_files' directory

2. Run 'mod_compare.py'

2. On first run you will be prompted to select mod folder paths.

3. Two csv files will be generated containing mod names and sizes of the Steam and documents mods folder, they will appear in 'host_csv_files' directory.

4. These will be compared aginst the client mod lists and any mods client is missing or of incorrect size will be downloaded and placed in the 'Mods' directory.

5. Send the 'Mods' directory to your client who can then place them in their mod folders.
