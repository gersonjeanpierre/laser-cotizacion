data "external_schema" "sqlalchemy" {
  program = [
   "atlas-provider-sqlalchemy",
   "--path", "./src/infrastructure/persistence/models",
   "--dialect", "postgresql"
  ]
}

env "dev" {
  src = data.external_schema.sqlalchemy.url
  dev = "postgresql://postgres:L4z4r0$@localhost:5432/CotizacionDev?sslmode=disable&search_path=public"
  // url = "postgresql://postgres:L4z4r0$@localhost:5432/Cotizacion?sslmode=disable&search_path=public"
  url = "postgresql://postgres:L4z4r0$@localhost:5432/CotizacionDev?sslmode=disable&search_path=public"
  migration {
    dir = "file://db/migrations"
  }
  exclude = ["atlas_schema_revisions"]
}

env "prod" {
  src = data.external_schema.sqlalchemy.url
  url = env("DATABASE_URL")
  migration {
    dir = "file://db/migrations"
  }
  exclude = ["atlas_schema_revisions"]
}

diff {
  skip {
    drop_schema = true
    drop_table  = true
  }
}