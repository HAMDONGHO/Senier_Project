#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 2: STT - getVoice2Text """

from __future__ import print_function
import grpc
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import MicrophoneStream as MS
import user_auth as UA
import audioop
import os
import time
import case1 as kws
import threadingTest as thread
from ctypes import *

HOST = 'gate.gigagenie.ai'
PORT = 4080
RATE = 16000
CHUNK = 512

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  dummy_var = 0
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

def generate_request():
    # with as 구문으로 음성을 열고 응답을 stream객체로 받아 처리하는 부분
    with MS.MicrophoneStream(RATE, CHUNK) as stream:
        # audid_generater으로 제너레이터를 사용해 stream객체를 할당
        audio_generator = stream.generator()
    
        for content in audio_generator:
            message = gigagenieRPC_pb2.reqVoice()
            message.audioContent = content
            # message에 기가지니 api의 텍스트변환 메소드를 지정하고 audioContent에
            #stream객체를 받아와서 제너레이터로 메시지를 얻음
            yield message
            
            rms = audioop.rms(content,2)
            #print_rms(rms)

#KT 기가지니 서버로부터 받은 text변환된 음성을 처리하는 기능 정의
def getVoice2Text():	
    print ("\n주문하실 메뉴를 말씀해주세요\n")
    channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
    #기가지니 채널 접속
    stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)
    #채널에 request 전달
    request = generate_request()
    resultText = ''
    #음성이 들어오는 실시간 상태에서는 200 값으로 출력 후, 최종 음성판단한 text에서 201 return.
    #kt api 가이드에 보면 200은 시작부터 진행중, 201은 종료
    for response in stub.getVoice2Text(request):
        if response.resultCd == 200: # partial
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

    #최종 인식 결과 print
    print ("\n\n인식결과 : %s " % (resultText))
    return resultText

def main():
    # STT
    KWSID = ['기가지니', '정호야', '동호야', '사장님']
    print ("\n안녕하세요!! BesTwo에 오신 것을 환영합니다!!! \n\n")
    #주문 내역을 확인할 수 있는 text파일 open
    file = open('/home/pi/bestwo/python3/Text/texttttt.txt', 'w')
    #주문을 받을 수 있는 main thread 외에 카메라 녹화를 위한 thread 시작
    thread.CameraOn()
    while(1):
        #주문 내역을 작성할 수 있도록 수정가능 상태로 text file open
        file = open('/home/pi/bestwo/python3/Text/texttttt.txt', 'a')
        #주문시 butten 클릭하면 음성인식 시작, 서버로 음성 송신, Voice2Text로 변환
        recog = kws.btn_test(KWSID[0])
        #변환 성공시 200 return
        if recog == 200:
            #text 변환된 voice를 변수에 저장
            text = getVoice2Text()
            #text 내용 파일에 작성
            file.write(time.strftime('table number:1 %2H:%2M:%2S [%4Y-%2m-%2d] -- ', time.localtime(time.time())) + text + '\n')
        #파일 close
        file.close()
        #주문 알림을 위한 부저 알림 및 LED 점멸 
        kws.BuzzerOn()
        
        

if __name__ == '__main__':
    main()
