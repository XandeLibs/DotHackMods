# change xp.ps1
$xpOffset = 0x7d4cc0, 0x8fb2d0, 0x9fa140, 0x9d9260
$lvlScaleInstructions = 0xF3, 0x41, 0x0F, 0x59, 0xD8
$lvlNoop = 0x90, 0x90, 0x90, 0x90, 0x90
$lvlScaleAddress = 0x48f695, 0x56b5f5, 0x5744c1, 0x557cb1
$step = 0x4
#$xpLR = 0xc3, 0xbd, 0xb6, 0xb0, 0xa9, 0xa3, 0x9c, 0x96, 0x82, 0x6f, 0x62, 0x55, 0x3b, 0x1a, 0x0d, 0x0a, 0x08, 0x06, 0x04
$xpOriginal = 0x96, 0x91, 0x8c, 0x87, 0x82, 0x7d, 0x78, 0x73, 0x64, 0x55, 0x4b, 0x41, 0x2d, 0x14, 0x0a, 0x07, 0x05, 0x04, 0x03

$xpmulti = Read-Host "% of original xp(base 100, 130 for last recode)"
if ([string]::IsNullOrWhiteSpace($xpmulti)){
  $xpmulti = 100
}

$xpmulti /= 100

Write-Host "Enable damage level scaling(Y/n)"

$dmg_scale = Read-Host
if ([string]::IsNullOrWhiteSpace($dmg_scale) -or $dmg_scale -eq "y", "Y"){
  $dmg_scale = "y"
}
elseif ($dmg_scale -eq "n","N"){
  $dmg_scale = "n"
}

for ($i = 1; $i -lt 5; $i++) {
  $path = Get-ChildItem .\"hackGU_vol$i.dll"

  $file = [System.IO.File]::ReadAllBytes($path)

  for ($j = 0; $j -lt $xpOriginal.Count; $j++) {
      $offset = $xpOffset[$i-1] + $step * $j
      $newXp = [int]($xpOriginal[$j] * $xpmulti)
      if ($newXp -lt 1) {
          $newXp = 1
      }
      
      $file[$offset]     = $newXp -band 0xFF
      $file[$offset + 1] = 0
      $file[$offset + 2] = 0
      $file[$offset + 3] = 0
  }

  if ($dmg_scale -eq "y"){
    for ($j = 0; $j -lt 5; $j++) {
      $file[$lvlScaleAddress[$i - 1] + $j] = $lvlScaleInstructions[$j]
    }
  }
  else{
    for ($j = 0; $j -lt 5; $j++) {
      $file[$lvlScaleAddress[$i - 1] + $j] = $lvlNoop[$j]
    }
  }

  [System.IO.File]::WriteAllBytes($path, $file)
}

Read-Host "Press any button to continue..."
