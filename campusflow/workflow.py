"""Assignment and status workflow (F3 ASSIGN, F4 WORKFLOW).

OWNER: Engineer B  (branch feat/2-ticket-operations-reporting)

Allowed path: open -> in_progress -> resolved.
A resolved ticket is locked until reopen_ticket() sets it back to open.
"""
from .tickets import ValidationError, get_ticket

STATUSES = ("open", "in_progress", "resolved")
ALLOWED_TRANSITIONS = {
    "open": {"in_progress"},
    "in_progress": {"resolved"},
    "resolved": set(),
}


class WorkflowError(ValidationError):
    """Raised when an assignment or status change is not allowed."""
staff_member = ["Alice", "Naza", "Divne", "Sam", "Celebrate"]

def assign_ticket(tickets, ticket_id, staff_name):
    # 1. Basic validation first (fail fast)
    name = (staff_name or "").strip()
    if not name:
        raise WorkflowError("Staff name cannot be empty")
        
    # 2. Case-insensitive staff validation
    # Create a lowercase map to find the correct capitalization
    staff_map = {staff.lower(): staff for staff in staff_member}
    
    if name.lower() not in staff_map:
        raise WorkflowError("Staff is not a valid member")
        
    # Standardize the name to the original capitalization (e.g., "alice" -> "Alice")
    matched_staff_name = staff_map[name.lower()]

    # 3. Retrieve and validate ticket state
    ticket = get_ticket(tickets, ticket_id)
    if ticket["status"] == "resolved":
        raise WorkflowError(f"{ticket['id']} is resolved. Reopen it before changing it.")
        
    # 4. Perform the assignment
    ticket["assigned_to"] = matched_staff_name
    return ticket
