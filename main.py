import sys
from campusflow.storage import StorageError, load_tickets, save_tickets

from campusflow.tickets import (
    CATEGORIES,
    create_ticket,
    get_ticket,
    format_ticket_detail,
    format_ticket_list,
    ValidationError
)

from campusflow.workflow import STATUSES, assign_ticket #, change_status, reopen_ticket

DATA_FILE = "tickets.json"

def handle_create(tickets):
    ticket = create_ticket(
        tickets,
        input("Title: "),
        input("Category (Network/Hardware/Software/Other): "),
        input("Urgency (low/medium/high): "),
        input("Affected users: "),
    )

    save_tickets(tickets, DATA_FILE)
    print(f"Created {ticket['id']} with {ticket['priority']} priority.")

def handle_list(tickets):
    print(format_ticket_list(tickets))
    if tickets:
        chosen = input("\nTicket ID to view in detail (ENter to skip): ").strip()
        if chosen:
            print(format_ticket_detail(get_ticket(tickets, chosen)))     
def handle_assign(tickets):
    """Handles assigning a ticket to a staff member with input validation and exit options."""
    while True:
        print("\nType 'Q' at any prompt to go back to the main menu.\n")
        
        # 1. Get and check Ticket ID
        ticket_id = input("Enter ticket ID: ").strip()
        if ticket_id.upper() == 'Q':
            break
        if not ticket_id:
            print("[Error] Ticket ID cannot be empty.")
            continue

        # 2. Get and check Staff Name
        staff_name = input("Enter the staff name to assign ticket: ").strip()
        if staff_name.upper() == 'Q':
            break
        if not staff_name:
            print("[Error] Staff name cannot be empty.")
            continue

        # 3. Process the assignment
        try:
            ticket = assign_ticket(tickets, ticket_id, staff_name)
            
            # Save immediately after a successful operation to prevent data loss
            save_tickets(tickets, DATA_FILE) 
            
            print(f"\n[Success] Ticket {ticket['id']} assigned to {ticket['assigned_to']}.")
            break # Exit the loop after a successful assignment
            
        except (ValidationError, StorageError) as err:
            print(f"[Error] {err}")


HANDLERS = {
    "1": handle_create,
    "2": handle_list,
    "3": handle_assign
}

MENU = """
--- CAMPUSFLOW NEXT ---
1. Create ticket
2. List / view tickets
3. Assign ticket
"""

def main():
    try:
        tickets = load_tickets(DATA_FILE)
    except StorageError as err:
        print(f"[Error] {err}")
        return 1
    while True:
        print(MENU)
        choice = input("Choose 1-8: ").strip()
        if choice == "8":
            print("Goodbye.")
            return 0
        handler = HANDLERS.get(choice)
        if handler is None:
            print("[Error] Please choose a number from 1 to 12.")
            continue
        try:
            handler(tickets)
        except (ValidationError, StorageError) as err:
            print(f"[Error] {err}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return 0
        

if __name__ == "__main__":
    sys.exit(main())