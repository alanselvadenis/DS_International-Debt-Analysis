import streamlit as st
import pandas as pd
import db

# Configure Streamlit page layout
st.set_page_config(page_title="Sales Intelligence Hub", page_icon="📊", layout="wide")

# Initialize session states
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None

# ==========================================
# LOGIN SCREEN
# ==========================================
def show_login():
    st.title("🔐 Sales Intelligence Hub - Login")
    st.write("Please sign in with your system credentials.")

    col1, col2 = st.columns([1, 2])
    with col1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login", type="primary")

        if login_button:
            if username and password:
                user = db.authenticate_user(username, password)
                if user:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = user
                    st.success(f"Welcome back, {user['username']}!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password.")
            else:
                st.warning("Please enter both username and password.")


# DASHBOARD PAGE

def show_dashboard(user):
    st.title("📈 Financial Summary & KPIs")
    
    st.subheader("🔍 Filter Controls")
    
    # Create 4 columns for the filter UI
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Branch Filter (Role-Based)
        if user["role"] == "Super Admin":
            branches = db.get_branches()
            branch_options = {"All Branches": None}
            for b in branches:
                branch_options[b["branch_name"]] = b["branch_id"]
            
            selected_branch_name = st.selectbox("Branch Name", list(branch_options.keys()))
            branch_id_filter = branch_options[selected_branch_name]
        else:
            branch_id_filter = user["branch_id"]
            st.selectbox("Branch Name", [user["branch_name"]], disabled=True)
            
    with col2:
        # Product Filter
        product_filter = st.selectbox("Product Name", ["All", "DS", "DA", "BA", "FSD", "SQL"])
        
    with col3:
        # Start Date Filter (Defaults to None to show all history)
        start_date_filter = st.date_input("Start Date", value=None)
        
    with col4:
        # End Date Filter
        end_date_filter = st.date_input("End Date", value=None)

    # Fetch dynamic data based on all 4 filters
    kpis = db.get_kpi_summary(branch_id_filter, product_filter, start_date_filter, end_date_filter)
    
    st.markdown("---")
    st.subheader("💵 Financial Summary")
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    kpi1.metric("Overall Revenue (Gross)", f"₹{kpis['total_gross']:,.2f}")
    kpi2.metric("Total Received Amount", f"₹{kpis['total_received']:,.2f}")
    kpi3.metric("Total Pending Amount", f"₹{kpis['total_pending']:,.2f}")
    
    pending_pct = (kpis['total_pending'] / kpis['total_gross'] * 100) if kpis['total_gross'] > 0 else 0
    kpi4.metric("Pending Collection Pct", f"{pending_pct:.1f}%")

    st.markdown("---")
    st.subheader("📋 Branch Course Records Summary")
    
    # Fetch and display the filtered DataFrame
    sales_df = db.get_sales_records(branch_id_filter, product_filter, start_date_filter, end_date_filter)
    st.dataframe(sales_df, use_container_width=True, hide_index=True)


# ADD NEW SALE PAGE

def show_add_sale(user):
    st.title("➕ Add New Sale Record")
    
    branches = db.get_branches()
    
    with st.form("new_sale_form"):
        if user["role"] == "Super Admin":
            branch_dict = {b["branch_name"]: b["branch_id"] for b in branches}
            selected_branch = st.selectbox("Select Branch", list(branch_dict.keys()))
            branch_id = branch_dict[selected_branch]
        else:
            branch_id = user["branch_id"]
            st.text_input("Assigned Branch", value=user["branch_name"], disabled=True)

        col1, col2 = st.columns(2)
        with col1:
            sale_date = st.date_input("Sale Date")
            customer_name = st.text_input("Customer Name")
            mobile_number = st.text_input("Mobile Number")
        with col2:
            product_name = st.selectbox("Product", ["DS", "DA", "BA", "FSD"])
            gross_sales = st.number_input("Gross Sale Amount (₹)", min_value=0.0, step=500.0)
            status = st.selectbox("Status", ["Open", "Close"])

        submit_btn = st.form_submit_button("Create Sale Record", type="primary")

        if submit_btn:
            if not customer_name or not mobile_number or gross_sales <= 0:
                st.error("Please fill in all required fields accurately.")
            else:
                try:
                    db.add_sales_entry(branch_id, sale_date, customer_name, mobile_number, product_name, gross_sales, status)
                    st.success(f"Sale for {customer_name} recorded successfully!")
                except Exception as e:
                    st.error(f"Failed to record sale: {e}")


# ADD PAYMENT SPLIT PAGE

