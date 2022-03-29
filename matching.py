# --------------------------------------------------------------------
# matching.py
# --------------------------------------------------------------------
from sys import stderr
import psycopg2

DATABASE_URL = 'file:TigerFriend.sqlite?mode=ro'

# --------------------------------------------------------------------

# given a user's net_id, returns a dictionary containing the following
# "overall_match": {net_id}
# "academic_match": {net_id}
# "extracurricular_match": {net_id}
# "personality_match": {net_id}
# "opinion_match": {net_id}
def get_user_matches(net_id, yr, major, res):
    try:
        # connect to database
        with psycopg2.connect(host="ec2-52-54-212-232.compute-1.amazonaws.com",
                              database="d1qoonauda49lp",
                              user="gehgaeoepuqelg",
                              password="8a2c415ed295edded3641f084099f247971fc720d4c83c7e79bf1951c3dcd38a") as connect:
            with connect.cursor() as cursor:
                # get user's survey response
                stmt = "SELECT * FROM rawdata WHERE net_id=\'" + net_id + "\'"
                cursor.execute(stmt)
                user_raw_data = cursor.fetchone()
                # print(user_raw_data)

                # get question types
                stmt = "SELECT q_type FROM survey"
                cursor.execute(stmt)
                q_type = cursor.fetchone()
                q_types = []
                while q_type is not None:
                    q_types.append(q_type[0])
                    q_type = cursor.fetchone()
                # print(q_types)

                # compare survey responses with other users
                stmt = "SELECT net_id FROM account Except SELECT net_id FROM rawdata WHERE net_id=\'" + net_id + "\'"
                cursor.execute(stmt)
                other_user = cursor.fetchone()
                other_users = []
                while other_user is not None:
                    other_users.append(str(other_user[0]))
                    other_user = cursor.fetchone()

                # prepare variables
                overall_match = None
                overall_match_threshold = 0
                academic_match = None
                academic_match_threshold = 0
                extracurricular_match = None
                extracurricular_match_threshold = 0
                personality_match = None
                personality_match_threshold = 0
                opinion_match = None
                opinion_match_threshold = 0

                for other_user in other_users:

                    overall_match_score = 0
                    academic_match_score = 0
                    extracurricular_match_score = 0
                    personality_match_score = 0
                    opinion_match_score = 0

                    stmt = "SELECT * FROM rawdata WHERE net_id=\'" + other_user + "\'"
                    cursor.execute(stmt)
                    other_raw_data = cursor.fetchone()

                    for i in range(len(q_types)):
                        # print("Question " + str(i + 1))
                        if user_raw_data[i + 1] == other_raw_data[i + 1]:
                            # print(str(user_raw_data[0]) + " and " + other_user +
                            #      " matched  with answer choice " + str(user_raw_data[i+1]))
                            overall_match_score += 1
                            # print("Question type " + str(q_types[i]))
                            if q_types[i] == 1:
                                academic_match_score += 1
                            elif q_types[i] == 2:
                                extracurricular_match_score += 1
                            elif q_types[i] == 3:
                                personality_match_score += 1
                            elif q_types[i] == 4:
                                opinion_match_score += 1

                    stmt = "SELECT class_year, major, res_college FROM account WHERE net_id=\'" + other_user + "\'"
                    cursor.execute(stmt)
                    other_user_info = cursor.fetchone()

                    if str(yr) == str(other_user_info[0]):
                        # print(str(user_raw_data[0]) + " and " + other_user + " matched on year " + str(yr))
                        overall_match_score += 1
                        personality_match_score += 1
                    if str(major) == str(other_user_info[1]):
                        # print(str(user_raw_data[0]) + " and " + other_user + " matched on year " + str(major))
                        overall_match_score += 1
                        academic_match_score += 1
                    if str(res) == str(other_user_info[2]):
                        # print(str(user_raw_data[0]) + " and " + other_user + " matched on year " + str(res))
                        overall_match_score += 1
                        extracurricular_match_score += 1

                    # print(str(user_raw_data[0]) + " and " + other_user +
                    #      " have overall score " + str(overall_match_score))
                    if overall_match_score > overall_match_threshold:
                        # print("Highest overall!")
                        overall_match = other_user
                        overall_match_threshold = overall_match_score
                    # print(str(user_raw_data[0]) + " and " + other_user +
                    #      " have academic score " + str(academic_match_score))
                    if academic_match_score > academic_match_threshold:
                        # print("Highest academic!")
                        academic_match = other_user
                        academic_match_threshold = academic_match_score
                    # print(str(user_raw_data[0]) + " and " + other_user +
                    #      " have extracurricular score " + str(extracurricular_match_score))
                    if extracurricular_match_score > extracurricular_match_threshold:
                        # print("Highest extracurricular!")
                        extracurricular_match = other_user
                        extracurricular_match_threshold = extracurricular_match_score
                    # print(str(user_raw_data[0]) + " and " + other_user +
                    #      " have personality score " + str(personality_match_score))
                    if personality_match_score > personality_match_threshold:
                        # print("Highest personality!")
                        personality_match = other_user
                        personality_match_threshold = personality_match_score
                    # print(str(user_raw_data[0]) + " and " + other_user +
                    #      " have opinion score " + str(opinion_match_score))
                    if opinion_match_score > opinion_match_threshold:
                        # print("Highest opinion!")
                        opinion_match = other_user
                        opinion_match_threshold = opinion_match_score

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]

    return {
        "overall_match": overall_match,
        "academic_match": academic_match,
        "extracurricular_match": extracurricular_match,
        "personality_match": personality_match,
        "opinion_match": opinion_match
    }


# "overall_match": [user, bio]
# "academic_match": [user, bio]
# "extracurricular_match": [user, bio]
# "personality_match": [user, bio]
# "opinion_match": [user, bio]
def get_match_info(match_dict):
    try:
        # connect to database
        with psycopg2.connect(host="ec2-52-54-212-232.compute-1.amazonaws.com",
                              database="d1qoonauda49lp",
                              user="gehgaeoepuqelg",
                              password="8a2c415ed295edded3641f084099f247971fc720d4c83c7e79bf1951c3dcd38a") as connect:
            with connect.cursor() as cursor:
                match_info = ()
                for key in match_dict:
                    net_id = match_dict[key]
                    stmt = "SELECT username, bio_string FROM account WHERE net_id=\'" + net_id + "\'"
                    cursor.execute(stmt)
                    account_data = cursor.fetchone()
                    match_info += ([str(account_data[0]), str(account_data[1])],)

    except (Exception, psycopg2.Error) as ex:
        print(ex, file=stderr)
        print("Data base connection failed", file=stderr)
        return ["unknown (database connection failed)", "unknown"]

    return {
        "overall_match": match_info[0],
        "academic_match": match_info[1],
        "extracurricular_match": match_info[2],
        "personality_match": match_info[3],
        "opinion_match": match_info[4]
    }


def get_user_match_info(net_id, yr, major, res):
    return get_match_info(get_user_matches(net_id, yr, major, res))


# unit test
def main():
    print(get_user_match_info("collado", 2024, "COS", "Whitman"))


# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
