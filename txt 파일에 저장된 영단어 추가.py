import pickle

def word_addition(English, Korean): 
	#단어장에 단어와 뜻을 추가합니다. 단어장이 없으면, 단어장을 만들어서 단어장을 넣어줍니다.
	try:
		Korean = Korean.split(', ')
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
	possible_answer_edit(English)

def possible_answer_edit(English):
	#단어 테스트를 진행할 때 가능한 정답들(answewrlist)을 wordlist와 비교하여 만들어 냅니다. 
	#기본적으로 문자열의 공백은 없애며, 영어가 포합된다면 소문자로 저장됩니다.
	try:
		with open('word.txt', 'rb') as f:
			wordlist = pickle.load(f)
		with open('answer.txt', 'rb') as g:
			answerlist = pickle.load(g)

		if English in answerlist:
			del answerlist[English]

		answerlist[English] = []

		for i in range(len(wordlist[English])):
			no_space_answer = wordlist[English][i].replace(" ", "") #공백만 없는 답
			no_space_answer = no_space_answer.lower()
			answerlist[English].append(no_space_answer)

			if '(' in no_space_answer:
				full_answer = no_space_answer.replace("(", "") #괄호만 제거한 전체 답
				full_answer = full_answer.replace(")", "")

				start = no_space_answer.find("(")
				end = no_space_answer.find(")")

				only_parentheses_answer = no_space_answer[start + 1 : end] #괄호 부분만 있는 답
				no_parentheses_answer = no_space_answer.replace("(" + only_parentheses_answer + ")", "") # 괄호 부분만 없는 답

				answerlist[English].append(full_answer)
				answerlist[English].append(only_parentheses_answer)
				answerlist[English].append(no_parentheses_answer)


		with open('word.txt', 'wb') as f:
			pickle.dump(wordlist, f)
		with open('answer.txt', 'wb') as g:
			pickle.dump(answerlist, g)

	except FileNotFoundError:

		print("단어장이 없습니다.")

#EBS VOCA 1800.txt에 저장된 영단어를 wordlist와 answerlist에 추가
with open('EBS VOCA 1800.txt', 'r', encoding="utf-8") as f:
    word = ''
    meaning = ''
    line = f.readlines()

    for i in range(len(line)):
        line[i] = line[i].strip()
        if len(line[i]) >= 1:
			#해당 줄에 단어가 입력되어 있으면
            if line[i].upper() != line[i].lower(): 
                #영단어인 경우 word로
                word = line[i]
            else: 
                #한국어 뜻인 경우 meaning으로
                if line[i].endswith(','): 
                    #한국어 뜻이 ','로 끝나는 경우(예외적인 상황)
                    meaning = line[i][0:line[i].find(',')]
                else: 
                    #한국어 뜻이 정상적으로 끝나는 경우
                    meaning = line[i]
        if word != '' and meaning != '':
            #영단어와 한국어 뜻이 매치되었다면 wordlist와 answerlist에 추가
            word_addition(word.strip(), meaning.strip())
            meaning = ''

print("\n끝!")