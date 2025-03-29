# auto_push.ps1
Set-Location "C:\Users\Admin\Desktop\dokuman_yonetim_sistemi"
git add .
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "Auto commit at $timestamp"
git push origin main
