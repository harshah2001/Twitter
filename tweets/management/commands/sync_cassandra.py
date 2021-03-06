from cassandra.cluster import Cluster
from click._compat import raw_input
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect()

        rows = session.execute(
            "SELECT * FROM system_schema.keyspaces WHERE keyspace_name='twitter'")

        if rows:
            msg = ' It looks like you already have a twitter keyspace.\nDo you '
            msg += 'want to delete it and recreate it? All current data will '
            msg += 'be deleted! (y/n): '
            resp = raw_input(msg)
            if not resp or resp[0] != 'y':
                print ("Ok, then we're done here.")
                return
            session.execute("DROP KEYSPACE twitter")

        session.execute("""
            CREATE KEYSPACE twitter
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
            """)

        # create tables
        session.set_keyspace("twitter")

        session.execute("""
            CREATE TABLE users (
                username text PRIMARY KEY,
                password varchar
            )
            """)

        session.execute("""
            CREATE TABLE friends (
                username text,
                friend text,
                since timestamp,
                PRIMARY KEY (username, friend)
            )
            """)

        session.execute("""
            CREATE TABLE tweets (
                tweet_id uuid PRIMARY KEY,
                username text,
                body text
            )
            """)

        session.execute("""
            CREATE TABLE userline (
                username text,
                time timeuuid,
                tweet_id uuid,
                PRIMARY KEY (username, time)
            ) WITH CLUSTERING ORDER BY (time DESC)
            """)

        session.execute("""
            CREATE TABLE timeline (
                username text,
                time timeuuid,
                tweet_id uuid,
                PRIMARY KEY (username, time)
            ) WITH CLUSTERING ORDER BY (time DESC)
            """)

        print('All done!')
