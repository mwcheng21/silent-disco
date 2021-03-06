import os
import psycopg2


def exec_statement(conn, stmt):
    try:
        with conn.cursor() as cur:
            cur.execute(stmt)
            row = cur.fetchone()
            print(row)
            conn.commit()
            if row: print(row[0])
    except psycopg2.ProgrammingError:
        return


def main():

    # Connect to CockroachDB
    connection = psycopg2.connect("postgresql://mwcheng:lMBa1RwkVbbuYlVq3ABi-w@free-tier14.aws-us-east-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Drustic-fish-1550")
    # connection = psycopg2.connect(os.environ['DATABASE_URL'])


    exec_statement(connection, "SELECT * FROM song WHERE tid='38d144f5-8df2-40c5-a9b5-e6296b291262';")

    # Close communication with the database
    connection.close()


if __name__ == "__main__":
    main()