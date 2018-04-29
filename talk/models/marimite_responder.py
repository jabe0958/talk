#!/usr/bin/env

print("__name__ : %s" % __name__)

from .abstract_responder import AbstractResponder
#from abstract_responder import AbstractResponder
import random
import mysql.connector


class MarimiteResponder(AbstractResponder):
    def talk(self):
        conn = None
        cursor = None

        text = ""
        tokens_limit = 40

        try:
            conn = mysql.connector.connect(host='localhost', user='dialoguetweets', password='', db='DialogueTweets',
                                           charset='utf8')
            conn.autocommit = False
            cursor = conn.cursor(prepared=True)
            # cursor = conn.cursor(buffered=True, prepared=True)
            token = "xxxSTARTxxx"
            # cursor.execute('select id from morphemes where surface = %s', [token])
            cursor.execute('select id from morphemes where surface = ?', (token, ))
            # token_row = cursor.fetchone()
            token_row = cursor.fetchall()
            token1_id = token_row[0][0]

            cursor.close()
            cursor = conn.cursor(buffered=True)
            cursor.execute('select sum(frequency) from markov_chain_trigram where account_id = %s and token1 = %s',
                           [1, token1_id])
            sum_row = cursor.fetchone()
            if sum_row == None:
                return text
            total_frequency = sum_row[0]
            cursor.execute(
                'select c.token1, c.token2, c.frequency, m.surface from markov_chain_trigram c left join morphemes m on c.token2 = m.id where c.account_id = %s and c.token1 = %s',
                [1, token1_id])
            rows = cursor.fetchall()
            if len(rows) == 0:
                return text
            idx = random.randint(0, total_frequency - 1)
            pre_frequency = 0
            sum_frequency = 0
            for row in rows:
                sum_frequency += row[2]
                if pre_frequency <= idx and idx < sum_frequency:
                    token = row[3]
                    token2_id = row[1]
                    break
                pre_frequency = sum_frequency
            if token == "xxxENDxxx":
                return text
            text += str(token)

            for i in range(tokens_limit):
                cursor.execute(
                    'select sum(frequency) from markov_chain_trigram where account_id = %s and token1 = %s and token2 = %s',
                    [1, token1_id, token2_id])
                sum_row = cursor.fetchone()
                if sum_row == None:
                    break
                total_frequency = sum_row[0]
                cursor.execute(
                    'select c.token1, c.token2, c.next_token, c.frequency, m.surface from markov_chain_trigram c left join morphemes m on c.next_token = m.id where c.account_id = %s and c.token1 = %s and c.token2 = %s',
                    [1, token1_id, token2_id])
                rows = cursor.fetchall()
                if len(rows) == 0:
                    break
                idx = random.randint(0, total_frequency - 1)
                pre_frequency = 0
                sum_frequency = 0
                for row in rows:
                    sum_frequency += row[3]
                    if pre_frequency <= idx and idx < sum_frequency:
                        token = row[4]
                        token1_id = token2_id
                        token2_id = row[2]
                        break
                    pre_frequency = sum_frequency
                if token == "xxxENDxxx":
                    break
                text += str(token)
        except Exception as e:
            if conn != None:
                conn.rollback()
            raise e
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.close()

        return text


if __name__ == "__main__":
    marimite = MarimiteResponder() 
    for i in range(5):
        print("> " + marimite.talk())
