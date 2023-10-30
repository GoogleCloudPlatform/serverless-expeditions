set -e
npx playwright install firefox --with-deps
wget https://raw.githubusercontent.com/kevin930321/BahAuto-Module/main/config.yml
npx bahamut-automation -c config.yml
echo All done!
