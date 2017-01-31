class SSException(Exception):
    METHOD_NOT_APPLICABLE = "Method is not applicable"

    DEVICE_TOKEN_EXISTS = "Device token exists."
    DEVICE_TOKEN_MISSING = "Device token is missing."

    AUTH_FAILED = "Authentication failed."
    CARD_NOT_PRESENT = "Card not present."
    CARD_ALREADY_REGISTERED = "Card is already registered."

    INVALID_INPUT = "Invalid input parameters."
    PROCESSING_FAILED = "Processing failed."
    INVALID_CARD = "Invalid card num"
    INVALID_USER = "Invalid User"

    CLIENT_NOT_PRESENT = "Client not registered."

    CARD_NUM_MISSING = "Card number is missing."
    PHONE_NUM_MISSING = "Phone number is missing."
    ACTIVATION_CODE_MISSING = "Activation code is missing."
    TXN_TYPE_MISSING = "Transaction type is missing."
    MERCHANT_ID_MISSING = "Merchant id is missing."
    MCC_CODE_MISSING = "MCC Code is missing."
    AMOUNT_MISSING = "Amount is missing."
    LOCATION_MISSING = "Location is missing."

    INVALID_TXN_TYPE = "Invalid transaction type"
    NO_REVIEW_TEMPLATE = "No review template defined"