CREATE TABLE "public"."job" ("id" bigserial NOT NULL, "status" text NOT NULL DEFAULT 'Waiting', "sleep_num" integer NOT NULL, "created_at" timestamptz NOT NULL DEFAULT now(), "updated_at" timestamptz NOT NULL DEFAULT now(), PRIMARY KEY ("id") );
CREATE OR REPLACE FUNCTION "public"."set_current_timestamp_updated_at"()
RETURNS TRIGGER AS $$
DECLARE
  _new record;
BEGIN
  _new := NEW;
  _new."updated_at" = NOW();
  RETURN _new;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER "set_public_job_updated_at"
BEFORE UPDATE ON "public"."job"
FOR EACH ROW
EXECUTE PROCEDURE "public"."set_current_timestamp_updated_at"();
COMMENT ON TRIGGER "set_public_job_updated_at" ON "public"."job" 
IS 'trigger to set value of column "updated_at" to current timestamp on row update';
