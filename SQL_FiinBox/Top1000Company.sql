 SELECT DISTINCT TOP (200)
    b.OrganizationId,
    a.OrganizationName,
    a.TaxCode,
    d.ICBId,
    LEFT(b.PeriodId, 4) AS YearReport,
    SUBSTRING(CONVERT(varchar(10), b.PeriodID), 5, 2) AS LengthReport,
    b.PeriodId,
    b.ReportTypeId,
    b.RecordStatusId,
    b.IsPriority,
    b.BS64,
    b.BS95,
    i.IS3,
    i.IS20
FROM [FiinRatings].[dbo].[FGFB_COFS_DR_BalanceSheet] b
LEFT JOIN [FiinRatings].[dbo].[FGFB_COIN_DR_Organization] a 
    ON b.OrganizationId = a.OrganizationID
LEFT JOIN [FiinRatings].[dbo].[FGFB_COIN_DR_Organization_ICB] d 
    ON b.OrganizationId = d.OrganizationId 
LEFT JOIN [FiinRatings].[dbo].[FGFB_COFS_DR_IncomeStatement] i 
    ON b.OrganizationID = i.OrganizationID 
    AND b.PeriodID = i.PeriodID 
    AND b.ReportTypeId = i.ReportTypeId
WHERE LEFT(b.PeriodId, 4) = '2023' 
    AND SUBSTRING(CONVERT(varchar(10), b.PeriodID), 5, 2) = '05'
    AND b.IsPriority = 1
    AND b.ReportTypeId = 5
    AND d.ICBId NOT IN (319, 325, 337, 338)
ORDER BY b.BS64 DESC, YearReport, LengthReport;
