@echo off
cd /d "%~dp0"
echo ============================================
echo  Desktop Cat - Push para GitHub
echo ============================================
echo.

git config --global user.name "IN4C1OTI"
git config --global user.email "noreply@users.noreply.github.com"

if not exist ".git" (
    git init
)

git checkout -b main 2>nul || git checkout main

git remote remove origin 2>nul
git remote add origin https://github.com/IN4C1OTI/desktop_cat.git

git add .

git commit -m "feat: Desktop Cat v1 Green Hacker Edition - visual neon verde, glitch, falas PT-BR e refs filmes, chaos do mouse, minimizar janelas, clone jutsu, prank desligamento, sons e memes"

echo.
echo Fazendo push...
git push -u origin main --force

echo.
echo ============================================
echo  Pronto! https://github.com/IN4C1OTI/desktop_cat
echo ============================================
pause
