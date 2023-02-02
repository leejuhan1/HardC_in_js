import requests
import re            # 정규표현식 사용을 위함
import argparse      # cmd 매개 변수 사용을 위함
import sys           # cmd 매개변수에도 사용하지만 오류 알아보려고 사용
import urllib.parse  # 검사할 url 도메인 확인을 위함

print('################ js 파일 하드코딩 문자열 검사 Start ##############')

################### 인자값을 받을 수 있는 인스턴스 생성 #######################
parser = argparse.ArgumentParser(description='js 파일 하드코딩 문자열 검사기입니다.')

# 입력받을 인자값 등록
parser.add_argument('--url', required=True, help='검사할 url 입력')  # required은 필수로 넣어야하는 파라미터로 설정하는 옵션
parser.add_argument('--word', required=False, default="password", nargs='*',help='하드코딩 단어 검색')  # nargs='*'은 다중 파라미터 쓰게 해주는 옵션

# 입력받은 인자값을 args에 저장 (type: namespace) 
args = parser.parse_args()



################### 입력 파일 받아오기 #######################
page = str(requests.get(args.url).content)

#.js 파일 필터링 정규표현식
js_match_src=re.compile('src=[ㄱ-ㅎ가-핳a-zA-Z0-9./:"\-_~@#!$%^&*()\+=\?<>]+\.js')  # src=로 시작하고 .js로 끝

# 정규표현식 적용 
result = js_match_src.findall(page)

# 검사 url 도메인
parsed_url = urllib.parse.urlparse(args.url)
target_doamin = parsed_url.scheme+"://"+parsed_url.netloc



################### 접근할 js 파일 url 생성 #######################
real_url = []
for i in result:
    url = i[5:]                         # src=" 문자열 삭제
    if re.match('^http',url):    
        real_url.append(url)  
    else:
        real_url.append(target_doamin+url)   



################### 파일 생성 #######################
js_cnt=0
with open('hardC_in_js.txt', 'w') as f:
    f.write('################ js 파일 하드코딩 문자열 검사기 ##############\n\n')
    f.write('URL : '+str(args.url)+"\n")
    f.write("검사할 문자열 : "+str(args.word)+"\n")
    f.write("js 파일 갯수 : "+str(len(real_url))+"\n\n")
    f.write(">> .js 목록\n")
    for i in real_url:
        js_cnt = js_cnt+1
        f.write(str(js_cnt)+". "+i+"\n")
    f.write("\n")



################### .js 파일에 하드코딩 존재 유무 #######################
print(" ")

for k in args.word:
    hardC = []
    for i in real_url:
        try:
            jspage = str(requests.get(i).content)
            if re.search(k,jspage):
                hardC.append(i+" = "+str(jspage.count(k))+"개 존재!\n")
        except:
            print(i+" = 연결안됨 : "+str(sys.exc_info()[0]))

    ###### 파일에 기록 ######
    with open('hardC_in_js.txt', 'a') as f:
        f.write('\n##### '+k+" : "+str(len(hardC))+'개 #####\n')
        for i in hardC:
            f.write(i)


print('################ js 파일 하드코딩 문자열 검사 End ##############')
