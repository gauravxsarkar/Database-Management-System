import streamlit as st
from sqlalchemy import create_engine, text
# import pandas as pd
# from datetime import date, time, datetime

# db connection
engine = create_engine("mysql+pymysql://root:Gaurav%40123@localhost/ecomm_db",
                        echo=False)

# crud functions
# c

# insert functions
def add_order(engine, order_id, customer_id):
    with engine.begin() as conn:
        conn.execute(
            text('''insert into orders(order_id, customer_id)
                 values (:oid, :cid)
                '''),
                {"oid": order_id, "cid": customer_id}
        )

def add_customer(engine, customer_id, city, state):
    with engine.begin() as conn:
        conn.execute(
            text('''insert into customers(customer_id, customer_city, customer_state)
                 values(:cid, :city, :state)
                '''),
                {"cid":customer_id, "city":city, "state":state}
        )

def check_customer(engine, customer_id):
    with engine.begin() as conn:
        return conn.execute(
                    text('''select 1 from customers where customer_id = :cid
                        '''),
                        {"cid": customer_id}
                ).fetchone()

# rud
# retrieve customer
def get_customer(engine, customer_id):
    with engine.begin() as conn:
        return conn.execute(text("""
                            select customer_id, customer_city, customer_state
                            from customers where customer_id = :cid
                        """),
                        {"cid":customer_id}
                        ).fetchone()

# update customer
def update_customer(engine, customer_id, city, state):
    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE customers
                SET customer_city = :city,
                    customer_state = :state
                WHERE customer_id = :cid
            """),
            {"cid": customer_id, "city": city, "state": state}
        )

# delete customer
def delete_customer(engine, customer_id):
    with engine.begin() as conn:
        conn.execute(
            text("""delete from customers where customer_id = :cid"""),
                    {"cid": customer_id}
                    )

# --UI--
st.title("E-Commerce Database Management System")

# customer details
st.subheader("Customer details Manager")

# data to input
customer_id = st.text_input("Enter Customer ID")
city = st.text_input("City")
state = st.text_input("State")

# buttons
cols = st.columns(3)

search_button = cols[0].button("Search")
update_button = cols[1].button("Update")
delete_button = cols[2].button("Delete")

# customer manager
if search_button:
    customer = get_customer(engine, customer_id)

    if customer:
        st.write("**Customer ID:**", customer[0])
        st.write("**City:**", customer[1])
        st.write("**State:**", customer[2])

        st.success("Customer found")

    else:
        st.warning("Customer not found")


if update_button:
    if not city or not state:
        st.warning("City and State required")
    else:
        update_customer(customer_id, city, state)
        st.success("Customer updated")


if delete_button:
    delete_customer(engine, customer_id)
    st.success("customer deleted")


# add customer
st.divider()
st.subheader("Add New Customer")

new_cid = st.text_input("New Customer ID")
new_city = st.text_input("New City")
new_state = st.text_input("New State")

if st.button("Add Customer"):
    if not new_cid or not new_city or not new_state:
        st.error("All fields required")
    else:
        add_customer(new_cid, new_city, new_state)
        st.success("Customer added")

# add order
st.divider()
st.subheader("Create Order")

order_id = st.text_input("Order ID")
order_customer_id = st.text_input("Customer ID for Order")

if st.button("Create Order"):
    customer = get_customer(order_customer_id)

    if not order_id or not order_customer_id:
        st.error("Both fields required")
    elif customer:
        add_order(order_id, order_customer_id)
        st.success("Order created")
    else:
        st.warning("Customer does not exist")
        

#####################################################################

st.divider()
st.header("Data Analysis")

# top customers acc to orders
if st.button("Show Top Customers by Orders"):
    with engine.begin() as conn:
        result = conn.execute(text("""
            select customer_id, count(order_id) as total_orders
            from orders
            group by customer_id
            order by total_orders desc limit 5
        """))

        data = result.fetchall()

    st.table(data)

# city wise customer distribution
if st.button("Show Customers by City"):
    with engine.begin() as conn:
        result = conn.execute(text("""
            select customer_city, count(*) as total_customers
            from customers
            group by customer_city
            order by total_customers desc limit 10
        """))

        data = result.fetchall()

    st.write("top 10")
    st.table(data)

