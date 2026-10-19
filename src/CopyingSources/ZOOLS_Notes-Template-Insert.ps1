$inputFile = "C:\DDRTools\log\persist.log"
$appendFile = Join-Path $PSScriptRoot "Note_Template.txt"
$outputFile = "C:\DDRTools\log\persist.log"

if (-not (Test-Path -LiteralPath $inputFile -PathType Leaf))
{
    Write-Host "Error: persist.log does not exist. Exiting."
    exit 1
}

# DEBUG, can remove after confirming it doesn't erase data
$Timestamp = (Get-Date).ToString("yyyy-MM-dd_HHmmss_fff")
Copy-Item -Path $inputFile -Destination "C:\DDRTools\log\persist-backup-$Timestamp.log"


$base64 = Get-Content $inputFile -Raw
$bytes = [Convert]::FromBase64String($base64)
$originalText = [System.Text.Encoding]::UTF8.GetString($bytes)
$appendText = Get-Content $appendFile -Raw

$combinedText = $originalText + $appendText
$combinedBites = [System.Text.Encoding]::UTF8.GetBytes($combinedText)
$outputBase64 = [Convert]::ToBase64String($combinedBites)

[System.IO.File]::WriteAllText($outputFile, $outputBase64)