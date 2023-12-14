from typing import List
import numpy as np
from PIL import Image,ImageDraw, ImageFont


def result(
    avg_evoked_list: List, times_list: List,image_folder: str, screen_width: int, screen_height: int, channels: List,result_dir:str
):
    #P300구하기
    #print("avg_evoked_list 시험 출력 ")
    #print(avg_evoked_list)
    #print("\n")
    max_values_per_channels = []
    for channel_idx in range(len(channels)):
        max_values = []
        for time in range(len(times_list)):
            selected_indices = [
                index
                for index, value in enumerate(times_list[time])
                if 0.1 <= value <= 0.5
            ]
            start_index = selected_indices[0]
            end_index = selected_indices[-1]

            max_value = max(
                avg_evoked_list[time][channel_idx][start_index : end_index + 1]
            )
            max_values.append(max_value)
        max_values_per_channels.append(max_values)
    print("avg_evoked_list의 각 채널별 시작-끝 사이에서의 max값 결과에 따른 max value값 ") ## 체크용
    print(max_values_per_channels) ##체크용
    print("\n")## 체크용
        
        
    '''
    ***************************
    방법1(평균) -> 짝수번 해도 가능
    ***************************
    '''   
    
    #채널별 mbti값 평균 저장
    '''
    채널1(좌뇌): E p300평균값, I p300평균값,...
    채널2(우뇌) : E p300평균값, I p300평균값,...)'''
    
    for channel in range(len(max_values_per_channels)):
        #index 순서: E,I,N,S,T,F,P,J
        mean_per_channels=np.array([[0 for i in range(8)],[0 for i in range(8)]])
        for i in range(len(max_values_per_channels[channel])):
            mean_per_channels[channel][i%8]+=max_values_per_channels[channel][i]
            
    #평균 계산
    mean_per_channels= mean_per_channels/(len(max_values_per_channels[channel])//8)
    
    mbti_alphabet = ["E", "I", "N", "S", "T", "F", "P", "J"]
    #좌뇌/우뇌의 mbti
    #두 번 돎(채널 두개)
    for channel in range(len(max_values_per_channels)):
        mbti = []#채널 돌 때마다 초기화
        #4번 돎- 0,2,4,6
        for i in range(0,len(mean_per_channels[channel]),2):
            #설마 같은 값은 안나오겠지?
            if  mean_per_channels[channel][i]> mean_per_channels[channel][i+1]: 
                mbti.append(mbti_alphabet[i])
                percent= (mean_per_channels[channel][i]/(mean_per_channels[channel][i]+mean_per_channels[channel][i+1]))*100
                print(i,"비율:",percent)
            else:
                mbti.append(mbti_alphabet[i+1])
                percent= (mean_per_channels[channel][i+1]/(mean_per_channels[channel][i]+mean_per_channels[channel][i+1]))*100
                print(i+1,"비율:",percent)
                
        if channel==0:
            print("좌뇌의 mbti는",mbti,"입니다.")
        else:
            print("우뇌의 mbti는",mbti,"입니다.")
    
    
    #전체 mbti(평균)
    total_mean= [(i+j)/2 for i,j in zip(mean_per_channels[0],mean_per_channels[1])]
    mbti=[]#다시 빈 리스트로 초기화
    for i in range(0,len(total_mean), 2):
        #설마 같은 값은 안나오겠지?
        if  total_mean[i]> total_mean[i+1]: 
            mbti.append(mbti_alphabet[i])
            percent= (total_mean[i]/(total_mean[i]+total_mean[i+1]))*100
            print(i,"비율:",percent)
        else:
            mbti.append(mbti_alphabet[i+1])
            percent= (total_mean[i+1]/(total_mean[i]+total_mean[i+1]))*100
            print(i+1,"비율:",percent)
    text="당신의 mbti는",mbti,"입니다."
    print(text)
    
    '''
    ********************************
    방법2 -개수 count(짝수..반반이면?)
    ********************************
    '''   
    """#채널 2개 봄
    for channel in range(len(max_values_per_channels)):
        #count index 순서 : E,I,N,S,T,F,P,J
        count_per_types=[[0 for i in range(8)],[0 for i in range(8)]]
        print(count_per_types)#체크용코드
        #0부터 40까지 2씩 증가
        for i in range(0,len(max_values_per_channels[channel]),2):
            #비교해서 더 큰 mbti 유형에 count 1씩 증가
            if max_values_per_channels[channel][i] > max_values_per_channels[channel][i+1]:
                count_per_types[channel][i%8]+=1
            else:
                count_per_types[channel][(i+1)%8]+=1
            
    
    #좌뇌/우뇌의 mbti
    #두 번 돎(채널 두개)
    mbti_alphabet = ["E", "I", "N", "S", "T", "F", "P", "J"]
    for channel in range(len(max_values_per_channels)):
        mbti = []#채널 돌 때마다 초기화
        #4번 돎
        for i in range(len(count_per_types[channel])//2):
            #같은 값이면?? -> 아무거나 보여주고 비율로 알아서 생각해라? or 둘 다 보여주기..?
            if  count_per_types[channel][i]> count_per_types[channel][i+1]: 
                print(count_per_types[channel][i]) #체크용 코드
                print(count_per_types[channel][i+1]) #체크용 코드
                mbti.append(mbti_alphabet[i])
                percent= (count_per_types[channel][i]/(count_per_types[channel][i]+count_per_types[channel][i+1]))*100
                print(i,"비율:",percent)
            else:
                print(count_per_types[channel][i]) #체크용 코드
                print(count_per_types[channel][i+1]) #체크용 코드
                mbti.append(mbti_alphabet[i+1])
                percent= (count_per_types[channel][i+1]/(count_per_types[channel][i]+count_per_types[channel][i+1]))*100
                print(i+1,"비율:",percent)
                
        if channel==0:
            print("좌뇌의 mbti는",mbti,"입니다.")
        else:
            print("우뇌의 mbti는",mbti,"입니다.")
    
    
    #전체 mbti(평균)
    total_count_per_types= [i+j for i,j in zip(count_per_types[0],count_per_types[1])]
    mbti=[]#다시 빈 리스트로 초기화
    for i in range(len(total_count_per_types)//2):
        #같은 값이면?
        if  total_count_per_types[i]> total_count_per_types[i+1]: 
            mbti.append(mbti_alphabet[i])
            percent= (total_count_per_types[i]/(total_count_per_types[i]+total_count_per_types[i+1]))*100
            print(i,"비율:",percent)
        else:
            mbti.append(mbti_alphabet[i+1])
            percent= (total_count_per_types[i+1]/(total_count_per_types[i]+total_count_per_types[i+1]))*100
            print(i+1,"비율:",percent)
    text="당신의 mbti는",mbti,"입니다."
    print(text)"""
    #################################################################################################################
    
    #화면에 띄우기
    mbti_str = ''.join(mbti)
    mbti_types = ["ENFP", "ENFJ", "ENTP", "ENTJ","ESFP","ESFJ","ESTP","ESTJ","INFP", "INFJ", "INTP", "INTJ","ISFP","ISFJ","ISTP","ISTJ"]
    for mbti_type in mbti_types:
        if mbti_str == mbti_type:
            image = Image.open(f"{image_folder}/results/{mbti_type}.png")
            image = image.resize((screen_width, screen_height))
            draw = ImageDraw.Draw(image)
            font_size = 50
            font = ImageFont.truetype("C:/Windows/Fonts/batang.ttc", font_size)
            
            # 텍스트 너비와 높이를 구하고 이미지 중앙 상단에 위치시키기
            #text_width, text_height = draw.textsize(text, font=font)
            text_bbox = draw.textbbox((0, 0), str(text), font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            text_x = (image.width - text_width) // 2
            text_y = 10  # 상단과 적당한 간격 두기
            
            # 텍스트 그리기 (black)
            draw.text((text_x, text_y), str(text), font=font, fill="black")
            
            # 변경된 이미지 저장
            image.save(f"{result_dir}/answer.png")
            image.show(f"{result_dir}/answer.png")
    
   



 