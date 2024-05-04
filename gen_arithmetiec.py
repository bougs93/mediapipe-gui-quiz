'''
gen()

'''
import random, math

class GenerateArithmetic():
    def __init__(self):
        # 총 레벨 갯수 1 ~ 15 레벨
        self.levels = [i+1 for i in range(15)]  # [1 ~ 15]

    # 문제, 정답 = create(1)
    def create(self, level):

        if level == 1:  # 0, 연산자 1개
            operand_min = 1; operand_max = 10
            operators = ['+','-','*']
            num_operators = 1
            operandsCho = [random.randint(operand_min, operand_max) for _ in range(num_operators + 1)]  # 숫자 선택
            operatorsCho = [random.choice(operators) for _ in range(num_operators)]  # 연산자 선택
            problem =''
            for i in range(num_operators):
                problem = problem + str(f'{operandsCho[i]}') + f'{operatorsCho[i]}'
            problem = problem + str(operandsCho[i+1])
            problem = problem.lstrip()  # 왼쪽 글자 삭제
            answer = eval(problem)
            return problem, answer
        
        elif level == 2: # 00, 연산자 1개
            operand_min = 11; operand_max = 100
            operators = ['+','-']
            num_operators = 1
            operandsCho = [random.randint(operand_min, operand_max) for _ in range(num_operators + 1)]  # 숫자 선택
            operatorsCho = [random.choice(operators) for _ in range(num_operators)]  # 연산자 선택
            problem =''
            for i in range(num_operators):
                problem = problem + str(f'{operandsCho[i]}') + f'{operatorsCho[i]}'
            problem = problem + str(operandsCho[i+1])
            problem = problem.lstrip()
            answer = eval(problem)
            return problem, answer

        elif level == 3:  # 0, 연산자 2개
            operand_min = 2; operand_max = 10
            operators = ['+','-','*']
            num_operators = 2
            operandsCho = [random.randint(operand_min, operand_max) for _ in range(num_operators + 1)]  # 숫자 선택
            operatorsCho = [random.choice(operators) for _ in range(num_operators)]  # 연산자 선택
            problem =''
            for i in range(num_operators):
                problem = problem + str(f'{operandsCho[i]}') + f'{operatorsCho[i]}'
            problem = problem + str(operandsCho[i+1])
            problem = problem.lstrip()  # 왼쪽 글자 삭제
            answer = eval(problem)
            return problem, answer

        elif level == 4: # 곱셈 00*0, 연산자 1개
            operators = ['*']
            num_operators = 1
            operandsCho = [random.randint(10, 100), random.randint(2, 9)]  # 숫자 선택
            operatorsCho = [random.choice(operators) for _ in range(num_operators)]  # 연산자 선택
            problem =''
            for i in range(num_operators):
                problem = problem + str(f'{operandsCho[i]}') + f'{operatorsCho[i]}'
            problem = problem + str(operandsCho[i+1])
            problem = problem.lstrip()  # 왼쪽 글자 삭제
            answer = eval(problem)
            return problem, answer

        elif level == 5 : # 나누기
            answer = random.randint(2, 10)
            divisor = random.randint(2, 10)
            dividend = answer * divisor
            problem = f"{dividend}÷{divisor}"
            return problem, answer

        elif level == 6: # 000, 연산자 1개
            operand_min = 11; operand_max = 1000
            operators = ['+','-']
            num_operators = 1
            operandsCho = [random.randint(operand_min, operand_max) for _ in range(num_operators + 1)]  # 숫자 선택
            operatorsCho = [random.choice(operators) for _ in range(num_operators)]  # 연산자 선택
            problem =''
            for i in range(num_operators):
                problem = problem + str(f'{operandsCho[i]}') + f'{operatorsCho[i]}'
            problem = problem + str(operandsCho[i+1])
            problem = problem.lstrip()
            answer = eval(problem)
            return problem, answer

        elif level == 7 : # 나누기
            answer = random.randint(2, 10)
            divisor = random.randint(11, 100)
            dividend = answer * divisor
            problem = f"{dividend}÷{divisor}"
            return problem, answer

        elif level == 8 : # 2제곱 + 1연산자, 0숫자
            square1Up = 2
            square1Dn = random.randint(2, 9)
            square1 = f'{square1Dn}**({square1Up})'

            operand_min = 1; operand_max = 10
            operators = ['+','-']
            num_operators = 1
            operandsCho = [random.randint(operand_min, operand_max), square1 ]  # 숫자 선택
            random.shuffle(operandsCho) # 순서 섞기
            operatorsCho = [random.choice(operators) for _ in range(num_operators)]  # 연산자 선택

            problem =''
            for i in range(num_operators):
                problem = problem + str(f'{operandsCho[i]}') + f'{operatorsCho[i]}'
            problem = problem + str(operandsCho[i+1])
            problem = problem.lstrip()
            answer = eval(problem)
            return problem, answer

        elif level == 9 : # 2제곱 + 1연산자, 00숫자
            square1Up = 2
            square1Dn = random.randint(2, 9)
            square1 = f'{square1Dn}**({square1Up})'

            operand_min = 11; operand_max = 100
            operators = ['+','-']
            num_operators = 1
            operandsCho = [random.randint(operand_min, operand_max), square1 ]  # 숫자 선택
            random.shuffle(operandsCho) # 순서 섞기
            operatorsCho = [random.choice(operators) for _ in range(num_operators)]  # 연산자 선택

            problem =''
            for i in range(num_operators):
                problem = problem + str(f'{operandsCho[i]}') + f'{operatorsCho[i]}'
            problem = problem + str(operandsCho[i+1])
            problem = problem.lstrip()
            answer = eval(problem)
            return problem, answer

        #################################################################################
        elif level == 10 : # 2제곱 + 2연산자, 0숫자
            square1Up = 2
            square1Dn = random.randint(2, 9)
            square1 = f'{square1Dn}**({square1Up})'

            operand_min = 1; operand_max = 10
            operators = ['+','-']
            num_operators = 2
            operandsCho = [random.randint(operand_min, operand_max) for _ in range(num_operators)]
            operandsCho.append(square1)  # 숫자 선택
            random.shuffle(operandsCho) # 순서 섞기
            operatorsCho = [random.choice(operators) for _ in range(num_operators)]  # 연산자 선택

            problem =''
            for i in range(num_operators):
                problem = problem + str(f'{operandsCho[i]}') + f'{operatorsCho[i]}'
            problem = problem + f'{str(operandsCho[i+1])}'
            problem = problem.lstrip()
            answer = eval(problem)
            return problem, answer

        elif level == 11 : # 2제곱 + 2연산자, 00숫자
            square1Up = 2
            square1Dn = random.randint(2, 9)
            square1 = f'{square1Dn}**({square1Up})'

            operand_min = 10; operand_max = 100
            operators = ['+','-']
            num_operators = 2
            operandsCho = [random.randint(operand_min, operand_max) for _ in range(num_operators)]
            operandsCho.append(square1)  # 숫자 선택
            random.shuffle(operandsCho) # 순서 섞기
            operatorsCho = [random.choice(operators) for _ in range(num_operators)]  # 연산자 선택

            problem =''
            for i in range(num_operators):
                problem = problem + str(f'{operandsCho[i]}') + f'{operatorsCho[i]}'
            problem = problem + str(f'{operandsCho[i+1]}')
            problem = problem.lstrip()
            answer = eval(problem)
            return problem, answer

        #################################################################################
        elif level == 12 : # 제곱근 + 1연산자
            sqrtCho = random.choice([4, 9, 16, 25, 36, 49, 64, 81]) # 정수 값을 갖는 제곱근
            sqrt = f'math.sqrt({sqrtCho})'

            operand_min = 1; operand_max = 10
            operators = ['+','-',]
            num_operators = 1
            operandsCho = [random.randint(operand_min, operand_max) for _ in range(num_operators) ]  # 숫자 선택
            operandsCho.append(sqrt)  # 숫자 선택
            random.shuffle(operandsCho) # 순서 섞기
            operatorsCho = [random.choice(operators) for _ in range(num_operators)]  # 연산자 선택

            problem =''
            for i in range(num_operators):
                problem = problem + str(f'{operandsCho[i]}') + f'{operatorsCho[i]}'
            problem = problem + f'{str(operandsCho[i+1])}'
            problem = problem.lstrip()
            answer = int(eval(problem))
            problem = problem.replace('math.sqrt(','√(')

            return problem, answer
            # pyqt square root LaTeX
            # https://stackoverflow.com/questions/32035251/displaying-latex-in-pyqt-pyside-qtablewidget

        elif level == 13 : # 제곱근 + 1연산자
            sqrtCho = random.choice([4, 9, 16, 25, 36, 49, 64, 81, 100]) # 정수 값을 갖는 제곱근
            sqrt = f'math.sqrt({sqrtCho})'

            operand_min = 11; operand_max = 100
            operators = ['+','-']
            num_operators = 1
            operandsCho = [random.randint(operand_min, operand_max) for _ in range(num_operators) ]  # 숫자 선택
            operandsCho.append(sqrt)  # 숫자 선택
            random.shuffle(operandsCho) # 순서 섞기
            operatorsCho = [random.choice(operators) for _ in range(num_operators)]  # 연산자 선택

            problem =''
            for i in range(num_operators):
                problem = problem + str(f'{operandsCho[i]}') + f'{operatorsCho[i]}'
            problem = problem + f'{str(operandsCho[i+1])}'
            problem = problem.lstrip()
            answer = int(eval(problem))
            problem = problem.replace('math.sqrt(','√(')

            return problem, answer

        elif level == 14 : # 2제곱 + 2연산자
            sqrtCho = random.choice([4, 9, 16, 25, 36, 49, 64, 81, 100]) # 정수 값을 갖는 제곱근
            sqrt = f'math.sqrt({sqrtCho})'

            operand_min = 11; operand_max = 100
            operators = ['+','-']
            num_operators = 2
            operandsCho = [random.randint(operand_min, operand_max) for _ in range(num_operators)]
            operandsCho.append(sqrt)  # 숫자 선택
            random.shuffle(operandsCho) # 순서 섞기
            operatorsCho = [random.choice(operators) for _ in range(num_operators)]  # 연산자 선택

            problem =''
            for i in range(num_operators):
                problem = problem + str(f'{operandsCho[i]}') + f'{operatorsCho[i]}'
            problem = problem + str(f'{operandsCho[i+1]}')
            problem = problem.lstrip()
            answer = int(eval(problem))
            problem = problem.replace('math.sqrt(','√(')

            return problem, answer

        #################################################################################
        elif level == 15 : # 2제곱 + 제곱근 , 2연산자
            square1Up = 2
            square1Dn = random.randint(2, 9)
            square1 = f'{square1Dn}**({square1Up})'

            sqrtCho = random.choice([4, 9, 16, 25, 36, 49, 64, 81, 100]) # 정수 값을 갖는 제곱근
            sqrt = f'math.sqrt({sqrtCho})'

            operand_min = 11; operand_max = 100
            operators = ['+','-']
            num_operators = 2
            operandsCho = [random.randint(operand_min, operand_max)]
            operandsCho.append(square1)
            operandsCho.append(sqrt)

            random.shuffle(operandsCho) # 순서 섞기
            operatorsCho = [random.choice(operators) for _ in range(num_operators)]  # 연산자 선택

            problem =''
            for i in range(num_operators):
                problem = problem + str(f'{operandsCho[i]}') + f'{operatorsCho[i]}'
            problem = problem + str(f'{operandsCho[i+1]}')
            problem = problem.lstrip()
            answer = int(eval(problem))
            problem = problem.replace('math.sqrt(','√(')

            return problem, answer

    # 유사한 오답을 생성 : 10이하 난수/ 11 이상은 뒷자리 동일, 같은 자릿수 숫자 생성
    def wrong(self, answer):
        # 정답 숫자의 부호 판별
        is_negative = True if answer < 0 else False
        # 정답 숫자의 뒷자리 숫자 추출
        last_digit = abs(answer) % 10   
        # 정답 숫자의 자릿수를 판별
        num_digits = len(str(abs(answer)))  # 부호를 제외한 자릿수

        while True:
            if abs(answer) > 10:
                #---------------------------------------------------------
                # 동일한 자릿수를 가지는 랜덤한 숫자 생성
                wrong_number1 = random.randint(10**(num_digits-1), (10**num_digits)-1)
                # wrong_number = random.randint(-(10**num_digits), (10**num_digits)-1)

                # 생성된 숫자의 뒷자리 숫자를 정답의 뒷자리 숫자와 동일하게 조정
                wrong_number1 = (wrong_number1 // 10) * 10 + last_digit

                # 오답에 부호를 적용
                wrong_number1 *= -1 if is_negative else 1
                #---------------------------------------------------------
                operation = random.choice(['+', '-'])
                num = random.randint(1, 9) * 10

                # 덧셈 또는 뺄셈 수행
                if operation == '+':
                    wrong_number2 = answer + num
                else:
                    wrong_number2 = answer - num

            else:
                wrong_number1 = random.randint(0, 10)
                wrong_number2 = random.randint(0, 10)
                if answer < 0:
                    wrong_number1 = -wrong_number1
                    wrong_number2 = -wrong_number2

            # 생성된 숫자가 정답과 다르다면 반환
            if (wrong_number1 != answer) and (wrong_number2 != answer)\
                  and (wrong_number1 != wrong_number2) :
                break

        return wrong_number1, wrong_number2


    # # 유사한 오답을 생성 : 10이하 난수/ 11 이상은 뒷자리 동일, 같은 자릿수 숫자 생성
    # def wrong(self, answer):
    #     # 정답 숫자의 부호 판별
    #     is_negative = True if answer < 0 else False
    #     # 정답 숫자의 뒷자리 숫자 추출
    #     last_digit = abs(answer) % 10   
    #     # 정답 숫자의 자릿수를 판별
    #     num_digits = len(str(abs(answer)))  # 부호를 제외한 자릿수

    #     while True:
    #         if abs(answer) > 10:
    #             # 동일한 자릿수를 가지는 랜덤한 숫자 생성
    #             wrong_number = random.randint(10**(num_digits-1), (10**num_digits)-1)
    #             # wrong_number = random.randint(-(10**num_digits), (10**num_digits)-1)

    #             # 생성된 숫자의 뒷자리 숫자를 정답의 뒷자리 숫자와 동일하게 조정
    #             wrong_number = (wrong_number // 10) * 10 + last_digit

    #             # 오답에 부호를 적용
    #             wrong_number *= -1 if is_negative else 1

    #         else:
    #             wrong_number = random.randint(0, 10)
    #             if answer < 0:
    #                 wrong_number = -wrong_number

    #         # 생성된 숫자가 정답과 다르다면 반환
    #         if wrong_number != answer and wrong_number !=0 :
    #             break

    #     return wrong_number


#######################################################################
'''
랜덤한 숫자 생성: 문제의 정답과 다른 임의의 숫자를 생성하여 오답으로 사용합니다.
 예를 들어, 정답이 10이라면 1부터 9 사이에서 랜덤하게 숫자를 선택하여 오답으로 사용할 수 있습니다.

연산자 오답: 문제의 연산자를 변경하여 오답을 생성합니다.
 예를 들어, 정답이 덧셈이라면 오답으로 뺄셈, 곱셈, 나눗셈 등의 연산자를 사용할 수 있습니다.

부호 변경: 문제의 숫자에 대해 부호를 변경하여 오답을 생성합니다.
 예를 들어, 정답이 5라면 오답으로 -5, +5 등을 사용할 수 있습니다.

계산 오류: 문제의 숫자 또는 연산을 잘못 계산하여 오답을 생성합니다. 
예를 들어, 정답이 8이라면 오답으로 7 또는 9를 계산할 수 있습니다.
'''
if __name__=="__main__":
    generateArithmetic = GenerateArithmetic()
    
    # idx = 0
    # for  i in range(1, 60):
    #     n = (i-1) % 3
    #     if n == 0:
    #         idx += 1
    #     print(n, idx)

    # for level in range(1,16):
    #     problem, ans = generateArithmetic.create(level)
    #     # print( pro, ans)
    #     wrong = generateArithmetic.wrong(ans)
    #     print(f'level {level} : {problem} = {ans} , 오답: {wrong}' )


    # print(eval(" - 12/4"))
    problem, ans = generateArithmetic.create(15)
    print(problem)

    f1 = problem.find("√(")
    if f1 != -1:
        # 인덱스 이후 첫 번째 문자만 교체
        idx = problem.find("√(")
        # problem = problem[:idx] + "√<span style='text-decoration: overline'>" + problem[idx+2:]
        problem = problem[:idx] + "√<span>" + problem[idx+2:]
        idx = problem.find(")", idx)
        problem = problem[:idx] + "</span>" + problem[idx+1:]
        
    f2 = problem.find("**(")
    if f2 != -1:
        # 인덱스 이후 첫 번째 문자만 교체
        idx = problem.find("**(")
        problem = problem[:idx] + "<sup>" + problem[idx+3:]
        idx = problem.find(")", idx)
        problem = problem[:idx] + "</sup>" + problem[idx+1:]

    print(problem)
