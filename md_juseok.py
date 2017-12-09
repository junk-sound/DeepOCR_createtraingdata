from PIL import Image, ImageFont, ImageDraw
import random
import glob

'''
Deep learning 기반 OCR 프로그램 개발을 위한 훈련 데이터 생성기
프로젝트 코드명 :Keyword_Carrier
Copyright ⓒ
2017 HanYang University AI & Business LAB, All Rights Reserved.

            <<< 개발 사항>>>
------------------------------------------------
Generator에 필요한 클래스 
VERSION_001b: 2017.06.12, 주석 추가. 안 쓰는 메소드 제거.
------------------------------------------------
'''

__author__ = "임근원"
VERSION = "001b"

class SettingBackground:
    '''
    배경 이미지를 세팅해주는 클래스입니다.
    '''
    def __init__(self, bgdata_folder_path):
        '''
        배경 이미지 폴더명을 리스트에 모아줍니다.
        :return :별도의 return 값이 없습니다.
        :param bgdata_folder_path: 배경 이미지의 경로를 지정해줍니다.
        '''
        self.bg_class_lst = glob.glob(bgdata_folder_path + "/*")
        bg_folder_name_lst = []
        for bg_folder_path in self.bg_class_lst:
            bg_folder_name = bg_folder_path.split('\\')[-1]
            bg_folder_name_lst.append(bg_folder_name)

        print("*** 배경 이미지 OFF 스위치 번호 입니다. ***")

        for bg_folder_idx, bg_folder_name in enumerate(bg_folder_name_lst):
            print(bg_folder_name,':',bg_folder_idx,'번')

    def switch_OFF(self, bg_del_lst):
        '''
        배경 이미지 폴더 중 제외할 폴더를 지정해줍니다. 배경 이미지 OFF 스위치 번호를 bg_del_lst에 포함시키면 그 배경 이미지 폴더를 제외시킵니다.
        :param bg_del_lst: 제외할 배경 이미지 폴더를 지정해줍니다.
        :return:별도의 return 값은 없습니다.
        '''
        if bg_del_lst == None:
            pass
        else:
            temp_lst = []
            for idx, bg_folder in enumerate(self.bg_class_lst):
                if idx not in bg_del_lst:
                    # print(bg_folder.split("/").pop() + " < ON >")
                    temp_lst.append(bg_folder)
            self.bg_class_lst = temp_lst
        print("*** 스위치 OFF 후 배경 이미지 폴더입니다. ***")
        af_s_name = [bg_path.split("\\").pop() for bg_path in self.bg_class_lst]
        print(af_s_name)

    def set_bg(self):
        '''
        배경 이미지를 열고 리스트에 저장합니다.
        :return: 배경 이미지 리스트
        '''
        self.img_obj_lst = []
        self.all_img_path_lst = []

        for bg_class in self.bg_class_lst:
            self.all_img_path_lst.extend(glob.glob(bg_class + "/*.*"))
        for path in self.all_img_path_lst:
            obj = Image.open(path)
            self.img_obj_lst.append(obj)
        return self.img_obj_lst

class Draw_it:
    '''
    배경 이미지에 글씨를 쓰는 클래스 입니다.
    '''
    def __init__(self, original_image, fill, font):
        '''
        :param original_image: 배경 이미지 입니다.
        :param fill: 글자 색상입니다.
        :param font: 글씨체입니다.
        '''
        self.draw = ImageDraw.Draw(original_image)
        self.fill = fill
        self.font = font

    def write_text_and_draw_rec(self, adress, keyword):
        '''
        :param adress: 글씨의 위치 정보입니다.
        :param keyword: 글씨의 내용 정보입니다.
        :return: 별도의 return은 없습니다.
        '''
        self.draw.text((adress[0], adress[1]), keyword, fill=self.fill, font=self.font)
        # self.draw.rectangle([adress[0], adress[1], adress[0] + adress[2], adress[1] + adress[3]], outline='red')
    def draw_only_rec(self, adress):
        self.draw.rectangle([adress[0], adress[1], adress[0] + adress[2], adress[1] + adress[3]], outline='red')


