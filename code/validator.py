
def validate_inputs(claim, evidence, sources):
    """Check whether required fact-checking inputs are provided."""

    errors = []

    if not claim or not claim.strip():
        errors.append("Please enter a social media claim.")

    if not evidence or not evidence.strip():
        errors.append("Please provide supporting evidence.")

    if len(claim.strip()) > 2000:
        errors.append("Claim is too long. Keep it under 2000 characters.")

    if len(evidence.strip()) > 10000:
        errors.append("Evidence is too long. Keep it under 10000 characters.")

    return errors
