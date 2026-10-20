Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$inputFile = "C:\DDRTools\log\persist.log"
$outputFile = "C:\DDRTools\log\persist.log"

if (-not (Test-Path -LiteralPath $inputFile -PathType Leaf))
{
    Write-Host "Error: persist.log does not exist. Exiting."
    exit 1
}




# $labelCountFontSize = 22
# $labelCountFont = New-Object System.Drawing.Font("Segoe UI", $labelCountFontSize, [System.Drawing.FontStyle]::Bold)
# $labelCountColor = [System.Drawing.Color]::Green
$buttonFont = New-Object System.Drawing.Font("Segoe UI", 12)

$formClicker = New-Object System.Windows.Forms.Form     # Define the form - this is the window where all other componenets will be added with Controls.Add()
$formClicker.Text = "Notes Template Maker: GUI"          # Title the window
$formClicker.ClientSize = New-Object System.Drawing.Size(500, 600)    # Size the form
$formClicker.StartPosition = "CenterScreen"             # Center our form when it loads
$formClicker.FormBorderStyle = "FixedSingle"            # Remove the resize handle
$formClicker.MinimizeBox = $false                       # Hides the minimize button
$formClicker.MaximizeBox = $false                       # Hides the maximize button
$formClicker.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon("$env:WINDIR\System32\msra.exe")   # Pick an icon

$startX = 20
$startY = 20
$rowSpacing = 40
$labelWidth = 130
$textBoxWidth = 280
$rowHeight = 20

$fieldNames = @(
    "Work Order",
    "Quality Care Email",
    "Trend Micro ProdKey",
    "Email 1",
    "Email 1 PW"
    "Email 2",
    "Email 2 PW",
    "Carb Email"
    "Carb PW",
    "Carb Key",
    "MS Email",
    "MS PW",
    "Office"
)
$script:textBoxes = @()
$script:formValues = @()

for ($i = 0; $i -lt $fieldNames.Count; $i++)
{
    $currentY = $startY + ($i * $rowSpacing)

    $label = New-Object System.Windows.Forms.label
    $label.Text = "$($fieldNames[$i]):"
    $label.Location = New-Object System.Drawing.Point($startX, $currentY)
    $label.Size = New-Object System.Drawing.Size($labelWidth, $rowHeight)
    $label.TextAlign = [System.Drawing.ContentAlignment]::MiddleLeft
    $label.Font = New-Object System.Drawing.Font("Segoe UI", 11)

    $formClicker.Controls.Add($label)
    
    $textBox = New-Object System.Windows.forms.TextBox
    $textBox.Location = New-Object System.Drawing.Point(200, $currentY)
    $textBox.Size = New-Object System.Drawing.Size($textBoxWidth, $rowHeight)
    $formClicker.Controls.Add($textBox)

    $script:textBoxes += $textBox
}

$buttonEnd = New-Object System.Windows.Forms.Button
$buttonEnd.Text = "Exit"
$buttonEnd.Font = $buttonFont                       
$buttonEnd.AutoSize = $true                         
$formClicker.Controls.Add($buttonEnd)

$buttonSkip = New-Object System.Windows.Forms.Button
$buttonSkip.Text = "Blank"
$buttonSkip.Font = $buttonFont                       
$buttonSkip.AutoSize = $true                         
$formClicker.Controls.Add($buttonSkip)

$buttonSub = New-Object System.Windows.Forms.Button
$buttonSub.Text = "Submit"
$buttonSub.Font = $buttonFont
$buttonSub.AutoSize = $true
$formClicker.Controls.Add($buttonSub)

$buttonY = $formClicker.ClientSize.Height - $buttonSkip.Height - 10

$totalWidth = $buttonSkip.Width + $buttonSub.Width + $buttonEnd.Width + 20
$startX = [int](($formClicker.ClientSize.Width - $totalWidth) / 2)

$buttonEnd.Location = New-Object System.Drawing.Point($startX, $buttonY)
$buttonSkip.Location = New-Object System.Drawing.Point(
    ($startX + $buttonSkip.Width + 10), $buttonY
)
$buttonSub.Location = New-Object System.Drawing.Point(
    ($startX + $buttonSkip.Width + $buttonSkip.Width + 20), $buttonY
)

# $buttonSkipX =(($formClicker.ClientSize.Width - $buttonSkip.Width - $buttonSub.Width)/2 - 5)
# $buttonSubX = ($buttonSkipX + $buttonSkip.Width + 5)
# $buttonY = ($formClicker.ClientSize.Height - $buttonSkip.Height - 10)

# # Place the elements on the form
# $buttonSkip.Location = New-Object System.Drawing.Point($buttonSkipX, $buttonY)
# $buttonSub.Location = New-Object System.Drawing.Point($buttonSubX, $buttonY)


#region Logic

$buttonEnd.Add_Click({
    $formClicker.Tag = "Cancel"
    $formClicker.Close()
})

$buttonSkip.Add_Click({
    $formClicker.Close()
})

$buttonSub.Add_Click({
    $script:formValues = @{}

    for ($i = 0; $i -lt $fieldNames.Count; $i++) {
        $script:formValues[$fieldNames[$i]] = $script:textBoxes[$i].Text
    }

    $formClicker.Close()
})

$formClicker.ShowDialog() | Out-Null

if ($formClicker.Tag -eq "Cancel")
{
    exit 0
}



$appendTextFormatted = @"
*****************************
Product Keys 
(modified as of WO#$($formValues["Work Order"]))
*****************************
Quality Care
Email: $($formValues["Quality Care Email"])
Trend Micro AV Key: $($formValues["Trend Micro ProdKey"])
*****************************
Email(s)
EM 1: $($formValues["Email 1"])
EM 1 PW: $($formValues["Email 1 PW"])
EM 2: $($formValues["Email 2"])
EM 2 PW: $($formValues["Email 2 PW"])
*****************************
Carbonite
Email: $($formValues["Carb Email"])
Carb PW: $($formValues["Carb PW"])
Key: $($formValues["Carb Key"])
*****************************
MS Account
email: $($formValues["MS Email"])
PW: $($formValues["MS PW"])
Office: $($formValues["Office"])
*****************************
"@


# DEBUG, can remove after confirming it doesn't erase data
$Timestamp = (Get-Date).ToString("yyyy-MM-dd_HHmmss_fff")
Copy-Item -Path $inputFile -Destination "C:\DDRTools\log\persist-backup-$Timestamp.log"


$base64 = Get-Content $inputFile -Raw
if ([string]::IsNullOrWhiteSpace($base64)) 
{
    $originalText = ""
}
else 
{
    $bytes = [Convert]::FromBase64String($base64)
    $originalText = [System.Text.Encoding]::UTF8.GetString($bytes)
}

$combinedText = $originalText + $appendTextFormatted
$combinedBites = [System.Text.Encoding]::UTF8.GetBytes($combinedText)
$outputBase64 = [Convert]::ToBase64String($combinedBites)

# Save the text to a file
[System.IO.File]::WriteAllText($outputFile, $outputBase64)