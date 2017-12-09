import os
import time
from PIL import Image
from PIL import ImageFile
from PIL.Image import ANTIALIAS
ImageFile.LOAD_TRUNCATED_IMAGES = True

"""
*** 개발 사항 ***
Ver.001a (2017/05/03)
"""

__author__ = "임근원"
VERSION = "001a"

class CatalogSashimi:

    def __init__(self, catalog_folder_path="/Users/junksound/PycharmProjects/Generator/data/withnonkey_original/", output_folder_path="/Users/junksound/PycharmProjects/Generator/data/withnonkey/"):

        print("*** MindEye's CatalogSashimi Ver." + VERSION + " ***")

        if catalog_folder_path == "./CATALOG_IMAGE/" and not os.path.exists("CATALOG_IMAGE"):
            os.makedirs("CATALOG_IMAGE")

        if output_folder_path == "./CATALOG_IMAGE_RESIZE/" and not os.path.exists("CATALOG_IMAGE_RESIZE"):
            os.makedirs("CATALOG_IMAGE_RESIZE")

        if not os.path.exists(catalog_folder_path):
            print("*** 오류 : 카탈로그 이미지 폴더가 없습니다. (init) ***")
            exit(-1)

        if not os.path.exists(output_folder_path):
            print("*** 오류 : 출력할 카탈로그 이미지 폴더가 없습니다. (init) ***")
            exit(-1)

        self.catalog_folder_path = catalog_folder_path
        self.output_folder_path = output_folder_path
        self.catalog_image_file_list_set = []

        catalog_file_list_set = os.listdir(catalog_folder_path)
        file_cnt = 0
        for file_name in catalog_file_list_set:
            ext = os.path.splitext(file_name)[-1]
            if ext == '.jpg' or ext == '.bmp' or ext == '.jpeg' or ext == '.gif' or ext == '.png':
                self.catalog_image_file_list_set.append(file_name)
                file_cnt += 1
        print("- %d개의 이미지 파일을 확인하였습니다." % file_cnt)

    def cut_catalog(self, base_weight=500, base_height=500, height_iou=100, start_num=0, end_num=0):

        if start_num == 0 and end_num == 0:
            catalog_image_file_list_set = self.catalog_image_file_list_set
        elif end_num != 0:
            catalog_image_file_list_set = self.catalog_image_file_list_set[start_num:end_num]
        elif start_num > end_num and end_num is 0:
            catalog_image_file_list_set = self.catalog_image_file_list_set[start_num:]
        elif start_num > end_num:
            print("*** 오류 : 읽기 시작할 파일의 번호가 끝날 파일의 번호보다 큽니다. (cut_catalog) ***")
            return None
        else:
            catalog_image_file_list_set = self.catalog_image_file_list_set[start_num:]

        print("- 총 " + str(len(catalog_image_file_list_set)) + "개의 카탈로그 이미지 파일을 분할합니다.")

        start_time = time.time()

        img_make_count = 0  # 분할한 파일 수

        for catalog_file_full_name in catalog_image_file_list_set:
            try:
                catalog_raw = Image.open(self.catalog_folder_path + catalog_file_full_name)
            except Exception as e:
                print(e)
                print("*** 오류 : " + catalog_file_full_name + " 카탈로그 이미지 파일을 불러오는데 실패하였습니다. (resize_catalog)")
                pass

            catalog_file_name = catalog_file_full_name.split(".")[0]
            add_white_weight = False
            add_white_height = False
            catalog_raw_weight = catalog_raw.size[0]
            catalog_raw_height = catalog_raw.size[1]

            if catalog_raw_weight < base_weight:  # 이미지 너비가 리사이즈 크기보다 작은 경우
                add_white_weight = True

            if catalog_raw_height < base_height:  # 이미지 높이가 리사이즈 크기보다 작은 경우
                add_white_height = True

            if add_white_weight is True and add_white_height is True:  # 높이와 너비 모두 리사이즈 기준치 미달일 경우
                resize_catalog = Image.new("RGB", (base_weight, base_height), (256, 256, 256))
                resize_catalog.paste(catalog_raw)

            elif add_white_weight is False and add_white_height is True:  # 높이만 리사이즈 기준치 미달인 경우
                resize_per = (base_weight / catalog_raw_weight)
                resize_height = max(int(catalog_raw_height * resize_per), 1)
                catalog_raw = catalog_raw.resize((base_weight, resize_height), ANTIALIAS)
                resize_catalog = Image.new("RGB", (base_weight, base_height), (256, 256, 256))
                resize_catalog.paste(catalog_raw)

            elif add_white_weight is True and add_white_height is False:  # 너비만 리사이즈 기준치 미달인 경우
                resize_catalog = Image.new("RGB", (base_weight, catalog_raw_height), (256, 256, 256))
                resize_catalog.paste(catalog_raw)

            else:  # 높이, 너비 모두 리사이즈 기준치 초과의 경우
                resize_per = (base_weight / catalog_raw_weight)
                resize_height = max(int(catalog_raw_height * resize_per), 1)

            # 높이별로 잘라내기 기능
            img_count = 1
            top_height = 0
            while True:
                if catalog_raw.size[1] > (top_height + base_height):
                    crop_area = (0, top_height, base_weight, (top_height + base_height))
                    crop_catalog = catalog_raw.crop(crop_area)
                    save_catalog_file_name = catalog_file_name + "_" + str(img_count-1) + ".jpg"

                    if crop_catalog.mode != "RGB":
                        crop_catalog = crop_catalog.convert("RGB")
                    crop_catalog.save(self.output_folder_path + save_catalog_file_name, 'JPEG')

                    img_count += 1
                    top_height = top_height + base_height
                else:
                    crop_area = (0, top_height, base_weight, catalog_raw.size[1])
                    crop_catalog = catalog_raw.crop(crop_area)


                    save_catalog_file_name = catalog_file_name + "_" + str(img_count-1) + ".jpg"

                    if crop_catalog.mode != "RGB":
                        crop_catalog = crop_catalog.convert("RGB")
                    crop_catalog.save(self.output_folder_path + save_catalog_file_name, 'JPEG')

                    break

            print("- " + catalog_file_full_name + "을 총 " + str(img_count) + "개로 분할하였습니다.")
            img_make_count += img_count

        end_time = time.time()
        print("- 총 %d개의 분할 이미지 파일을 생성하였습니다." % img_make_count)
        print("- 이미지 분할 소요 시간 : %d초" % (end_time - start_time))
        print("- 건당 평균 이미지 분할 소요 시간 : %f초" % ((end_time - start_time) / img_make_count))

