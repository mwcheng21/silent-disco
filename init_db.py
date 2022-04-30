import os
import psycopg2


def exec_statement(conn, stmt):
    try:
        with conn.cursor() as cur:
            cur.execute(stmt)
            row = cur.fetchone()
            conn.commit()
            if row: print(row[0])
    except psycopg2.ProgrammingError:
        return


def main():

    # Connect to CockroachDB
    connection = psycopg2.connect("postgresql://mwcheng:lMBa1RwkVbbuYlVq3ABi-w@free-tier14.aws-us-east-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Drustic-fish-1550")
    # connection = psycopg2.connect(os.environ['DATABASE_URL'])

    statements = [
        
        "CREATE TABLE IF NOT EXISTS song (id SERIAL PRIMARY KEY, tid VARCHAR(255), TrackName VARCHAR(255), Artists VARCHAR(255), CoverArt VARCHAR(255), Location VARCHAR(255))",
        "CREATE TABLE IF NOT EXISTS currentSong (id SERIAL PRIMARY KEY, tid VARCHAR(255), SongCurrentTime VARCHAR(255), MasterTime VARCHAR(255))",
        "CREATE TABLE IF NOT EXISTS nextSong (id SERIAL PRIMARY KEY, tid VARCHAR(255))",
    ]

    for statement in statements:
        exec_statement(connection, statement)

    # Close communication with the database
    connection.close()


if __name__ == "__main__":
    main()