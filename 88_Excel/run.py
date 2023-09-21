import pandas as pd
from tkinter import Tk, filedialog
import datetime

##############################
# 엑셀 파일 읽기 함수
##############################
def load_excel_file():
    # 파일 선택 대화상자 열기
    root = Tk()
    root.withdraw()  # tkinter 창 숨기기
    file_path = filedialog.askopenfilename(title="엑셀 파일 선택", filetypes=[("Excel Files", "*.xls;*.xlsx")])
    
    if not file_path:
        return None

    # pandas를 사용하여 엑셀 파일 읽기(최대 189행)
    df = pd.read_excel(file_path, usecols="A:D")
    return df


# 엑셀파일 읽기
input_data = load_excel_file()

if input_data is not None:
    print(input_data.head())  # 데이터프레임의 첫 5행 출력
else:
    print("파일이 선택되지 않았습니다.")
    exit(0)

# 사용할 컬럼 리스트 정의
columns = [
    "Cash", "Credit Card", "Debit Card", "EBT SNAP", "Tenders In Drawer Totals", 
    "All Voids", "Item Corrects", "No Sales", "Negative Totals", 
    "125 - CHUPA SODA_6PK", "Discount Totals", "LOTTERY WINNER", "LOYALTY", 
    "Paid Out Totals", "Returns", "SCRATCHER WINNER"
]

data_list = []

# 입력 데이터에서 유일한 이름 추출하기 
for name in input_data['NAME'].unique():
    # 현재 이름에 대한 행 필터링 
    name_data = input_data[input_data['NAME'] == name]
    
    # 현재 이름에 대한 데이터 보관을 위한 Dictionary 생성
    data_dict = {"Name": name}
    
    # 각 컬럼에 대한 데이터 추출
    for col in columns:
        data_dict[col] = name_data[name_data['DATA'] == col]['AMOUNT'].values[0] if col in name_data['DATA'].values else None
    
    # 데이터 리스트에 한 사람에 대한 딕셔너리 추가
    data_list.append(data_dict)

# 데이터프레임으로 변환
output_data = pd.DataFrame(data_list)

# NaN 값을 0으로 채우기
output_data.fillna(0, inplace=True) 

# 현재 날짜 가져오기
today = datetime.datetime.now().strftime('%Y%m%d')

# 결과 엑셀 파일 경로 설정 
output_filepath = f"result_{today}.xlsx"
output_data.to_excel(output_filepath, index=False)