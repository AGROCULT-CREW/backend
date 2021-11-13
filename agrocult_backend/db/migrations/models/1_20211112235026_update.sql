-- upgrade --
CREATE TABLE IF NOT EXISTS "grainculture" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "average_weight_thousand_grains" DOUBLE PRECISION NOT NULL
);
COMMENT ON TABLE "grainculture" IS 'Model for grain culture purpose.';;
CREATE TABLE IF NOT EXISTS "yieldcalculationcontainer" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "note" TEXT,
    "planting_area" DOUBLE PRECISION NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "calculated_at" TIMESTAMPTZ,
    "custom_average_weight_thousand_grains" DOUBLE PRECISION,
    "status" VARCHAR(200) NOT NULL  DEFAULT 'uploaded',
    "custom_average_stems_per_meter" DOUBLE PRECISION,
    "grain_culture_id" INT REFERENCES "grainculture" ("id") ON DELETE SET NULL
);
COMMENT ON COLUMN "yieldcalculationcontainer"."status" IS 'uploaded: uploaded\nprocessing: processing\ncomplete: complete\ninternal_error: internal_error';
COMMENT ON TABLE "yieldcalculationcontainer" IS 'Model for yield calculation container purpose.';;
CREATE TABLE IF NOT EXISTS "yieldcalculationcontainerphoto" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "file_name" VARCHAR(255) NOT NULL,
    "unique_file_name" VARCHAR(255) NOT NULL,
    "s3_path" TEXT NOT NULL,
    "status" VARCHAR(200) NOT NULL  DEFAULT 'uploaded',
    "average_grains_in_basket" DOUBLE PRECISION,
    "container_id" INT NOT NULL REFERENCES "yieldcalculationcontainer" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "yieldcalculationcontainerphoto"."status" IS 'uploaded: uploaded\nprocessing: processing\ncomplete: complete\ninternal_error: internal_error';
COMMENT ON TABLE "yieldcalculationcontainerphoto" IS 'Model for yield calculation container''s photo purpose.';-- downgrade --
DROP TABLE IF EXISTS "grainculture";
DROP TABLE IF EXISTS "yieldcalculationcontainer";
DROP TABLE IF EXISTS "yieldcalculationcontainerphoto";
