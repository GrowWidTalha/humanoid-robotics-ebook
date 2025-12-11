-- Fix malformed metadata in chat_messages table
-- Convert string '"{}"' to proper JSONB '{}'

UPDATE chat_messages
SET metadata = '{}'::jsonb
WHERE metadata::text = '"{}"' OR metadata::text = '"null"';

-- Verify the fix
SELECT id, metadata, metadata::text as metadata_text
FROM chat_messages
LIMIT 10;
