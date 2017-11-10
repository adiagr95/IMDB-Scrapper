import pymysql
import pymysql.cursors

class Database:
    def __init__(self):
        self.connection = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='root', db='imdb', cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def insert(self, df):

        for data in list(df):
            year = data[3] if data[3] else 0
            duration = data[5] if data[5] else 0
            ratings = data[7] if data[7] else 0
            votes = data[11] if data[11] else 0

            self.cursor.execute(f"""Insert into `Movies` (`Link`, `Title`, `Year`, `Certificate`, `Duration`, `Ratings`, `Desc`, `Votes`) values ("{data[1]}", "{data[2]}", {year} , "{data[4]}", {duration}, {ratings}, "{data[8]}", {votes})""")
            movie_id = self.connection.insert_id()

            for data_actor in data[10]:
                self.cursor.execute(f"""Select * from `Actors` where `name` = "{data_actor}";""")
                actor = self.cursor.fetchone()
                if actor:
                    actor_id = actor['id']
                else:
                    self.cursor.execute(f"""Insert into `Actors` (`name`) values ("{data_actor}")""")
                    actor_id = self.connection.insert_id()
                self.cursor.execute(f"""Insert into `MovieActorMapping` (`m_id`, `a_id`) values ({movie_id}, {actor_id})""")

            for data_director in data[9]:
                self.cursor.execute(f"""Select * from `Directors` where `name` = "{data_director}";""")
                director = self.cursor.fetchone()
                if director:
                    director_id = director['id']
                else:
                    self.cursor.execute(f"""Insert into `Directors` (`name`) values ("{data_director}")""")
                    director_id = self.connection.insert_id()
                self.cursor.execute(f"""Insert into `MovieDirectorMapping` (`m_id`, `d_id`) values ({movie_id}, {director_id})""")

            for data_genere in data[6]:
                self.cursor.execute(f"""Select * from `Generes` where `name` = "{data_genere}";""")
                genere = self.cursor.fetchone()
                if genere:
                    genere_id = genere['id']
                else:
                    self.cursor.execute(f"""Insert into `Generes` (`name`) values ("{data_genere}")""")
                    genere_id = self.connection.insert_id()
                self.cursor.execute(f"""Insert into `MovieGenereMapping` (`m_id`, `g_id`) values ({movie_id}, {genere_id})""")
        self.connection.commit()

    def deleteAll(self):
        self.cursor.execute("delete from `MovieActorMapping`")
        self.cursor.execute("delete from `MovieDirectorMapping`")
        self.cursor.execute("delete from `MovieGenereMapping`")
        self.cursor.execute("delete from `Movies`")
        self.cursor.execute("delete from `Actors`")
        self.cursor.execute("delete from `Directors`")
        self.cursor.execute("delete from `Generes`")

    def delete_repeat(self):
        self.cursor.execute(f"""select * , COUNT(*) c  from Movies group by Link  having c > 1;""")
        movies = self.cursor.fetchall()
        for movie in movies:
            print(movie['id'])
            print(f"delete from `MovieActorMapping` where m_id = {movie['id']} : ", self.cursor.execute(f"delete from `MovieActorMapping` where m_id = {movie['id']}"))
            print(f"delete from `MovieDirectorMapping` where m_id = {movie['id']} : ", self.cursor.execute(f"delete from `MovieDirectorMapping` where m_id = {movie['id']}"))
            print(f"delete from `MovieGenereMapping` where m_id = {movie['id']} : ", self.cursor.execute(f"delete from `MovieGenereMapping` where m_id = {movie['id']}"))
            print(f"delete from `Movies` where id = {movie['id']} : ", self.cursor.execute(f"delete from `Movies` where id = {movie['id']}"))
            print("\n")
        self.connection.commit()

    def delete_incorrect(self):
        self.cursor.execute(f"""select *  from Movies;""")
        movies = self.cursor.fetchall()
        for movie in movies:
            if len(str(movie['Year'])) != 4:
                print(f"delete from `MovieActorMapping` where m_id = {movie['id']} : ", self.cursor.execute(f"delete from `MovieActorMapping` where m_id = {movie['id']}"))
                print(f"delete from `MovieDirectorMapping` where m_id = {movie['id']} : ", self.cursor.execute(f"delete from `MovieDirectorMapping` where m_id = {movie['id']}"))
                print(f"delete from `MovieGenereMapping` where m_id = {movie['id']} : ", self.cursor.execute(f"delete from `MovieGenereMapping` where m_id = {movie['id']}"))
                print(f"delete from `Movies` where id = {movie['id']} : ", self.cursor.execute(f"delete from `Movies` where id = {movie['id']}"))
        self.connection.commit()
