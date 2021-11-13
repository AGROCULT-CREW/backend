-- upgrade --
ALTER TABLE "yieldcalculationcontainer" ADD "name" VARCHAR(255) NOT NULL;
ALTER TABLE "yieldcalculationcontainer" ADD "coordinates" VARCHAR(255) NOT NULL;
-- downgrade --
ALTER TABLE "yieldcalculationcontainer" DROP COLUMN "name";
ALTER TABLE "yieldcalculationcontainer" DROP COLUMN "coordinates";
