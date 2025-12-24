from sql_connect.sqllite_connect import create_session
from learning_english.learning_system import LearningSystem

ls = LearningSystem()
session = next(create_session())

def menu():
    print("1. 添加单词")
    print("2. 查询英文")
    print("3. 查询翻译")
    print("4. 根据中文拼写英文（练习）")
    print("5. 根据英文写中文（练习）")
    print("0. 退出")


while True:
    menu()
    choice = input("选择功能：")

    if choice == "1":
        word = input("英文：")
        trans = input("翻译：")
        result = ls.save_to_db(session, word, trans)
        print("成功添加：", result)

    elif choice == "2":
        word = input("要查询的英文：")
        print(ls.query_word(session, word))

    elif choice == "3":
        trans = input("要查询的翻译：")
        print(ls.query_translation(session, trans))

    elif choice == "4":
        count = int(input("练习数量："))
        questions = ls.practice_spell(session, count)
        correct = 0
        for q in questions:
            user = input(f"{q['translation']} -> 英文：")
            if user == q["answer"]:
                print("正确")
                correct += 1
            else:
                print("错误，答案是：", q["answer"])
        print("正确率：", correct / len(questions))

    elif choice == "5":
        count = int(input("练习数量："))
        questions = ls.practice_translation(session, count)
        correct = 0
        for q in questions:
            user = input(f"{q['word']} -> 翻译：")
            answers = q["answer"].split("/") if "/" in q["answer"] else [q["answer"]]

            if user in answers:
                print("正确")
                correct += 1
            else:
                print("错误，答案是：", q["answer"])
        print("正确率：", correct / len(questions))

    elif choice == "0":
        break
