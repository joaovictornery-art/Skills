$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $PSScriptRoot

Get-ChildItem -LiteralPath (Join-Path $repo 'skills') -Recurse -Filter 'SKILL.md' |
    ForEach-Object { $_.FullName.Substring($repo.Length + 1) } |
    Sort-Object
