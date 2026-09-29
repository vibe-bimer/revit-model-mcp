<#
.SYNOPSIS
Runs one or more Revit instances as a copy farm for revit_rebuild_model_ids, with ids that never overlap.

.DESCRIPTION
The add-in takes its port, token and channel directory from REVIT_MCP_HTTP_PORT, REVIT_MCP_TOKEN and
REVIT_MCP_CHANNEL_DIR, so every instance can run next to the others without code changes. Each instance
gets its own scheduled task, because Revit refuses to start from an SSH session.

Copies are handed out in batches. One batch runs inside one new document, where Revit keeps handing out
higher ids, so the batch's copies never overlap. Every following batch is pushed into a block of its own
with `seed`: the destination's ids start at the template's own base id (2473 for the metric template and
this model), and a seed of N moves that start N ids up. A batch therefore reserves
copiesPerBatch * BlockSize ids; BlockSize defaults to 2048 against the measured span of 1784 ids per copy.

A copy that Revit refuses to paste in one call comes out of the element by element path with
idMappingVerified=false. The farm then redoes that single copy in a fresh document, seeded to start right
after the copy before it, and reports the repair.

.PARAMETER Action
setup   creates the extra instances (directory, scheduled task) and starts them
run     writes the copies and verifies that no two copies share an id
status  shows what the instances answer
teardown removes the extra instances and their directories

.EXAMPLE
.\rebuild-farm.ps1 -Action setup -Instances 3
.\rebuild-farm.ps1 -Action run -Instances 3 -Copies 21 -CopiesPerBatch 7
.\rebuild-farm.ps1 -Action teardown -Instances 3
#>
param(
    [ValidateSet('setup', 'run', 'status', 'teardown')] [string] $Action = 'status',
    [int] $Instances = 3,
    [int] $Copies = 21,
    [int] $CopiesPerBatch = 7,
    [string] $Model = 'E:\revitmcp-test\建筑结构.rvt',
    [string] $Destination = 'E:\revitmcp-test\farm',
    [int] $FirstPort = 53110,
    [int] $BlockSize = 2048,
    [switch] $SkipVerification
)

$ErrorActionPreference = 'Stop'
$revitExe = 'D:\Program Files\Autodesk\Revit 2020\Revit.exe'
$logDirectory = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'RevitModelMcp\Logs'

$standardDirectory = Join-Path $env:LOCALAPPDATA 'RevitModelMcp'
$standardSettings = Join-Path $standardDirectory 'settings.json'
$standardToken = if (Test-Path $standardSettings) { (Get-Content $standardSettings -Raw | ConvertFrom-Json).token } else { '' }

function Get-FarmInstance {
    param([int] $Index)
    $port = $FirstPort + $Index
    if ($Index -eq 0) {
        return [pscustomobject]@{
            Index     = 0
            Port      = $port
            Token     = $standardToken
            Directory = $standardDirectory
            Task      = 'RevitMcpLaunch2020'
            Prefix    = 'batch1'
            Standard  = $true
        }
    }
    [pscustomobject]@{
        Index     = $Index
        Port      = $port
        Token     = "farm-$port-token"
        Directory = (Join-Path 'C:\Users\Administrator' "rmcp-$port")
        Task      = "RevitMcpFarm$port"
        Prefix    = "batch$($Index + 1)"
        Standard  = $false
    }
}

function Invoke-FarmRequest {
    param([string] $Method, [int] $Port, [string] $Token, [string] $Path, [string] $Body = '')
    $uri = "http://127.0.0.1:$Port$Path"
    $headers = @{ Authorization = "Bearer $Token" }
    if ($Body) {
        return Invoke-RestMethod -Method $Method -Uri $uri -Headers $headers -ContentType 'application/json' -Body $Body -TimeoutSec 900
    }
    return Invoke-RestMethod -Method $Method -Uri $uri -Headers $headers -TimeoutSec 30
}

function Wait-FarmInstance {
    param([pscustomobject] $Instance, [int] $Seconds = 240)
    $deadline = (Get-Date).AddSeconds($Seconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $health = Invoke-FarmRequest -Method Get -Port $Instance.Port -Token $Instance.Token -Path '/health'
            if ($health.ok) { return $health }
        } catch { }
        Start-Sleep -Seconds 5
    }
    throw "Instance on port $($Instance.Port) did not answer within $Seconds seconds."
}

