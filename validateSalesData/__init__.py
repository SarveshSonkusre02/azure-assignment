import logging
import azure.functions as func
import pandas as pd
import io

# Expected schema
EXPECTED_COLUMNS = ["TransactionID", "ProductName", "Quantity", "Amount", "SaleDate"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("validateSalesData function triggered.")

    try:
        # Read file from HTTP request body
        file_bytes = req.get_body()
        if not file_bytes:
            return func.HttpResponse(
                "No file provided in request body.", status_code=400
            )

        # Load into pandas
        df = pd.read_csv(io.BytesIO(file_bytes))

        # Check schema
        if list(df.columns) != EXPECTED_COLUMNS:
            return func.HttpResponse(
                f"Invalid schema. Expected {EXPECTED_COLUMNS}, got {list(df.columns)}",
                status_code=400,
            )

        # Basic row validations
        if df["Quantity"].lt(1).any():
            return func.HttpResponse("Invalid data: Quantity must be >= 1", status_code=400)

        if df["Amount"].le(0).any():
            return func.HttpResponse("Invalid data: Amount must be > 0", status_code=400)

        # If everything is fine
        return func.HttpResponse("VALID", status_code=200)

    except Exception as e:
        logging.exception("Validation failed.")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
