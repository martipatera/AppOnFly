$basePath = "D:\VM"
$vmNames = @("Test-Server1", "Test-Server2", "Test-Server3")

foreach ($name in $vmNames) {
    # Zastavení, pokud běží
    if ((Get-VM -Name $name).State -ne 'Off') {
        Stop-VM -Name $name -Force
        Start-Sleep -Seconds 2
    }

    # Odebrání z Hyper-V
    Remove-VM -Name $name -Force
    Write-Output "❌ VM odebrána: $name"

    # Smazání složky s daty
    $vmPath = "$basePath\$name"
    Remove-Item -Path $vmPath -Recurse -Force
    Write-Output "🧹 Smazána složka: $vmPath"
}
