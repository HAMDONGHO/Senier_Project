#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 1: GiGA Genie Keyword Spotting"""
# kt api예제입니다. 호출어를 받아 테스트하는 코드

from __future__ import print_function

# 음성 데이터를 바꾸기 위한 audioop(마이크 입력시 사용됨)
import audioop
# 파이썬용 외부함수 라이브러리!, Error Handler를 위해 가져왔습니다.
from ctypes import *
# 파이썬으로 GPIO모듈을 제어하기 위함
import RPi.GPIO as GPIO
# kt gigagenie 호출어 인식 모듈
import ktkws # KWS
# 파이썬 마이크 입력 받는 오픈소스
import MicrophoneStream as MS
KWSID = ['기가지니', '지니야', '친구야', '자기야']
RATE = 16000
CHUNK = 512

# GPIO 세팅하기 위함
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# 29번 핀으로 풀업저항을 이용해서 스위치 사용
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# 31번 핀으로 LED출력을 위함(스위치)
GPIO.setup(31, GPIO.OUT)
# 기본적으로 버튼 상태를 false로 두었습니다.
btn_status = False

#정상적으로 핀의 In, Out을 통해 이벤트 발생을 하기 위함입니다.(btn_status조작으로)
def callback(channel):  
	print("falling edge detected from pin {}".format(channel))
	global btn_status
	# 버튼을 눌렀으므로, 상태를 truefh 바꾸고 출력해서 확인하게 했습니다.
	btn_status = True
	print(btn_status)

# 버튼을 눌러왔을때, 파이썬 인터럽트 처리 방식을 인용했습니다. 여기서 저희는 1에서 0으로 전이 됐을때인 Falling으로 설정했습니다.
GPIO.add_event_detect(29, GPIO.FALLING, callback=callback, bouncetime=10)

# 예외처리부분(기본코드)
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  dummy_var = 0
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)


def detect():
	with MS.MicrophoneStream(RATE, CHUNK) as stream:
		audio_generator = stream.generator()

		for content in audio_generator:
			# 음성 데이터에 호출어가 포함되어 있는지 확인하고, 포함되면 1 아니면 0이 rc에 저장
			rc = ktkws.detect(content)
			# 마이크를 통해 입력된 음성데이터의 음량을 숫자로 출력(주석처리해서 pring안됨, 지워도 무방할듯)
			rms = audioop.rms(content,2)
			#print('audio rms = %d' % (rms))
			
			#호출어가 인식되 rc가 1이면 소리 출력하고 200을 반환
			if (rc == 1):
				MS.play_file("../data/sample_sound.wav")
				return 200

# 버튼이 눌렸을 때 처리해주는 부분입니다.
def btn_detect():
	global btn_status
	# 마이크 사용을 위한 클래스를 이용해 음성데이터를 RATE, CHUNK를 어떻게 해서 가져올지 정하고
	# 변수에 음성데이터를 generator()함수를 이용해 전달했습니다.
	with MS.MicrophoneStream(RATE, CHUNK) as stream:
		audio_generator = stream.generator()
		# content에 가져온 음성 데이터를 할당하고
		for content in audio_generator:
			# LED를 점등시킵니다.
			GPIO.output(31, GPIO.HIGH)
			rc = ktkws.detect(content)
			rms = audioop.rms(content,2)
			#print('audio rms = %d' % (rms))
			GPIO.output(31, GPIO.LOW)
			#버튼 상태에 따라서 rc값을 반환
			if (btn_status == True):
				rc = 1
				btn_status = False			
			if (rc == 1):
				# 버튼이 눌리면 led가 점등됨
				GPIO.output(31, GPIO.HIGH)
				# 눌러을때 음성파일을 가져왔습니다.
				MS.play_file("../data/sample_sound.wav")
				return 200

def test(key_word = '기가지니'):
	rc = ktkws.init("../data/kwsmodel.pack")
	print ('init rc = %d' % (rc))
	rc = ktkws.start()
	print ('start rc = %d' % (rc))
	print ('\n호출어를 불러보세요~\n')
	ktkws.set_keyword(KWSID.index(key_word))
	rc = detect()
	print ('detect rc = %d' % (rc))
	print ('\n\n호출어가 정상적으로 인식되었습니다.\n\n')
	ktkws.stop()
	return rc

# 버튼을 인식하고 진행을 확인하기 위한 함수를 정의했습니다.
def btn_test(key_word = '기가지니'):
	global btn_status
	# kt api를 가져와 rc값의 시작을 가져오고 화면에 출력했습니다.
	rc = ktkws.init("../data/kwsmodel.pack")
	print ('init rc = %d' % (rc))
	# kt api의 시작을 불러와 시작하게 하고,
	rc = ktkws.start()
	print ('start rc = %d' % (rc))
	print ('\n버튼을 눌러보세요~\n')
	# 받아온 변수 값을 4개의 호출어 중 어떤것을 이용할지 정함
	ktkws.set_keyword(KWSID.index(key_word))
	rc = btn_detect()
	print ('detect rc = %d' % (rc))
	print ('\n\n호출어가 정상적으로 인식되었습니다.\n\n')
	ktkws.stop()
	return rc

def main():
	test()

if __name__ == '__main__':
	main()
