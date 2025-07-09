# Cesta, kam se uloží VM
$basePath = "D:\VM"
$vhdSize = 20GB
$memory = 2GB
$isoPath = "D:\VM\Windows_Server_2025.iso"  # Cesta k tvému ISO

# Názvy VM, které chceme vytvořit
$vmNames = @("Test-Server1", "Test-Server2", "Test-Server3")

foreach ($name in $vmNames) {
    $vmPath = "$basePath\$name"
    $vhdPath = "$vmPath\$name.vhdx"

    # Vytvoř složku pro VM
    New-Item -ItemType Directory -Path $vmPath -Force | Out-Null

    # Vytvoření VM
    New-VM -Name $name -MemoryStartupBytes $memory -Generation 2 -NewVHDPath $vhdPath -NewVHDSizeBytes $vhdSize -Path $vmPath

    # Připojení ISO k VM
    Set-VMDvdDrive -VMName $name -Path $isoPath

    # Připojení sítě (pokud máš virtuální switch např. "Default Switch")
    Connect-VMNetworkAdapter -VMName $name -SwitchName "Default Switch"

    Write-Output "✅ Vytvořeno: $name"
}
