# OpacityImage 개요 
## 이미지를 여러 개 올려놓고, 특정 레이어를 불투명하게 설정해서 이미지를 겹쳐 보이게 할 수 있는 쓸데없는 프로그램입니다.
## 저장은 무조건 png로만 돼요, 그냥 그렇게 했습니다. 


# 주요 기능
![image](https://github.com/user-attachments/assets/f0e48262-fdbb-4107-9741-971655dc0d71)
## 실행하면 보이는 화면에서 거의 절반을 차지하고 있는 흰색 Canvas는, 이미지들이 올려질 공간입니다. 
![image](https://github.com/user-attachments/assets/b3305eff-7967-4201-9096-a266a99de947)
## 아래의 Width와 Height를 조정하여 Canvas의 px크기 및 비율을 조정할 수 있습니다. 
### 한 가지 특별한 점은, Width와 Height를 5000 * 5000 으로 변경한 다음에, 
### 500 * 500의 이미지를 불러와도 그 이미지 또한 Canvas의 비율에 맞춰 5000 * 5000이 된다는 사실입니다. 
### 당연히 실제로 이미지를 저장할 때도 설정하신 Width와 Height px 크기로 저장됩니다. 

![image](https://github.com/user-attachments/assets/bb4fd930-07cd-473b-b52a-2bf5465724ff)
### 그리고 이 버튼들은... 
## Add Layer: 
### 사진을 추가합니다. 1 Image == 1 Layer라고 생각하시면 됩니다. 
### 가장 나중에 추가된 사진이 맨 위에 올려집니다. 
## Remove Layer: 
### Layers에서 선택한 Layer, 또는 방금 추가한 레이어를 삭제합니다. 
## Rename Layer: 
### Layers에서 선택한 Layer, 또는 방금 추가한 레이어의 이름을 수정합니다. 
## Save Composite: 
### 현재 Canvas에서 보이는 화면을 저장합니다. 
### 만약, 첫 번째 레이어까지 투명화되어있다면, 저장된 사진도 투명할 겁니다. 

![image](https://github.com/user-attachments/assets/d0ca1bb0-7bb4-43ac-aaab-bc2b745c34ba)
## 여기선 레이어를 선택할 수 있습니다. 
### 맨 위에 있는 애가 가장 아래에 있는 이미지고, 최대 10개까지 만들 수 있어요. 
### 10개 개수 제한이 불편하다면 소스코드 열어서 "self.layer_max_count"를 10에서 다른 수로 바꾸세요. 

![image](https://github.com/user-attachments/assets/62d7cde3-ab65-43eb-900b-a5b1c5e7449d)
## 이 스크롤바를 사용해서 불투명도를 조정할 수 있습니다. 


# 여담 
## 이 소스코드는 어... 그러니까 오픈소스입니다. 제가 이런 걸 처음 올려봐서 이렇게 말하는 게 맞을지는 모르겠는데. 
## 만약 소스코드를 변경해서 재배포하거나, 다른 곳에 이 프로그램을 공 하실 일이 있다면 여기 링크 하나만 남겨주십쇼... 
## 그 외에는 바라는 거 없습니다. 어차피 대부분은 챗지피티에게 시킨 사이드 프로젝트이기 때문에. 
## 파이썬 코드를 exe로 생성한 방법은 pyinstaller를 사용했습니다. 
## 감사합니다. 
