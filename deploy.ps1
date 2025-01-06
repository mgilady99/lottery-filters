# Deploy script
$env:RENDER_API_KEY = "YOUR_RENDER_API_KEY"
$env:RENDER_SERVICE_ID = "srv-clr8vvkgqk4c73d1v5f0"

# Trigger deploy on Render
$headers = @{
    "Authorization" = "Bearer $env:RENDER_API_KEY"
    "Content-Type" = "application/json"
}

$url = "https://api.render.com/v1/services/$env:RENDER_SERVICE_ID/deploys"

Invoke-RestMethod -Uri $url -Method Post -Headers $headers
