$vmNames = @("Test-Server1", "Test-Server2", "Test-Server3")

foreach ($name in $vmNames) {
    Stop-VM -Name $name -Force
    Write-Output "⏹️ VM vypnuta: $name"
}
