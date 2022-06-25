deploy apki na heroku:

1. stworzyć skrypt w pythonie

2. utworzenie pliku Procfile (w terminalu: echo > Procfile)

3. w Procfile skonfigurować nazwe głównego skryptu:
    web: python oferty_praca_bot.py
    worker: python oferty_praca_bot.py

3. utworzenie pliku requirements.txt (w terminalu: pip freeze > requirements.txt)

4. kolejnym krokiem jest utworzenie apki na githubie i podłączenie sie do niej poprzez heroku (przez Pycharma VCS > Share project on GitHub lub ręcznie:

    terminal:

    heroku login
    heroku git: remote -a oferty_praca_bot
    git add .
    git commit -am "First commit"
    git push heroku master
