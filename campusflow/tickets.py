"""Ticket creation, validation, lookup and display (F1 CREATE, F2 LIST / VIEW).

OWNER: Engineer A  (branch feat/1-ticket-core-management)

Tickets are plain dictionaries kept in one in-memory list:
    id, title, category, urgency, affected_users, priority, status, assigned_to, notes
"""

CATEGORIES = ("Network", "Hardware", "Software", "Other")
URGENCIES = ("low", "medium", "high")



class ValidationError(Exception):
    """Raised when user input is rejected."""
class TicketNotFoundError(ValidationError):
    """Raised when a ticket ID does not exist."""

# ---------------------------------------------------------------- validation
def validate_title(raw):
    title = (raw or "").strip()
    if not title:
        raise ValidationError("Title cannot be blank.")
    return title


def normalize_category(raw):
    value = (raw or "").strip().lower()
    for category in CATEGORIES:
        if category.lower() == value:
            return category
    raise ValidationError(f"Category must be one of: {', '.join(CATEGORIES)}.")


def normalize_urgency(raw):
    value = (raw or "").strip().lower()
    if value not in URGENCIES:
        raise ValidationError(f"Urgency must be one of: {', '.join(URGENCIES)}.")
    return value


def parse_affected_users(raw):
    # Explicitly reject booleans (since isinstance(True, int) is True in Python) and floats
    if isinstance(raw, bool) or isinstance(raw, float):
        raise ValidationError("Affected users must be a whole number greater than 0.")
    if isinstance(raw, int):
        if raw <= 0:
            raise ValidationError("Affected users must be greater than 0.")
        return raw
    if isinstance(raw, str):
        text = raw.strip()
        if text.isascii() and text.isdigit():
            number = int(text)
            if number > 0:
                return number
    raise ValidationError("Affected users must be a whole number greater than 0.")

def ticket_number(ticket_id):
    """'T012' -> 12 (used for numeric tie-breaking and ID generation)."""
    if (
        not isinstance(ticket_id, str)
        or len(ticket_id) < 2
        or not ticket_id.startswith("T")
        or not (ticket_id[1:].isascii() and ticket_id[1:].isdigit())
    ):
        raise ValidationError(f"Invalid ticket ID format: '{ticket_id}'.")
    num = int(ticket_id[1:])
    if num <= 0:
        raise ValidationError(f"Invalid ticket ID number: '{ticket_id}'.")
    return num


def next_ticket_id(tickets):
    """Next ID is max existing number + 1, so IDs stay unique after a reload."""
    highest = max((ticket_number(t["id"]) for t in tickets), default=0)
    return f"T{highest + 1:03d}"


def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"
 
# -------------------------------------------------------------------- create
def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate input, build the ticket, append it to `tickets` and return it."""
    ticket = {
        "id": next_ticket_id(tickets),
        "title": validate_title(title),
        "category": normalize_category(category),
        "urgency": normalize_urgency(urgency),
        "affected_users": parse_affected_users(affected_users),
        "priority": None,
        "status": "open",
        "assigned_to": None,
    }

    ticket["priority"] = calculate_priority(ticket["urgency"], ticket["affected_users"])
    tickets.append(ticket) 
    return ticket

def format_ticket_list(tickets):
    pass
def format_ticket_detail(ticket):
    return "\n".join(
        [
            f"=== Ticket {ticket['id']} ===",
            f"Title:          {ticket['title']}",
            f"Category:       {ticket['category']}",
            f"Urgency:        {ticket['urgency']}",
            f"Affected users: {ticket['affected_users']}",
            f"Priority:       {ticket['priority']}",
            f"Status:         {ticket['status']}",
            f"Assigned to:    {ticket['assigned_to'] or 'unassigned'}",
        ]
    )
def get_ticket(tickets, ticket_id):
    wanted = ticket_id.upper().strip()
    for ticket in tickets:
        if ticket["id"] == wanted:
            return ticket
    raise TicketNotFoundError(f"No ticket with ID '{(ticket_id or '').strip()}'.")