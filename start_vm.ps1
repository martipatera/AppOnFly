$vmNames = @("Test-Server1", "Test-Server2", "Test-Server3")

foreach ($name in $vmNames) {
    Start-VM -Name $name
    Write-Output "▶️ VM spuštěna: $name"
}
