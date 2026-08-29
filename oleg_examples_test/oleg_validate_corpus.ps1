$ErrorActionPreference = 'Stop'

$root = (Resolve-Path -LiteralPath $PSScriptRoot).Path
$errors = New-Object 'System.Collections.Generic.List[string]'

function Add-Error([string]$Message) {
    [void]$script:errors.Add($Message)
}

function Get-DeclaredRecordCount([string]$Text) {
    $number = '(?:\d+|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen)'
    $patterns = @(
        "(?im)^(?:[-#]+\s*|\d+\.\s*)?(?:The\s+)?final\s+(?:registry|register|records|result)(?:\s+size)?[^\r\n]*?(?<count>$number)",
        "(?im)^\s*\d+\.\s*Produce\s+exactly\s+(?<count>$number)\s+final\s+records\b",
        '(?im)^(?:[-#]+\s*|\d+\.\s*)?(?:\u041a\u043e\u043d\u0435\u0447\u043d\u044b\u0439|\u0418\u0442\u043e\u0433\u043e\u0432\u044b\u0439|\u0422\u0440\u0435\u0431\u0443\u0435\u043c\u043e\u0435(?:\s+\u043a\u043e\u043d\u0435\u0447\u043d\u043e\u0435)?)\s+(?:\u0440\u0435\u0435\u0441\u0442\u0440|\u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435)[^\r\n]*?(?<count>\d+)\s+\u0437\u0430\u043f\u0438\u0441'
    )
    $wordValues = @{ zero = 0; one = 1; two = 2; three = 3; four = 4; five = 5; six = 6; seven = 7; eight = 8; nine = 9; ten = 10; eleven = 11; twelve = 12; thirteen = 13; fourteen = 14; fifteen = 15; sixteen = 16 }
    $counts = @()
    foreach ($pattern in $patterns) {
        foreach ($match in [regex]::Matches($Text, $pattern)) {
            $value = $match.Groups['count'].Value.ToLowerInvariant()
            $counts += if ($value -match '^\d+$') { [int]$value } else { $wordValues[$value] }
        }
    }
    return @($counts | Select-Object -Unique)
}

$scenarios = [ordered]@{
    'T001-distributed-release'         = @{ Id = 'T001'; Tier = 'scale';    Namespace = 'AURORA-R7/';      MinFiles = 8;  MinBytes = 40960; MinLines = 400 }
    'T002-supplier-customs'            = @{ Id = 'T002'; Tier = 'standard'; Namespace = 'KITE-CLEAR/';     MinFiles = 5;  MinBytes = 12288; MinLines = 100 }
    'T003-finance-close'               = @{ Id = 'T003'; Tier = 'standard'; Namespace = 'MERIDIAN-CLOSE/'; MinFiles = 5;  MinBytes = 12288; MinLines = 100 }
    'T004-support-incident'            = @{ Id = 'T004'; Tier = 'standard'; Namespace = 'NORTHSTAR-INC/';  MinFiles = 5;  MinBytes = 12288; MinLines = 100 }
    'T005-field-repair'                = @{ Id = 'T005'; Tier = 'standard'; Namespace = 'CEDAR-FIELD/';    MinFiles = 5;  MinBytes = 12288; MinLines = 100 }
    'T006-hr-onboarding'               = @{ Id = 'T006'; Tier = 'standard'; Namespace = 'LANTERN-HR/';     MinFiles = 5;  MinBytes = 12288; MinLines = 100 }
    'T007-healthcare-administration'   = @{ Id = 'T007'; Tier = 'standard'; Namespace = 'HARBOR-ADMIN/';   MinFiles = 5;  MinBytes = 12288; MinLines = 100 }
    'T008-civic-permit'                = @{ Id = 'T008'; Tier = 'standard'; Namespace = 'CIVIC-ORCHID/';   MinFiles = 5;  MinBytes = 12288; MinLines = 100 }
    'T009-travel-event'                = @{ Id = 'T009'; Tier = 'standard'; Namespace = 'ATLAS-EVENT/';    MinFiles = 5;  MinBytes = 12288; MinLines = 100 }
    'T010-research-grant'              = @{ Id = 'T010'; Tier = 'standard'; Namespace = 'QUILL-GRANT/';    MinFiles = 5;  MinBytes = 12288; MinLines = 100 }
    'T011-construction-facilities'     = @{ Id = 'T011'; Tier = 'standard'; Namespace = 'STONEBRIDGE-FM/'; MinFiles = 5;  MinBytes = 12288; MinLines = 100 }
    'T012-retail-catalogue'            = @{ Id = 'T012'; Tier = 'scale';    Namespace = 'MOSAIC-CAT/';     MinFiles = 15; MinBytes = 40960; MinLines = 1 }
    'T013-nonprofit-volunteer'         = @{ Id = 'T013'; Tier = 'standard'; Namespace = 'COMMON-GOOD/';    MinFiles = 5;  MinBytes = 12288; MinLines = 100 }
    'T014-multilingual-operations'     = @{ Id = 'T014'; Tier = 'standard'; Namespace = 'POLYGLOT-OPS/';   MinFiles = 5;  MinBytes = 12288; MinLines = 100 }
    'T015-high-noise-zero'             = @{ Id = 'T015'; Tier = 'zero';     Namespace = 'ECHO-ZERO/';      MinFiles = 5;  MinBytes = 15360; MinLines = 100 }
    'T016-damaged-export-zero'         = @{ Id = 'T016'; Tier = 'zero';     Namespace = 'FRACTURE-ZERO/';  MinFiles = 5;  MinBytes = 15360; MinLines = 100 }
}

