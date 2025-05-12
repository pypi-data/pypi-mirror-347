# project-manager-assistant (Cléa)

Optionally, create a `.env` file like this:
```
ANTHROPIC_API_KEY=
LINEAR_API_KEY=
```
If you don't, you are going to be asked the informations through the CLI.

Make sure you have Python 3.11 installed.

Install Poetry:
```sh
pip install poetry
```

Run in a terminal window:
```sh
poetry run clea
```

Ask questions:
```
>: Hi Cléa, I'd like to see my issues for next cycle

>: How much points to you think the unestimated tasks are worth?
```

TODO
- Sauvegarder l'historique des conversations
- Faire un éxécutable pour simplifier l'installation
- Questions sur les projets
- Questions sur les membres de l'équipe
