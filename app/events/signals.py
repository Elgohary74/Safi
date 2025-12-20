from blinker import signal

expense_created = signal("expense-created")
invite_sent = signal("invite-sent")
confirmation_requested = signal("confirmation-requested")
transaction_confirmed = signal("transaction-confirmed")