$expectedFolders = @($scenarios.Keys)
$scenarioDirs = @(Get-ChildItem -LiteralPath $root -Directory | Where-Object { $_.Name -match '^T\d{3}(?:-|$)' })
$actualFolders = @($scenarioDirs | ForEach-Object Name)

foreach ($folder in $expectedFolders) {
    if ($actualFolders -notcontains $folder) { Add-Error "Missing scenario directory: $folder" }
}
foreach ($folder in $actualFolders) {
    if ($expectedFolders -notcontains $folder) { Add-Error "Unexpected Txxx directory: $folder" }
}
foreach ($group in @($scenarioDirs | ForEach-Object { $_.Name.Substring(0, 4) } | Group-Object | Where-Object Count -gt 1)) {
    Add-Error "Duplicate scenario ID in directories: $($group.Name)"
}

$metrics = @{}
$expectedRecordCounts = @{}
$allNamespaces = @($scenarios.Values | ForEach-Object Namespace)
$bannedPhrases = @(
    'informational only', 'for information only', 'do not infer', 'no task',
    'not a task', 'must not create', 'do not create'
)
$secretPatterns = [ordered]@{
    'private key block' = '-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'
    'AWS access key' = '(?<![A-Z0-9])AKIA[A-Z0-9]{16}(?![A-Z0-9])'
    'GitHub token' = '(?<![A-Za-z0-9])gh[pousr]_[A-Za-z0-9]{36,}'
    'Slack token' = '(?<![A-Za-z0-9])xox[baprs]-[A-Za-z0-9-]{20,}'
    'JWT token' = '(?<![A-Za-z0-9_-])eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'
    'secret assignment' = '(?i)\b(?:api[_-]?key|password|passwd|secret|access[_-]?token)\b\s*[:=]\s*["'']?[A-Za-z0-9/+_.-]{16,}'
}

