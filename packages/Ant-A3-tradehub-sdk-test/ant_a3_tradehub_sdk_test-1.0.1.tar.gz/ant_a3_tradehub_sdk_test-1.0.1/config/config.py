
class ServiceProps:
    """Service Props class for API settings and endpoints."""

    # Base URL for API requests
    BASE_URL = "https://antuat.aliceblueonline.com/"
    API_NAME = "Codifi ProTrade - Python Library"
    CONTRACT_BASE_URL = "https://v2api.aliceblueonline.com/restpy/static/contract_master/"

    # Endpoints for authorization
    GET_VENDOR_SESSION = "open-api/od-rest/v1/vendor/getUserDetails"

    # Endpoint for client profile
    GET_PROFILE = "open-api/od-rest/v1/profile/"

    # Endpoint for funds
    GET_FUNDS = "open-api/od-rest/v1/limits/"

    # Endpoints for positions and holdings
    GET_POSITIONS = "open-api/od-rest/v1/positions"
    GET_HOLDINGS = "open-api/od-rest/v1/holdings"

    # Endpoints for position conversion & margin
    POSITION_CONVERSION = ""
    SINGLE_ORDER_MARGIN = "open-api/od-rest/v1/orders/checkMargin"

    # Endpoints for orders
    ORDER_EXECUTE = "open-api/od-rest/v1/orders/placeorder"
    ORDER_MODIFY = "open-api/od-rest/v1/orders/modify/"
    ORDER_CANCEL = "open-api/od-rest/v1/orders/cancel/"
    EXIT_BRACKET_ORDER = "open-api/od-rest/v1/orders/exit/sno"
    POSITION_SQR_OFF = "open-api/od-rest/v1/orders/positions/sqroff"

    # Endpoints for orders details
    GET_ORDER_BOOK = "open-api/od-rest/v1/orders/book"
    GET_TRADE_BOOK = "open-api/od-rest/v1/orders/trades"
    GET_ORDER_HISTORY = "open-api/od-rest/v1/orders/history/"

    # Placeholder for chart history endpoint
    GET_CHART_HISTORY = ""  # Replace with a valid endpoint or remove if not needed

    @staticmethod
    def get_full_url(endpoint):
        """Return full URL for a given endpoint."""
        return f"{ServiceProps.BASE_URL}{endpoint}"


