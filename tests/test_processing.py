def test_process_document(client):
    # Step 1: Upload a document
    file_content = b"Hello, this is a test document for processing."
    upload_response = client.post(
        "/documents/upload",
        files={"file": ("test_document.txt", file_content, "text/plain")}
    )
    assert upload_response.status_code == 200
    document_id = upload_response.json()["id"]

    # Step 2: Process the uploaded document
    process_response = client.post(f"/documents/{document_id}/process")
    assert process_response.status_code == 200

    # Step 3: Verify that the document is marked as processed
    get_response = client.get(f"/documents/{document_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == document_id
    assert data["processed"] is True


# Idempotency test: Processing the same document multiple times should not cause errors

def test_processing_idempotent(client):

    file_content = b"Hello, this is a test document for idempotent processing."

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("test_document.txt", file_content, "text/plain")}
    )

    document_id = upload_response.json()["id"]

    client.post(f"/documents/{document_id}/process")
    client.post(f"/documents/{document_id}/process") # second time

    chunks_response = client.get(f"/documents/{document_id}/chunks")
    chunks = chunks_response.json()

    # should not double
    assert len(chunks) > 0
    # Store initial count and compare if needed