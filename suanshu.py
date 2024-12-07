from flask import Flask, request, jsonify, render_template, session
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 请更换为您的秘密密钥以确保安全

# 生成算术题
def generate_questions(num_questions, num_count, num_range, result_range, operators):
    questions = []
    used_questions = set()  # 用于记录已生成的题目
    attempt = 0
    while len(questions) < num_questions and attempt < num_questions * 10:
        nums = [random.randint(1, num_range) for _ in range(num_count)]
        ops = [random.choice(operators) for _ in range(num_count - 1)]
        question = ""
        result = None
        try:
            for i in range(len(nums)):
                question += str(nums[i])
                if i < len(ops):
                    question += f" {ops[i]} "
            # 计算结果
            result = eval(question)
            # 确保结果在指定范围内且是整数
            if (result < result_range['min'] or 
                result > result_range['max'] or 
                not float(result).is_integer() or 
                question in used_questions):  # 检查是否重复
                attempt += 1
                continue
            
            questions.append({"question": question, "answer": int(result)})
            used_questions.add(question)  # 记录已生成的题目
            
        except (ZeroDivisionError, SyntaxError):
            attempt += 1
            continue
    return questions

# 生成详细解题思路
def generate_solution(question, answer):
    parts = question.split(' ')
    if len(parts) == 3:
        num1, op, num2 = parts
        num1 = int(num1)
        num2 = int(num2)
        
        if op == '*':
            if num2 <= 5:
                # 使用连加法和图形展示
                steps = [f"<div class='step'><strong>第一步：</strong>把 {num1} × {num2} 转化为连加</div>"]
                rows = []
                total_apples = []
                for i in range(num2):
                    apples = '🍎' * num1
                    rows.append(apples)
                    total_apples.extend(['🍎'] * num1)
                    steps.append(f"<div class='step'><strong>第{i+2}步：</strong>{apples} ({num1}个)</div>")
                
                steps.append(
                    f"<div class='step'><strong>最后：</strong>数一数一共有多少个<br>"
                    f"<div class='apples'>{''.join(total_apples)}</div>"
                    f"<strong>答案：</strong>{num1} × {num2} = {answer}</div>"
                )
                return "".join(steps)
            
            elif num1 <= 10 and num2 <= 10:
                # 使用乘法口诀
                solution = (
                    f"<div class='step'><strong>第一步：</strong>想一想乘法口诀：<br>"
                    f"{min(num1, num2)} × {max(num1, num2)} = {answer}</div>"
                    f"<div class='step'><strong>答案：</strong>{num1} × {num2} = {answer}</div>"
                )
                return solution
            
            else:
                # 使用分解法
                if num2 >= 10:
                    # 把大数拆成 10 和余数
                    remainder = num2 - 10
                    step1 = f"<div class='step'><strong>第一步：</strong>把{num2}拆成 10 + {remainder}</div>"
                    step2 = f"<div class='step'><strong>第二步：</strong>先算 {num1} × 10 = {num1 * 10}</div>"
                    step3 = f"<div class='step'><strong>第三步：</strong>再算 {num1} × {remainder} = {num1 * remainder}</div>"
                    step4 = f"<div class='step'><strong>第四步：</strong>最后把两个结果相加：{num1 * 10} + {num1 * remainder} = {answer}</div>"
                    return f"{step1}{step2}{step3}{step4}"
                else:
                    # 把较大的数拆成方便计算的部分
                    split = 5
                    step1 = f"<div class='step'><strong>第一步：</strong>把{num1}拆成 {split} + {num1 - split}</div>"
                    step2 = f"<div class='step'><strong>第二步：</strong>先算 {split} × {num2} = {split * num2}</div>"
                    step3 = f"<div class='step'><strong>第三步：</strong>再算 {num1 - split} × {num2} = {(num1 - split) * num2}</div>"
                    step4 = f"<div class='step'><strong>第四步：</strong>最后把两个结果相加：{split * num2} + {(num1 - split) * num2} = {answer}</div>"
                    return f"{step1}{step2}{step3}{step4}"

        elif op == '/':
            if num2 <= 5:
                # 使用连减法
                steps = [f"<div class='step'><strong>第一步：</strong>把{num1}分成若干组，每组{num2}个</div>"]
                remaining = num1
                count = 0
                while remaining >= num2:
                    count += 1
                    steps.append(f"<div class='step'><strong>第{count+1}步：</strong>{remaining} - {num2} = {remaining - num2}</div>")
                    remaining -= num2
                steps.append(f"<div class='step'><strong>答案：</strong>一共能分成 {answer} 组</div>")
                return "".join(steps)
            
            else:
                # 转化为乘法验证
                step1 = f"<div class='step'><strong>第一步：</strong>{num1} ÷ {num2} = {answer}</div>"
                step2 = f"<div class='step'><strong>第二步：</strong>验算：{num2} × {answer} = {num1}</div>"
                step3 = f"<div class='step'><strong>答案：</strong>{num1} ÷ {num2} = {answer}</div>"
                return f"{step1}{step2}{step3}"

        elif op == '+':
            if num1 + num2 <= 10:
                # 使用苹果图形直观展示
                apples1 = '🍎' * num1
                apples2 = '🍎' * num2
                solution = (
                    f"<div class='step'><strong>第一步：</strong>画出第一个数 {num1}<br>"
                    f"<div class='apples'>{apples1}</div></div>"
                    f"<div class='step'><strong>第二步：</strong>再画出第二个数 {num2}<br>"
                    f"<div class='apples'>{apples2}</div></div>"
                    f"<div class='step'><strong>第三步：</strong>数一数一共有多少个<br>"
                    f"<div class='apples'>{apples1}{apples2}</div>"
                    f"<strong>答案：</strong>{answer}个</div>"
                )
                return solution.strip()
            
            elif num2 <= 5:
                # 一步一步数数
                steps = [f"<div class='step'><strong>第一步：</strong>从{num1}开始，往后数{num2}个数</div>"]
                current = num1
                for i in range(num2):
                    steps.append(f"<div class='step'><strong>第{i+2}步：</strong>{current} + 1 = {current + 1}</div>")
                    current += 1
                steps.append(f"<div class='step'><strong>答案：</strong>{num1} + {num2} = {answer}</div>")
                return "".join(steps)
            
            else:
                # 选择更接近10的数来凑十
                dist1 = abs(10 - num1)
                dist2 = abs(10 - num2)
                
                if dist1 <= dist2:  # 如果第一个数更接近10
                    if num1 < 10:  # 需要凑到10
                        to_ten = 10 - num1
                        solution = (
                            f"<div class='step'><strong>第一步：</strong>先把{num1}凑成10<br>"
                            f"{num1} + {to_ten} = 10</div>"
                            f"<div class='step'><strong>第二步：</strong>还剩下 {num2 - to_ten} 要加<br>"
                            f"10 + {num2 - to_ten} = {answer}</div>"
                            f"<div class='step'><strong>答案：</strong>{num1} + {num2} = {answer}</div>"
                        )
                        return solution.strip()

        elif op == '-':
            if num1 <= 10 and num2 <= 10:
                # 使用图形直观展示
                apples_total = '🍎' * num1
                crossed = '❌' * num2
                remaining = '🍎' * (num1 - num2)
                solution = (
                    f"<div class='step'><strong>第��步：</strong>画出被减数 {num1}<br>"
                    f"<div class='apples'>{apples_total}</div></div>"
                    f"<div class='step'><strong>第二步：</strong>划掉 {num2} 个<br>"
                    f"<div class='apples'>{crossed}{remaining}</div></div>"
                    f"<div class='step'><strong>第三步：</strong>数一数还剩下多少个<br>"
                    f"<div class='apples'>{remaining}</div>"
                    f"<strong>答案：</strong>{answer}个</div>"
                )
                return solution.strip()
            
            elif num2 <= 5:
                # 一步一步往前数
                steps = [f"<div class='step'><strong>第一步：</strong>从{num1}开始，往前数{num2}个数</div>"]
                current = num1
                for i in range(num2):
                    steps.append(f"<div class='step'><strong>第{i+2}步：</strong>{current} - 1 = {current - 1}</div>")
                    current -= 1
                steps.append(f"<div class='step'><strong>答案：</strong>{num1} - {num2} = {answer}</div>")
                return "".join(steps)
            
            elif num2 >= 10:
                # 先减十再减剩余
                step1 = f"<div class='step'><strong>第一步：</strong>先减去10：{num1} - 10 = {num1 - 10}</div>"
                step2 = f"<div class='step'><strong>第二步：</strong>再减去{num2 - 10}：{num1 - 10} - {num2 - 10} = {answer}</div>"
                step3 = f"<div class='step'><strong>答案：</strong>{num1} - {num2} = {answer}</div>"
                return f"{step1}{step2}{step3}"
            
            else:
                # 使用分解法
                split = 5
                step1 = f"<div class='step'><strong>第一步：</strong>把{num2}拆成 {split} + {num2 - split}</div>"
                step2 = f"<div class='step'><strong>第二步：</strong>先减{split}：{num1} - {split} = {num1 - split}</div>"
                step3 = f"<div class='step'><strong>第三步：</strong>再减{num2 - split}：{num1 - split} - {num2 - split} = {answer}</div>"
                return f"{step1}{step2}{step3}"

    return "<div class='step'><strong>提示：</strong>这道题目暂时无法生成解题思路。</div>"

