def test_upload_document(client):
    file_content = b"Hello, this is a test document."

    response = client.post(
        "/documents/upload",
        data={
            "user_id": "1",
            "title": "test document"
       },
       files={"file": ("test_document.txt", file_content, "text/plain")}
   )

    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert data["processed"] is False