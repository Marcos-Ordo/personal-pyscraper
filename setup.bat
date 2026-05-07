@echo off
echo Installing Python dependencies...
pip install -r requirements.txt

echo Building React app...
cd website
npm install
npm run build
cd ..

echo Done! Run run.bat to start the app.
pause
