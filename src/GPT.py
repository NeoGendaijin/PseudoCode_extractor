import base64
from tqdm import tqdm
import requests
import os, json

prompt = r"""
Given an image input containing pseudo-code, output the LaTeX code that accurately represents the content. The LaTeX code should be:

- Free of compilation errors.
- Strictly adherent to LaTeX syntax and conventions.
- Precise in reflecting all aspects of the pseudo-code, including subscripts and special notation.
- If there is no pseudo-code in the image, the output should be an empty string.
- Do not write ''' or latex in the output.

Ensure the output is the pure LaTeX code required for direct compilation without any additional comments or extraneous content. Attention to detail is paramount to avoid any discrepancies in notation.
Write from \begin{algorithm} to \end{algorithm}.
"""

def process_image(image_path):
    # OpenAI API Key
    api_key = os.environ["OPENAI_API_KEY"]

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    """
    # Display the image with a specific size
    display(Image(filename=image_path, width=600, height=400))

    content = response.json()["choices"][0]["message"]["content"]
    print(content)
    return content
    """
    # Check the response status and content
    if response.status_code != 200:
        print("Failed to fetch response:", response.status_code)
        print("Response content:", response.text)
        return ""

    try:
        # Attempt to extract the content
        content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        return content
    except KeyError as e:
        # Handle missing keys
        print(f"KeyError: {e}")
        print("Response content:", response.text)
        return ""


def process_paper():
    # 擬似コードが存在する画像のリスト
    pseudo_code_list = []

    # ディレクトリ内のすべてのファイルを取得
    path_to_images = "./detected_images"
    files = os.listdir(path_to_images)

    # PNGファイルのみを処理
    png_files = [file for file in files if file.endswith(".png")]

    # 各PNGファイルに対してprocess_image関数を呼び出し
    for png_file in tqdm(png_files, desc="Processing images GPT-4"):
        image_path = os.path.join(path_to_images, png_file)
        result_str = process_image(image_path)
        # result_strがNoneの場合、次の画像へ進む
        if result_str != "":
            pseudo_code_list.append(result_str)

    # 擬似コードのリストを返す
    return pseudo_code_list