foreach ($folder in $expectedFolders) {
    $rule = $scenarios[$folder]
    $scenarioPath = Join-Path $root $folder
    if (-not (Test-Path -LiteralPath $scenarioPath -PathType Container)) { continue }

    $inputPath = Join-Path $scenarioPath 'input'
    $expectedPath = Join-Path $scenarioPath 'expected.md'
    if (-not (Test-Path -LiteralPath $inputPath -PathType Container)) {
        Add-Error "$folder has no input directory"
        continue
    }
    if (-not (Test-Path -LiteralPath $expectedPath -PathType Leaf)) {
        Add-Error "$folder has no expected.md"
    }

    $inputFiles = @(Get-ChildItem -LiteralPath $inputPath -File -Recurse)
    $bytes = [int64]0
    $nonblank = 0
    $combined = New-Object System.Text.StringBuilder
    foreach ($file in $inputFiles) {
        $bytes += $file.Length
        $text = [IO.File]::ReadAllText($file.FullName)
        [void]$combined.AppendLine($text)
        $nonblank += @($text -split "`r?`n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }).Count

        foreach ($phrase in $bannedPhrases) {
            if ($text.IndexOf($phrase, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
                Add-Error "$folder input contains banned evaluator phrase '$phrase' in $($file.Name)"
            }
        }
        foreach ($entry in $secretPatterns.GetEnumerator()) {
            if ($text -match $entry.Value) {
                Add-Error "$folder input contains an obvious $($entry.Key) shape in $($file.Name)"
            }
        }
        foreach ($match in [regex]::Matches($text, '(?i)(?:https?://|@)(?<host>[A-Za-z0-9.-]+\.[A-Za-z]{2,})')) {
            $internetHost = $match.Groups['host'].Value.ToLowerInvariant()
            if ($internetHost -notmatch '\.(?:example|test|invalid|localhost)$') {
                Add-Error "$folder input uses non-reserved internet host '$internetHost' in $($file.Name)"
            }
        }
    }

    if ($inputFiles.Count -lt $rule.MinFiles) { Add-Error "$folder has $($inputFiles.Count) input files; floor is $($rule.MinFiles)" }
    if ($bytes -lt $rule.MinBytes) { Add-Error "$folder has $bytes input bytes; floor is $($rule.MinBytes)" }
    if ($nonblank -lt $rule.MinLines) { Add-Error "$folder has $nonblank nonblank lines; floor is $($rule.MinLines)" }
    $metrics[$folder] = @{ Files = $inputFiles.Count; Bytes = $bytes; Lines = $nonblank }

    $allText = $combined.ToString()
    if ($allText.IndexOf($rule.Namespace, [StringComparison]::Ordinal) -lt 0) {
        Add-Error "$folder does not contain its required namespace $($rule.Namespace)"
    }
    foreach ($match in [regex]::Matches($allText, '(?<![A-Za-z0-9])[A-Z][A-Z0-9]+(?:-[A-Z0-9]+)+/')) {
        if ($match.Value -ne $rule.Namespace -and $allNamespaces -contains $match.Value) {
            Add-Error "$folder contains another scenario namespace $($match.Value)"
        }
    }

    if (Test-Path -LiteralPath $expectedPath -PathType Leaf) {
        $expectedText = [IO.File]::ReadAllText($expectedPath)
        $declaredCounts = @(Get-DeclaredRecordCount $expectedText)
        if ($declaredCounts.Count -eq 0) {
            Add-Error "$folder expected.md has no recognized final record count"
        } elseif ($declaredCounts.Count -gt 1) {
            Add-Error "$folder expected.md has conflicting final record counts: $($declaredCounts -join ', ')"
        } else {
            $expectedRecordCounts[$folder] = $declaredCounts[0]
        }
        foreach ($match in [regex]::Matches($expectedText, '(?i)(?<![A-Za-z0-9])input/[A-Za-z0-9][A-Za-z0-9._/-]*')) {
            $relative = $match.Value.TrimEnd('.', ',', ';', ':')
            $sourcePath = Join-Path $scenarioPath ($relative -replace '/', [IO.Path]::DirectorySeparatorChar)
            if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
                Add-Error "$folder expected.md references missing source $relative"
            }
        }
    }
}

$indexPath = Join-Path $root 'index.csv'
if (-not (Test-Path -LiteralPath $indexPath -PathType Leaf)) {
    Add-Error 'Missing index.csv'
} else {
    $indexRows = @(Import-Csv -LiteralPath $indexPath)
    if ($indexRows.Count -ne 16) { Add-Error "index.csv has $($indexRows.Count) rows; expected 16" }
    foreach ($group in @($indexRows | Group-Object id | Where-Object Count -gt 1)) {
        Add-Error "Duplicate scenario ID in index.csv: $($group.Name)"
    }
    foreach ($row in $indexRows) {
        if (-not $scenarios.Contains($row.folder)) {
            Add-Error "index.csv lists unexpected folder $($row.folder)"
            continue
        }
        $rule = $scenarios[$row.folder]
        if ($row.id -ne $rule.Id) { Add-Error "index.csv ID mismatch for $($row.folder)" }
        if ($row.tier -ne $rule.Tier) { Add-Error "index.csv tier mismatch for $($row.folder)" }
        $metric = $metrics[$row.folder]
        if ($null -eq $metric) { continue }
        if ([int]$row.input_files -ne $metric.Files) { Add-Error "index.csv input_files mismatch for $($row.folder)" }
        if ([int64]$row.input_bytes -ne $metric.Bytes) { Add-Error "index.csv input_bytes mismatch for $($row.folder)" }
        if ([int]$row.nonblank_lines -ne $metric.Lines) { Add-Error "index.csv nonblank_lines mismatch for $($row.folder)" }
        if ($expectedRecordCounts.ContainsKey($row.folder) -and [int]$row.expected_records -ne $expectedRecordCounts[$row.folder]) {
            Add-Error "index.csv expected_records mismatch for $($row.folder): index has $($row.expected_records), expected.md declares $($expectedRecordCounts[$row.folder])"
        }
    }
}

if ($errors.Count -gt 0) {
    Write-Host "Corpus validation failed with $($errors.Count) error(s):" -ForegroundColor Red
    foreach ($message in $errors) { Write-Host "- $message" -ForegroundColor Red }
    exit 1
}

$totalFiles = ($metrics.Values | ForEach-Object Files | Measure-Object -Sum).Sum
$totalBytes = ($metrics.Values | ForEach-Object Bytes | Measure-Object -Sum).Sum
$totalLines = ($metrics.Values | ForEach-Object Lines | Measure-Object -Sum).Sum
Write-Host "Corpus validation passed: 16 scenarios, $totalFiles input files, $totalBytes input bytes, $totalLines nonblank input lines."
exit 0
