-- upgrade --
ALTER TABLE "yieldcalculationcontainer" ALTER COLUMN "status" SET DEFAULT 'YieldCalculationContainerStatus.created';
ALTER TABLE "yieldcalculationcontainer" ALTER COLUMN "status" TYPE VARCHAR(200) USING "status"::VARCHAR(200);
-- downgrade --
ALTER TABLE "yieldcalculationcontainer" ALTER COLUMN "status" SET DEFAULT 'YieldCalculationContainerStatus.uploaded';
ALTER TABLE "yieldcalculationcontainer" ALTER COLUMN "status" TYPE VARCHAR(200) USING "status"::VARCHAR(200);
