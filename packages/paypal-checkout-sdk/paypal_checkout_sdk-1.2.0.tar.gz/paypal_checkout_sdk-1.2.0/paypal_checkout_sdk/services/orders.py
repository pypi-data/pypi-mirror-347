from typing import TYPE_CHECKING, Optional
from ..models.orders import (
    CreateOrderRequest, CreateOrderResponse,
    CaptureOrderRequest, CaptureOrderResponse, Order, PatchOperation
)
from ..exceptions import PayPalError, APIError, RequestError
import httpx # Import httpx for type hinting if needed, actual client is passed

if TYPE_CHECKING:
    from ..client import PayPalClient # Import for type hinting only

class OrdersService:
    """
    Service class for interacting with the PayPal Orders API V2.

    Provides methods for creating, retrieving, updating, and capturing orders.
    """
    def __init__(self, client: 'PayPalClient'):
        """
        Initializes the OrdersService.

        Args:
            client: An instance of the PayPalClient.
        """
        self._client = client
        self._base_path = "/v2/checkout/orders"

    def create_order(self, order_request: CreateOrderRequest, paypal_request_id: Optional[str] = None, prefer: str = "return=representation") -> CreateOrderResponse:
        """
        Creates a PayPal order.

        Args:
            order_request: A CreateOrderRequest model instance containing order details.
            paypal_request_id: Optional PayPal request ID for idempotency.
            prefer: Representation preference (e.g., 'return=minimal', 'return=representation').

        Returns:
            A CreateOrderResponse model instance representing the created order.

        Raises:
            APIError: If the PayPal API returns an error.
            RequestError: If there's an issue with the HTTP request itself.
            AuthenticationError: If authentication fails.
            ConfigurationError: If the client is not configured properly.
            PayPalError: For other SDK-related errors.
        """
        headers = {}
        if paypal_request_id:
            headers["PayPal-Request-Id"] = paypal_request_id
        if prefer:
            headers["Prefer"] = prefer

        try:
            status_code, response_data = self._client._make_request(
                method="POST",
                path=self._base_path,
                json_data=order_request.model_dump(exclude_none=True), # Use model_dump for Pydantic v2
                headers=headers
            )

            if status_code in [200, 201]: # 201 Created is standard, 200 OK might occur sometimes
                 # Parse the response using the Pydantic model
                return CreateOrderResponse.model_validate(response_data)
            else:
                # Let _make_request handle raising APIError for non-2xx codes
                 raise APIError(status_code, response_data) # Should be handled by _make_request, but as fallback

        except httpx.TimeoutException as e:
            raise RequestError(f"Request timed out: {e}")
        except httpx.RequestError as e:
            raise RequestError(f"An HTTP request error occurred: {e}")
        except APIError as e: # Re-raise APIError if caught from _make_request
             raise e
        except Exception as e: # Catch other potential errors during processing
            raise PayPalError(f"An unexpected error occurred during order creation: {e}")


    def capture_order(self, order_id: str, capture_request: Optional[CaptureOrderRequest] = None, paypal_request_id: Optional[str] = None, prefer: str = "return=representation") -> CaptureOrderResponse:
        """
        Captures payment for a previously approved PayPal order.

        Args:
            order_id: The ID of the order to capture payment for.
            capture_request: Optional request body details (rarely needed for basic capture).
            paypal_request_id: Optional PayPal request ID for idempotency.
            prefer: Representation preference (e.g., 'return=minimal', 'return=representation').

        Returns:
            A CaptureOrderResponse model instance representing the captured order details.

        Raises:
            APIError: If the PayPal API returns an error (e.g., order not approved, already captured).
            RequestError: If there's an issue with the HTTP request itself.
            AuthenticationError: If authentication fails.
            ConfigurationError: If the client is not configured properly.
            PayPalError: For other SDK-related errors.
        """
        path = f"{self._base_path}/{order_id}/capture"
        headers = {
            "Content-Type": "application/json" # Required by PayPal for capture
        }
        if paypal_request_id:
            headers["PayPal-Request-Id"] = paypal_request_id
        if prefer:
            headers["Prefer"] = prefer

        # Prepare JSON body - often empty, but handle if provided
        json_data = capture_request.model_dump(exclude_none=True) if capture_request else None

        try:
            status_code, response_data = self._client._make_request(
                method="POST",
                path=path,
                json_data=json_data, # Pass None if capture_request is None
                headers=headers
            )

            if status_code in [200, 201]: # 201 Created is standard, 200 OK might occur
                 # Parse the response using the Pydantic model
                return CaptureOrderResponse.model_validate(response_data)
            else:
                # Let _make_request handle raising APIError for non-2xx codes
                 raise APIError(status_code, response_data) # Should be handled by _make_request, but as fallback

        except httpx.TimeoutException as e:
            raise RequestError(f"Request timed out: {e}")
        except httpx.RequestError as e:
            raise RequestError(f"An HTTP request error occurred: {e}")
        except APIError as e: # Re-raise APIError if caught from _make_request
             raise e
        except Exception as e: # Catch other potential errors during processing
            raise PayPalError(f"An unexpected error occurred during order capture: {e}")

    def get_order(self, order_id: str) -> Order:
        """
        Retrieves the details of a PayPal order.

        Args:
            order_id: The ID of the order to retrieve.

        Returns:
            An Order model instance containing the order details.

        Raises:
            APIError: If the PayPal API returns an error (e.g., order not found).
            RequestError: If there's an issue with the HTTP request itself.
            AuthenticationError: If authentication fails.
            ConfigurationError: If the client is not configured properly.
            PayPalError: For other SDK-related errors.
        """
        path = f"{self._base_path}/{order_id}"
        try:
            status_code, response_data = self._client._make_request(
                method="GET",
                path=path
            )

            if status_code == 200:
                return Order.model_validate(response_data)
            else:
                 raise APIError(status_code, response_data) # Should be handled by _make_request

        except httpx.TimeoutException as e:
            raise RequestError(f"Request timed out: {e}")
        except httpx.RequestError as e:
            raise RequestError(f"An HTTP request error occurred: {e}")
        except APIError as e: # Re-raise APIError if caught from _make_request
             raise e
        except Exception as e: # Catch other potential errors during processing
            raise PayPalError(f"An unexpected error occurred while getting order details: {e}")

    def patch_order(self, order_id: str, patch_operations: list[PatchOperation], paypal_request_id: Optional[str] = None) -> None:
            """
            Updates an order with a `CREATED` or `APPROVED` status.
            You can patch these attributes and objects:
            `intent`, `purchase_units`, `purchase_units[].amount`,
            `purchase_units[].description`, `purchase_units[].custom_id`,
            `purchase_units[].invoice_id`, `purchase_units[].soft_descriptor`,
            `purchase_units[].shipping`, `purchase_units[].payments.payment_instruction`.

            A successful request returns an HTTP `204 No Content` status code with no JSON response body.

            Args:
                order_id: The ID of the order to update.
                patch_operations: A list of PatchOperation objects detailing the changes.
                paypal_request_id: Optional PayPal request ID for idempotency.

            Raises:
                APIError: If the PayPal API returns an error (e.g., order not found, invalid patch).
                RequestError: If there's an issue with the HTTP request itself.
                PayPalError: For other SDK-related errors.
            """
            path = f"{self._base_path}/{order_id}"
            headers = {
                "Content-Type": "application/json" # Required for PATCH with JSON body
            }
            if paypal_request_id:
                headers["PayPal-Request-Id"] = paypal_request_id

            # Convert list of PatchOperation models to list of dicts
            # Using by_alias=True to ensure 'from_path' is serialized as 'from'
            json_data = [op.model_dump(exclude_none=True, by_alias=True) for op in patch_operations]

            try:
                status_code, response_data = self._client._make_request(
                    method="PATCH",
                    path=path,
                    json_data=json_data,
                    headers=headers
                )

                if status_code == 204: # Successful PATCH typically returns 204 No Content
                    return None # No content to return
                else:
                    # If it's not 204, it's likely an error or unexpected success response
                    # _make_request should raise APIError for non-2xx, but this is a safeguard.
                    raise APIError(status_code, response_data or {"message": f"Unexpected status code {status_code} for PATCH operation."})

            except httpx.TimeoutException as e:
                raise RequestError(f"Request to patch order {order_id} timed out: {e}")
            except httpx.RequestError as e:
                raise RequestError(f"An HTTP request error occurred while patching order {order_id}: {e}")
            except APIError as e: # Re-raise APIError if caught from _make_request
                 raise e
            except Exception as e: # Catch other potential errors during processing
                raise PayPalError(f"An unexpected error occurred during order patch for {order_id}: {e}")
