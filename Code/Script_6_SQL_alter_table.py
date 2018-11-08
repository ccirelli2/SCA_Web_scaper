-- UPDATE SCA_data
-- SET defendant_name = 'crap'
-- WHERE page_number = 2;
-- 

ALTER TABLE SCA_data
MODIFY COLUMN 1934_Exchange_Act smallint;

-- 
-- ALTER TABLE SCA_data
-- MODIFY COLUMN 1933_Act	smallint, 
-- MODIFY COLUMN 10b5		smallint,
-- MODIFY COLUMN Derivative	smallint,
-- MODIFY COLUMN IPO			smallint,
-- MODIFY COLUMN Secondary_Offering	smallint,
-- MODIFY COLUMN Bankruptcy	smallint,
-- MODIFY COLUMN False_misleading	smallint,
-- MODIFY COLUMN Failed_disclose	smallint,
-- MODIFY COLUMN Commissions	smallint,
-- MODIFY COLUMN Fees			smallint,
-- MODIFY COLUMN Accounting	smallint,
-- MODIFY COLUMN Conflicts_Interest	smallint,
-- MODIFY COLUMN Corporate_Governance	smallint,
-- MODIFY COLUMN 10Q_Filling			smallint,
-- MODIFY COLUMN 10K_Filling			smallint,
-- MODIFY COLUMN Press_Release			smallint,
-- MODIFY COLUMN Second_Quarter		smallint,
-- MODIFY COLUMN Third_Quarter			smallint,
-- MODIFY COLUMN Fourth_Quarter		smallint,
-- MODIFY COLUMN Customers				smallint,
-- MODIFY COLUMN Net_Income			smallint,
-- MODIFY COLUMN Revenue_Rec			smallint,
-- MODIFY COLUMN Cash_Flow				smallint,
-- MODIFY COLUMN Stock_Drop			smallint,
-- MODIFY COLUMN Heavy_trading			smallint;
-- 
-- 
-- ALTER TABLE SCA_data
-- ADD Ref_class_period_start	DATE, 
-- ADD Ref_class_period_end	DATE;  
-- 
SELECT * FROM SCA_data;





