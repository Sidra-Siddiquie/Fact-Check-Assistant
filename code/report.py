
def format_report(result):
    """
    Prepare the user's supplied fact-check response for display.
    """

    if not result or not result.strip():
        return None

    return result.strip()


def get_report_status(result):
    """
    Check whether a report response has been provided.
    """

    if result and result.strip():
        return "Report available"

    return "No report submitted"
