#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 2: STT - getVoice2Text """

from __future__ import print_function

# kt 서버와 통신하기 위함입니다.
import grpc
# kt 서버에 제공하는 함수들과 목록, 요청 및 응답 형식이 저장되어 있느 모듈
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
# 마이크 조작 모듈
import MicrophoneStream as MS
# 사용자 인증(서비스 키)
import user_auth as UA
# 오디오 조작 모듈
import audioop
# 운영체제에서 제공하는 여러 기능을 파이썬에서 사용할 수 있게(텍스트 저장을 위함)
import os
import time
import ex1_kwstest as kws
# 예외처리 위한 파이썬 용 외부 함수 라이브러리 모듈
from ctypes import *

# kt서버에 접속할 호스트, 포트, RATE, CHUNK값 지정
HOST = 'gate.gigagenie.ai'
PORT = 4080
RATE = 16000
CHUNK = 512

# 예외처리
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  dummy_var = 0
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

# 마이크에 입력된 음성 데이터 처리 함수
def generate_request():
    with MS.MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
    
        for content in audio_generator:
            # 입련된 음성을 message에 저장하여 변환
            message = gigagenieRPC_pb2.reqVoice()
            # message의 audioContent에 generator로 받아오 content를 할당
            message.audioContent = content
            yield message
            
            rms = audioop.rms(content,2)
            #print_rms(rms)

# 음성데이터를 텍스트로 변환하기 위한 함수
def getVoice2Text():	
    print ("\n\n음성인식을 시작합니다.\n\n종료하시려면 Ctrl+\ 키를 누루세요.\n\n\n")
    # kt 서버 사이 데이터를 주고 받을 수 있는  통로 설정, HOST와 PORT와 사용자 인증키도 사용
    channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
    # kt 서버가 제공해주는 서비스들을 내부 함수를 호출하듯이 사용하게 만듦
    stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)
    # 마이크로 입력된 음성 데이터(message)를 저장
    request = generate_request()
    resultText = ''
    # kt 서버로 보내서 음성인식 결과를 받아옵니다.
    for response in stub.getVoice2Text(request):
        # resultCd는 상태코드이고, 200은 음성인식 일부 완성 201은 완성입니다.
        if response.resultCd == 200: # partial
            # recongizedText는 인식된 문장을 담는 kt 서버 변수입니다.
            print('resultCd=%d | recognizedText= %s' 
                  % (response.resultCd, response.recognizedText))
            resultText = response.recognizedText
        elif response.resultCd == 201: # final
            print('resultCd=%d | recognizedText= %s' 
                  % (response.resultCd, response.recognizedText))
            resultText = response.recognizedText
            break
        else:
            print('resultCd=%d | recognizedText= %s' 
                  % (response.resultCd, response.recognizedText))
            break
        #결과적으로 resultText를 반환해줍니다.
    print ("\n\n인식결과: %s \n\n\n" % (resultText))
    return resultText

def main():
    # 내부 file의 txt파일을 불러옵니다.
    file = open('/home/pi/ai-makers-kit/python3/Text/texttttt.txt', 'w')
    while(1):
        # 무한루프를 통해서 열고 닫으며 주문사항과 시간 날짜를 받습니다.
        file = open('/home/pi/ai-makers-kit/python3/Text/texttttt.txt', 'a')
        KWSID = ['기가지니', '지니야', '친구야', '자기야']
        recog = kws.btn_test(KWSID[3])
        if recog == 200:
            text = getVoice2Text()
            file.write(text + ' ' + time.strftime('table number : 1 - %H:%M:%S - %Y-%m-%d', time.localtime(time.time())) + '\n')
        file.close()
        


if __name__ == '__main__':
    main()
