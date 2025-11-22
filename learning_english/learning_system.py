"""
英语学习系统
存入数据库使用sqlmodel -> 定义数据库连接的包
"""
from sqlmodel import select

from sql_connect.sql_connect_system import SessionDep, English, create_session


class LearningSystem(object):
    # 属性
    # 方法
    # 定义静态方法菜单
    @classmethod
    def menu(cls):
        print('1,存入数据库')
        print('2,通过文件存入数据库')
        print('3,查询英文')
        print('4,查询翻译')

        print('5,根据中文意思拼写英文')
        print('6,根据英文翻译中文意思')

    # 定义存入数据库方法
    def save_to_db(self, session: SessionDep, e_word=None, e_translation=None):
        # 使用数据库依赖
        english = English(e_word=e_word, e_translation=e_translation)
        session.add(english)
        session.commit()
        session.refresh(english)
        print(f'添加成功, 信息为{english}')

    # 定义根据中文意思拼写英文方法
    def learning_spell(self, session: SessionDep):
        # 练习多少组
        count = 0
        n = int(input('要练习多少个'))
        result = session.exec(select(English).limit(n)).all()
        for i in result:
            if input(f'根据意思拼写单词, {i.e_translation}') == i.e_word:
                print('正确')
                count += 1
            else:
                print(f'错误, 正确的拼写应该为{i.e_word}')
        print(f'总共答对的次数为{count}, 正确率{count / len(result):.2%}')

    # 定义翻译英文
    def translation(self, session: SessionDep):
        # 练习多少组
        count = 0
        n = int(input('要练习多少个'))
        result = session.exec(select(English).limit(n)).all()
        for i in result:
            if '/' in i.e_translation:
                if input(f'根据单词翻译意思,{i.e_word}') in i.e_translation.split('/'):
                    print('正确')
                    count += 1
                else:
                    print(f'错误, 正确的拼写应该为{i.e_translation}')
            else:
                if input(f'根据单词翻译意思,{i.e_word}') == i.e_translation:
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
        return result

    def query_translation(self, session: SessionDep, e_translation=None):
        result = session.exec(select(English).where(English.e_translation == e_translation)).first()
        if not result:
            return '没有相关信息'
        return result

    def save_file_to_db(self, session: SessionDep):
        with open('../单词.txt', 'r', encoding='utf8') as f:
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
                # 把内容存到数据库
                self.save_to_db(session, e_word=word, e_translation=translation)




if __name__ == '__main__':
    # 测试
    ls = LearningSystem()
    session = next(create_session())
    while True:
        ls.menu()
        result = input('输入功能编号')
        if result == '1':
            word = input('单词')
            translation = input('翻译')
            ls.save_to_db(session, word, translation)
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
        else:
            break
