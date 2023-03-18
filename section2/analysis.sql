-- 1. Which are the top 10 members by spending
SELECT 
    concat(m.First_name, ' ', m.Last_name) AS Member_name,
    SUM(t.Total_cost) AS Total_spending
FROM Member m
    INNER JOIN Transactions t ON m.ID = t.Membership_id
GROUP BY t.Membership_id
ORDER BY Total_spending DESC
LIMIT 10;


-- 2. Which are the top 3 items that are frequently brought by members
SELECT
    it.Name AS Item_name,
    SUM(pd.Quantity) AS Total_item_count
FROM Purchase_details pd
    INNER JOIN Item it ON pd.ItemID = it.ID
GROUP BY pd.ItemID
ORDER BY Total_item_count DESC
LIMIT 3;
