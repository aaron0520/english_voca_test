# [추가해야할 기능] 
# 단어 Test 여러 가지 mode 추가
# 예문 추가 & 삭제
# EBS VOCA 1800는 기본적으로 + 일반 단어는 1800번째 단어 이후에

from bs4 import BeautifulSoup as bs
import requests
import random
import pickle

def word_addition(English, Korean, from_home): 
	#단어장에 단어와 뜻을 추가합니다. 단어장이 없으면, 단어장을 만들어서 단어장을 넣어줍니다.
	if from_home:
		# '4.검색'을 통해 사전에 있는 단어를 추가하는 상황이 아니라 HOME에서 '1.추가'를 통해 온 경우, 영단어와 한국어 뜻을 따로 입력하게끔 합니다.
		while True: #영단어 추가
			English = input("단어 : ")
			if English == '':
				print("단어가 입력되지 않았습니다. 다시 입력해주세요.\n")
				continue

			while True: #한국어 뜻 추가
				Korean = input("뜻 : ")
				if Korean == '':
					print("뜻이 입력되지 않았습니다. 다시 입력해주세요.\n")
					continue
				break

			break

	try:
		Korean = Korean.split(', ') #한국어 뜻을 ', '를 기준으로 나눕니다.

		with open('word.txt', 'rb') as f:
			wordlist = pickle.load(f)
		with open('word.txt', 'wb') as f:
			if English in wordlist:
				#A가 이미 단어장에 있으면, 해당 key의 val 리스트에 의미 B를 append합니다.
				for i in range(len(Korean)):
					if Korean[i] not in wordlist[English]:
						wordlist[English].append(Korean[i])
						print("- \"%s\" 의미가 추가되었습니다." % Korean[i])

					else:
						print("- \"%s\" 의미가 이미 등록되어 있습니다." % Korean[i])
			else:
				#A가 단어장에 없었으면, dict에 새로운 key-val 쌍을 만듭니다.
				wordlist[English] = Korean
				for i in range(len(Korean)):
					print("- \"%s\" 의미가 추가되었습니다." % Korean[i])
			pickle.dump(wordlist,f)

	except:
		with open('word.txt','wb') as f:
			pickle.dump({English:Korean},f)

	possible_answer_edit(English) #단어장이 변경되었으므로 테스트 답도 수정합니다.

def possible_answer_edit(English):
	#단어 테스트를 진행할 때 가능한 정답들(answewrlist)을 wordlist와 비교하여 만들어 냅니다. 
	#기본적으로 문자열의 공백은 없애며, 영어가 포합된다면 소문자로 저장됩니다.
	try:
		with open('word.txt', 'rb') as f:
			wordlist = pickle.load(f)
		with open('answer.txt', 'rb') as g:
			answerlist = pickle.load(g)

		if English in answerlist:
			#answerlist 초기화
			del answerlist[English]

		answerlist[English] = []

		for i in range(len(wordlist[English])):
			no_space_answer = wordlist[English][i].replace(" ", "") #공백만 없는 답
			no_space_answer = wordlist[English][i].replace("ㅤ", "") #한글채움문자(U+3164)도 제외
			no_space_answer = no_space_answer.lower() #소문자로 저장
			answerlist[English].append(no_space_answer)

			if '(' in no_space_answer:
				full_answer = no_space_answer.replace("(", "") #괄호만 제거한 전체 답
				full_answer = full_answer.replace(")", "")

				start = no_space_answer.find("(")
				end = no_space_answer.find(")")

				only_parentheses_answer = no_space_answer[start + 1 : end] #괄호 안쪽 부분만 있는 답
				no_parentheses_answer = no_space_answer.replace("(" + only_parentheses_answer + ")", "") # 괄호 바깥쪽 부분만 있는 답

				answerlist[English].append(full_answer)
				answerlist[English].append(only_parentheses_answer)
				answerlist[English].append(no_parentheses_answer)


		with open('word.txt', 'wb') as f:
			pickle.dump(wordlist, f)
		with open('answer.txt', 'wb') as g:
			pickle.dump(answerlist, g)

	except FileNotFoundError:
		print("단어장에 단어가 없습니다.")
	except EOFError:
		print("단어장에 단어가 없습니다.")

