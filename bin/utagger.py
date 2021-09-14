#-*- coding: utf-8 -*-
import sys
import os
from ctypes import *
from ctypes import cdll

#주의! 유태거 dll은 보통 64비트이기 때문에, 파이썬도 64비트를 사용해야 합니다.

dll_name = r'UTagger.so'
dll_path = os.getenv('UTAGGER_PATH') + dll_name
lib = cdll.LoadLibrary(dll_path)

def Init_Utagger():

    print("python call utagger function")

    hlx_name = r'Hlxcfg.txt'
    hlx_pass = os.getenv('HLX_PATH') + hlx_name
    cstr_hlx = c_char_p( hlx_pass.encode('cp949') )#hlxcfg 파일 경로를 cp949로 인코딩.

    lib.Global_init2.restype = c_wchar_p #유태거 초기화 함수의 반환자 정의
    msg = lib.Global_init2( cstr_hlx , 0) # Hlxcfg.txt 위치 지정. 학습 파일 로딩. 오래걸림.

    if msg != '': # Hlxcfg.txt와 모든 학습 파일을 읽었는지 확인.
        print("hlxcfg bug")
        print(msg)
        sys.exit(1)

    lib.newUCMA2.restype = c_wchar_p #ucma 생성 함수의 반환자 정의
    msg = lib.newUCMA2(0) # 유태거의 0번 객체 생성(0~99까지 생성 가능)
    if msg != '':
        print("newUCMA bug")
        print(msg)
        sys.exit(1)

    lib.cmaSetNewlineN(0) #유태거 tag_line이 newline을 만들 때 /r/n 이 아니라 /n이 되게 한다.
    #lib.cmaSetNewlineN(0) #유태거 tag_line이 newline을 만들 때 /n이 되게 한다.

    #dll의 태깅함수 정의. 사용하기 편하게.
    tag_line = lib.cma_tag_line_BSP #함수 가져오기
    tag_line.restype = c_wchar_p #반환자 설정.

    tag_line_json = lib.cma_tag_line_json2 #함수 가져오기
    tag_line_json.restype = c_wchar_p #반환자 설정.

    tag_depen = lib.cma_depen_json2
    tag_depen.restype = c_wchar_p

    #uwm api 함수 정의
    uwm1_api = lib.DLL_UWM_1
    uwm1_api.restype = c_wchar_p

    #대역어 함수 정의
    tw_api = lib.cma_tag_target_word_json2
    tw_api.restype = c_wchar_p

    arr = [tag_line, tag_line_json, tag_depen, uwm1_api, tw_api]
    
    return arr
   
arr = Init_Utagger()
tag_line = arr[0]
tag_line_json = arr[1]
tag_depen = arr[2]
uwm1_api = arr[3]
tw_api = arr[4]

print("로딩 성공") #여기까지 오면 유태거 사용가능.

if __name__ == "__main__":
    # 지역 변수 테스트
    #s = "유태거 안녕 나는 사과가 맛있더라."
    s="" #빈 문자열 테스트.
    rt = tag_line(0, c_wchar_p(s), 0)  #분석!
    print(rt)


    # 키보드로 직접 문장을 입력하여 유태거 테스트.

    s = ".."
    while(len(s)>1):
        s = input('input line = ')
        rt = tag_line(0, c_wchar_p(s), 3) #분석!
        print(rt)


    s = ".."
    while(len(s)>1):
        s = input('input line = ')
        rt = tag_line_json(0, c_wchar_p(s), 3) #분석!
        print(rt)
        #rt2 = tag_depen(0, c_wchar_p(rt) )
        #print(rt2)


    s = ".."
    while(len(s)>1):
        s = input('uwm api = ')
        rt = uwm1_api(0, c_wchar_p(s))
        print(rt)


    s = ".."
    while(len(s)>1):
        s = input('tw json input = ')
        rt = tw_api(0, c_wchar_p(s), 1, 0)
        print(rt)

    lib.deleteUCMA(0) # 0번 객체 삭제
    lib.Global_release() # 메모리 해제

    print("종료")
