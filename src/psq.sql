DROP TABLE IF EXISTS claims;

CREATE TABLE IF NOT EXISTS claims (
    patent_id VARCHAR(255),
    claim_sequence INTEGER,
    claim_text TEXT,
    dependent VARCHAR(255),
    claim_number VARCHAR(16),
    exemplary BOOLEAN
);

CREATE INDEX idx_claims_patent_id ON claims(patent_id);


\COPY claims(patent_id, claim_sequence, claim_text, dependent, claim_number, exemplary) FROM '/home/thomas/Documents/samples/RAG-docker/data/g_claims_1976.tsv' WITH (FORMAT CSV, DELIMITER E'\t', HEADER);