def wordbook():
	#단어장을 보여줍니다. 저장해 놓은 단어가 없으면, "단어장에 단어가 없습니다." 메시지가 나옵니다.
	try:
		with open('word.txt', 'rb') as f:
			wordlist = pickle.load(f)

			if len(wordlist) == 0:
				#단어장에 단어가 없다면
				print("단어장에 단어가 없습니다.")

			else:
				#단어장에 단어가 하나라도 있다면
				listed_wordlist_keys = list(wordlist.keys())

				while True:
					day = input("Day 몇의 단어를 공부할지 입력해주세요 : ")

					if day.isdigit():
						#day에 정수를 입력하였다면
						day = int(day)

						if 0 < day <= (len(wordlist) - 1) // 30 + 1:
							if 0 < day <= (len(wordlist) - 1) // 30:
								#day를 제대로 입력하였다면
								end_index = day * 30
							elif day == (len(wordlist) - 1) // 30 + 1:
								#단어장에 있는 마지막 Day를 입력하였다면
								end_index = len(wordlist)
							
							print("")
							for i in range((day - 1) * 30, end_index):
								#영어 단어와, 대응되는 한국어 뜻을 출력합니다.
								print("%s - " % listed_wordlist_keys[i], end = '')
								for j in range(len(wordlist[listed_wordlist_keys[i]])): 
									print("%d.%s " % (j + 1, wordlist[listed_wordlist_keys[i]][j]), end = '')
								print("")
							break

						else:
							#day에 다른 정수를 입력하였다면
							if (len(wordlist) // 30 + 1) == 1:
								print("현재 단어장의 Day는 1뿐입니다. 바르게 입력되었는지 확인해주세요.\n")
							elif (len(wordlist) // 30 + 1) > 1:
								print("현재 단어장의 Day 범위는 1 ~ %d입니다. 바르게 입력되었는지 확인해주세요.\n" % ((len(wordlist) - 1) // 30 + 1))

					else:
						#day에 정수를 입력하지 않았다면
						print("바르게 입력되었는지 확인해주세요.\n")

	except FileNotFoundError:
		print("단어장에 단어가 없습니다.")
	except EOFError:
		print("단어장에 단어가 없습니다.")
		
def word_test_settings():
	#HOME에서 '3.테스트'를 선택했을 때 테스트 사전 작업을 수행합니다.
	try:
		with open('word.txt', 'rb') as f:
			wordlist = pickle.load(f)

		global day

		is_re_test = False
		word = []
		while_loop_break = False

		while True:
			if while_loop_break: break
			day = input("Day 몇의 단어를 테스트 할지 입력해주세요 : ")

			if day.isdigit():
				#day에 정수를 입력하였다면
				day = int(day)

				if 0 < day <= len(wordlist) // 30 + 1:
					if 0 < day <= len(wordlist) // 30:
						#day를 제대로 입력하였다면
						start_index = (day - 1) * 30
						end_index = day * 30
					elif day == len(wordlist) // 30 + 1:
						#단어장에 있는 마지막 Day를 입력하였다면
						start_index = (day - 1) * 30
						end_index = len(wordlist)

					for k in range(start_index, end_index):
						#단어 keys를 word라는 리스트에 append
						word.append(list(wordlist.keys())[k])

					word_test(word, is_re_test) #단어 테스트 함수
					while_loop_break = True

				else:
					#day에 다른 정수를 입력하였다면
					if (len(wordlist) // 30 + 1) == 1:
						print("현재 단어장의 Day는 1뿐입니다. 바르게 입력되었는지 확인해주세요.\n")
					elif (len(wordlist) // 30 + 1) > 1:
						print("현재 단어장의 Day 범위는 1 ~ %d입니다. 바르게 입력되었는지 확인해주세요.\n" % (len(wordlist) // 30 + 1))

			else:
				#day에 정수를 입력하지 않았다면
				print("바르게 입력되었는지 확인해주세요.\n")

	except FileNotFoundError:
		print("단어장에 단어가 없습니다.")
	except EOFError:
		print("단어장에 단어가 없습니다.")

def word_test(word, is_re_test): 
	#입력한 Day에 있는 단어를 테스트 합니다.
	
	global wrong_answer_dic
	global number_of_tested_words
	wrong_answer_dic = {}
	number_of_tested_words = 1

	random.shuffle(word) #단어 섞기

	with open('word.txt', 'rb') as f:
		wordlist = pickle.load(f)
	with open('answer.txt', 'rb') as g:
		answerlist = pickle.load(g)

	print("(참고 : 'q'를 입력하면 테스트를 종료합니다.)\n")

	for key in word:
		answer = input("%d.%s: " % (word.index(key) + 1, key))
		if answer == 'q' or answer == 'Q': 
			#'q' 또는 'Q'를 입력하면, 테스트를 종료합니다.
			break
		answer = answer.split(', ')
		for j in range(len(answer)):
			#입력에서 공백은 제외하고, 소문자로 변환하여 answerlist와 비교합니다. 
			no_space_answer = answer[j].replace(" ", "")
			no_space_answer = no_space_answer.lower()
			if no_space_answer not in answerlist[key]: 
				print("틀렸습니다.")
				wrong_answer_dic[key] = wordlist[key] #오답노트에 저장
				break
		else:
			print("정답입니다!")
		number_of_tested_words += 1 #테스트한 단어 개수 += 1

	#정답 개수를 표시합니다.
	if is_re_test:
		print("\n[Day %d(재시험) 채점 결과]: %d개 / %d개" % (day, number_of_tested_words - 1 - len(wrong_answer_dic), number_of_tested_words - 1)) 
	else:
		print("\n[Day %d 채점 결과]: %d개 / %d개" % (day, number_of_tested_words - 1 - len(wrong_answer_dic), number_of_tested_words - 1))

	if wrong_answer_dic != {}: 
		# 오답이 있으면, 오답만 출력합니다.
		print("[오답 확인]:")
		for key, val in wrong_answer_dic.items():
			print("%s - " % key, end = '')
			for i in range(len(val)):
				print("%d.%s " % (i + 1, val[i]), end = '')
			print("")

		print("")
		
		while True:
			#오답노트의 단어로 재시험을 치를지 묻습니다.
			wrong_answer_test = input("틀린 단어로 다시 테스트 하시겠습니까? (y/n) : ")
			if(wrong_answer_test == 'y' or wrong_answer_test == 'Y'):
				is_re_test = True
				word_test(list(wrong_answer_dic.keys()), is_re_test) #오답 재시험
				break
			elif(wrong_answer_test == 'n' or wrong_answer_test == 'N'):
				break
			else:
				print("바르게 입력되었는지 확인해주세요.\n")


	# [원래 ver.]: Day 분류 X, 단어 테스트 개수를 입력하는 방식
	# else:
	# 	more_test_answered = False
	# 	while_loop_break = False
	# 	while True:
	# 		if while_loop_break: break
	# 		test_number = input("몇 개의 단어를 테스트 할지 입력해주세요 : ")
	# 		if test_number.isdigit() and 0 < int(test_number) <= len(wordlist):
	# 			#단어장의 단어 개수보다 작거나 같은 자연수를 입력하면, 단어 테스트를 시행합니다.
	# 			print("(참고 : 'q'를 입력하면 테스트를 종료합니다.)")
	# 			test_number = int(test_number)
	# 			word = list(wordlist.keys())
	# 			random.shuffle(word)
	# 			for key in word:
	# 				if while_loop_break: break
	# 				answer = input("%d.%s: " % (word.index(key) + 1, key))
	# 				if answer == 'q' or answer == 'Q': 
	# 					#'q' 또는 'Q'를 입력하면, 테스트를 종료합니다.
	# 					while_loop_break = True
	# 					break
	# 				answer = answer.split(', ')
	# 				for j in range(len(answer)):
	# 					no_space_answer = answer[j].replace(" ", "")
	# 					no_space_answer = no_space_answer.lower()
	# 					if no_space_answer not in answerlist[key]: 
	# 						print("틀렸습니다.")
	# 						wrong_answer_dic[key] = wordlist[key]
	# 						break
	# 				else:
	# 					print("정답입니다!")
	# 				i += 1
					
	# 				if i > test_number and i - 1 == len(wordlist):
	# 					#테스트 개수와 단어장의 단어 개수가 같다면, 테스트를 마칩니다.
	# 					while_loop_break = True
	# 				elif i > test_number and test_number < len(wordlist) and more_test_answered == False: 
	# 					#초기 지정된 테스트를 마치고 단어가 남아있다면, 테스트를 이어서 더 할지 물어봅니다.
	# 					while True:
	# 						a = input("\n아직 단어가 남아있습니다. 이어서 테스트 하시겠습니까? (y/n) : ")
	# 						if(a == 'y' or a == 'Y'):
	# 							more_test_answered = True
	# 							while_loop_break = False
	# 							break
	# 						elif(a == 'n' or a == 'N'):
	# 							more_test_answered = True
	# 							while_loop_break = True
	# 							break
	# 						else:
	# 							print("바르게 입력되었는지 확인해주세요.\n")

	# 		elif test_number.isdigit() and 0 < int(test_number) > len(wordlist):
	# 			#단어장의 단어 개수보다 큰 자연수를 입력하면, 더 작은 수를 입력하라고 합니다.
	# 			print("단어장에 있는 단어는 총 %d개입니다. 더 작은 수를 입력해주세요.\n" % len(wordlist))

	# 		else: 
	# 			print("바르게 입력되었는지 확인해주세요.\n")
		
def crawling(search): 
	#daum 포털사이트 단어사전을 크롤링해서 뜻과 예문을 출력해줍니다. 추가 기능도 있습니다.
	try:
		dic_url = 'https://dic.daum.net/search.do?q='
		src_url = dic_url + search + '&dic=eng&search_first=Y'
		res = requests.get(src_url)
		html = res.text
		
		soup = bs(html, 'html.parser')
		
		searched_word = soup.select('.search_cleanword > .tit_cleansch > .txt_cleansch > .txt_emph1')

		meanings = soup.select('.cleanword_type.kuek_type > ul > li')

		if len(meanings) == 0:
			print("Daum 영어사전에 등록되지 않았습니다.")
			return

		print("\n검색된 단어: %s" % searched_word[0].text)

		#의미를 출력합니다.
		for meaning in meanings:
			print(meaning.text)

		exm = soup.select('.card_word > .cont_example > ul > li > .box_example.box_sound > .txt_example > .txt_ex')
		
		exm_mean = soup.select('.card_word > .cont_example > ul > li > .box_example.box_sound > .mean_example > .txt_ex')
		
		#예문을 출력합니다.
		print('\n예문')
		print(exm[0].text)
		print(exm_mean[0].text+'\n')

		while True:
			#단어장에 추가할지 묻습니다.
			add = input("단어장에 추가하시겠습니까? (y/n): ")
			if(add == 'y' or add == 'Y'): 
				for i in range(len(meanings)):
					if len(meanings) == 1: 
						#한국어 뜻이 하나일 때
						word_addition(searched_word[0].text, meanings[i].text[0:].lstrip(), False)
					else: 
						#한국어 뜻이 여러 개일 때
						word_addition(searched_word[0].text, meanings[i].text[2:].lstrip(), False)
				break
			elif(add == 'n' or add == 'N'):
				print("- 추가되지 않았습니다.")
				break
			else:
				print("바르게 입력되었는지 확인해주세요.\n")

	except:
		print("인터넷이 연결되어 있는지 확인해주세요.")
		
def word_search(): 
	#단어장 혹은 영어사전에서 단어 검색을 합니다.
	while True:
		print("")
		print("[검색]")
		print("-----------------------------------------------")
		print("1.단어장 검색   2.영어사전 검색".center(35, ' '))
		print("-----------------------------------------------")
		search_option = input("번호를 선택하세요 : ")

		if search_option == '1':
			#단어장 검색
			try:
				with open('word.txt', 'rb') as f:
					wordlist = pickle.load(f)

				if len(wordlist) == 0:
					print("단어장에 단어가 없습니다.")
				else:
					search = input("\n검색 : ").strip()
					listed_wordlist_keys = list(wordlist.keys())
					print("Day %d" % (listed_wordlist_keys.index(search) // 30 + 1)) #Day 몇에 있는 단어인지 출력

					for i in range(len(wordlist[search])): #한국어 뜻 출력
						print("%d.%s " % (i + 1, wordlist[search][i]))

			except ValueError:
				print("%s는 단어장에 없습니다." % search)
			except FileNotFoundError:
				print("단어장에 단어가 없습니다.")
			except EOFError:
				print("단어장에 단어가 없습니다.")

		elif search_option == '2':
			#영어사전 검색: search 변수에 단어를 입력받아서 crawling 함수로 전달합니다.
			search = input("\n검색 : ")
			crawling(search)

		else:
			print("바르게 입력되었는지 확인해주세요.")

def word_remove():
	#단어를 입력하여 해당 단어를 단어장에서 삭제합니다.
	try:
		with open('word.txt', 'rb') as f:
			wordlist = pickle.load(f)
		with open('answer.txt', 'rb') as g:
			answerlist = pickle.load(g)
		if len(wordlist) == 0:
			print("단어장에 단어가 없습니다.")
			return

		while True:
			meaning_to_be_removed = [0] * 1000
			print("")
			print("[삭제]")
			print("-----------------------------------------------")
			print("1.단어 자체  2.단어 의미  3.초기화".center(35, ' '))
			print("-----------------------------------------------")
			remove_option = input("번호를 선택하세요 : ")

			if remove_option == '1': 
				#'1'를 입력했다면, 단어 자체를 삭제합니다.

				if len(wordlist) == 0:
					#단어장에 단어가 없을 때
					print("단어장에 단어가 없습니다.")
					return

				English = input("\n삭제할 단어 : ") #삭제할 단어 입력
				English = English.split(', ')
				for key in English:
					if key in wordlist:
						del wordlist[key]
						print("- \"%s\" 삭제되었습니다." % key)
					else:
						print("- \"%s\"는 단어장에 없습니다." % key)

			elif remove_option == '2': 
				#'2'을 입력했다면, 단어의 특정 의미를 삭제합니다.
				option_out_of_range = False
				English = input("\n삭제할 영단어 : ") #삭제할 단어 입력
				if English in wordlist:
					for i in range(len(wordlist[English])):
						#삭제하려는 단어에 저장된 의미 목록을 보여줍니다.
						print("%d.%s" % (i + 1, wordlist[English][i]))
					print("")

					int_remove_option = list(map(int, input("삭제하려는 의미의 번호를 입력하세요 : ").split(", ")))

					for i in range(len(int_remove_option)):
						#입력한 번호에 해당하는 의미가 있는지 확인합니다.
						if 1 <= int_remove_option[i] <= len(wordlist[English]):
							meaning_to_be_removed[i] = wordlist[English][int_remove_option[i] - 1]
						else:
							print("바르게 입력되었는지 확인해주세요.")
							option_out_of_range = True
							break

					for i in range(len(int_remove_option)):
						#입력한 번호의 의미를 삭제합니다.
						if option_out_of_range: break
						wordlist[English].remove(meaning_to_be_removed[i])
						print("- \"%s\" 의미가 삭제되었습니다." % meaning_to_be_removed[i])

					if len(wordlist[English]) == 0:
						#더 이상 영단어에 한국어 뜻이 남아있지 않다면 wordlist에서 삭제합니다.
						del wordlist[English]

					possible_answer_edit(English) #단어장이 변경되었으므로 테스트 답도 수정합니다.
					
				else:
					print("\"%s\"는 단어장에 없습니다." % English)

			elif remove_option == '3': 
				#'3'를 입력했다면, 초기화합니다.
				word_initiate() #단어장을 초기화하는 함수

			else: 
				#다르게 입력했다면, 다시 입력합니다.
				print("바르게 입력되었는지 확인해주세요.")

			if remove_option != '3':
				#초기화했으면 word_inititate 함수에서 저장이 이미 되었으니까 다시 wordlist를 dump하지 않습니다.
				with open('word.txt', 'wb') as f:
					pickle.dump(wordlist, f)
				with open('answer.txt', 'wb') as g:
					pickle.dump(answerlist, g)

	except FileNotFoundError:
		print("단어장에 단어가 없습니다.")
	except EOFError:
		print("단어장에 단어가 없습니다.")

def word_initiate():
	#단어장을 초기화합니다.
	try:
		with open('word.txt', 'rb') as f:
			wordlist = pickle.load(f)
		with open('answer.txt', 'rb') as g:
			answerlist = pickle.load(g)

			if len(wordlist) == 0:
				print("단어장에 단어가 없습니다.")

			else:
				while True:
					really = input("정말 단어장을 초기화하시겠습니까? (y/n) : ")

					if(really == 'y' or really == 'Y'): #초기화
						wordlist.clear()
						answerlist.clear()
						print("- 초기화되었습니다.")
						break

					elif(really == 'n' or really == 'N'): #초기화X
						print("- 초기화되지 않았습니다.")
						break

					else:
						print("바르게 입력되었는지 확인해주세요.\n")

		with open('word.txt', 'wb') as f:
			pickle.dump(wordlist, f)
		with open('answer.txt', 'wb') as g:
			pickle.dump(answerlist, g)

	except FileNotFoundError:
		print("단어장에 단어가 없습니다.")
	except EOFError:
		print("단어장에 단어가 없습니다.")

#main
while True:
	try:
		print("")
		print("[HOME] *Tip: \"Ctrl + C\" 입력하면 HOME으로!*")
		print("===============================================")
		print("  1.추가  2.단어장  3.테스트  4.검색  5.삭제 ")
		print("===============================================")

		n = int(input("번호를 선택하세요 : "))

		if(n == 1): word_addition('', '', True)
		elif(n == 2): wordbook()
		elif(n == 3): word_test_settings()
		elif(n == 4): word_search()
		elif(n == 5): word_remove()
		else:
			print("바르게 입력되었는지 확인하세요.")
			
	except ValueError:
		print("바르게 입력되었는지 확인해주세요.")
	except KeyboardInterrupt:
		print("")
	