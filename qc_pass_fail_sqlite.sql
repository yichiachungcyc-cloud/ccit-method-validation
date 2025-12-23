-- QC pass/fail logic for CCIT vacuum leak test
-- Database: SQLite
-- Part of Python → SQLite → Power BI data pipeline

SELECT 
    Test_No,
    Test_ID,
    Type,
    Cycle1_mbar,
    Cycle1_Pa,
    Cycle2_mbar,
    Cycle2_Pa,
    
    -- 判斷 Cycle1_mbar Pass/Fail
    CASE 
        WHEN Cycle1_mbar BETWEEN 360 AND 460 THEN 'Pass'
        ELSE 'Fail'
    END AS Cycle1_mbar_QC,
    
    -- 判斷 Cycle1_Pa Pass/Fail
    CASE 
        WHEN Cycle1_Pa BETWEEN -5 AND 50 THEN 'Pass'
        ELSE 'Fail'
    END AS Cycle1_Pa_QC,
    
    -- 判斷 Cycle2_mbar Pass/Fail
    CASE 
        WHEN Cycle2_mbar BETWEEN 0 AND 10 THEN 'Pass'
        ELSE 'Fail'
    END AS Cycle2_mbar_QC,
    
    -- 判斷 Reject Limit (Cycle2_Pa) Pass/Fail
    CASE
        WHEN Cycle2_Pa BETWEEN -5 AND 70 THEN 'Pass'
        ELSE 'Fail'
    END AS Reject_Limit_QC
    
FROM ccit_raw_table;