def show_add_payment(user):
    st.title("💳 Record Split Payment")
    
    branch_id = user["branch_id"] if user["role"] == "Admin" else None
    sales_df = db.get_sales_records(branch_id)
    
    # Filter sales that have pending balance or status Open
    open_sales = sales_df[sales_df["pending_amount"] > 0]
    
    if open_sales.empty:
        st.info("No pending sales found for payment recording.")
        return

    sale_options = {
        f"Sale ID #{row['sale_id']} - {row['customer_name']} (Pending: ₹{row['pending_amount']:,.2f})": row['sale_id']
        for _, row in open_sales.iterrows()
    }

    with st.form("payment_split_form"):
        selected_sale_str = st.selectbox("Select Sale Transaction", list(sale_options.keys()))
        sale_id = sale_options[selected_sale_str]
        
        col1, col2 = st.columns(2)
        with col1:
            payment_date = st.date_input("Payment Date")
            amount_paid = st.number_input("Amount Paid (₹)", min_value=1.0, step=100.0)
        with col2:
            payment_method = st.selectbox("Payment Method", ["UPI", "Card", "Cash"])

        submit_payment = st.form_submit_button("Record Payment", type="primary")

        if submit_payment:
            try:
                db.add_payment_split(sale_id, payment_date, amount_paid, payment_method)
                st.success("Payment recorded successfully! Trigger has updated total received and pending amounts.")
                st.rerun()
            except Exception as e:
                st.error(f"Error recording payment: {e}")


# PREDEFINED SQL QUERIES PAGE

def show_sql_queries():
    st.title("🔍 SQL Analytical Query Engine")
    st.write("Execute predefined SQL queries against the active database.")

    queries = {
        "1. Retrieve all records from customer_sales": 
            "SELECT * FROM customer_sales;",
        "2. Retrieve all records from branches": 
            "SELECT * FROM branches;",
        "3. Display all sales with status = 'Open'": 
            "SELECT * FROM customer_sales WHERE status = 'Open';",
        "4. Calculate total gross sales across all branches": 
            "SELECT SUM(gross_sales) AS total_gross_sales FROM customer_sales;",
        "5. Calculate total received amount across all sales": 
            "SELECT SUM(received_amount) AS total_received FROM customer_sales;",
        "6. Calculate total pending amount across all sales": 
            "SELECT SUM(pending_amount) AS total_pending FROM customer_sales;",
        "7. Count total number of sales per branch": 
            "SELECT b.branch_name, COUNT(cs.sale_id) AS total_sales_count FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id GROUP BY b.branch_name;",
        "8. Retrieve sales details along with branch name": 
            "SELECT cs.sale_id, b.branch_name, cs.name, cs.gross_sales, cs.received_amount, cs.pending_amount FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id;",
        "9. Show branch-wise total gross sales": 
            "SELECT b.branch_name, SUM(cs.gross_sales) AS branch_total_gross FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id GROUP BY b.branch_name;",
        "10. Retrieve sales details along with payment method used": 
            "SELECT cs.sale_id, cs.name, ps.amount_paid, ps.payment_method, ps.payment_date FROM customer_sales cs JOIN payment_splits ps ON cs.sale_id = ps.sale_id;",
        "11. Retrieve sales along with branch admin name": 
            "SELECT cs.sale_id, cs.name AS customer_name, b.branch_name, b.branch_admin_name FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id;",
        "12. Find sales where pending amount is greater than 5000": 
            "SELECT * FROM customer_sales WHERE pending_amount > 5000;",
        "13. Retrieve top 3 highest gross sales": 
            "SELECT * FROM customer_sales ORDER BY gross_sales DESC LIMIT 3;",
        "14. Find branch with highest total gross sales": 
            "SELECT b.branch_name, SUM(cs.gross_sales) AS total_sales FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id GROUP BY b.branch_name ORDER BY total_sales DESC LIMIT 1;",
        "15. Calculate payment method-wise total collection": 
            "SELECT payment_method, SUM(amount_paid) AS total_collected FROM payment_splits GROUP BY payment_method;"
    }

    selected_query_label = st.selectbox("Select Predefined SQL Analytical Query", list(queries.keys()))
    sql_to_run = queries[selected_query_label]

    st.code(sql_to_run, language="sql")

    if st.button("Run SQL Query", type="primary"):
        try:
            df_result = db.execute_predefined_query(sql_to_run)
            st.success("Query executed successfully!")
            st.dataframe(df_result, use_container_width=True)
        except Exception as e:
            st.error(f"Query execution failed: {e}")


# MAIN ROUTER

def main():
    if not st.session_state["logged_in"]:
        show_login()
    else:
        user = st.session_state["user"]
        
        # Sidebar Navigation
        st.sidebar.title("📌 Navigation")
        st.sidebar.write(f"Logged in as: **{user['username']}**")
        st.sidebar.write(f"Role: **{user['role']}**")
        
        page = st.sidebar.radio("Go to", [
            "Dashboard & Analytics", 
            "Add New Sale", 
            "Record Split Payment", 
            "SQL Analytical Queries"
        ])

        if st.sidebar.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.rerun()

        if page == "Dashboard & Analytics":
            show_dashboard(user)
        elif page == "Add New Sale":
            show_add_sale(user)
        elif page == "Record Split Payment":
            show_add_payment(user)
        elif page == "SQL Analytical Queries":
            show_sql_queries()

if __name__ == "__main__":
    main()