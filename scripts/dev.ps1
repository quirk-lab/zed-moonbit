param(
    [switch]$Watch,
    [switch]$Log
)

$ErrorActionPreference = "Stop"

# Find Python
$py = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $py = "python"
}
elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $py = "py"
}
elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $py = "python3"
}
else {
    Write-Error "Python was not found in PATH."
    exit 1
}

if ($Watch) {
    $args_list = @("scripts/watch.py", "--open-zed")
    if ($Log) {
        $args_list += "--log"
    }
    & $py @args_list
}
else {
    $args_list = @("scripts/dev.py")
    if ($Log) {
        $args_list += "--log"
    }
    & $py @args_list
}