class KeywordCarrier:
    '''
    글씨 정보와 관련된 클래스입니다.
    '''
    def __init__(self, font_folder_path, keyword_folder_path, original_image):
        '''
        글씨체 폴더, 키워드 폴더, 배경 이미지를 지정해주고 폰트 리스트, 글씨 크기 리스트, 색상 리스트, 키워드 리스트를 만들어줍니다.
        :param font_folder_path: 글씨체 폴더의 주소입니다.
        :param keyword_folder_path: 키워드 폴더의 주소입니다.
        :param bgdata_folder_path: 배경 이미지 폴더의 주소입니다.
        :param original_image: 배경 이미지입니다.
        '''
        self.r = random.Random()
        self.original_image = original_image
        self.font_class_lst = glob.glob(font_folder_path + "/*")
        self.size_lst = [(13,13),(14,14),(15,15),(16,16),(17,17),(20,20),(30,30),(40,40),(50,50),(60,60),(70,70),(75,75),(80,80),(90,90)]
        self.resize_lst = [(12,18), (20, 30), (40, 50)]
        self.color_lst = []
        for r in range(201):
            for g in range(201):
                for b in range(201):
                    color_instance = (r, g, b)
                    self.color_lst.append(color_instance)
        self.key_class_lst = glob.glob(keyword_folder_path + "/*")

    "폰트 이름 결정"
    def decidefontname(self):
        '''
        글씨체를 정해줍니다.
        :return: 한글 폰트와 영문 폰트. 현재 한글 폰트만 사용하고 있습니다.
        '''
        for font_folder in self.font_class_lst:
            if "korean" in font_folder:
                self.font_folder_kr = font_folder
                k_ttf_lst = glob.glob(self.font_folder_kr + "/*.ttf")
                self.k_ttf_fullname = self.r.choice(k_ttf_lst)
            elif "eng" in font_folder:
                self.font_folder_eng = font_folder
                e_ttf_lst = glob.glob(self.font_folder_eng + '/*.ttf')
                self.e_ttf_fullname = self.r.choice(e_ttf_lst)
        return self.k_ttf_fullname, self.e_ttf_fullname

    "폰트 이름 재결정"
    def redecidefontname(self):
        '''
        글씨체를 다시 정해줍니다. 글씨체를 고정시키기 위함입니다.
        :return: 다시 정한 한글 폰트와 영문 폰트.
        '''
        for font_folder_re in self.font_class_lst:
            if "korean" in font_folder_re:
                self.font_folder_re_kr = font_folder_re
                k_ttf_lst = glob.glob(self.font_folder_re_kr + "/*.ttf")
                self.k_ttf_fullname_re = self.r.choice(k_ttf_lst)
            elif "eng" in font_folder_re:
                self.font_folder_re_eng = font_folder_re
                e_ttf_lst = glob.glob(self.font_folder_re_eng + '/*.ttf')
                self.e_ttf_fullname = self.r.choice(e_ttf_lst)
        return self.k_ttf_fullname_re, self.e_ttf_fullname

    "폰트 결정"
    def decidefont(self,fontname_kr, txt_size):
        '''
        정한 글씨체를 열어줍니다.
        :return: 선택된 한글 폰트, 선택된 영어 폰트
        :주의: 대중소와 연결을 다시 고려해봐야 합니다.
        '''
        self.k_ttf = ImageFont.truetype(fontname_kr, txt_size)
        self.e_ttf = ImageFont.truetype(self.e_ttf_fullname, txt_size)
        return self.k_ttf, self.e_ttf

    "글자크기 결정"
    def decide_txt_size(self):
        '''
        글자 크기를 정해줍니다.
        :return: 글자 크기
        주의: 대중소와 연결을 고려해보아야합니다.
        '''
        # 대 중 소 텍스트 중 하나 사용시 텍스트 사이즈 지정
        if len(self.size_lst) == 14:
            dice = random.randrange(1, 101)
            if 1 <= dice <= 3:
                self.txt_size = self.size_lst[13]
            elif 4 <= dice <= 6:
                self.txt_size = self.size_lst[12]
            elif 7 <= dice <= 9:
                self.txt_size = self.size_lst[11]
            elif 10 <= dice <= 12:
                self.txt_size = self.size_lst[10]
            elif 13 <= dice <= 16:
                self.txt_size = self.size_lst[9]
            elif 17 <= dice <= 20:
                self.txt_size = self.size_lst[8]
            elif 21 <= dice <= 30:
                self.txt_size = self.size_lst[7]
            elif 31 <= dice <= 40:
                self.txt_size = self.size_lst[6]
            elif 41 <= dice <= 65:
                self.txt_size = self.size_lst[5]
            elif 66 <= dice <= 80:
                self.txt_size = self.size_lst[4]
            elif 81 <= dice <= 85:
                self.txt_size = self.size_lst[3]
            elif 86 <= dice <= 90:
                self.txt_size = self.size_lst[2]
            elif 91 <= dice <= 95:
                self.txt_size = self.size_lst[1]
            elif 96 <= dice <= 100:
                self.txt_size = self.size_lst[0]
            return self.txt_size

    '글자크기 재결정'
    def redecide_txt_size(self, ex_txt_size):
        '''
        글자 크기를 다시 정해줍니다. 글자 크기를 고정해주기 위함입니다.
        :param ex_txt_size: 이전 글자 크기입니다.
        :return: 이전보다 작은 글씨 크기.
         주의: 현재 사용하지 않고 있습니다.
        '''
        dice = random.randrange(1, 101)
        self.re_txt_size = self.r.randint(1, ex_txt_size)
        return self.re_txt_size

    "색상결정"
    def decide_color(self):
        '''
        글자 색상을 지정해줍니다.
        :return: 글자 색상
        '''
        self.txt_color = self.r.choice(self.color_lst)
        return self.txt_color

    "색상재결정"
    def redecide_color(self):
        '''
        글자 색상을 다시 지정해줍니다. 글자 색상을 고정시켜주기 위함입니다.
        :return: 글자 색상
        '''
        self.retxt_color = self.r.choice(self.color_lst)
        return self.retxt_color

    "몇개의 키워드 뽑을 지 결정"
    def num_key_nonkey(self):
        '''
        키워드의 종류를 정해주고 각 키워드에 따른 개수를 지정해줍니다. 개수가 적은 키워드부터 정렬해줍니다.
        :return은 아니지만 구해지는 것: nonkeyword에 따른 개수 튜플
        :return: keyword에 따른 개수 튜플
        '''

    "몇개의 키워드 뽑을 지 결정"
    def num_key_nonkey(self):
        '''
        키워드의 종류를 구하고 각 키워드의 개수를 지정합니다.
        :return: keyword에 따른 개수 튜플.
        주의: return은 아니지만 구해지는 것: nonkeyword에 따른 개수 튜플
        '''

        self.num_nonkey_selected_dict = {}
        self.num_key_selected_dict = {}
        self.size = self.original_image.size[0] * self.original_image.size[1]
        num_per_img_key = self.r.choice(range(6, 8))
        num_per_img_nonkey = self.r.choice(range(150, 200))
        def mykey(t):
            return t[1], t[0]
        for folder_path in self.key_class_lst:
            if "non" in folder_path:
                non_key_txt = glob.glob(folder_path + "/*.txt")
                non_key_lst = []
                f1 = open(non_key_txt[0])
                lst_1 = f1.readlines()
                f1.close()
                for non_key in lst_1:
                    non_key_lst.append(non_key.rstrip())
                num_nonkey_lst = len(non_key_lst)
                '''논키워드의 종류를 지정해줍니다. num_nonkey_lst의 개수 내에서 랜덤으로 지정해줍니다.'''
                nonkey_selected = []
                for num in range(num_per_img_nonkey):
                    indexing_keyword = self.r.choice(range(num_nonkey_lst))
                    nonkey_selected.append(non_key_lst[indexing_keyword])
                '''각 논키워드 당 개수를 지정해줍니다.'''
                for one_nonkey in nonkey_selected:
                    num_per_one_nonkey = self.r.choice(range(1, 4))
                    self.num_nonkey_selected_dict[one_nonkey] = num_per_one_nonkey
            elif "long" in folder_path:
                pass
            else:
                key_txt = glob.glob(folder_path + "/*.txt")
                key_lst = []
                f2 = open(key_txt[0])
                lst_2 = f2.readlines()
                f2.close()
                for key in lst_2:
                    key_lst.append(key.rstrip())
                num_key_lst = len(key_lst)
                key_selected = []
                '''키워드의 종류를 지정해줍니다. num_key_lst의 개수 내에서 랜덤으로 지정해줍니다.'''
                for num2 in range(num_per_img_key):
                    indexing_keyword2 = self.r.choice(range(num_key_lst))
                    key_selected.append(key_lst[indexing_keyword2])
                '''각 키워드 당 개수를 지정해줍니다.'''
                for one_key in key_selected:
                    '''키워드당 개수 지정'''
                    num_per_one_key = self.r.choice(range(35, 40))
                    self.num_key_selected_dict[one_key] = num_per_one_key
        '''개수가 적은 키워드 순으로 정렬해줍니다.'''
        self.num_selected_nonkey = sorted(self.num_nonkey_selected_dict.items(), key=mykey)
        self.num_selected_key = sorted(self.num_key_selected_dict.items(), key=mykey)

        return self.num_selected_key

    "키워드 펼치기 " "즉, 내가 그릴 것 전부"
    def key_all_lst(self):
        '''
        이후 논키워드를 지정하기 위해 논키워드를 나열해줍니다.
        :return: 전체 키워드 리스트, 전체 논키워드 리스트
        '''
        try:
            self.num_selected_key
            self.num_selected_nonkey
        except :
            print('key_all_lst함수는 num_key_nonkey함수를 먼저 실행해야 합니다.')
        else:
            self.selected_key_lst = []

            for key_tuple in self.num_selected_key:
                keyname = key_tuple[0]
                for num_of_keyname in range(key_tuple[1]):
                    self.selected_key_lst.append(keyname)

            self.selected_non_key_lst = []
            for nonkeyname_tuple in self.num_selected_nonkey:
                nonkeyname = nonkeyname_tuple[0]
                for num_of_nonkeyname in range(nonkeyname_tuple[1]):
                    self.selected_non_key_lst.append(nonkeyname)

    '''nonkeyword 지정'''
    def pic_nonkey(self):
        '''
        논키워드를 지정합니다. 이 논키워드는 짧은 단어입니다.
        :return: 첫 번째 짧은 논키워드, 두 번째 짧은 논키워드
        '''
        try:
            self.selected_non_key_lst
        except AttributeError:
            print('pic_nonkey함수는 key_all_lst함수를 먼저 실행해야 합니다.')
        else:
            try:
                self.selected_nonkey = self.r.choice(self.selected_non_key_lst)
                self.selected_nonkey2 = self.r.choice(self.selected_non_key_lst)
            except IndexError:
                self.selected_nonkey = ''
                self.selected_nonkey2 = ''
        return self.selected_nonkey, self.selected_nonkey2

    def pic_long_nonkey(self):
        '''
        긴 논키워드를 지정해줍니다.
        :return: 첫 번째 긴 논키워드, 두 번째 긴 논키워드.
        '''
        for folder_path in self.key_class_lst:
            if "long" in folder_path:
                long_non_txt = glob.glob(folder_path + "/*.txt")
                long_non_lst = []
                f3 = open(long_non_txt[0])
                lst_3 = f3.readlines()
                f3.close()
                for long_non in lst_3:
                    long_non_lst.append(long_non.rstrip())
        self.selected_long_non1 = self.r.choice(long_non_lst)
        self.selected_long_non2 = self.r.choice(long_non_lst)
        return self.selected_long_non1, self.selected_long_non2

'''지역 index 구하는 랜덤값'''

class Loaction_Average :
    '''
    위치 지정과 관련된 클래스입니다. 문장을 카탈로그 이미지 내에 임의로 위치시킵니다.
    '''
    def __init__(self, original_image):
        '''
        :param original_image: 배경 이미지
        '''
        self.draw = ImageDraw.Draw(original_image)
        self.keyword_name_dic = {}
        self.original_image = original_image
        self.r = random.Random()

    def loc_fisrtword_random(self, keyword1, keyword2, keyword3, fontinf1, fontinf2, fontinf3, div_idx):
        '''

        배경 이미지에 논키워드, 키워드 논키워드 순서로 문장을 위치시킵니다. 이 때 지역 정보를 참고합니다. 지역 정보는 각 카탈로그 이미지를 정사각형으로 자를 때 붙이는 번호입니다.
        :param keyword1: 첫 번째 논키워드
        :param keyword2: 키워드
        :param keyword3: 두 번째 논키워드
        :param fontinf1: 첫 번째 논키워드의 글씨 정보(글씨체, 글씨 크기)
        :param fontinf2: 키워드의 글씨 정보(글씨체, 글씨 크기)
        :param fontinf3: 두 번째 논키워드의 글씨 정보(글씨체, 글씨 크기)
        :param div_idx: 지역 번호
        :return: 첫 번째 논키워드의 위치정보
        '''
        fake_x1 = self.r.choice(range(0, self.original_image.size[0]))
        fake_y1 = self.r.choice(range((self.original_image.size[0] * div_idx) + 2, (self.original_image.size[0] * (div_idx+1))-2))
        font1 = ImageFont.truetype(fontinf1[0], fontinf1[1])
        self.fir_w = self.draw.textsize(keyword1, font=font1)[0]
        self.fir_h = self.draw.textsize(keyword1, font=font1)[1]
        fake_x2 = fake_x1 + self.fir_w + 1
        font2 = ImageFont.truetype(fontinf2[0], fontinf2[1])
        self.sec_w = self.draw.textsize(keyword2, font=font2)[0]
        self.sec_h = self.draw.textsize(keyword2, font=font2)[1]
        fake_x3 = fake_x2 + self.sec_w + 1
        font3 = ImageFont.truetype(fontinf3[0], fontinf3[1])
        self.thi_w = self.draw.textsize(keyword3, font=font3)[0]
        self.thi_h = self.draw.textsize(keyword3, font= font3)[1]

        if fake_x3 + self.thi_w <  self.original_image.size[0]:
            self.fir_x = fake_x1
        else:
            if self.fir_w + self.sec_w + self.thi_w >= self.original_image.size[0]-22:
                self.fir_x = '넘쳤다'
            else:
                while fake_x3 + self.thi_w >= self.original_image.size[0]:
                    fake_x1 = self.r.choice(range(0, self.original_image.size[0]))
                    fake_x2 = fake_x1 + self.fir_w + 1
                    fake_x3 = fake_x2 + self.sec_w + 1
                self.fir_x = fake_x1
        if fake_y1+max([self.fir_h, self.sec_h, self.thi_h]) < (self.original_image.size[0] * (div_idx+1))-2:
            self.fir_y = fake_y1
        else:
            while fake_y1 + max([self.fir_h, self.sec_h, self.thi_h]) >= (self.original_image.size[0] *(div_idx+1))-2:
                fake_y1 = self.r.choice(range((self.original_image.size[0] * div_idx) + 2 , self.original_image.size[0] * (div_idx+1)))
            self.fir_y = fake_y1
        return [self.fir_x, self.fir_y, self.fir_w, self.fir_h]

    def loc_secondword(self):
        '''
        :return: 키워드의 위치정보
        '''
        if self.fir_x == '넘쳤다':
            self.sec_x = '넘쳤다'
            self.sec_y = self.fir_y
        else:
            self.sec_x = self.fir_x + self.fir_w + 1
            self.sec_y = self.fir_y
        return [self.sec_x, self.sec_y, self.sec_w, self.sec_h]

    def loc_thirdword(self):
        '''
        :return: 두 번째 논키워드의 위치정보
        '''
        if self.sec_x == '넘쳤다':
            self.thi_x = '넘쳤다'
            self.thi_y = self.fir_y
        else:
            self.thi_x = self.sec_x + self.sec_w + 1
            self.thi_y = self.fir_y

        return [self.thi_x, self.thi_y, self.thi_w, self.thi_h]

