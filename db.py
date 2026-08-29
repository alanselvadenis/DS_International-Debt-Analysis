import mysql.connector
import pandas as pd

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',  # <--- Change this to your MySQL password
    'database': 'sales_management_system'
}

def get_connection():
  
    return mysql.connector.connect(**DB_CONFIG)

def authenticate_user(username, password):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT u.user_id, u.username, u.role, u.branch_id, b.branch_name 
        FROM users u
        LEFT JOIN branches b ON u.branch_id = b.branch_id
        WHERE u.username = %s AND u.password = %s
    """
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_branches():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT branch_id, branch_name FROM branches")
    branches = cursor.fetchall()
    conn.close()
    return branches

def add_sales_entry(branch_id, date, name, mobile_number, product_name, gross_sales, status='Open'):

    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO customer_sales (branch_id, date, name, mobile_number, product_name, gross_sales, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (branch_id, date, name, mobile_number, product_name, gross_sales, status))
    conn.commit()
    conn.close()

def add_payment_split(sale_id, payment_date, amount_paid, payment_method):
    
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO payment_splits (sale_id, payment_date, amount_paid, payment_method)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (sale_id, payment_date, amount_paid, payment_method))
    conn.commit()
    conn.close()

def get_sales_records(branch_id=None, product_name=None, start_date=None, end_date=None):
   
    conn = get_connection()
    query = """
        SELECT cs.sale_id, b.branch_name, cs.date, cs.name AS customer_name, 
               cs.mobile_number, cs.product_name, cs.gross_sales, 
               cs.received_amount, cs.pending_amount, cs.status
        FROM customer_sales cs
        JOIN branches b ON cs.branch_id = b.branch_id
        WHERE 1=1
    """
    params = []
    
    if branch_id:
        query += " AND cs.branch_id = %s"
        params.append(branch_id)
    if product_name and product_name != "All":
        query += " AND cs.product_name = %s"
        params.append(product_name)
    if start_date:
        query += " AND cs.date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND cs.date <= %s"
        params.append(end_date)
        
    query += " ORDER BY cs.sale_id DESC"
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def get_kpi_summary(branch_id=None, product_name=None, start_date=None, end_date=None):
   
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            COALESCE(SUM(gross_sales), 0) AS total_gross,
            COALESCE(SUM(received_amount), 0) AS total_received,
            COALESCE(SUM(pending_amount), 0) AS total_pending
        FROM customer_sales
        WHERE 1=1
    """
    params = []
    
    if branch_id:
        query += " AND branch_id = %s"
        params.append(branch_id)
    if product_name and product_name != "All":
        query += " AND product_name = %s"
        params.append(product_name)
    if start_date:
        query += " AND date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND date <= %s"
        params.append(end_date)
        
    cursor.execute(query, params)
    kpis = cursor.fetchone()
    conn.close()
    return kpis

def execute_predefined_query(query_str):

    conn = get_connection()
    df = pd.read_sql(query_str, conn)
    conn.close()
    return df