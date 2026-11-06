@echo off
chcp 65001 >nul
cd /d "%~dp0"
set /p FAI=Operateur et acces (ex: Free fibre) : 
echo.
echo === Tour de test (1 a 2 minutes) ===
py -3 moniteur_reseaux.py --vantage fixe --fai "%FAI%" --once
echo.
echo Verifiez le tableau ci-dessus, puis appuyez sur une touche pour lancer la mesure continue.
echo (Ctrl+C pour arreter. Laissez cette fenetre ouverte.)
pause >nul
py -3 moniteur_reseaux.py --vantage fixe --fai "%FAI%"
pause
