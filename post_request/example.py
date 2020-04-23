from post_request.PostRequest import PostRequest

if __name__ == "__main__":
    request = PostRequest("../post_request_properties.json")
    request.submitRequest("testing")