class Location_Relocate :
    '''
    위치 재지정과 관련된 클래스입니다. 이 때 지역 번호를 참조합니다. 카탈로그 이미지를 잘랐을 때 이전에 위치시킨 것과 같은 이미지에 위치시키기 위함입니다.
    '''

    def __init__(self, original_image, now_instance, div_idx, key_num_tuple, page_num):
        '''

        전역 변수 값을 지정해줍니다. 다시 말해 배경이미지, 문장 정보, 지역번호, 각 단어의 가로 세로 값을 지정해줍니다.
        :param original_image : 배경이미지
        :param now_instance : 재조정하려는 문장 정보
        :param div_idx : 지역번호
        :param key_num_tuple : 키워드 종류와 각 키워드의 개수
        :param page_num : 카탈로그 이미지 번호
        주의: page_num과 key_num_tuple은 오류를 확인하기 위함입니다.
        '''
        self.original_image = original_image
        self.now_instance = now_instance
        self.div_idx = div_idx
        self.r = random.Random()
        if self.now_instance[0]:
            self.w_1 = self.now_instance[0][-1][2]
            self.h_1 = self.now_instance[0][-1][3]
        if self.now_instance[1]:
            self.w_2 = self.now_instance[1][-1][2]
            self.h_2 = self.now_instance[1][-1][3]
        if self.now_instance[2]:
            self.w_3 = self.now_instance[2][-1][2]
            self.h_3 = self.now_instance[2][-1][3]
        self.r = random.Random()
        '''while 문제를 체크하기 위한 변수'''
        self.page_num = page_num
        self.key_num_tuple = key_num_tuple
        self.key_num_sum = 0
        for key_num in self.key_num_tuple:
            self.key_num_sum += key_num[1]

    def Relocate_1(self, nonkey_av_instance):
        '''
        문단의 첫 번째 문장을 임의로 위치시킵니다. 중복 문제를 해결하면 문장 중 어떤 단어가 없어지는지 제어 불가한데, 단어가 없어지는 모든 상황에서
        :param nonkey_av_instance: 문장 중 키워드 없이 첫 번째 논키워드, 두 번째 논키워드만 있을 때 키워드의 위치를 비워두기 위한 변수입니다.
        :return: 위치가 바뀐 문장 정보
        '''
        # '''첫번째 워드가 있을 때입니다.'''
        if self.now_instance[0]:
            self.fake_x1 = self.r.choice(range(0, self.original_image.size[0]))
            self.fake_y1 = self.r.choice(range((self.original_image.size[0] * self.div_idx) + 2,
                                               self.original_image.size[0] * (self.div_idx + 1)))
            # '''두번째 키워드가 있을 때입니다.'''
            if self.now_instance[1]:
                self.fake_x2 = self.fake_x1 + self.w_1 + 1

                # '''세번째 키워드가 있을 때입니다.'''
                if self.now_instance[2]:
                    self.fake_x3 = self.fake_x2 + self.w_2 + 1

                    # x를 결정합니다.
                    if self.fake_x3 + self.w_3 < self.original_image.size[0]:
                        self.re_x1 = self.fake_x1
                    else:
                        print('while 문제_1_1')
                        while self.fake_x3 + self.w_3 >= self.original_image.size[0]:
                            self.fake_x1 = self.r.choice(range(0, self.original_image.size[0]))
                            self.fake_x2 = self.fake_x1 + self.w_1 + 1
                            self.fake_x3 = self.fake_x2 + self.w_2 + 1

                        self.re_x1 = self.fake_x1
                    self.re_x2 = self.re_x1 + self.w_1 + 1
                    self.re_x3 = self.re_x2 + self.w_2 + 1

                    # y를 결정합니다.
                    if self.fake_y1 + max([self.h_1, self.h_2, self.h_3]) < (
                        self.original_image.size[0] * (self.div_idx + 1)) - 2:
                        self.re_y1 = self.fake_y1
                    else:
                        print('while 문제_1_2')
                        while self.fake_y1 + max([self.h_1, self.h_2, self.h_3]) >= (
                            self.original_image.size[0] * (self.div_idx + 1)) - 2:
                            self.fake_y1 = self.r.choice(range((self.original_image.size[0] * self.div_idx) + 2,
                                                                (self.original_image.size[0] * (self.div_idx + 1)) - max([self.h_1, self.h_2, self.h_3])))
                        self.re_y1 = self.fake_y1
                    self.re_y2 = self.re_y1
                    self.re_y3 = self.re_y1
                    self.now_instance[0][-1][0] = self.re_x1
                    self.now_instance[0][-1][1] = self.re_y1
                    self.now_instance[1][-1][0] = self.re_x2
                    self.now_instance[1][-1][1] = self.re_y2
                    self.now_instance[2][-1][0] = self.re_x3
                    self.now_instance[2][-1][1] = self.re_y3
                    return self.now_instance

                # '''세 번째 키워드가 없을 때입니다.'''
                else:
                    # x를 결정합니다.
                    if self.fake_x2 + self.w_2 < self.original_image.size[0]:
                        self.re_x1 = self.fake_x1
                    else:
                        print('while 문제_1_3')
                        while self.fake_x2 + self.w_2 >= self.original_image.size[0]:
                            self.fake_x1 = self.r.choice(range(0, self.original_image.size[0]))
                            self.fake_x2 = self.fake_x1 + self.w_1 + 1
                        self.re_x1 = self.fake_x1
                    self.re_x2 = self.re_x1 + self.w_1 + 1

                    # y를 결정합니다.
                    if self.fake_y1 + max([self.h_1, self.h_2]) < self.original_image.size[0] * (self.div_idx + 1):
                        self.re_y1 = self.fake_y1
                    else:
                        print('while 문제_1_4')
                        while self.fake_y1 + max([self.h_1, self.h_2]) >= self.original_image.size[0] * (
                            self.div_idx + 1):
                            self.fake_y1 = self.r.choice(range((self.original_image.size[0] * self.div_idx) + 2,
                                                                (self.original_image.size[0] * (self.div_idx + 1))-max([self.h_1,self.h_2])))
                        self.re_y1 = self.fake_y1
                    self.re_y2 = self.re_y1
                    self.now_instance[0][-1][0] = self.re_x1
                    self.now_instance[0][-1][1] = self.re_y1
                    self.now_instance[1][-1][0] = self.re_x2
                    self.now_instance[1][-1][1] = self.re_y2
                    return self.now_instance

            # ''' 두 번째 키워드가 없을 때입니다. '''
            else:
                # ''' 세 번째 키워드가 있을 때입니다. '''
                if self.now_instance[2]:
                    self.fake_x2 = self.fake_x1 + self.w_1 + 1
                    w_2 = nonkey_av_instance[2][-1][0] - (nonkey_av_instance[0][-1][0] + nonkey_av_instance[0][-1][2])
                    self.fake_x3 = self.fake_x2 + w_2 + 1

                    # x를 결정합니다.
                    if self.fake_x3 + self.w_3 < self.original_image.size[0]:
                        self.re_x1 = self.fake_x1
                    else:
                        print('while 문제_1_5')
                        while self.fake_x3 + self.w_3 >= self.original_image.size[0]:
                            self.fake_x1 = self.r.choice(range(0, self.original_image.size[0]))
                            self.fake_x2 = self.fake_x1 + self.w_1 + 1
                            self.fake_x3 = self.fake_x2 + w_2 + 1
                        self.re_x1 = self.fake_x1
                    self.re_x2 = self.re_x1 + self.w_1 + 1
                    self.re_x3 = self.re_x2 + w_2 + 1

                    # y를 결정합니다.
                    if self.fake_y1 + max([self.h_1, self.h_3]) < self.original_image.size[0] * (self.div_idx + 1):
                        self.re_y1 = self.fake_y1
                    else:
                        print('while 문제_1_6')
                        while self.fake_y1 + max([self.h_1, self.h_3]) >= self.original_image.size[0] * (
                            self.div_idx + 1):
                            self.fake_y1 = self.r.choice(range((self.original_image.size[0] * self.div_idx) + 2,
                                                                (self.original_image.size[0] * (self.div_idx + 1))-max([self.h_1,self.h_3])))
                        self.re_y1 = self.fake_y1
                    self.re_y3 = self.re_y1
                    self.now_instance[0][-1][0] = self.re_x1
                    self.now_instance[0][-1][1] = self.re_y1
                    self.now_instance[2][-1][0] = self.re_x3
                    self.now_instance[2][-1][1] = self.re_y3
                    return self.now_instance

                # '''세 번째 키워드가 없을 때입니다. '''
                else:
                    # x를 결정합니다.
                    if self.fake_x1 + self.w_1 < self.original_image.size[0]:
                        self.re_x1 = self.fake_x1
                    else:
                        print('while 문제_1_7')
                        while self.fake_x1 + self.w_1 >= self.original_image.size[0]:
                            self.fake_x1 = self.r.choice(range(0, self.original_image.size[0]))
                        self.re_x1 = self.fake_x1

                    # y를 결정합니다.
                    if self.fake_y1 + max([self.h_1]) < self.original_image.size[0] * (self.div_idx + 1):
                        self.re_y1 = self.fake_y1
                    else:
                        print('while 문제_1_8')
                        while self.fake_y1 + max([self.h_1]) >= self.original_image.size[0] * (self.div_idx + 1):
                            self.fake_y1 = self.r.choice(range((self.original_image.size[0] * self.div_idx) + 2,
                                                                (self.original_image.size[0] * (self.div_idx + 1))-max([self.h_1])))
                        self.re_y1 = self.fake_y1

                    self.now_instance[0][-1][0] = self.re_x1
                    self.now_instance[0][-1][1] = self.re_y1
                    return self.now_instance


        # '''첫 번째 키워드가 없을 때입니다. '''
        else:
            # '''두 번째 키워드가 있을 때입니다. '''
            if self.now_instance[1]:
                self.fake_x2 = self.r.choice(range(0, self.original_image.size[0]))
                self.fake_y2 = self.r.choice(range((self.original_image.size[0] * self.div_idx) + 2 , (self.original_image.size[0] *(self.div_idx+1))-self.h_2))

                # '''세번째 키워드가 있을 때입니다.'''
                if self.now_instance[2]:
                    self.fake_x3 = self.fake_x2 + self.w_2 + 1

                    # x를 결정합니다.
                    if self.fake_x3 + self.w_3 < self.original_image.size[0]:
                        self.re_x2 = self.fake_x2
                    else:
                        print('while 문제_1_9')
                        while self.fake_x3 + self.w_3 >= self.original_image.size[0]:
                            self.fake_x2 = self.r.choice(range(0, self.original_image.size[0]))
                            self.fake_x3 = self.fake_x2 + self.w_2 + 1
                        self.re_x2 = self.fake_x2
                    self.re_x3 = self.re_x2 + self.w_2 + 1

                    # y를 결정합니다.
                    if self.fake_y2 + max([self.h_2, self.h_3]) < self.original_image.size[0] * (self.div_idx+1):
                        self.re_y2 = self.fake_y2
                    else:
                        print('while 문제_1_10')
                        while self.fake_y2 + max([self.h_2, self.h_3]) >= self.original_image.size[0] *(self.div_idx+1):
                            self.fake_y2 = self.r.choice(range((self.original_image.size[0] * self.div_idx)+2, (self.original_image.size[0] *(self.div_idx+1))-max([self.h_2,self.h_3])))
                        self.re_y2 = self.fake_y2
                    self.re_y3 = self.re_y2
                    self.now_instance[1][-1][0] = self.re_x2
                    self.now_instance[1][-1][1] = self.re_y2
                    self.now_instance[2][-1][0] = self.re_x3
                    self.now_instance[2][-1][1] = self.re_y3
                    return self.now_instance
                # '''세 번째 키워드가 없을 때입니다.'''
                else:
                    # x를 결정합니다.
                    if self.fake_x2 + self.w_2 < self.original_image.size[0]:
                        self.re_x2 = self.fake_x2
                    else:
                        print('while 문제_1_11')
                        while self.fake_x2 + self.w_2 >= self.original_image.size[0]:
                            self.fake_x2 = self.r.choice(range(0, self.original_image.size[0]))
                        self.re_x2 = self.fake_x2
                    # y를 결정합니다.
                    if self.fake_y2 + max([self.h_2]) < self.original_image.size[0] *(self.div_idx+1):
                        self.re_y2 = self.fake_y2
                    else:
                        print('while 문제_1_12')
                        while self.fake_y2 + max([self.h_2]) >= self.original_image.size[0] * (self.div_idx+1):
                            self.fake_y2 = self.r.choice(range((self.original_image.size[0] * self.div_idx) + 2, (self.original_image.size[0] *(self.div_idx+1))-max([self.h_2])))
                        self.re_y2 = self.fake_y2
                    self.now_instance[1][-1][0] = self.re_x2
                    self.now_instance[1][-1][1] = self.re_y2
                    return self.now_instance
            # '''두 번째 키워드가 없을 때입니다. '''
            else:
                # ''' 세 번째 키워드가 있을 때입니다. '''
                if self.now_instance[2]:
                    self.fake_x3 = self.r.choice(range(0, self.original_image.size[0]))
                    self.fake_y3 = self.r.choice(range((self.original_image.size[0] *self.div_idx) + 2, (self.original_image.size[0] * (self.div_idx+1))-self.h_3))

                    # x를 결정합니다.
                    if self.fake_x3 + self.w_3 < self.original_image.size[0]:
                        self.re_x3 = self.fake_x3
                    else:
                        print('while 문제_1_13')
                        while self.fake_x3 + self.w_3 >= self.original_image.size[0]:
                            self.fake_x3 = self.r.choice(range(0, self.original_image.size[0]))
                        self.re_x3 = self.fake_x3
                    # y를 결정합니다.
                    if self.fake_y3 + max([self.h_3]) < self.original_image.size[0] * (self.div_idx+1):
                        self.re_y3 = self.fake_y3
                    else:
                        print('while 문제_1_14')
                        while self.fake_y3 + max([self.h_3]) >= self.original_image.size[0] *(self.div_idx+1):
                            self.fake_y3 = self.r.choice(range((self.original_image.size[0] *self.div_idx)+2, (self.original_image.size[0] *(self.div_idx+1))-self.h_3))
                        self.re_y3 = self.fake_y3
                    self.now_instance[2][-1][0] = self.re_x3
                    self.now_instance[2][-1][1] = self.re_y3
                    return self.now_instance
                # ''' 세 번째 키워드가 없을 때입니다. '''
                else:
                    return self.now_instance

    def Relocate_2_down(self, ex_instance, nonkey_av_instance):
        '''
        문장을 문단 단위로 위치시키기 위해 문장을 이전 문장을 참고하여 아래로 위치시킵니다. 
        :param ex_instance: 이전 문장 정보입니다.
        :param nonkey_av_instance: 문장 중 키워드 없이 첫 번째 논키워드, 두 번째 논키워드만 있을 때 키워드의 위치를 비워두기 위한 변수입니다.
        :return: 위치가 바뀐 문장 정보
        '''

        self.ex_instance = ex_instance
        if self.ex_instance[0]:
            self.ex_x1 = self.ex_instance[0][-1][0]
            self.ex_y1 = self.ex_instance[0][-1][1]
            self.ex_w_1 = self.ex_instance[0][-1][2]
            self.ex_h_1 = self.ex_instance[0][-1][3]
        if self.ex_instance[1]:
            self.ex_x2 = self.ex_instance[1][-1][0]
            self.ex_y2 = self.ex_instance[1][-1][1]
            self.ex_w_2 = self.ex_instance[1][-1][2]
            self.ex_h_2 = self.ex_instance[1][-1][3]
        if self.ex_instance[2]:
            self.ex_x3 = self.ex_instance[2][-1][0]
            self.ex_y3 = self.ex_instance[2][-1][1]
            self.ex_w_3 = self.ex_instance[2][-1][2]
            self.ex_h_3 = self.ex_instance[2][-1][3]


        # '''이전 인스턴스의 x좌표 최솟값, y 대푯값, h 최댓값을 구합니다(ex_x_min, ex_y_repre, ex_h_max).
        # '''첫번째가 있을 때입니다.'''
        if self.ex_instance[0]:
            self.ex_x_min = self.ex_instance[0][-1][0]
            self.ex_y_repre = self.ex_y1
            # '''두 번째가 있을 때입니다.'''
            if self.ex_instance[1]:
                # '''세 번째가 있을 때입니다.'''
                if self.ex_instance[2]:
                    self.ex_h_max = max([self.ex_h_1, self.ex_h_2, self.ex_h_3])
                # '''세 번째가 없을 때입니다.'''
                else:
                    self.ex_h_max = max([self.ex_h_1, self.ex_h_2])
            # '''두 번째가 없을 때입니다.'''
            else:
                # '''세 번째가 있을 때입니다.'''
                if self.ex_instance[2]:
                    self.ex_h_max = max([self.ex_h_1, self.ex_h_3])
                # '''세 번째가 없을 때입니다.'''
                else:
                    self.ex_h_max = max([self.ex_h_1])
        # '''첫번째가 없을 때입니다.'''
        else:
            # '''두 번째가 있을 때입니다.'''
            if self.ex_instance[1]:
                self.ex_x_min = self.ex_instance[1][-1][0]
                self.ex_y_repre = self.ex_y2
                # '''세 번째가 있을 때입니다.'''
                if self.ex_instance[2]:
                    self.ex_h_max = max([self.ex_h_2, self.ex_h_3])
                # '''세 번째가 없을 때입니다.'''
                else:
                    self.ex_h_max = max([self.ex_h_2])
            # '''두 번째가 없을 때입니다.'''
            else:
                # '''세 번째가 있을 때입니다.'''
                if self.ex_instance[2]:
                    self.ex_x_min = self.ex_instance[2][-1][0]
                    self.ex_y_repre = self.ex_y3
                    self.ex_h_max = max([self.ex_h_3])
                # '''세 번째가 없을 때입니다.'''
                else:
                    pass

        # ''' 현재 문장 정보(now_instance)를 조정해줍니다. '''
        # '''첫번째 워드가 있을 때입니다.'''
        if self.now_instance[0]:
            self.fake_x1 = self.ex_x_min

            # '''두번째 키워드가 있을 때입니다.'''
            if self.now_instance[1]:
                self.fake_x2 = self.fake_x1 + self.w_1 + 1
                # '''세번째 키워드가 있을 때입니다.'''
                if self.now_instance[2]:
                    self.fake_x3 = self.fake_x2 + self.w_2 + 1
                    self.fake_y1 = self.ex_y_repre + self.ex_h_max + 1
                    self.now_h_max = max([self.h_1, self.h_2, self.h_3])
                    # * x, y를 결정합니다.
                    if self.fake_x3 + self.w_3 < self.original_image.size[0] and self.fake_y1 + self.now_h_max < \
                                    self.original_image.size[0] * (self.div_idx + 1):
                        self.re_x1 = self.fake_x1
                        self.re_x2 = self.re_x1 + self.w_1 + 1
                        self.re_x3 = self.re_x2 + self.w_2 + 1
                        self.re_y1 = self.fake_y1
                        self.re_y2 = self.re_y1
                        self.re_y3 = self.re_y2
                    else:
                        print('while 문제_2_1')
                        while self.fake_x3 + self.w_3 >= self.original_image.size[0]:
                            self.fake_x1 = self.r.choice(range(0, self.original_image.size[0]))
                            self.fake_x2 = self.fake_x1 + self.w_1 + 1
                            self.fake_x3 = self.fake_x2 + self.w_2 + 1
                        self.re_x1 = self.fake_x1
                        self.re_x2 = self.re_x1 + self.w_1 + 1
                        self.re_x3 = self.re_x2 + self.w_2 + 1
                        while self.fake_y1 + self.now_h_max >= self.original_image.size[0] * (self.div_idx + 1):
                            self.fake_y1 = self.r.choice(range((self.original_image.size[0] * self.div_idx) + 2,
                                                                (self.original_image.size[0] * (self.div_idx + 1))-self.now_h_max))
                        self.re_y1 = self.fake_y1
                        self.re_y2 = self.re_y1
                        self.re_y3 = self.re_y2
                    self.now_instance[0][-1][0] = self.re_x1
                    self.now_instance[0][-1][1] = self.re_y1
                    self.now_instance[1][-1][0] = self.re_x2
                    self.now_instance[1][-1][1] = self.re_y2
                    self.now_instance[2][-1][0] = self.re_x3
                    self.now_instance[2][-1][1] = self.re_y3
                    return self.now_instance
                # '''세 번째 키워드가 없을 때입니다.'''
                else:
                    self.fake_y1 = self.ex_y_repre + self.ex_h_max + 1
                    self.now_h_max = max(self.h_1, self.h_2)
                    # x , y를 결정합니다.
                    if self.fake_x2 + self.w_2 < self.original_image.size[0] and self.fake_y1 + self.now_h_max < \
                                    self.original_image.size[0] * (self.div_idx + 1):
                        self.re_x1 = self.fake_x1
                        self.re_x2 = self.re_x1 + self.w_1 + 1
                        self.re_y1 = self.fake_y1
                        self.re_y2 = self.re_y1
                    else:
                        print('while 문제_2_2')
                        while self.fake_x2 + self.w_2 >= self.original_image.size[0]:
                            self.fake_x1 = self.r.choice(range(0, self.original_image.size[0]))
                            self.fake_x2 = self.fake_x1 + self.w_1 + 1
                        self.re_x1 = self.fake_x1
                        self.re_x2 = self.re_x1 + self.w_1 + 1
                        while self.fake_y1 + max([self.h_1, self.h_2]) >= self.original_image.size[0] * (
                            self.div_idx + 1):
                            self.fake_y1 = self.r.choice(range((self.original_image.size[0] * self.div_idx) + 2,
                                                                (self.original_image.size[0] * (self.div_idx + 1))-self.now_h_max))
                        self.re_y1 = self.fake_y1
                        self.re_y2 = self.re_y1
                    self.now_instance[0][-1][0] = self.re_x1
                    self.now_instance[0][-1][1] = self.re_y1
                    self.now_instance[1][-1][0] = self.re_x2
                    self.now_instance[1][-1][1] = self.re_y2
                    return self.now_instance
            # ''' 두 번째 키워드가 없을 때입니다. '''
            else:
                # ''' 세 번째 키워드가 있을 때입니다. '''
                if self.now_instance[2]:
                    self.fake_x2 = self.fake_x1 + self.w_1 + 1
                    w_2 = nonkey_av_instance[2][-1][0] - (
                    nonkey_av_instance[0][-1][0] + nonkey_av_instance[0][-1][2])
                    self.fake_x3 = self.fake_x2 + w_2 + 1
                    self.fake_y1 = self.ex_y_repre + self.ex_h_max + 1
                    self.now_h_max = max([self.h_1, self.h_3])
                    # * x, y를 결정합니다.
                    if self.fake_x3 + self.w_3 < self.original_image.size[0] and self.fake_y1 + self.now_h_max < \
                                    self.original_image.size[0] * (self.div_idx + 1):
                        self.re_x1 = self.fake_x1
                        self.re_x2 = self.re_x1 + self.w_1 + 1
                        self.re_x3 = self.re_x2 + w_2 + 1
                        self.re_y1 = self.fake_y1
                        self.re_y3 = self.re_y1
                    else:
                        print('while 문제_2_3')
                        while self.fake_x3 + self.w_3 >= self.original_image.size[0]:
                            self.fake_x1 = self.r.choice(range(0, self.original_image.size[0]))
                            self.fake_x2 = self.fake_x1 + self.w_1 + 1
                            self.fake_x3 = self.fake_x2 + w_2 + 1
                        self.re_x1 = self.fake_x1
                        self.re_x2 = self.re_x1 + self.w_1 + 1
                        self.re_x3 = self.re_x2 + w_2 + 1
                        while self.fake_y1 + self.now_h_max >= self.original_image.size[0] * (self.div_idx + 1):
                            self.fake_y1 = self.r.choice(range((self.original_image.size[0] * self.div_idx) + 2,
                                                                (self.original_image.size[0] * (self.div_idx + 1))-self.now_h_max))
                        self.re_y1 = self.fake_y1
                        self.re_y3 = self.re_y1
                    self.now_instance[0][-1][0] = self.re_x1
                    self.now_instance[0][-1][1] = self.re_y1
                    self.now_instance[2][-1][0] = self.re_x3
                    self.now_instance[2][-1][1] = self.re_y3
                    return self.now_instance

                # '''세 번째 키워드가 없을 때입니다. '''
                else:
                    self.fake_y1 = self.ex_y_repre + self.ex_h_max + 1
                    self.now_h_max = max([self.h_1])
                    # x, y를 결정합니다.
                    if self.fake_x1 + self.w_1 < self.original_image.size[0] and self.fake_y1 + self.now_h_max < \
                                    self.original_image.size[0] * (self.div_idx + 1):
                        self.re_x1 = self.fake_x1
                        self.re_y1 = self.fake_y1
                    else:
                        print('while 문제_2_4')
                        while self.fake_x1 + self.w_1 >= self.original_image.size[0]:
                            self.fake_x1 = self.r.choice(range(0, self.original_image.size[0]))
                        self.re_x1 = self.fake_x1

                        while self.fake_y1 + self.now_h_max >= self.original_image.size[0] * (self.div_idx + 1):
                            self.fake_y1 = self.r.choice(range((self.original_image.size[0] * self.div_idx) + 2,
                                                                (self.original_image.size[0] * (self.div_idx + 1))-self.now_h_max))
                        self.re_y1 = self.fake_y1
                    self.now_instance[0][-1][0] = self.re_x1
                    self.now_instance[0][-1][1] = self.re_y1
                    return self.now_instance
        # '''첫 번째 키워드가 없을 때입니다. '''
        else:
            # '''두 번째 키워드가 있을 때입니다. '''
            if self.now_instance[1]:
                self.fake_x2 = self.ex_x_min

                # '''세번째 키워드가 있을 때입니다.'''
                if self.now_instance[2]:
                    self.fake_x3 = self.fake_x2 + self.w_2 + 1
                    self.fake_y2 = self.ex_y_repre + self.ex_h_max + 1
                    self.now_h_max = max([self.h_2, self.h_3])
                    # x, y를 결정합니다.
                    if self.fake_x3 + self.w_3 < self.original_image.size[0] and self.fake_y2 + self.now_h_max < \
                                    self.original_image.size[0] * (self.div_idx + 1):
                        self.re_x2 = self.fake_x2
                        self.re_x3 = self.re_x2 + self.w_2 + 1
                        self.re_y2 = self.fake_y2
                        self.re_y3 = self.re_y2
                    else:
                        print('while 문제_2_5')
                        while self.fake_x3 + self.w_3 >= self.original_image.size[0]:
                            self.fake_x2 = self.r.choice(range(0, self.original_image.size[0]))
                            self.fake_x3 = self.fake_x2 + self.w_2 + 1
                        self.re_x2 = self.fake_x2
                        self.re_x3 = self.re_x2 + self.w_2 + 1
                        while self.fake_y2 + self.now_h_max >= self.original_image.size[0] * (self.div_idx + 1):
                            self.fake_y2 = self.r.choice(range((self.original_image.size[0] * self.div_idx) + 2,
                                                                (self.original_image.size[0] * (self.div_idx + 1))-self.now_h_max))
                        self.re_y2 = self.fake_y2
                        self.re_y3 = self.re_y2
                    self.now_instance[1][-1][0] = self.re_x2
                    self.now_instance[1][-1][1] = self.re_y2
                    self.now_instance[2][-1][0] = self.re_x3
                    self.now_instance[2][-1][1] = self.re_y3
                    return self.now_instance
                # '''세번째 키워드가 없을 때입니다.'''
                else:
                    self.fake_y2 = self.ex_y_repre + self.ex_h_max + 1
                    self.now_h_max = max([self.h_2])
                    # x , y를 결정합니다.
                    if self.fake_x2 + self.w_2 < self.original_image.size[0] and self.fake_y2 + self.now_h_max < \
                                    self.original_image.size[0] * (self.div_idx + 1):
                        self.re_x2 = self.fake_x2
                        self.re_y2 = self.fake_y2
                    else:
                        print('while 문제_2_6')
                        while self.fake_x2 + self.w_2 >= self.original_image.size[0]:
                            self.fake_x2 = self.r.choice(range(0, self.original_image.size[0]))

                        self.re_x2 = self.fake_x2

                        while self.fake_y2 + self.now_h_max >= self.original_image.size[0] * (self.div_idx + 1):
                            self.fake_y2 = self.r.choice(range((self.original_image.size[0] * self.div_idx) + 2,
                                                                (self.original_image.size[0] * (self.div_idx + 1))-self.now_h_max))
                        self.re_y2 = self.fake_y2
                    self.now_instance[1][-1][0] = self.re_x2
                    self.now_instance[1][-1][1] = self.re_y2
                    return self.now_instance
            # ''' 두 번째 키워드가 없을 때입니다. '''
            else:
                # ''' 세 번째 키워드가 있을 때입니다. '''
                if self.now_instance[2]:
                    self.fake_x3 = self.ex_x_min
                    self.fake_y3 = self.ex_y_repre + self.ex_h_max + 1
                    self.now_h_max = max([self.h_3])
                    # x, y를 결정합니다.
                    if self.fake_x3 + self.w_3 < self.original_image.size[0] and self.fake_y3 + self.now_h_max < \
                                    self.original_image.size[0] * (self.div_idx + 1):
                        self.re_x3 = self.fake_x3
                        self.re_y3 = self.fake_y3
                    else:
                        print('while 문제_2_7')
                        while self.fake_x3 + self.w_3 >= self.original_image.size[0]:
                            self.fake_x3 = self.r.choice(range(0, self.original_image.size[0]))
                        self.re_x3 = self.fake_x3
                        while self.fake_y3 + self.now_h_max >= self.original_image.size[0] * (self.div_idx + 1):
                            self.fake_y3 = self.r.choice(range((self.original_image.size[0] * self.div_idx) + 2,
                                                                (self.original_image.size[0] * (self.div_idx + 1))-self.now_h_max))
                        self.re_y3 = self.fake_y3
                    self.now_instance[2][-1][0] = self.re_x3
                    self.now_instance[2][-1][1] = self.re_y3
                    return self.now_instance
                else:
                    return self.now_instance

    def Relocate_3_check(self,re_instance, adress_all, adress_printed, true_or_false_for_instance, nonkey_av_instance):
        '''
        다시 위치시킨 문장이 겹치는 문제를 해결합니다. 중복이 되면 랜덤으로 다시 위치시킵니다.
        :param re_instance: 
        :param adress_all: 
        :param adress_printed: 
        :param true_or_false_for_instance: 
        :param nonkey_av_instance: 
        :return: 위치가 바뀌었고 겹치지 않는 문장 정보
        '''

        #'''x,y의 최솟값, 최댓값(min, max)을 구합니다.'''
        #'''첫번째 키워드가 있을 때입니다.'''

        if re_instance[0]:
            self.x_min = re_instance[0][-1][0]
            self.y_min = re_instance[0][-1][1]
            # '''두번째 키워드가 있을 때입니다.'''
            if re_instance[1]:
                # '''세번째 키워드가 있을 때입니다.'''
                if re_instance[2]:
                    self.x_max = re_instance[2][-1][0] + re_instance[2][-1][2]
                    self.y_max = self.y_min + max([re_instance[0][-1][-1], re_instance[1][-1][-1], re_instance[2][-1][-1]])

                # '''세 번째 키워드가 없을 때입니다.'''
                else:
                    self.x_max = re_instance[1][-1][0] + re_instance[1][-1][2]
                    self.y_max = self.y_min + max([re_instance[0][-1][-1], re_instance[1][-1][-1]])
            # ''' 두 번째 키워드가 없을 때입니다. '''
            else:
                # ''' 세 번째 키워드가 있을 때입니다. '''
                if re_instance[2]:
                    self.x_max = re_instance[2][-1][0] + re_instance[2][-1][2]
                    self.y_max = self.y_min + max([re_instance[0][-1][-1], re_instance[2][-1][-1]])
                # '''세 번째 키워드가 없을 때입니다. '''
                else:
                    self.x_max = re_instance[0][-1][0] + re_instance[0][-1][2]
                    self.y_max = self.y_min + max([re_instance[0][-1][-1]])
        # '''첫 번째 키워드가 없을 때입니다. '''
        else:
            # '''두 번째 키워드가 있을 때입니다. '''
            if re_instance[1]:
                self.x_min = re_instance[1][-1][0]
                self.y_min = re_instance[1][-1][1]
                # '''세번째 키워드가 있을 때입니다.'''
                if re_instance[2]:
                    self.x_max = re_instance[2][-1][0] + re_instance[2][-1][2]
                    self.y_max = self.y_min + max([re_instance[1][-1][-1], re_instance[2][-1][-1]])
                # '''세 번째 키워드가 없을 때입니다.'''
                else:
                    self.x_max = re_instance[1][-1][0] + re_instance[1][-1][2]
                    self.y_max = self.y_min + max([re_instance[1][-1][-1]])
            # '''두 번째 키워드가 없을 때입니다. '''
            else:
                # ''' 세 번째 키워드가 있을 때입니다. '''
                if re_instance[2]:
                    self.x_min = re_instance[2][-1][0]
                    self.y_min = re_instance[2][-1][1]
                    self.x_max = self.x_min + re_instance[2][-1][2]
                    self.y_max = self.y_min + max([re_instance[2][-1][-1]])
                # ''' 세 번째 키워드가 없을 때입니다. '''
                else:
                    pass

        # '''중복 문제를 해결합니다.'''
        for num_p1, instance_p in enumerate(adress_all):

            try:
                printed_instance = adress_printed[num_p1]

                #'''이미 프린트된 문장의 x, y의 최솟값과 최댓값(min, max)을 지정해줍니다.'''
                #'''첫 번째 키워드가 있을 때입니다.
                if printed_instance[0]:
                    self.printed_x_min = printed_instance[0][-1][0]
                    self.printed_y_min = printed_instance[0][-1][1]

                    # '''두번째 키워드가 있을 때입니다.'''
                    if printed_instance[1]:
                        # '''세번째 키워드가 있을 때입니다.'''
                        if printed_instance[2]:
                            self.printed_x_max = printed_instance[2][-1][0] + printed_instance[2][-1][2]
                            self.printed_y_max = self.printed_y_min + max([printed_instance[0][-1][3], printed_instance[1][-1][3], printed_instance[2][-1][3]])

                        # '''세 번째 키워드가 없을 때입니다.'''
                        else:
                            self.printed_x_max = printed_instance[1][-1][0] + printed_instance[1][-1][2]
                            self.printed_y_max = self.printed_y_min + max([printed_instance[0][-1][3], printed_instance[1][-1][3]])

                    # ''' 두 번째 키워드가 없을 때입니다. '''
                    else:
                        # ''' 세 번째 키워드가 있을 때입니다. '''
                        if printed_instance[2]:
                            self.printed_x_max = printed_instance[2][-1][0] + printed_instance[2][-1][2]
                            self.printed_y_max = self.printed_y_min + max([printed_instance[0][-1][3], printed_instance[2][-1][3]])
                        # '''세 번째 키워드가 없을 때입니다. '''
                        else:
                            self.printed_x_max = printed_instance[0][-1][0] + printed_instance[0][-1][2]
                            self.printed_y_max = self.printed_y_min + max([printed_instance[0][-1][3]])

                # '''첫 번째 키워드가 없을 때입니다. '''
                else:
                    # '''두 번째 키워드가 있을 때입니다. '''
                    if printed_instance[1]:
                        self.printed_x_min = printed_instance[1][-1][0]
                        self.printed_y_min = printed_instance[1][-1][1]
                        # '''세번째 키워드가 있을 때입니다.'''
                        if printed_instance[2]:
                            self.printed_x_max = printed_instance[2][-1][0] + printed_instance[2][-1][2]
                            self.printed_y_max = self.printed_y_min + max([printed_instance[1][-1][3], printed_instance[2][-1][3]])
                        # '''세 번째 키워드가 없을 때입니다.'''
                        else:
                            self.printed_x_max = printed_instance[1][-1][0] + printed_instance[1][-1][2]
                            self.printed_y_max = self.printed_y_min + max([printed_instance[1][-1][3]])
                    # '''두 번째 키워드가 없을 때입니다. '''
                    else:
                        # ''' 세 번째 키워드가 있을 때입니다. '''
                        if printed_instance[2]:
                            self.printed_x_min = printed_instance[2][-1][0]
                            self.printed_y_min = printed_instance[2][-1][1]
                            self.printed_x_max = self.printed_x_min + printed_instance[2][-1][2]
                            self.printed_y_max = self.printed_y_min + max([printed_instance[2][-1][3]])
                        # ''' 세 번째 키워드가 없을 때입니다. '''
                        else:
                            pass

                # '''중복 문제를 해결합니다.'''
                # ''' 왼쪽 위 꼭지점이 들어감'''
                if self.x_min >= self.printed_x_min and self.x_min <= self.printed_x_max and self.y_min >= self.printed_y_min and self.y_min <= self.printed_y_max:
                    true_or_false_for_instance.append('false')
                    print('겹침 확인_재조정: 겹쳤습니다-1번유형')
                    break
                # '''오른쪽 위 꼭지점이 들어감'''
                elif self.x_max >= self.printed_x_min and self.x_max <= self.printed_x_max and self.y_min >= self.printed_y_min and self.y_min <= self.printed_y_max:
                    true_or_false_for_instance.append('false')
                    print('겹침 확인_재조정: 겹쳤습니다-2번유형')
                    break
                # '''왼쪽 아래 꼭지점이 들어감'''
                elif self.x_min >= self.printed_x_min and self.x_min <= self.printed_x_max and self.y_max >= self.printed_y_min and self.y_max <= self.printed_y_max:
                    true_or_false_for_instance.append('false')
                    print('겹침 확인_재조정: 겹쳤습니다-3번유형')
                    break
                # '''오른쪽 아래 꼭지점이 들어감'''
                elif self.x_max >= self.printed_x_min and self.x_max <= self.printed_x_max and self.y_max >= self.printed_y_min and self.y_max <= self.printed_y_max:
                    true_or_false_for_instance.append('false')
                    print('겹침 확인_재조정: 겹쳤습니다-4번유형')
                    break
                elif self.x_min <= self.printed_x_min and self.x_max >= self.printed_x_max and self.y_max >= self.printed_y_min and self.y_max <= self.printed_y_max:
                    true_or_false_for_instance.append('false')
                    print('겹침 확인_재조정: 겹쳤습니다-5번유형')
                    break
                elif self.x_min <= self.printed_x_min and self.x_max >= self.printed_x_max and self.y_min >= self.printed_y_min and self.y_min <= self.printed_y_max:
                    true_or_false_for_instance.append('false')
                    print('겹침 확인_재조정: 겹쳤습니다-6번유형')
                    break
                elif self.x_max >= self.printed_x_min and self.x_max <= self.printed_x_max and self.y_min <= self.printed_y_min and self.y_max >= self.printed_y_max:
                    true_or_false_for_instance.append('false')
                    print('겹침 확인_재조정: 겹쳤습니다-7번유형')
                    break
                elif self.x_min >= self.printed_x_min and self.x_min <= self.printed_x_max and self.y_min <= self.printed_y_min and self.y_max >= self.printed_y_max:
                    true_or_false_for_instance.append('false')
                    print('겹침 확인_재조정: 겹쳤습니다-8번유형')
                    break
                elif self.x_min <= self.printed_x_min and self.x_max >= self.printed_x_max and self.y_min <= self.printed_y_min and self.y_max >= self.printed_y_max:
                    true_or_false_for_instance.append('false')
                    print('겹침 확인_재조정: 겹쳤습니다-9번유형')
                    break
                else:
                    pass
            except:
                pass
        if 'false' in true_or_false_for_instance:
            while 'false' in true_or_false_for_instance:
                print('현재 페이지 넘버:', self.page_num)
                print('현재 키워드 개수:', self.key_num_sum)
                print('현재 배경이미지 사이즈:', self.original_image.size[0]*self.original_image.size[1])
                print('현재 지역 번호:', self.div_idx)
                print('재조정 한 인스턴스가 겹칩니다.',re_instance, true_or_false_for_instance)
                print('현재 이미지 사이즈:', self.original_image.size[0] * self.original_image.size[1])
                true_or_false_for_instance = []
                re_locate = Location_Relocate(self.original_image, now_instance= re_instance, div_idx=self.div_idx, key_num_tuple=self.key_num_tuple, page_num=self.page_num)
                self.re_re_instance = re_locate.Relocate_1(nonkey_av_instance= nonkey_av_instance)
                print('겹친 인스턴스의 주소를 바꿨습니다:', self.re_re_instance)
                # '''문장의 x,y의 최솟값과 최댓값(min, max)을 다시 정해줍니다.'''
                # '''첫번째 워드가 있을 때입니다.'''
                if self.re_re_instance[0]:
                    x_min_re = self.re_re_instance[0][-1][0]
                    y_min_re = self.re_re_instance[0][-1][1]
                    # '''두번째 키워드가 있을 때입니다.'''
                    if self.re_re_instance[1]:
                        # '''세번째 키워드가 있을 때입니다.'''
                        if self.re_re_instance[2]:
                            x_max_re = self.re_re_instance[2][-1][0] + self.re_re_instance[2][-1][2]
                            y_max_re = y_min_re + max([self.re_re_instance[0][-1][3], self.re_re_instance[1][-1][3], self.re_re_instance[2][-1][3]])
                        # '''세 번째 키워드가 없을 때입니다.'''
                        else:
                            x_max_re = self.re_re_instance[1][-1][0] + self.re_re_instance[1][-1][2]
                            y_max_re = y_min_re + max([self.re_re_instance[0][-1][3], self.re_re_instance[1][-1][3]])
                    # ''' 두 번째 키워드가 없을 때입니다. '''
                    else:
                        # ''' 세 번째 키워드가 있을 때입니다. '''
                        if self.re_re_instance[2]:
                            x_max_re = self.re_re_instance[2][-1][0] + self.re_re_instance[2][-1][2]
                            y_max_re = y_min_re + max([self.re_re_instance[0][-1][3], self.re_re_instance[2][-1][3]])
                        # '''세 번째 키워드가 없을 때입니다. '''
                        else:
                            x_max_re = self.re_re_instance[0][-1][0] + self.re_re_instance[0][-1][2]
                            y_max_re = y_min_re + max([self.re_re_instance[0][-1][3]])
                # '''첫 번째 키워드가 없을 때입니다. '''
                else:
                    # '''두 번째 키워드가 있을 때입니다. '''
                    if self.re_re_instance[1]:
                        x_min_re = self.re_re_instance[1][-1][0]
                        y_min_re = self.re_re_instance[1][-1][1]
                        # '''세번째 키워드가 있을 때입니다.'''
                        if self.re_re_instance[2]:
                            x_max_re = self.re_re_instance[2][-1][0] + self.re_re_instance[2][-1][2]
                            y_max_re = y_min_re + max([self.re_re_instance[1][-1][3], self.re_re_instance[2][-1][3]])
                        # '''세 번째 키워드가 없을 때입니다.'''
                        else:
                            x_max_re = self.re_re_instance[1][-1][0] + self.re_re_instance[1][-1][2]
                            y_max_re = y_min_re + max([self.re_re_instance[1][-1][3]])
                    # '''두 번째 키워드가 없을 때입니다. '''
                    else:
                        # ''' 세 번째 키워드가 있을 때입니다. '''
                        if self.re_re_instance[2]:
                            x_min_re = self.re_re_instance[2][-1][0]
                            y_min_re = self.re_re_instance[2][-1][1]
                            x_max_re = x_min_re + self.re_re_instance[2][-1][2]
                            y_max_re = y_min_re + max([self.re_re_instance[2][-1][3]])
                        # ''' 세 번째 키워드가 없을 때입니다. '''
                        else:
                            pass
                # '''중복 문제를 해결합니다.'''
                for num_t1, instance_e in enumerate(adress_all):
                    try:
                        printed_instance_sec = adress_printed[num_t1]
                        # '''이미 프린트된 문장의 x, y의 최솟값과 최댓값(min, max)을 지정해줍니다.'''
                        # '''첫 번째 키워드가 있을 때입니다.
                        if printed_instance_sec[0]:
                            printed_x_min_re = printed_instance_sec[0][-1][0]
                            printed_y_min_re = printed_instance_sec[0][-1][1]
                            # '''두번째 키워드가 있을 때입니다.'''
                            if printed_instance_sec[1]:
                                # '''세번째 키워드가 있을 때입니다.'''
                                if printed_instance_sec[2]:
                                    printed_x_max_re = printed_instance_sec[2][-1][0] + printed_instance_sec[2][-1][2]
                                    printed_y_max_re = printed_y_min_re + max(
                                        [printed_instance_sec[0][-1][3], printed_instance_sec[1][-1][3],
                                         printed_instance_sec[2][-1][3]])

                                # '''세 번째 키워드가 없을 때입니다.'''
                                else:
                                    printed_x_max_re = printed_instance_sec[1][-1][0] + printed_instance_sec[1][-1][2]
                                    printed_y_max_re = printed_y_min_re + max(
                                        [printed_instance_sec[0][-1][2], printed_instance_sec[1][-1][3]])

                            # ''' 두 번째 키워드가 없을 때입니다. '''
                            else:
                                # ''' 세 번째 키워드가 있을 때입니다. '''
                                if printed_instance_sec[2]:
                                    printed_x_max_re = printed_instance_sec[2][-1][0] + printed_instance_sec[2][-1][2]
                                    printed_y_max_re = printed_y_min_re + max(
                                        [printed_instance_sec[0][-1][3], printed_instance_sec[2][-1][3]])
                                # '''세 번째 키워드가 없을 때입니다. '''
                                else:
                                    printed_x_max_re = printed_instance_sec[0][-1][0] + printed_instance_sec[0][-1][2]
                                    printed_y_max_re = printed_y_min_re + max([printed_instance_sec[0][-1][3]])
                        # '''첫 번째 키워드가 없을 때입니다. '''
                        else:
                            # '''두 번째 키워드가 있을 때입니다. '''
                            if printed_instance_sec[1]:
                                printed_x_min_re = printed_instance_sec[1][-1][0]
                                printed_y_min_re = printed_instance_sec[1][-1][1]
                                # '''세번째 키워드가 있을 때입니다.'''
                                if printed_instance_sec[2]:
                                    printed_x_max_re = printed_instance_sec[2][-1][0] + printed_instance_sec[2][-1][2]
                                    printed_y_max_re = printed_y_min_re + max(
                                        [printed_instance_sec[1][-1][3], printed_instance_sec[2][-1][3]])
                                # '''세 번째 키워드가 없을 때입니다.'''
                                else:
                                    printed_x_max_re = printed_instance_sec[1][-1][0] + printed_instance_sec[1][-1][2]
                                    printed_y_max_re = printed_y_min_re + max([printed_instance_sec[1][-1][3]])

                            # '''두 번째 키워드가 없을 때입니다. '''
                            else:
                                # ''' 세 번째 키워드가 있을 때입니다. '''
                                if printed_instance_sec[2]:
                                    printed_x_min_re = printed_instance_sec[2][-1][0]
                                    printed_y_min_re = printed_instance_sec[2][-1][1]
                                    printed_x_max_re = printed_x_min_re + printed_instance_sec[2][-1][2]
                                    printed_y_max_re = printed_y_min_re + max([printed_instance_sec[2][-1][3]])
                                # ''' 세 번째 키워드가 없을 때입니다. '''
                                else:
                                    pass

                        # '''중복 문제를 해결합니다.'''
                        if x_min_re >= printed_x_min_re and x_min_re <= printed_x_max_re and y_min_re >= printed_y_min_re and y_min_re <= printed_y_max_re:
                            true_or_false_for_instance.append('false')
                            print('겹침 확인_재재조정: 겹쳤습니다-1번유형:','겹친키워드:', printed_instance_sec, '프린트된 놈의', 'xmin:',printed_x_min_re,'xmax:',printed_x_max_re, 'ymin:',printed_y_min_re,'ymax:',printed_y_max_re)
                            break
                        # '''오른쪽 위 꼭지점이 들어감'''
                        elif x_max_re >= printed_x_min_re and x_max_re <= printed_x_max_re and y_min_re >= printed_y_min_re and y_min_re <= printed_y_max_re:
                            true_or_false_for_instance.append('false')
                            print('겹침 확인_재재조정: 겹쳤습니다-2번유형:','겹친키워드:', printed_instance_sec)
                            break
                        # '''왼쪽 아래 꼭지점이 들어감'''
                        elif x_min_re >= printed_x_min_re and x_min_re <= printed_x_max_re and y_max_re >= printed_y_min_re and y_max_re <= printed_y_max_re:
                            true_or_false_for_instance.append('false')
                            print('겹침 확인_재재조정: 겹쳤습니다-3번유형:','겹친키워드:', printed_instance_sec)
                            break
                        # '''오른쪽 아래 꼭지점이 들어감'''
                        elif x_max_re >= printed_x_min_re and x_max_re <= printed_x_max_re and y_max_re >= printed_y_min_re and y_max_re <= printed_y_max_re:
                            true_or_false_for_instance.append('false')
                            print('겹침 확인_재재조정: 겹쳤습니다-4번유형:','겹친키워드:', printed_instance_sec)
                            break
                        elif x_min_re <= printed_x_min_re and x_max_re >= printed_x_max_re and y_max_re >= printed_y_min_re and y_max_re <= printed_y_max_re:
                            true_or_false_for_instance.append('false')
                            print('겹침 확인_재재조정: 겹쳤습니다-5번유형:','겹친키워드:', printed_instance_sec)
                            break
                        elif x_min_re <= printed_x_min_re and x_max_re >= printed_x_max_re and y_min_re >= printed_y_min_re and y_min_re <= printed_y_max_re:
                            true_or_false_for_instance.append('false')
                            print('겹침 확인_재재조정: 겹쳤습니다-6번유형:', '겹친키워드:', printed_instance_sec)
                            break
                        elif x_max_re >= printed_x_min_re and x_max_re <= printed_x_max_re and y_min_re <= printed_y_min_re and y_max_re >= printed_y_max_re:
                            true_or_false_for_instance.append('false')
                            print('겹침 확인_재재조정: 겹쳤습니다-7번유형:', '겹친키워드:', printed_instance_sec)
                            break
                        elif x_min_re >= printed_x_min_re and x_min_re <= printed_x_max_re and y_min_re <= printed_y_min_re and y_max_re >= printed_y_max_re:
                            true_or_false_for_instance.append('false')
                            print('겹침 확인_재재조정: 겹쳤습니다-8번유형:', '겹친키워드:', printed_instance_sec)
                            break
                        elif x_min_re <= printed_x_min_re and x_max_re >= printed_x_max_re and y_min_re <= printed_y_min_re and y_max_re >= printed_y_max_re:
                            true_or_false_for_instance.append('false')
                            print('겹침 확인_재재조정: 겹쳤습니다-9번유형:', '겹친키워드:', printed_instance_sec)
                            break
                        else:
                            true_or_false_for_instance = []

                    except:
                        pass
            add_to_print = self.re_re_instance

            print('재조정을 마쳤습니다')
        else:
            add_to_print = re_instance
            print('재조정을 마쳤습니다')

        return add_to_print







if __name__ == "__main__":
    # a = SettingBackground(bgdata_folder_path='C:\python\\1\making_img\\bg_data')
    # a.switch_OFF(bg_del_lst=[0])
    a = SettingBackground(bgdata_folder_path='C:\python\\1\making_img\\bg_data')

    b = KeywordCarrier(font_folder_path='C:\python\\1\making_img\\font', keyword_folder_path='C:\python\\1\making_img\keyword', original_image=a.set_bg()[0])
    b.num_key_nonkey()
    b.key_all_lst()
