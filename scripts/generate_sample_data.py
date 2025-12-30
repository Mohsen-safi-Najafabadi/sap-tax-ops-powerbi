import numpy as np
import pandas as pd

np.random.seed(42)

# ---------- Dimensions ----------
companies = pd.DataFrame({
    "CompanyID": [1,2,3],
    "CompanyName": ["Alpha GmbH","Beta AG","Gamma SE"],
    "Region": ["EMEA","EMEA","AMER"],
    "Country": ["DE","DE","US"]
})

processes = pd.DataFrame({
    "ProcessID": [10, 20, 30],
    "ProcessName": ["Tax Filing", "Invoice Ops", "Returns Ops"]
})

customers = pd.DataFrame({
    "CustomerID": range(1001, 1021),
    "Segment": np.random.choice(["B2B","B2C","Enterprise"], 20, p=[0.4,0.4,0.2]),
    "Country": np.random.choice(["DE","FR","NL","US"], 20)
})

departments = pd.DataFrame({
    "DeptID": [1,2,3,4,5],
    "DeptName": ["Tax","Finance","Operations","Customer Experience","HR"]
})

# ---------- Date dimension ----------
dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
dim_date = pd.DataFrame({"Date": dates})
dim_date["Year"] = dim_date["Date"].dt.year
dim_date["Quarter"] = "Q" + dim_date["Date"].dt.quarter.astype(str)
dim_date["MonthNo"] = dim_date["Date"].dt.month
dim_date["MonthName"] = dim_date["Date"].dt.strftime("%b")
dim_date["WeekNo"] = dim_date["Date"].dt.isocalendar().week.astype(int)
dim_date["YearMonth"] = dim_date["Date"].dt.strftime("%Y-%m")

# ---------- FactTaxOpsDaily ----------
rows = []
for d in dates:
    for c in companies["CompanyID"]:
        for p in processes["ProcessID"]:
            volume = np.random.poisson(120)
            tax_amount = max(0, np.random.normal(50000, 12000))
            adj = np.random.normal(0, 2000)
            cycle = max(0.5, np.random.normal(8, 2))
            rows.append([d.date(), c, p, round(tax_amount,2), round(adj,2), int(volume), round(cycle,2)])

fact_taxops = pd.DataFrame(rows, columns=[
    "Date","CompanyID","ProcessID","TaxAmount","TaxAdjustments","OperationalVolume","CycleTimeHours"
])

# ---------- FactCXDaily ----------
rows = []
for d in dates:
    for c in companies["CompanyID"]:
        for cust in customers["CustomerID"]:
            opened = np.random.poisson(2)
            resolved = max(0, opened - np.random.binomial(opened, 0.1))
            unresolved = opened - resolved
            sla_target = 24
            sla_actual = max(1, np.random.normal(22, 6))
            nps = int(np.clip(np.random.normal(7, 2), 0, 10))
            svc = int(np.clip(np.random.normal(80, 10), 0, 100))
            rows.append([d.date(), c, cust, opened, resolved, unresolved, sla_target, round(sla_actual,2), nps, svc])

fact_cx = pd.DataFrame(rows, columns=[
    "Date","CompanyID","CustomerID","TicketsOpened","TicketsResolved","UnresolvedCases",
    "SLA_TargetHours","SLA_ActualHours","NPS_Score","ServiceQualityScore"
])

# ---------- FactHRMonthly ----------
months = pd.date_range("2024-01-01", "2025-12-01", freq="MS")
rows = []
for m in months:
    for c in companies["CompanyID"]:
        for dept in departments["DeptID"]:
            headcount = int(np.clip(np.random.normal(60, 20), 10, 200))
            engagement = int(np.clip(np.random.normal(72, 8), 30, 95))
            onboarding = float(np.clip(np.random.normal(0.82, 0.08), 0.4, 1.0))
            turnover_risk = float(np.clip(np.random.normal(0.25, 0.12), 0.0, 1.0))
            rows.append([m.date(), c, dept, headcount, engagement, round(onboarding,3), round(turnover_risk,3)])

fact_hr = pd.DataFrame(rows, columns=[
    "MonthStartDate","CompanyID","DeptID","Headcount","EngagementScore",
    "Onboarding30dCompletionRate","TurnoverRiskIndex"
])

# ---------- Save ----------
out_dir = "data/sample"
companies.to_csv(f"{out_dir}/DimCompany.csv", index=False)
processes.to_csv(f"{out_dir}/DimProcess.csv", index=False)
customers.to_csv(f"{out_dir}/DimCustomer.csv", index=False)
departments.to_csv(f"{out_dir}/DimDepartment.csv", index=False)
dim_date.to_csv(f"{out_dir}/DimDate.csv", index=False)
fact_taxops.to_csv(f"{out_dir}/FactTaxOpsDaily.csv", index=False)
fact_cx.to_csv(f"{out_dir}/FactCXDaily.csv", index=False)
fact_hr.to_csv(f"{out_dir}/FactHRMonthly.csv", index=False)

print("Sample data generated in data/sample/")
