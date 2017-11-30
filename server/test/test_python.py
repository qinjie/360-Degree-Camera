import boto3
import pymysql
import time
import json


# Test
def test_ec2_get_sqs():
    queue_name = '360-degree-camera'
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    while True:
        msg_list = queue.receive_messages(MaxNumberOfMessages=5)
        if msg_list:
            for message in msg_list:
                print(message.body)
                data = json.loads(message.body)

                # Process job

                message.delete()
                time.sleep(1)
        else:
            print("No message found.")
            break


def test_rds_save_data():
    db_host = 'iot-centre-rds.crqhd2o1amcg.ap-southeast-1.rds.amazonaws.com'
    db_name = '360-degree-camera'
    db_username = 'root'
    db_password = 'Soe7014Ece'
    conn = pymysql.connect(host=db_host, port=3306, user=db_username, passwd=db_password, db=db_name)

    data1 = {"node_id": "1", "s3_path": "360_degree_camera/001.jpg"}
    try:
        cur = conn.cursor()
        sql = "INSERT INTO photo (node_id, s3_path) VALUES('{0}', '{1}');SELECT LAST_INSERT_ID();"
        sql = sql.format(data1['node_id'], data1['s3_path'])
        print(sql)
        cur.execute(sql)
        result1 = cur.fetchone()
        print(result1)

        photo_id = result1[0]

        sql = "INSERT INTO analysis (photo_id, type, result) VALUES({0}, '{1}', {2})"
        sql = sql.format(photo_id, 'crowd_index', 0.81)
        print(sql)
        cur.execute(sql)
        result2 = cur.fetchone()
        print(result2)

        time.sleep(1)
        cur.close()
    except:
        conn.rollback()
        conn.close()
        raise
    else:
        conn.commit()
        conn.close()


if __name__ == '__main__':
    test_rds_save_data()
