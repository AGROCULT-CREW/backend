-- upgrade --
ALTER TABLE "yieldcalculationcontainer" ADD "biological_yield" DOUBLE PRECISION;
-- downgrade --
ALTER TABLE "yieldcalculationcontainer" DROP COLUMN "biological_yield";
