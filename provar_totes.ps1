# provar_totes.ps1
# Executa quantitzacio + desquantitzacio (escalar, regions, blocs) sobre totes les imatges.
# Us:  powershell -ExecutionPolicy Bypass -File .\provar_totes.ps1
#      .\provar_totes.ps1 -Deltas 2,5,10 -MidaBloc 256 -MaxDelta 23 -Entropia 0

param(
    [string]$DirImatges = "..\imatges",
    [int]$Entropia      = 0,
    [int[]]$Deltas      = @(5),
    [int]$MidaBloc      = 256,
    [int]$MaxDelta      = 23,
    [string]$Log        = "resultats_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
)

$imatges = @(
    "03508649.ube16_1_512_512.raw",
    "03508649.ube16_64_512_512.raw",
    "aviris_yellowstone_f060925t01p00r12_sc00_cal.sbe16_224_512_677.raw",
    "italia.ube16_1_5490_5490.raw",
    "Landsat_agriculture.ube16_6_1024_1024.raw",
    "mamo_1.ube16_1_3576_2944.raw",
    "mamo_1.ule2_1_3576_2944.raw",
    "n1_GRAY.ube8_1_2560_2048.raw",
    "n1_RGB.ube8_3_2560_2048.raw"
)

$resum = New-Object System.Collections.Generic.List[object]

function Escriu([string]$text) {
    Write-Host $text
    Add-Content -Path $Log -Value $text
}

function Executa([string]$img, [string[]]$argsExtra) {
    $ruta = Join-Path $DirImatges $img
    $cmd  = "python .\main.py $ruta $Entropia $($argsExtra -join ' ')"
    Escriu "`n>>> $cmd"

    if (-not (Test-Path $ruta)) {
        Escriu "    [SKIP] No existeix $ruta"
        $resum.Add([pscustomobject]@{ Imatge=$img; Prova=($argsExtra -join ' '); Estat="NO TROBADA"; Segons=0 })
        return
    }

    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $sortida = & python .\main.py $ruta $Entropia @argsExtra 2>&1 | ForEach-Object { "$_" }
    $codi = $LASTEXITCODE
    $sw.Stop()

    foreach ($linia in $sortida) { Escriu "    $linia" }

    $estat = if ($codi -eq 0) { "OK" } else { "ERROR ($codi)" }
    Escriu ("    [{0}] {1:N1} s" -f $estat, $sw.Elapsed.TotalSeconds)

    $resum.Add([pscustomobject]@{
        Imatge = $img
        Prova  = ($argsExtra -join ' ')
        Estat  = $estat
        Segons = [math]::Round($sw.Elapsed.TotalSeconds, 1)
    })
}

Escriu "Inici: $(Get-Date)  |  Entropia=$Entropia  Deltas=$($Deltas -join ',')  Bloc=$MidaBloc  MaxDelta=$MaxDelta"

foreach ($img in $imatges) {
    Escriu "`n==================== $img ===================="
    foreach ($d in $Deltas) {
        Executa $img @("escalar", "$d")
        Executa $img @("regions", "$d")
    }
    Executa $img @("blocs", "$MidaBloc", "$MaxDelta")
}

Escriu "`n==================== RESUM ===================="
$taula = $resum | Format-Table -AutoSize | Out-String
Escriu $taula
Escriu "Log guardat a: $Log"
