# Klíčová slova, podle kterých chceme najít procesy
$keywords = @("spotify", "riot", "steam", "razer", "vanguard", "teams", "discord")

foreach ($keyword in $keywords) {
    $matchingProcesses = Get-Process | Where-Object { $_.ProcessName -like "*$keyword*" }

    foreach ($proc in $matchingProcesses) {
        Write-Host "Ukončuji $($proc.ProcessName) (ID: $($proc.Id))"
        Stop-Process -Id $proc.Id -Force
    }

    if ($matchingProcesses.Count -eq 0) {
        Write-Host "Nebyly nalezeny žádné procesy obsahující '$keyword'"
    }
}
