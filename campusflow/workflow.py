"""Assignment and status workflow (F3 ASSIGN, F4 WORKFLOW).

OWNER: Engineer B  (branch feat/2-ticket-operations-reporting)

Allowed path: open -> in_progress -> resolved.
A resolved ticket is locked until reopen_ticket() sets it back to open.
"""
from .tickets import TicketError, get_ticket

STATUSES = ("open", "in_progress", "resolved")
ALLOWED_TRANSITIONS = {
    "open": {"in_progress"},
    "in_progress": {"resolved"},
    "resolved": set(),
}


class WorkflowError(TicketError):
    """Raised when an assignment or status change is not allowed."""
staff_member = ["Alice", "Naza", "Divne", "sam", "celebrate"]
def assign_ticket(tickets, ticket_id, staff_name):
    if staff_name not in staff_member:
        raise WorkflowError("Staff not a valide member")
    

