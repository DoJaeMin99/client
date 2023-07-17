import socket
import time
import cv2
import os

time.sleep(3)

folder_path = "D:\\UDP\\images\\real"  # 이미지가 있는 폴더 경로
file_names = ['0']*340  # jpg 파일 이름을 저장할 배열

# 폴더 내 모든 파일에 대해 반복
for file_name in os.listdir(folder_path):
    index = file_name.find('_')
    num = file_name[index+1:-4]
    file_names[int(num)-1] = file_name


# 서버 주소 및 포트
server_address = ('192.168.0.207', 7942)

# UDP 클라이언트 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

file_path = "D:\\UDP\\images\\gt\\image_gt.txt"

data = []  # 배열에 저장할 값들을 담을 배열

with open(file_path, 'r') as file:
    for line in file:
        line = line.strip()  # 줄 바꿈 문자 및 공백 제거
        data.append(line)


index = 0
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", 1000, 760)
for index, file_name in enumerate(file_names):
    file_path = os.path.join(folder_path, file_name)

    if os.path.isfile(file_path) and file_name.lower().endswith((".jpg", ".jpeg", ".png")):
        image = cv2.imread(file_path)

        client_socket.sendto(data[index].encode(), server_address)
        print("name", data[index].encode())

        cv2.setWindowTitle("Image", data[index][:-1])  # 창의 제목 변경
        index += 1
        cv2.imshow("Image", image)
        key = cv2.waitKey(1500)
        if key == ord('q'):
            break

# 소켓 닫기
client_socket.close()
