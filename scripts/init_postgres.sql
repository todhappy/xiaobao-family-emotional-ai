CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  email VARCHAR,
  avatar_url VARCHAR,
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS families (
  id SERIAL PRIMARY KEY,
  owner_id INTEGER REFERENCES users(id),
  name VARCHAR,
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS family_members (
  id SERIAL PRIMARY KEY,
  family_id INTEGER REFERENCES families(id),
  name VARCHAR,
  role VARCHAR,
  avatar_url VARCHAR,
  is_virtual BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS memory_records (
  id SERIAL PRIMARY KEY,
  family_id INTEGER REFERENCES families(id),
  member_id INTEGER REFERENCES family_members(id),
  content TEXT,
  tags TEXT[],
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS memory_embeddings (
  id SERIAL PRIMARY KEY,
  memory_id INTEGER REFERENCES memory_records(id),
  embedding vector(1536),
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_messages (
  id SERIAL PRIMARY KEY,
  family_id INTEGER REFERENCES families(id),
  member_id INTEGER REFERENCES family_members(id),
  role VARCHAR,
  content TEXT,
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS devices (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  name VARCHAR,
  type VARCHAR,
  platform VARCHAR,
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mcp_sessions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  session_token VARCHAR,
  status VARCHAR,
  created_at TIMESTAMP
);

INSERT INTO users (name, email, avatar_url, created_at) VALUES ('余哥', 'yuge@example.com', '', NOW()) RETURNING id;

-- assume owner_id = currval of users_id_seq
INSERT INTO families (owner_id, name, created_at) VALUES (currval('users_id_seq'), '余氏家族', NOW()) RETURNING id;

INSERT INTO family_members (family_id, name, role, is_virtual, created_at)
VALUES (currval('families_id_seq'), '爸爸', '父亲', FALSE, NOW()),
       (currval('families_id_seq'), '妈妈', '母亲', FALSE, NOW());

INSERT INTO memory_records (family_id, member_id, content, tags, created_at)
VALUES (currval('families_id_seq'), currval('family_members_id_seq') - 1, '家庭聚餐记忆', ARRAY['聚餐','家庭'], NOW()) RETURNING id;

INSERT INTO memory_embeddings (memory_id, embedding, created_at)
VALUES (currval('memory_records_id_seq'), ARRAY_FILL(0.1::float4, ARRAY[1536])::vector, NOW());

INSERT INTO chat_messages (family_id, member_id, role, content, created_at)
VALUES (currval('families_id_seq'), currval('family_members_id_seq') - 1, 'assistant', '欢迎加入家庭系统', NOW());

INSERT INTO devices (user_id, name, type, platform, created_at)
VALUES (currval('users_id_seq'), 'iPhone', 'mobile', 'iOS', NOW());

INSERT INTO mcp_sessions (user_id, session_token, status, created_at)
VALUES (currval('users_id_seq'), 'token-demo', 'active', NOW());

-- validation queries
\echo Users count:
SELECT COUNT(*) FROM users;
\echo Families count:
SELECT COUNT(*) FROM families;
\echo FamilyMembers count:
SELECT COUNT(*) FROM family_members;
\echo MemoryRecords count:
SELECT COUNT(*) FROM memory_records;
\echo MemoryEmbeddings count:
SELECT COUNT(*) FROM memory_embeddings;
\echo ChatMessages count:
SELECT COUNT(*) FROM chat_messages;
\echo Devices count:
SELECT COUNT(*) FROM devices;
\echo MCPSessions count:
SELECT COUNT(*) FROM mcp_sessions;

\echo Cosine similarity test:
SELECT memory_id, (embedding <=> ARRAY_FILL(0.1::float4, ARRAY[1536])::vector) AS cos_dist
FROM memory_embeddings
ORDER BY cos_dist
LIMIT 1;

\echo Join test:
SELECT fm.name AS member_name, f.name AS family_name
FROM family_members fm
JOIN families f ON fm.family_id = f.id
LIMIT 1;