# Data Schema (Public Sample)

## Dimensions
### DimDate
- Date (Date, unique)
- Year (Int)
- Quarter (Text)
- MonthNo (Int)
- MonthName (Text)
- WeekNo (Int)
- YearMonth (Text, e.g. 2025-12)

### DimCompany
- CompanyID (Int, PK)
- CompanyName (Text)
- Region (Text)
- Country (Text)

### DimProcess
- ProcessID (Int, PK)
- ProcessName (Text)

### DimCustomer
- CustomerID (Int, PK)
- Segment (Text)
- Country (Text)

### DimDepartment
- DeptID (Int, PK)
- DeptName (Text)

## Facts
### FactTaxOpsDaily
- Date (Date, FK -> DimDate[Date])
- CompanyID (Int, FK)
- ProcessID (Int, FK)
- TaxAmount (Decimal)
- TaxAdjustments (Decimal)
- OperationalVolume (Int)
- CycleTimeHours (Decimal)

### FactCXDaily
- Date (Date, FK)
- CompanyID (Int, FK)
- CustomerID (Int, FK)
- TicketsOpened (Int)
- TicketsResolved (Int)
- UnresolvedCases (Int)
- SLA_TargetHours (Decimal)
- SLA_ActualHours (Decimal)
- NPS_Score (Int 0-10)
- ServiceQualityScore (Int 0-100)

### FactHRMonthly
- MonthStartDate (Date, FK -> DimDate[Date])
- CompanyID (Int, FK)
- DeptID (Int, FK)
- Headcount (Int)
- EngagementScore (Int 0-100)
- Onboarding30dCompletionRate (Decimal 0-1)
- TurnoverRiskIndex (Decimal 0-1)
