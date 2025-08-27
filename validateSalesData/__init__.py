import logging
import azure.functions as func
import csv
import io

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("validateSalesData function triggered.")

    try:
        # Get the uploaded file from request body
        file_bytes = req.get_body()
        file_text = file_bytes.decode("utf-8")
        reader = csv.DictReader(io.StringIO(file_text))

        required_fields = ["TransactionID", "ProductName", "Amount"]

        for row_num, row in enumerate(reader, start=1):
            # Check for missing required fields
            for field in required_fields:
                if not row.get(field):
                    return func.HttpResponse(
                        f"Invalid Data: Missing {field} in row {row_num}",
                        status_code=400
                    )

            # Validate Amount (non-negative)
            try:
                amount = float(row["Amount"])
                if amount < 0:
                    return func.HttpResponse(
                        f"Invalid Data: Negative amount in row {row_num}",
                        status_code=400
                    )
            except ValueError:
                return func.HttpResponse(
                    f"Invalid Data: Amount not numeric in row {row_num}",
                    status_code=400
                )

        # If all validations pass
        return func.HttpResponse("Validation Passed", status_code=200)

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return func.HttpResponse(
            f"Internal Server Error: {str(e)}",
            status_code=500
        )
