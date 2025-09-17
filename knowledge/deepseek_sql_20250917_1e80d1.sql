CREATE TABLE core_documentchunk (
    id UUID PRIMARY KEY,
    document_id UUID NOT NULL,
    text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL CHECK (chunk_index >= 0),
    qdrant_id VARCHAR(255),

    CONSTRAINT fk_document  -- This is the Foreign Key constraint
        FOREIGN KEY(document_id)
        REFERENCES core_document(id)
        ON DELETE CASCADE
);