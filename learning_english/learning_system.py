"""
英语学习系统
存入数据库使用sqlmodel -> 定义数据库连接的包
"""
from sqlmodel import select
from sqlalchemy.sql import func
from sql_connect.sqllite_connect import SessionDep, English, create_session


class LearningSystem(object):
    # 属性
    # 方法
    # 定义静态方法菜单
    @staticmethod
    def menu():
        print('1,通过单词以及意思存入数据库')
        print('2,通过文件存入数据库')
        print('3,查询库内英文对应的翻译')
        print('4,查询库内中文对应的翻译')
        print('5,根据中文意思拼写英文')
        print('6,根据英文翻译中文意思')
        print('7,随机100题得分挑战!')

    # 定义存入数据库方法
    def save_to_db(self, session: SessionDep, e_word=None, e_translation=None):
        english = English(e_word=e_word, e_translation=e_translation)
        if session.exec(select(English).where(English.e_word == e_word)).all():
            print('已存在,未再次添加')
            return
        session.add(english)
        session.commit()
        session.refresh(english)
        print(f'添加成功, {english}')

    # 定义根据中文意思拼写英文方法
    def learning_spell(self, session: SessionDep):
        # 练习多少组
        count = 0
        # 定义空字典,用于临时存放错误的
        error_word = {}
        try:
            n = int(input('输入数量,回车默认999数量'))
        except:
            n = int(input('输入异常请重新输入数量,回车默认999数量'))
        if n == '':
            n = 999
            result = session.exec(select(English).limit(n)).all()
        else:
            n = int(n)
            result = session.exec(select(English).limit(n)).all()
        for i in result:
            user_input = input(f'根据意思拼写单词, "{i.e_translation} "的单词是? 输入"exit"可强制退出! ')
            # 加一层判断可以在运行过程中还能退出
            if user_input == 'exit':
                return
            if user_input == i.e_word:
                print('正确')
                count += 1
            else:
                print(f'错误, 正确的拼写应该为{i.e_word}')
                error_word[i.e_translation] = i.e_word
        else:
            print(f'总共答对的次数为{count}, 正确率{count / len(result):.2%}')
        if count / len(result) < 1:
            while True:
                if len(error_word) > 0:
                    continue_exercise = input('继续错误习题练习请输入1,输入其他返回主菜单 ')
                    if continue_exercise == '1':
                        count_two = 0
                        ec = error_word.copy()
                        for i in ec:
                            if input(f'根据意思拼写单词, {i} ') == error_word[i]:
                                print('正确')
                                count_two += 1
                                del error_word[i]
                            else:
                                print(f'错误, 正确的拼写应该为{error_word[i]}')
                        if len(error_word) == 0:
                            print('再次练习,正确率为100%')
                            break
                        print(f'二次练习答对的次数为{count_two}, 正确率{count_two / len(ec):.2%}')
                    else:
                        break
    # 定义翻译英文
    def translation(self, session: SessionDep):
        # 练习多少组
        # todo 待优化成拼写练习
        count = 0
        n = int(input('要练习多少个'))
        result = session.exec(select(English).limit(n)).all()
        for i in result:
            if '/' in i.e_translation:
                if input(f'根据单词翻译意思,{i.e_word} ') in i.e_translation.split('/'):
                    print('正确')
                    count += 1
                else:
                    print(f'错误, 正确的拼写应该为{i.e_translation}')
            else:
                if input(f'根据单词翻译意思,{i.e_word}' ) == i.e_translation:
                    print('正确')
                    count += 1
                else:
                    print(f'错误, 正确的拼写应该为{i.e_translation}')
        print(f'总共答对的次数为{count}, 正确率{count / len(result):.2%}')

    # 查询单词
    def query_word(self, session: SessionDep, e_word=None):
        # 通过单词意思或者单词来查询相关信息
        result = session.exec(select(English).where(English.e_word == e_word)).all()
        if not result:
            return '没有相关信息'
        print(result)
        return result

    def query_translation(self, session: SessionDep, e_translation=None):
        result = session.exec(select(English).where(English.e_translation == e_translation)).first()
        if not result:
            return '没有相关信息'
        return result

    def save_file_to_db(self, session: SessionDep):
        with open("data/单词.txt", 'r', encoding='utf8') as f:
            while True:
                # 每次读取一行
                result = f.readline()
                # 判断是否有数据
                if not result:
                    return
                # 去除\n
                result = result.strip()
                # 切分空格分开单词和意思
                result = result.split(' ')
                translation = result[0]
                word = result[1]
                # 判断是否存在,如果存在跳过
                if session.exec(select(English).where(English.e_word==word)).all():
                    continue
                # 把内容存到数据库
                self.save_to_db(session, e_word=word, e_translation=translation)


    def get_random_100(self,session: SessionDep):
        """
        随机获取100到练习
        :return:
        """
        count = 0
        # 定义空字典,用于临时存放错误的
        error_word = {}
        result = session.exec(select(English).order_by(func.random()).limit(100)).all()
        print(result)
        for i in result:
            user_input = input(f'根据意思拼写单词, "{i.e_translation} "的单词是? 输入"exit"可强制退出! ')
            # 加一层判断可以在运行过程中还能退出
            if user_input == 'exit':
                return
            if user_input == i.e_word:
                print('正确')
                count += 1
            else:
                print(f'错误, 正确的拼写应该为{i.e_word}')
                error_word[i.e_translation] = i.e_word
        else:
            score = count / len(result) * 100
            print(f'总共答对的次数为{count}, 正确率{count / len(result):.2%}, 得分为{score:.1f}')
        if count / len(result) < 1:
            while True:
                if len(error_word) > 0:
                    continue_exercise = input('继续错误习题练习请输入1,输入其他返回主菜单 ')
                    if continue_exercise == '1':
                        count_two = 0
                        ec = error_word.copy()
                        for i in ec:
                            if input(f'根据意思拼写单词, {i} ') == error_word[i]:
                                print('正确')
                                count_two += 1
                                del error_word[i]
                            else:
                                print(f'错误, 正确的拼写应该为{error_word[i]}')
                        if len(error_word) == 0:
                            print('再次练习,正确率为100%')
                            break
                        print(f'二次练习答对的次数为{count_two}, 正确率{count_two / len(ec):.2%}')
                    else:
                        break



if __name__ == '__main__':
    # 测试
    ls = LearningSystem()
    session = next(create_session())
    while True:
        ls.menu()
        result = input('输入功能编号')
        if result == '1':
            while True:
                word = input('单词 ')
                translation = input('中文翻译 ')
                ls.save_to_db(session, word, translation)
                num = input('继续添加输入1,输入其他退回主菜单, 回车默认退回主菜单')
                if num == '1':
                    continue
                else:
                    break
        elif result == '2':
            ls.save_file_to_db(session)

        elif result == '3':
            word = input('查询单词')
            print(ls.query_word(session, word))
        elif result == '4':
            translation = input('查询翻译')
            print(ls.query_translation(session, translation))
        elif result == '5':
            ls.learning_spell(session)
        elif result == '6':
            ls.translation(session)

        elif result == '7':
            ls.get_random_100(session)

        else:
            break
