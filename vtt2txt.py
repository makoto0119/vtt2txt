import sys
import time
import os
import re

# vtt→txt 変換関数
def convert_vtt_to_text(filename):  
    with open(filename, 'r', encoding='utf-8') as file:  
        lines = file.readlines()  
      
    # 意味のない文字列のリスト
    useless_words = ["なんか", "うん", "あの", "なんだ", "まあ", "ちょっと", "なんて", "だから", "えっと", "ですね",
                     "そう", "なんです", "なんですよ", "なんですけど", "なんだろう", "なんかね", "なんかこう",
                     "なんかその", "なんかあの", "なんかこれ", "なんかそれ", "なんかなんだ", "なんかまあ",
                     "なんかちょっと", "なんかなんて", "なんかだから", "なんかえっと", "なんかですね",
                     "はい", "ああ","じゃあ","ええ","そうですね","そうそう","うーん" ]

    # 正規表現パターンの作成
    pattern = '|'.join(map(re.escape, useless_words))

    converted_lines = []  
    before_speaker = ''  
    current_speaker = ''  
    current_text = ''
    current_prefix = ''
    previous_prefix = ''
    index = 0  
    index2 = 0  
      
    for line in lines:  
        if '-->' in line:
            # 行の先頭4文字を取得 hh:mm なので、分が変わったら出力
            current_prefix = line[:5]
            # プレフィックスが変わったかどうかを確認
            if current_prefix != previous_prefix:
                converted_lines.append(current_prefix)
                previous_prefix = current_prefix  
            continue  # 時間行削除

        if '<v' not in line and  '</v>' not in line:  
            continue  # どちらも無いと内容ではない
          
        if line.startswith('<v'): # 先頭行
            index = line.find('>') 
            current_speaker = line[2:index].strip() # 最初の > は、話者名の文字列
            if current_speaker != before_speaker : # 直前の話者と異なる
                converted_lines.append(current_speaker)
                before_speaker = current_speaker
            index2 = line.find('</v>') 
            if index2 != -1:
                current_text = line[line.find('>')+1:-5].strip()
            else :
                current_text = line[line.find('>')+1:index2].strip() 
        else :   
            index = line.find('</v>')
            current_text += line[:index].strip() 
  
        if current_text != '':
            current_text = re.sub(pattern, '', current_text)  
            # 行頭の「、」や「。」を削除
            current_text = re.sub(r'^[、。]+', '', current_text.strip())
            if current_text != '': #改行だけの行はサプレス
                converted_lines.append(current_text.strip())
                current_text =''
      
    return '\n'.join(converted_lines)

# main
if(len(sys.argv) <= 1):  #起動時 引数が無い
    print(' ERR : ファイルをドロップして下さい')
    time.sleep(10)
    sys.exit()

extension = os.path.splitext(sys.argv[1])[1]
if(extension != '.vtt'):  #起動時 引数が vtt ファイルじゃない
    print(' ERR : .vtt ファイルをドロップして下さい')
    time.sleep(10)
    sys.exit()

with open(os.path.splitext(sys.argv[1])[0]+'.txt', 'w', encoding='utf-8') as file:
    file.writelines(convert_vtt_to_text(sys.argv[1]))

    print(' INFO: txt ファイルを生成しました')
    time.sleep(3)