function Start-FarmInstance {
    param([pscustomobject] $Instance)
    if ($Instance.Standard) {
        Start-ScheduledTask -TaskName $Instance.Task
        Write-Output "standard instance started (port $($Instance.Port))"
        return
    }
    New-Item -ItemType Directory -Force -Path $Instance.Directory | Out-Null
    $wrapper = @"
`$env:REVIT_MCP_HTTP_PORT = '$($Instance.Port)'
`$env:REVIT_MCP_TOKEN = '$($Instance.Token)'
`$env:REVIT_MCP_CHANNEL_DIR = '$($Instance.Directory)'
Start-Process '$revitExe' -ArgumentList '"$Model"'
"@
    $wrapperPath = Join-Path 'C:\Users\Administrator' "launch-$($Instance.Task).ps1"
    Set-Content -Path $wrapperPath -Value $wrapper -Encoding ASCII
    schtasks /create /tn $Instance.Task /tr "powershell -NoProfile -ExecutionPolicy Bypass -File $wrapperPath" /sc once /st 23:59 /f /it | Out-Null
    Start-ScheduledTask -TaskName $Instance.Task
    Write-Output "instance $($Instance.Port) started (channel $($Instance.Directory))"
}

function Stop-FarmInstance {
    param([pscustomobject] $Instance)
    schtasks /delete /tn $Instance.Task /f 2>&1 | Out-Null
    Remove-Item (Join-Path 'C:\Users\Administrator' "launch-$($Instance.Task).ps1") -Force -ErrorAction SilentlyContinue
}

function Submit-CopyBatch {
    param([pscustomobject] $Instance, [string] $Pattern, [int] $Count, [int] $Seed)
    $payload = @{
        command         = 'rebuild-model-ids'
        destinationPath = $Pattern
        copies          = $Count
        overwrite       = $true
    }
    if ($Seed -gt 0) { $payload['seed'] = $Seed }
    $body = $payload | ConvertTo-Json -Compress
    for ($attempt = 1; $attempt -le 40; $attempt++) {
        try {
            return Invoke-FarmRequest -Method Post -Port $Instance.Port -Token $Instance.Token -Path '/jobs' -Body $body
        } catch {
            # A busy instance answers 409 while another job still runs; waiting is the whole fix.
            Start-Sleep -Seconds 15
        }
    }
    throw "Instance on port $($Instance.Port) stayed busy for the batch."
}

function Get-CopyIds {
    param([object] $CopyResult)
    $ids = New-Object System.Collections.Generic.HashSet[int64]
    foreach ($pair in $CopyResult.idMapping) { [void]$ids.Add([int64]$pair.new) }
    return $ids
}

$farm = @()
for ($index = 0; $index -lt $Instances; $index++) { $farm += Get-FarmInstance -Index $index }

switch ($Action) {
    'status' {
        foreach ($instance in $farm) {
            try {
                $health = Invoke-FarmRequest -Method Get -Port $instance.Port -Token $instance.Token -Path '/health'
                Write-Output ("port {0} ok plugin={1} document='{2}'" -f $instance.Port, $health.pluginVersion, $health.documentName)
            } catch {
                Write-Output ("port {0} not reachable" -f $instance.Port)
            }
        }
    }

    'setup' {
        foreach ($instance in $farm) {
            try {
                $health = Invoke-FarmRequest -Method Get -Port $instance.Port -Token $instance.Token -Path '/health'
                Write-Output ("port {0} already answering document='{1}'" -f $instance.Port, $health.documentName)
                continue
            } catch { }
            Start-FarmInstance -Instance $instance
        }
        foreach ($instance in $farm) { $health = Wait-FarmInstance -Instance $instance; Write-Output ("port {0} ready document='{1}'" -f $instance.Port, $health.documentName) }
    }

    'teardown' {
        Get-Process Revit -ErrorAction SilentlyContinue | Stop-Process -Force
        Start-Sleep -Seconds 8
        foreach ($instance in ($farm | Where-Object { $_.Index -gt 0 })) {
            Stop-FarmInstance -Instance $instance
            Remove-Item $instance.Directory -Recurse -Force -ErrorAction SilentlyContinue
        }
        Start-ScheduledTask -TaskName 'RevitMcpLaunch2020'
        Write-Output 'farm removed, the standard instance is coming back'
    }

    'run' {
        New-Item -ItemType Directory -Force -Path $Destination | Out-Null
        $perInstance = [math]::Ceiling($Copies / $Instances)
        $batches = @()
        for ($index = 0; $index -lt $Instances; $index++) {
            $remaining = $Copies - ($index * $perInstance)
            if ($remaining -le 0) { continue }
            $batches += [pscustomobject]@{
                Instance = $farm[$index]
                Count    = [math]::Min($CopiesPerBatch, $remaining)
                Seed     = $index * $perInstance * $BlockSize
                First    = $index * $perInstance + 1
            }
        }
        $watch = [Diagnostics.Stopwatch]::StartNew()
        $workers = @()
        foreach ($batch in $batches) {
            $pattern = Join-Path $Destination "$($batch.Instance.Prefix)-{n}.rvt"
            $workers += Start-Job -ScriptBlock {
                param($port, $token, $pattern, $count, $seed)
                $payload = @{ command = 'rebuild-model-ids'; destinationPath = $pattern; copies = $count; overwrite = $true }
                if ($seed -gt 0) { $payload['seed'] = $seed }
                $body = $payload | ConvertTo-Json -Compress
                for ($attempt = 1; $attempt -le 60; $attempt++) {
                    try {
                        $answer = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:$port/jobs" -Headers @{ Authorization = "Bearer $token" } -ContentType 'application/json' -Body $body -TimeoutSec 1800
                        if (-not $answer.data) {
                            $keys = ($answer | Get-Member -MemberType NoteProperty | Select-Object -ExpandProperty Name) -join ','
                            Write-Output ("port {0}: answer without data, keys={1}" -f $port, $keys)
                        }
                        if ($answer.jobId -and -not $answer.data) {
                            # The channel stops waiting after about two minutes and hands back a job id; the job
                            # itself keeps running, so the result is fetched until it is there.
                            for ($poll = 1; $poll -le 600; $poll++) {
                                Start-Sleep -Seconds 5
                                $answer = Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:$port/jobs/$($answer.jobId)" -Headers @{ Authorization = "Bearer $token" } -TimeoutSec 60
                                if ($answer.data) { break }
                            }
                        }
                        return [pscustomobject]@{ Port = $port; Ok = $true; Result = $answer }
                    } catch { Start-Sleep -Seconds 15 }
                }
                return [pscustomobject]@{ Port = $port; Ok = $false; Error = 'stayed busy' }
            } -ArgumentList $batch.Instance.Port, $batch.Instance.Token, $pattern, $batch.Count, $batch.Seed
            Write-Output ("batch on port {0}: {1} copies, seed {2}" -f $batch.Instance.Port, $batch.Count, $batch.Seed)
        }
        Wait-Job $workers -Timeout 3600 | Out-Null
        $results = Receive-Job $workers
        Remove-Job $workers -Force
        Write-Output ("wall clock: {0}s" -f [int]$watch.Elapsed.TotalSeconds)
        foreach ($workerResult in $results) {
            if ($workerResult.Ok) {
                Write-Output ("port {0}: success={1} copies={2} copyResults={3} message='{4}'" -f $workerResult.Port, $workerResult.Result.success, $workerResult.Result.data.copies, @($workerResult.Result.data.copyResults).Count, $workerResult.Result.message)
            } else {
                Write-Output ("port {0}: worker failed: {1}" -f $workerResult.Port, $workerResult.Error)
            }
        }

        # Keep a record of every copy: file, id range, whether the batch had to isolate elements.
        $copyList = @()
        $failures = @()
        foreach ($batch in $batches) {
            $worker = $results | Where-Object { $_.Port -eq $batch.Instance.Port } | Select-Object -First 1
            if (-not $worker -or -not $worker.Ok) {
                $failures += "port $($batch.Instance.Port): $($worker.Error)"
                continue
            }
            $index = 0
            foreach ($copy in $worker.Result.data.copyResults) {
                $index++
                $copyList += [pscustomobject]@{
                    Port         = $batch.Instance.Port
                    Seed         = $batch.Seed
                    Count        = $copy.count
                    Verified     = [bool]$copy.idMappingVerified
                    Min          = [int64]$copy.newIdMin
                    Max          = [int64]$copy.newIdMax
                    Path         = $copy.destinationPath
                    Global       = $batch.First + $index - 1
                    Ids          = (Get-CopyIds -CopyResult $copy)
                }
            }
        }

        # A copy that came out of the element by element path is redone alone in a fresh document, seeded to
        # start right after the copy before it, so the repaired copy keeps its own id block.
        foreach ($copy in ($copyList | Where-Object { -not $_.Verified })) {
            $previous = $copyList | Where-Object { $_.Global -lt $copy.Global } | Sort-Object Global -Descending | Select-Object -First 1
            $base = ($copyList | Sort-Object Min | Select-Object -First 1).Min
            $seed = if ($previous) { [int](($previous.Max + 1) - $base) } else { $copy.Seed }
            if ($seed -lt 0) { $seed = 0 }
            $target = $copy.Path
            Write-Output ("repairing copy {0} (port {1}, {2} elements) with seed {3}" -f $copy.Global, $copy.Port, $copy.Count, $seed)
            $instance = $farm | Where-Object { $_.Port -eq $copy.Port } | Select-Object -First 1
            $payload = @{ command = 'rebuild-model-ids'; destinationPath = $target; copies = 1; overwrite = $true; seed = $seed } | ConvertTo-Json -Compress
            $repair = Submit-CopyBatch -Instance $instance -Pattern $target -Count 1 -Seed $seed
            $repaired = $repair.data.copyResults | Select-Object -First 1
            $copy.Count = $repaired.count
            $copy.Verified = [bool]$repaired.idMappingVerified
            $copy.Min = [int64]$repaired.newIdMin
            $copy.Max = [int64]$repaired.newIdMax
            $copy.Ids = Get-CopyIds -CopyResult $repaired
            if (-not $copy.Verified) { $failures += "copy $($copy.Global) stayed degraded" }
        }

        # Rows are easier to compare when the files carry a global number.
        foreach ($copy in ($copyList | Sort-Object Global)) {
            $extension = [IO.Path]::GetExtension($copy.Path)
            $renamed = Join-Path $Destination ("copy-{0}{1}" -f $copy.Global, $extension)
            if ($copy.Path -ne $renamed) {
                Move-Item -Path $copy.Path -Destination $renamed -Force
                $copy.Path = $renamed
            }
        }

        Write-Output ''
        Write-Output ('{0,-6} {1,-10} {2,-8} {3,-7} {4,-12} {5,-14} {6}' -f 'copy', 'elements', 'verified', 'seed', 'id min', 'id max', 'file')
        foreach ($copy in ($copyList | Sort-Object Global)) {
            Write-Output ('{0,-6} {1,-10} {2,-8} {3,-7} {4,-12} {5,-14} {6}' -f $copy.Global, $copy.Count, $copy.Verified, $copy.Seed, $copy.Min, $copy.Max, [IO.Path]::GetFileName($copy.Path))
        }

        if (-not $SkipVerification) {
            $sorted = $copyList | Sort-Object Min
            $overlaps = @()
            for ($index = 1; $index -lt $sorted.Count; $index++) {
                $previous = $sorted[$index - 1]
                $current = $sorted[$index]
                $shared = [System.Linq.Enumerable]::Intersect([int64[]]$previous.Ids, [int64[]]$current.Ids)
                $count = @($shared).Count
                if ($count -gt 0) { $overlaps += "copy $($previous.Global) and copy $($current.Global) share $count ids" }
            }
            if ($overlaps.Count -eq 0) {
                Write-Output ("verification: {0} copies, {1} ids, no id is used by two copies" -f $copyList.Count, ($copyList | Measure-Object -Property Count -Sum).Sum)
            } else {
                Write-Output 'verification: overlapping ids found'
                $overlaps | ForEach-Object { Write-Output "  $_" }
            }
        }

        if ($failures.Count -gt 0) {
            Write-Output 'problems:'
            $failures | ForEach-Object { Write-Output "  $_" }
        }
    }
}
