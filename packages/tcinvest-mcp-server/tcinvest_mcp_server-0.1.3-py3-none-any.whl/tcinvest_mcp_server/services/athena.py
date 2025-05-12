from ..api.client import ApiClient

def get_room_info(client: ApiClient) -> dict:
    """
    Get room information from Athena API.
    """
    response = client.get("athena/v1/roomInfo")
    return response
