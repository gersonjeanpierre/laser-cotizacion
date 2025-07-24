# Laser Cotiza

```
$env:PYTHONPATH = "$PWD" win

export PYTHONPATH="$PWD" 
python -c "from src.infrastructure.persistence.models import customer"
atlas-provider-sqlalchemy --path ./src/infrastructure/persistence/models
atlas migrate diff --env dev
atlas migrate apply --env dev
```

PostgreSQL setear hora Lima
```
ALTER DATABASE "Cotizacion" SET timezone TO 'America/Lima';
```

git config --global user.name "Gerson Jean Pierre";
git config --global user.email jalukone@outlook.com;
git config --global init.defaultBranch main;
git config --global core.editor nvim;
# ssh
ssh-keygen -t rsa -b 4096 -C "jalukone@outlook.com"