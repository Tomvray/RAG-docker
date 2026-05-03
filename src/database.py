import psycopg2


class Database:
    def __init__(self, host, port, database, user, password):
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        print("Database connection established.")
        #print tables
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()
            print("Tables in the database:")
            for table in tables:
                print(table[0])

    def execute_query(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_claims(self, patent_id):
        """RETURN ALL CLAIMS FOR A GIVEN PATENT ID ordered by claim number"""
        query = f"SELECT claim_text FROM claims WHERE patent_id = '{patent_id}' ORDER BY claim_number"
        return self.execute_query(query)
    
    def get_claims_str(self, patent_id):
        """RETURN ALL CLAIMS FOR A GIVEN PATENT ID ordered by claim number as a single string"""

        claims = self.get_claims(patent_id)
        return "\n".join([claim[0] for claim in claims])
    
    def get_claims_ids(self):
        """return all patent IDs that have claims in the database"""

        query = f"SELECT distinct patent_id FROM claims"
        ids = self.execute_query(query)
        return [id[0] for id in ids]

    def close(self):
        self.connection.close()


if __name__ == "__main__":
    db = Database(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password=" "
    )
        
    db.close()