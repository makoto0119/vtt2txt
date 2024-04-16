import sys
import time

# vtt→txt 変換関数
def convert_vtt_to_text(filename):  
    with open(filename, 'r', encoding='utf-8') as file:  
        lines = file.readlines()  
      
    converted_lines = []  
    before_speaker = ''  
    current_speaker = ''  
    current_text = ''  
      
    for line in lines:  
        if '-->' in line:  
            continue  
          
        if line.startswith('<v'):
            current_speaker = line[2:line.find('>')].strip()
            if current_speaker != before_speaker :
                converted_lines.append(current_speaker)  
                before_speaker = current_speaker 

            current_text = line[line.find('>')+1:-5].strip()  
            if current_text != '':  
                converted_lines.append(current_text.strip())  
                current_text = ''  
        else:  
            current_text += line.strip()  
      
    if current_text != '':  
        converted_lines.append(current_text.strip())  
      
    return '\n'.join(converted_lines)

# main  
if(len(sys.argv) <= 1):  #起動時 引数が無い
    print(' ERR : .vtt ファイルをドロップして下さい')
    time.sleep(10)
    sys.exit()

with open('out.txt', 'w', encoding='utf-8') as file:
    file.writelines(convert_vtt_to_text(sys.argv[1]))

    print(' INFO: out.txt ファイルを生成しました')
    time.sleep(3)