# Laser Cotiza

```
$env:PYTHONPATH = "$PWD"
python -c "from src.infrastructure.persistence.models import customer"
atlas-provider-sqlalchemy --path ./src/infrastructure/persistence/models
atlas migrate diff --env dev
atlas migrate apply --env dev
```