# 主页路由
@app.route('/')
def home():
    session['wrong_questions'] = []  # 初始化错题集
    return render_template('index.html')

# 生成题目接口
@app.route('/generate_questions', methods=['POST'])
def generate_questions_route():
    data = request.json
    num_questions = data.get('num_questions', 10)  # 获取题目数量
    num_count = data.get('num_count', 2)
    num_range = data.get('num_range', 10)
    result_range = data.get('result_range', {"min":0, "max":100})
    operators = data.get('operators', ['+', '-'])
    questions = generate_questions(num_questions, num_count, num_range, result_range, operators)
    # 添加解题思路
    for q in questions:
        q['solution'] = generate_solution(q['question'], q['answer'])
    return jsonify({"questions": questions})

# 提交答案接口
@app.route('/submit_answers', methods=['POST'])
def submit_answers_route():
    data = request.json
    submitted = data.get('submitted', [])
    correct = data.get('correct', [])
    questions = data.get('questions', [])
    
    results = []
    correct_count = 0
    wrong_questions = session.get('wrong_questions', [])
    
    for sub, cor, q in zip(submitted, correct, questions):
        # 添加日志输出
        print(f"Processing question: {q}, correct answer: {cor}")
        
        is_correct = sub == cor
        if is_correct:
            correct_count += 1
        else:
            # 添加错题到错题集
            existing = next((item for item in wrong_questions if item['question'] == q), None)
            if not existing:
                solution = generate_solution(q, cor)
                wrong_questions.append({
                    "question": q,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "correct_count": 0,
                    "solution": solution
                })
        
        solution = generate_solution(q, cor)  # 生成解题思路
        print(f"Generated solution: {solution}")
        
        results.append({
            "your_answer": sub,
            "correct_answer": cor,
            "is_correct": is_correct,
            "solution": solution
        })
    
    session['wrong_questions'] = wrong_questions
    total_questions = len(correct)
    if total_questions > 0:
        score = int((correct_count / total_questions) * 100)
        all_correct = correct_count == total_questions
    else:
        score = 0
        all_correct = False
    
    return jsonify({
        "results": results,
        "score": score,
        "all_correct": all_correct
    })

# 获取错题集接口
@app.route('/get_wrong_questions', methods=['GET'])
def get_wrong_questions():
    wrong_questions = session.get('wrong_questions', [])
    # 获取排序方式
    sort_order = request.args.get('sort_order', 'recent')  # 'recent' 或 'random'
    if sort_order == 'random':
        random.shuffle(wrong_questions)
    else:
        # 按时间从近到远排序
        sorted_wrong = sorted(wrong_questions, key=lambda x: x['timestamp'], reverse=True)
        wrong_questions = sorted_wrong
    return jsonify({"wrong_questions": wrong_questions})

if __name__ == '__main__':
    # 确保Flask应用绑定到所有可用IP地址，并使用固定端口
    app.run(host='0.0.0.0', port=5001, debug=True)
