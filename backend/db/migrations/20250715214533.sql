-- Modify "stores" table
ALTER TABLE "stores" ADD COLUMN "phone_number_secondary" character varying(15) NULL, ADD COLUMN "yape_phone_number" character varying(15) NULL, ADD COLUMN "bcp_cta" character varying(16) NULL, ADD COLUMN "bcp_cci" character varying(20) NULL;
