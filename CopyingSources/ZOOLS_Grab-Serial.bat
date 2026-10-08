@echo off
powershell -NoProfile -ExecutionPolicy Bypass -Command "$f=[IO.File]::ReadAllText('%~f0'); Invoke-Expression ($f.Substring($f.IndexOf('#'+'PS-START')))"
echo.
pause
exit /b
#PS-START
function Clean($v) {
    if ([string]::IsNullOrWhiteSpace($v) -or $v -match '^(None|Default string|To be filled by O\.E\.M\.|System Serial Number|Not Specified|N/A|0+)$') { '(not programmed)' }
    else { $v.Trim() }
}

$cs   = Get-CimInstance Win32_ComputerSystem
$csp  = Get-CimInstance Win32_ComputerSystemProduct
$bios = Get-CimInstance Win32_BIOS
$bb   = Get-CimInstance Win32_BaseBoard
$enc  = Get-CimInstance Win32_SystemEnclosure

Write-Host ""
Write-Host "Manufacturer  : $($cs.Manufacturer)"
Write-Host "Model         : $($cs.Model)"
Write-Host "BIOS Serial   : $(Clean $bios.SerialNumber)"
Write-Host "Board Serial  : $(Clean $bb.SerialNumber)"
Write-Host "Product S/N   : $(Clean $csp.IdentifyingNumber)"
Write-Host "Enclosure S/N : $(Clean ($enc.SerialNumber | Select-Object -First 1))"
Write-Host "System UUID   : $($csp.UUID)"
Write-Host ""
Write-Host "Disks:"
Get-PhysicalDisk | Format-Table FriendlyName, BusType, MediaType, SerialNumber -AutoSize | Out-String | Write-Host