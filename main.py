import sys
from campusflow.storage import StorageError, load_tickets, save_tickets

from campusflow.tickets import (
    CATEGORIES,
    create_ticket,
    get_ticket,
    format_ticket_detail,
    format_ticket_list,
)

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
    
HANDLERS = {
    "1": handle_create,
    "2": handle_list
}

MENU = """
--- CAMPUSFLOW NEXT ---
1. Create ticket
2. List / view tickets
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
        except StorageError as err:
            print(f"[Error] {err}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return 0
        

if __name__ == "__main__":
    sys.exit(main())