.\.venv\Scripts\activate
$profileFolder = ".\.dbt"
#get path of dbt folder
$profilePath = Resolve-Path $profileFolder
Push-Location .\dbt_project
dbt deps --profiles-dir $profilePath
dbt build --profiles-dir $profilePath
Pop-Location