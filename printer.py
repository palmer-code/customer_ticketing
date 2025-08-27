import time, platform

if platform.system() == 'Windows':
    import win32print

def print_ticket(prefix, number, counter):
    ticket_text = (
        "CUSTOMER SERVICE CENTER\n"
        "-------------------------\n"
        f"Ticket No: {prefix}{number}\n"
        f"Counter: {counter}\n"
        f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        "-------------------------\n"
        "Please wait for your number to be called.\n\n\n"
    )
    try:
        printer_name = win32print.GetDefaultPrinter()
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Ticket", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, ticket_text.encode('utf-8'))
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)
    except Exception as e:
        print("Printing error:", e)
