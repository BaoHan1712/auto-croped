from PIL import Image
import os
import cv2

cropping = False
x_start, y_start, x_end, y_end = 0, 0, 0, 0
image = None

def mouse_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping, image

    if event == cv2.EVENT_LBUTTONDOWN:
        cropping = True
        x_start, y_start = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping:
            x_end, y_end = x, y
            temp_image = image.copy()
            cv2.rectangle(temp_image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
            cv2.imshow("image", temp_image)

    elif event == cv2.EVENT_LBUTTONUP:
        cropping = False
        x_end, y_end = x, y
        cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        cv2.imshow("image", image)

def get_crop_area(img_path):
    global image
    image = cv2.imread(img_path)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_crop)
    
    while True:
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
        
# Nhấn ESC để thoát

        if key == 27: 
            break
# Nhấn 'r' để reset
        elif key == ord("r"):  

            image = clone.copy()
# Nhấn 'c' để hoàn thành cắt
        elif key == ord("c"): 

            break

    cv2.destroyAllWindows()
    return (x_start, y_start, x_end, y_end)

def crop_images_in_subfolders(data_folder, output_folder, crop_area):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for folder in os.listdir(data_folder):
        curr_path = os.path.join(data_folder, folder)
        if os.path.isdir(curr_path):
            output_subfolder = os.path.join(output_folder, folder)
            if not os.path.exists(output_subfolder):
                os.makedirs(output_subfolder)

            for file in os.listdir(curr_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    input_path = os.path.join(curr_path, file)
                    output_path = os.path.join(output_subfolder, file)

                    with Image.open(input_path) as img:
                        cropped_img = img.crop(crop_area)
                        cropped_img.save(output_path)
                        print(f"Đã cắt và lưu {file} vào {output_path}")

if __name__ == "__main__":
    
# Thay thế bằng đường dẫn tới thư mục chính
    data_folder = 'data'  
# Xuát ra folder
    output_folder = 'output'  

    subfolders = next(os.walk(data_folder))[1]
    if not subfolders:
        print("Không tìm thấy thư mục con nào trong data_folder.")
    else:
        first_folder = subfolders[0]
        first_folder_path = os.path.join(data_folder, first_folder)
        
        # Kiểm tra xem thư mục con có ảnh nào không
        image_files = [f for f in os.listdir(first_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        if not image_files:
            print("Không tìm thấy ảnh nào trong thư mục con đầu tiên.")
        else:
            first_image_path = os.path.join(first_folder_path, image_files[0])
            print(f"Mở ảnh đầu tiên: {first_image_path}")
            crop_area = get_crop_area(first_image_path)

            crop_images_in_subfolders(data_folder, output_folder, crop_area)
