#한글 파일에 표로 정리된 수능특강 단어의 텍스트만 복사하고 텍스트 파일로 저장하기
import win32com.client as win32
import pyperclip

hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
hwp.RegisterModule('FilePathCheckDLL', 'SecurityModule') #보안승인모듈 설정
hwp.Open(r'C:\EBS VOCA 1800.hwp',"HWP","forceopen:true")

hwp.Run("SelectAll") #전체 선택
hwp.Run("Copy") #복사
hwp.Run("Erase") #지우기
hwp.Run("PasteSpecial") #골라 붙이기
hwp.Run("Cancel") #esc

# #수정된 파일을 저장하고 나갑니다. 
# hwp.Save()
# hwp.Quit()

pasted = pyperclip.paste()

with open('EBS VOCA 1800.txt', 'w', encoding="utf-8") as f:
    f.write(pasted)
