import os
from ultralytics import YOLO
from pdf2image import convert_from_path
from PIL import Image
from tqdm import tqdm

# モデルのロード
model = YOLO('../weights/best.pt')

def convert_all_pdf_to_pngs(pdf_path, image_dir = "./images/"):
    # PDFディレクトリが存在しない場合、処理を中断
    if not os.path.exists(pdf_path):
        print(f"PDF directory {pdf_path} does not exist.")
        return

    # 画像ディレクトリが存在しない場合、ディレクトリを作成
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Convert the PDF to a list of PIL images
    images = convert_from_path(pdf_path)

    # Save each image as PNG
    for i, image in enumerate(images):
        png_path = os.path.join(image_dir, f"{pdf_name}_page_{i + 1}.png")
        image.save(png_path, 'PNG')
        print(f"Saved {png_path}")

def delete_png_and_images_dir(images_dir="./images/"):
    # ./imagesディレクトリが存在する場合、ディレクトリ内の全ファイルを削除後、ディレクトリ自体を削除
    if os.path.exists(images_dir) and os.path.isdir(images_dir):
        # ディレクトリ内の全ファイルを削除
        for filename in os.listdir(images_dir):
            file_path = os.path.join(images_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        # 空のディレクトリを削除
        os.rmdir(images_dir)
        print(f"Deleted directory: {images_dir}")
    else:
        print(f"Directory does not exist: {images_dir}")

def img2pseudoimg(image_path,save_dir):

    # モデルによる予測
    results = model.predict(image_path, save=False, conf=0.9,verbose=False)

    # 検出結果をもとに画像を切り取る
    image = Image.open(image_path)

    # 仮に検出されたオブジェクトのリストが以下のように得られるとします
    detected_objects = results[0]  # この行はモデルの出力に応じて変更する必要があります

    # 検出されたオブジェクトごとにループ
    for i, obj in enumerate(detected_objects):
        # バウンディングボックスの座標を取得
        [x1, y1, x2, y2] = obj.boxes.xyxy[0].tolist()

        # オブジェクトの領域を切り取る
        cropped_image = image.crop((x1, y1, x2, y2))

        # 切り取った画像を保存
        full_file_name = os.path.basename(image_path)
        file_name = os.path.splitext(full_file_name)[0]
        save_path = os.path.join(save_dir,f'detected_pseudocode_{file_name}_{i}.png')
        cropped_image.save(save_path)
        #print(f'Saved {save_path}')

    return len(detected_objects)


def imgs2pseudoimgs():
    # 擬似コードのカウント
    pseudo_code_count = 0

    # ディレクトリ内のすべてのファイルを取得
    imgs_dir = './images'
    files = os.listdir(imgs_dir)

    # PNGファイルのみを処理
    png_files = [file for file in files if file.endswith(".png")]


    # 保存先のディレクトリを作成
    save_dir = './detected_images'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)

    # 各PNGファイルに対してprocess_image関数を呼び出し
    for png_file in tqdm(png_files, desc="Processing images YOLOv8"):
        image_path = os.path.join(imgs_dir, png_file)
        pseudo_code_count += img2pseudoimg(image_path,save_dir)


    # 擬似コードのリストを返す
    return pseudo_code_count
