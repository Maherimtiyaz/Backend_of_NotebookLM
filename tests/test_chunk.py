def test_chunk_created(client):
    file_content = b"Hello, this is a test document for chunk creation." 

    # Step 1: Upload a document
    upload_response = client.post(
        "/documents/upload",
        files={"file": ("test_document.txt", file_content, "text/plain")}
    )

    document_id = upload_response.json()["id"]

    client.post(f"/documents/{document_id}/process")

    # Step 2: Retrieve chunks for the document
    chunks_response = client.get(f"/documents/{document_id}/chunks")
    
    chunks = chunks_response.json()

    assert len(chunks) > 0

    for i, chunk in enumerate(chunks):
        assert chunk["document_id"] == document_id
        assert chunk["chunk_index"] == i
        assert chunk["content"] != ""