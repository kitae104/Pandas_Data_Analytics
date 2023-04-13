import csv

with open('result.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['이름', '키(cm)', '몸무게(kg)', 'BMI', '비만여부', '정상체중까지 필요한 무게(kg)'])

    while True:
        name = input("이름을 입력하세요(그만 입력하려면 '그만'을 입력하세요): ")
        if name == "그만":
            break
        height = float(input("키를 입력하세요(cm): "))
        weight = float(input("몸무게를 입력하세요(kg): "))

        bmi = weight / ((height/100)**2)
        if bmi < 20:
            obesity = "저체중"
        elif bmi < 25:
            obesity = "정상"
        elif bmi < 30:
            obesity = "과체중"
        else:
            obesity = "비만"
            need_weight = (bmi - 24) * ((height/100)**2)

        writer.writerow([name, height, weight, bmi, obesity, need_weight if obesity == "비만" else ""])
