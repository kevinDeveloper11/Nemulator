<?php
$files = glob("*.{nes,smc,sfc,gb,gbc,gba,z64,nds,bin,iso,cue}", GLOB_BRACE);
echo json_encode($files);
