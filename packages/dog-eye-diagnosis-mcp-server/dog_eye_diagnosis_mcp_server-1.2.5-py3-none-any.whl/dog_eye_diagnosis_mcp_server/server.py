import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Dog Eye Diagnosis", dependencies=["requests"])

@mcp.tool()
def puppy_eye_diagnosis(image_path: str) -> str:
    with open(image_path, 'rb') as img_file:
        response = requests.post(
            "http://13.124.223.37/v1/prediction/binary",
            files={'img_file': ('original.jpg', img_file, 'image/jpeg')}
        )

    try:
        return response.json()
    except ValueError:
        return f"Invalid response from server: {response.text}"

def serve():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    serve()
