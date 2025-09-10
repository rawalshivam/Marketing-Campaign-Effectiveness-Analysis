-- 1. Campaign Acceptance Rate

SELECT 
    (SUM(AcceptedCmp1) * 100.0 / COUNT(*)) AS Cmp1_AcceptanceRate,
    (SUM(AcceptedCmp2) * 100.0 / COUNT(*)) AS Cmp2_AcceptanceRate,
    (SUM(AcceptedCmp3) * 100.0 / COUNT(*)) AS Cmp3_AcceptanceRate,
    (SUM(AcceptedCmp4) * 100.0 / COUNT(*)) AS Cmp4_AcceptanceRate,
    (SUM(AcceptedCmp5) * 100.0 / COUNT(*)) AS Cmp5_AcceptanceRate
FROM marketing_campaign;

-----------------------------------------------------------------------------

-- 2. Response Rate by Education

SELECT 
    Education,
    COUNT(*) AS Total_Customers,
    SUM(Response) AS Positive_Responses,
    ROUND(100.0 * SUM(Response) / COUNT(*), 2) AS Response_Rate
FROM marketing_campaign
GROUP BY Education
ORDER BY Response_Rate DESC;

-----------------------------------------------------------------------------

-- 3. Response Rate by Marital Status

SELECT 
    Marital_Status,
    COUNT(*) AS Total_Customers,
    SUM(Response) AS Positive_Responses,
    ROUND(100.0 * SUM(Response) / COUNT(*), 2) AS Response_Rate
FROM marketing_campaign
GROUP BY Marital_Status
ORDER BY Response_Rate DESC;

-----------------------------------------------------------------------------

-- 4. Average Spending of Responders vs Non-Responders

SELECT 
    Response,
    ROUND(AVG(MntWines + MntFruits + MntMeatProducts + 
              MntFishProducts + MntSweetProducts + MntGoldProds), 2) AS Avg_Spending
FROM marketing_campaign
GROUP BY Response;

-----------------------------------------------------------------------------

-- 5. Purchases by Channel (Web, Catalog, Store)

SELECT 
    ROUND(AVG(NumWebPurchases),2) AS Avg_Web_Purchases,
    ROUND(AVG(NumCatalogPurchases),2) AS Avg_Catalog_Purchases,
    ROUND(AVG(NumStorePurchases),2) AS Avg_Store_Purchases
FROM marketing_campaign;

-----------------------------------------------------------------------------

-- 6. Campaign Success by Income Group

SELECT 
    CASE 
        WHEN Income < 30000 THEN 'Low Income'
        WHEN Income BETWEEN 30000 AND 60000 THEN 'Middle Income'
        WHEN Income BETWEEN 60001 AND 100000 THEN 'High Income'
        ELSE 'Very High Income'
    END AS Income_Group,
    COUNT(*) AS Customers,
    SUM(Response) AS Positive_Responses,
    ROUND(100.0 * SUM(Response) / COUNT(*), 2) AS Response_Rate
FROM marketing_campaign
GROUP BY Income_Group
ORDER BY Response_Rate DESC;

-----------------------------------------------------------------------------

-- 7. Top 5 Highest Spending Customers

SELECT 
    ID,
    Income,
    (MntWines + MntFruits + MntMeatProducts + 
     MntFishProducts + MntSweetProducts + MntGoldProds) AS Total_Spending
FROM marketing_campaign
ORDER BY Total_Spending DESC
LIMIT 5;

-----------------------------------------------------------------------------

-- 8. Average Web Visits by Responders vs Non-Responders

SELECT 
    Response,
    ROUND(AVG(NumWebVisitsMonth),2) AS Avg_Web_Visits
FROM marketing_campaign
GROUP BY Response;

-----------------------------------------------------------------------------

-- 9. Campaign Acceptance by Age Group

SELECT 
    CASE 
        WHEN (2025 - Year_Birth) < 30 THEN 'Under 30'
        WHEN (2025 - Year_Birth) BETWEEN 30 AND 45 THEN '30-45'
        WHEN (2025 - Year_Birth) BETWEEN 46 AND 60 THEN '46-60'
        ELSE 'Above 60'
    END AS Age_Group,
    COUNT(*) AS Customers,
    SUM(Response) AS Positive_Responses,
    ROUND(100.0 * SUM(Response) / COUNT(*), 2) AS Response_Rate
FROM marketing_campaign
GROUP BY Age_Group
ORDER BY Response_Rate DESC;

-----------------------------------------------------------------------------

-- 10. Correlation Between Deals & Campaign Response

SELECT 
    CASE 
        WHEN NumDealsPurchases = 0 THEN 'No Deals'
        WHEN NumDealsPurchases BETWEEN 1 AND 3 THEN '1-3 Deals'
        WHEN NumDealsPurchases BETWEEN 4 AND 6 THEN '4-6 Deals'
        ELSE '7+ Deals'
    END AS Deal_Category,
    COUNT(*) AS Customers,
    SUM(Response) AS Positive_Responses,
    ROUND(100.0 * SUM(Response) / COUNT(*), 2) AS Response_Rate
FROM marketing_campaign
GROUP BY Deal_Category
ORDER BY Response_Rate DESC;

-----------------------------------------------------------------------------


