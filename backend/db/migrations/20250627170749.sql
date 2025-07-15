-- Create "type_clients" table
CREATE TABLE "type_clients" (
  "id" serial NOT NULL,
  "code" character varying(10) NOT NULL,
  "name" character varying(50) NOT NULL,
  "margin" double precision NOT NULL,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp NULL,
  "deleted_at" timestamp NULL,
  PRIMARY KEY ("id"),
  CONSTRAINT "type_clients_code_key" UNIQUE ("code"),
  CONSTRAINT "type_clients_name_key" UNIQUE ("name")
);
-- Create "customers" table
CREATE TABLE "customers" (
  "id" serial NOT NULL,
  "type_client_id" integer NOT NULL,
  "entity_type" character varying(1) NOT NULL,
  "ruc" character varying(11) NULL,
  "dni" character varying(8) NULL,
  "doc_foreign" character varying(20) NULL,
  "name" character varying(35) NULL,
  "last_name" character varying(40) NULL,
  "business_name" character varying(150) NULL,
  "phone_number" character varying(15) NOT NULL,
  "email" character varying(100) NOT NULL,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp NULL,
  "deleted_at" timestamp NULL,
  PRIMARY KEY ("id"),
  CONSTRAINT "customers_dni_key" UNIQUE ("dni"),
  CONSTRAINT "customers_doc_foreign_key" UNIQUE ("doc_foreign"),
  CONSTRAINT "customers_email_key" UNIQUE ("email"),
  CONSTRAINT "customers_ruc_key" UNIQUE ("ruc"),
  CONSTRAINT "customers_type_client_id_fkey" FOREIGN KEY ("type_client_id") REFERENCES "type_clients" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
-- Create "extra_options" table
CREATE TABLE "extra_options" (
  "id" serial NOT NULL,
  "name" character varying(255) NOT NULL,
  "price" numeric(10,2) NOT NULL,
  "description" text NULL,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp NULL,
  "deleted_at" timestamp NULL,
  PRIMARY KEY ("id"),
  CONSTRAINT "extra_options_name_key" UNIQUE ("name")
);
-- Create "order_status" table
CREATE TABLE "order_status" (
  "id" serial NOT NULL,
  "code" character varying(10) NOT NULL,
  "name" character varying(50) NOT NULL,
  "description" text NULL,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp NULL,
  "deleted_at" timestamp NULL,
  PRIMARY KEY ("id"),
  CONSTRAINT "order_status_code_key" UNIQUE ("code"),
  CONSTRAINT "order_status_name_key" UNIQUE ("name")
);
-- Create "stores" table
CREATE TABLE "stores" (
  "id" serial NOT NULL,
  "code" character varying(10) NULL,
  "name" character varying(100) NOT NULL,
  "address" character varying(255) NULL,
  "phone_number" character varying(15) NULL,
  "email" character varying(100) NULL,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp NULL,
  "deleted_at" timestamp NULL,
  PRIMARY KEY ("id"),
  CONSTRAINT "stores_code_key" UNIQUE ("code"),
  CONSTRAINT "stores_email_key" UNIQUE ("email")
);
-- Create "orders" table
CREATE TABLE "orders" (
  "id" serial NOT NULL,
  "customer_id" integer NOT NULL,
  "store_id" integer NOT NULL,
  "order_status_id" integer NOT NULL,
  "total_amount" numeric(10,2) NOT NULL,
  "profit_margin" numeric(10,2) NOT NULL,
  "discount_applied" numeric(10,2) NOT NULL,
  "final_amount" numeric(10,2) NOT NULL,
  "payment_method" character varying(50) NULL,
  "shipping_address" character varying(200) NULL,
  "notes" text NULL,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp NULL,
  "deleted_at" timestamp NULL,
  PRIMARY KEY ("id"),
  CONSTRAINT "orders_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "orders_order_status_id_fkey" FOREIGN KEY ("order_status_id") REFERENCES "order_status" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "orders_store_id_fkey" FOREIGN KEY ("store_id") REFERENCES "stores" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
-- Create "products" table
CREATE TABLE "products" (
  "id" serial NOT NULL,
  "sku" character varying(20) NOT NULL,
  "name" character varying(150) NOT NULL,
  "description" character varying(150) NULL,
  "unity_measure" character varying(40) NOT NULL,
  "price" numeric(10,2) NOT NULL,
  "image_url" character varying(150) NULL,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp NULL,
  "deleted_at" timestamp NULL,
  PRIMARY KEY ("id"),
  CONSTRAINT "products_sku_key" UNIQUE ("sku")
);
-- Create "order_details" table
CREATE TABLE "order_details" (
  "id" serial NOT NULL,
  "order_id" integer NOT NULL,
  "product_id" integer NOT NULL,
  "height" numeric(10,2) NULL,
  "width" numeric(10,2) NULL,
  "quantity" integer NOT NULL,
  "linear_meter" numeric(10,2) NULL,
  "subtotal" numeric(10,2) NOT NULL,
  "total_extra_options" numeric(10,2) NOT NULL,
  "created_at" timestamp NOT NULL,
  "deleted_at" timestamp NULL,
  PRIMARY KEY ("id"),
  CONSTRAINT "order_details_order_id_fkey" FOREIGN KEY ("order_id") REFERENCES "orders" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "order_details_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "products" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
-- Create "order_detail_extra_options" table
CREATE TABLE "order_detail_extra_options" (
  "order_detail_id" integer NOT NULL,
  "extra_option_id" integer NOT NULL,
  "quantity" numeric(10,2) NOT NULL,
  "linear_meter" numeric(10,2) NULL,
  PRIMARY KEY ("order_detail_id", "extra_option_id"),
  CONSTRAINT "order_detail_extra_options_extra_option_id_fkey" FOREIGN KEY ("extra_option_id") REFERENCES "extra_options" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "order_detail_extra_options_order_detail_id_fkey" FOREIGN KEY ("order_detail_id") REFERENCES "order_details" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
-- Create "product_extra_options" table
CREATE TABLE "product_extra_options" (
  "product_id" integer NOT NULL,
  "extra_option_id" integer NOT NULL,
  "created_at" timestamp NULL,
  PRIMARY KEY ("product_id", "extra_option_id"),
  CONSTRAINT "product_extra_options_extra_option_id_fkey" FOREIGN KEY ("extra_option_id") REFERENCES "extra_options" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "product_extra_options_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "products" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
-- Create "product_types" table
CREATE TABLE "product_types" (
  "id" serial NOT NULL,
  "name" character varying(255) NOT NULL,
  "description" text NULL,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp NULL,
  "deleted_at" timestamp NULL,
  PRIMARY KEY ("id"),
  CONSTRAINT "product_types_name_key" UNIQUE ("name")
);
-- Create "product_product_types" table
CREATE TABLE "product_product_types" (
  "product_id" integer NOT NULL,
  "product_type_id" integer NOT NULL,
  "created_at" timestamp NULL,
  PRIMARY KEY ("product_id", "product_type_id"),
  CONSTRAINT "product_product_types_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "products" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "product_product_types_product_type_id_fkey" FOREIGN KEY ("product_type_id") REFERENCES "product_types" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
