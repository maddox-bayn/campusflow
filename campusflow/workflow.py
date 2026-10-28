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
staff_member = ["Alice", "Naza", "Divne", "sam", "celebrate"]
def assign_ticket(tickets, ticket_id, staff_name):
    ticket = get_ticket(tickets, ticket_id)
    if staff_name not in staff_member:
        raise WorkflowError("Staff not a valide member")
    name = (staff_name or "").strip()
    if not name:
        raise WorkflowError("staff name can not be empty")
    if ticket["status"] == "resolved":
        raise WorkflowError(f"{ticket['id']} is resolved. Reopen it before changing it.")
    ticket["assigned_to"] = name
    return ticket
