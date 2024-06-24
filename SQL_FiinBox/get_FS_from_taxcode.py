import pandas as pd
import numpy as np
import pyodbc
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from requests_html import AsyncHTMLSession
asession = AsyncHTMLSession()
from datetime import date
from dateutil.relativedelta import relativedelta
import os
pdf_folder = os.path.expanduser("~/Desktop/")
idx = pd.IndexSlice
pd.options.display.float_format = '{:,.3f}'.format


connection_string = "DRIVER={SQL Server};SERVER=113.160.94.133,63830;DATABASE=FiinRatings;UID=FiinRatings.FRA.View;PWD=Fiin@1212"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=42.112.22.30,63866;'
#                       'Database=FiinRatings;'
#                       'UID=FiinRatings.FRA.View;'
#                       'PWD=adflsdwlLMJJ09)8_dsKJI'
#                       'Trusted_Connection=no;'
#                      )
def get_SQL(taxcode):
    
#     query = """SELECT a.OrganizationName,
# left(b.PeriodId,4) as YearReport, 
# substring(convert(varchar(10),b.PeriodID),5,2) as LengthReport,
# * 
# FROM  [FiinRatings].[dbo].[FGFB_COFS_DR_BalanceSheet] b
# left join [FiinRatings].[dbo].[FGFB_COIN_DR_OrganizationInformation] a on b.OrganizationId = a.OrganizationID
# left join [FiinRatings].[dbo].[FGFB_COFS_DR_IncomeStatement] i on 
# b.OrganizationID = i.OrganizationID and 
# b.PeriodID = i.PeriodID and 
# b.ReportTypeId = i.ReportTypeId

# left join [FiinRatings].[dbo].[FGFB_COFS_DR_CashFlow] c on 
# b.OrganizationID = c.OrganizationID and 
# b.PeriodID = c.PeriodID and 
# b.ReportTypeId = c.ReportTypeId	

# WHERE a.TaxCode in (""" + taxcode + """)
# ORDER BY YearReport, LengthReport""" 

    query = """ 
   SELECT DISTINCT
    tb.RecordId,
    a.TaxCode,
    a.OrganizationName,
    b.ReportTypeId,
    p.RealYear,
    p.RealQuarter,
    b.IsPriority,
    -- Balance Sheet
    b.BS64, b.BS1, b.BS27, -- Asset, Current Asset, Non-Current Asset
    b.BS65, b.BS66, b.BS81, -- Liability, Current Liability, Non-Current Liability
    b.BS95, -- Equity
    -- Current Assets
    b.BS2, b.BS5, -- Cash & ST Investments
    b.BS9, b.BS10, b.BS11, b.BS14, b.BS16, -- Current Accounts Receivable
    b.BS18, -- Net Inventory
    -- Non-Current Assets
    b.BS28, b.BS29, b.BS35, -- Long-Term Accounts Receivable
    b.BS36, b.BS37, b.BS38, b.BS39, b.BS40, b.BS41, b.BS42, b.BS43, b.BS44, b.BS46, b.BS47, b.BS48, b.BS49, b.BS50, b.BS51, -- Fixed Assets & CIP
    b.BS52, b.BS53, b.BS54, -- Long-Term Investments
    b.BS63, -- Goodwill
    -- Current Liabilities
    b.BS67, b.BS74, b.BS76, b.BS67, -- CL
    -- Non-Current Liabilities
    b.BS83, b.BS87, b.BS89, b.BS90, b.BS91, -- NCL
    -- Total Equity
    b.BS95, b.BS97, b.BS99, b.BS100, b.BS109, b.BS110, b.BS111, b.BS112, -- TE
    -- Income Statement
    i.IS1, i.IS2, i.IS3, i.IS5, i.IS6, i.IS7, i.IS8, i.IS9, i.IS10, i.IS11, i.IS13, i.IS14, i.IS15, i.IS16, i.IS17, i.IS20, i.IS21, i.IS22,
    -- Cash Flow
    c.CF19, c.CF30, c.CF37, -- CFO, CFI, CFF
    c.CF2, c.CF3, c.CF4, c.CF5, -- Depreciation & Amortization
    c.CF15, c.CF16, -- Interest Paid & Tax Paid
    c.CF9, -- CF before WC
    c.CF20, c.CF21, c.CF22, -- CF In & Out
    c.CF23, c.CF24, -- Capex & Disposal
    c.CF31, c.CF32, c.CF36, -- Equity Raise, Treasury, Dividend
    c.CF33 -- Borrowing
FROM (
    SELECT DISTINCT RecordId, OrganizationId, PeriodId, ReportTypeId, RecordStatusId, IsPriority
    FROM FGFB_COFS_DR_BalanceSheet b
    WHERE 
        CAST(SUBSTRING(CONVERT(varchar(10), b.PeriodID), 6, 1) AS tinyint) = 5
        AND IsHistory = 0
        AND RecordStatusId <= 1
) tb
JOIN FGFB_COFS_DR_BalanceSheet b ON b.RecordId = tb.RecordId
JOIN FGFB_COIN_DR_Organization a ON tb.OrganizationId = a.OrganizationId
JOIN FGFB_SYDI_DR_Period p ON tb.PeriodId = p.PeriodId
LEFT JOIN FGFB_COFS_DR_IncomeStatement i ON 
    tb.OrganizationID = i.OrganizationID  
    AND tb.PeriodID = i.PeriodID
    AND tb.ReportTypeId = i.ReportTypeId
    AND tb.RecordStatusId = i.RecordStatusId
    AND tb.IsPriority = i.IsPriority
LEFT JOIN FGFB_COFS_DR_CashFlow c ON 
    tb.OrganizationID = c.OrganizationID
    AND tb.PeriodID = c.PeriodID
    AND tb.ReportTypeId = c.ReportTypeId
    AND tb.RecordStatusId = c.RecordStatusId
    AND tb.IsPriority = c.IsPriority
WHERE 
	a.TaxCode in (""" + taxcode + """)    
ORDER BY a.TaxCode ASC, p.RealYear ASC, p.RealQuarter ASC;

"""

 
    with engine.begin() as conn:
        df = pd.read_sql_query(sa.text(query), conn)
        df = df.loc[:,~df.columns.duplicated()]  
        df.to_excel(pdf_folder + df['OrganizationName'][0] + '.xlsx')
        print('Đã lưu '+df['OrganizationName'][0])
while True:
    t = input("Nhập mã số thuế:")
    try:
        get_SQL(t)

    except:
        print('Ehhhh, sai mã số thuế roài. Nhập lại đi')
