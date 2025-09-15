#!/usr/bin/env python3
import logging
import os

from cassandra.cluster import Cluster

import model

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('logistics.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', '127.0.0.1')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'logistics')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')

def print_menu():
    mm_options = {
        0: "Populate sample data",
        1: "Show orders by customer (Q1)",
        2: "Show products by order (Q2)",
        3: "Show all shipments by order (Q3.1)",
        4: "Show shipments by order with date range (Q3.2)",
        5: "Show shipments by order and status with date range (Q3.3)",
        6: "Show shipments by order and type with date range (Q3.4)",
        7: "Show shipments by order, type and status with date range (Q3.5)",
        8: "Change working email",
        9: "Exit",
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def set_customer_email():
    print("\nSample customer emails:")
    for email, name, _, _ in model.CUSTOMERS:
        print(f"  - {email} ({name})")
    
    email = input('\n**** Customer email to use: ').strip()
    log.info(f"Customer email set to {email}")
    return email

def get_order_number():
    order_number = input('Enter order number: ').strip()
    return order_number

def get_shipment_status():
    print(f"\nAvailable statuses: {', '.join(model.SHIPMENT_STATUSES)}")
    status = input('Enter shipment status: ').strip()
    return status

def get_shipment_type():
    print(f"\nAvailable types: {', '.join(model.SHIPMENT_TYPES)}")
    ship_type = input('Enter shipment type: ').strip()
    return ship_type

def main():
    log.info("Connecting to Cluster")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)

    model.create_schema(session)

    customer_email = set_customer_email()

    while(True):
        print("\n" + "="*50)
        print_menu()
        try:
            option = int(input('\nEnter your choice: '))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if option == 0:
            print("Populating sample data...")
            model.bulk_insert(session)
            print("Sample data populated successfully!")

        elif option == 1:
            print(f"\nQ1: Getting orders for customer: {customer_email}")
            model.get_orders_by_customer(session, customer_email)

        elif option == 2:
            pass

        elif option == 3:
            pass

        elif option == 4:
            pass

        elif option == 5:
            pass

        elif option == 6:
            pass

        elif option == 7:
            pass

        elif option == 8:
            customer_email = set_customer_email()

        elif option == 9:
            print("Exiting logistics application...")
            exit(0)

        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()