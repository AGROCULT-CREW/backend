-- upgrade --
ALTER TABLE "yieldcalculationcontainerphoto" ADD "calculated_at" TIMESTAMPTZ;
ALTER TABLE "yieldcalculationcontainerphoto" ADD "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
-- downgrade --
ALTER TABLE "yieldcalculationcontainerphoto" DROP COLUMN "calculated_at";
ALTER TABLE "yieldcalculationcontainerphoto" DROP COLUMN "created_at";
